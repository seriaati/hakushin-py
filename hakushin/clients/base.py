from __future__ import annotations

import json
import time
from typing import TYPE_CHECKING, Any, Final, Self

import aiofiles
import aiofiles.os
from aiohttp_client_cache.backends.sqlite import SQLiteBackend
from aiohttp_client_cache.session import CachedSession
from loguru import logger

from hakushin.models.manifest import GameManifest, ManifestResponse

from ..constants import HSR_API_LANG_MAP
from ..enums import Game, Language
from ..errors import HakushinError, NotFoundError

if TYPE_CHECKING:
    import aiohttp


class BaseClient:
    """Provide base functionality for interacting with the Hakushin API.

    This class handles HTTP requests, caching, session management, and error handling
    for all game-specific clients. It implements the async context manager protocol
    for proper resource management.

    Attributes:
        BASE_URL: The base URL for the Hakushin API.
        lang: The language for API responses.
        cache_ttl: Time-to-live for cached responses in seconds.
    """

    BASE_URL: Final[str] = "https://static.nanoka.cc"

    def __init__(
        self,
        game: Game,
        lang: Language = Language.EN,
        *,
        use_live: bool = False,
        cache_path: str = "./.cache/hakushin/aiohttp-cache.db",
        cache_ttl: int = 3600,
        headers: dict[str, Any] | None = None,
        debug: bool = False,
        session: aiohttp.ClientSession | None = None,
    ) -> None:
        """Initialize the Hakushin API client.

        Args:
            game: The game to fetch data for.
            lang: The language to fetch data in.
            use_live: Whether to use the live game version in API requests. If false, use latest version.
            cache_path: The path to the cache database.
            cache_ttl: The time-to-live for cache entries.
            headers: The headers to pass with the request.
            debug: Whether to enable debug logging.
            session: The client session to use.
        """
        self.lang = lang
        self.cache_ttl = cache_ttl
        self.use_live = use_live

        self._game = game
        self._using_custom_session = session is not None
        self._session = session
        self._cache = SQLiteBackend(cache_path, expire_after=cache_ttl)
        self._headers = headers or {"User-Agent": "hakuashin-py"}
        self._debug = debug

    async def __aenter__(self) -> Self:
        await self.start()
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:  # noqa: ANN001
        await self.close()

    async def _get_game_version(self) -> str:
        try:
            async with aiofiles.open("./.cache/hakushin/version.json") as f:
                version_data = await f.read()
                version_json: dict[str, Any] = json.loads(version_data)
        except (FileNotFoundError, json.JSONDecodeError):
            version_json = {}

        last_updated = version_json.get("last_updated", 0)
        if time.time() - last_updated < 24 * 3600:  # 24 hours
            game_version = version_json.get(self._game.value, {}).get(
                "live" if self.use_live else "latest"
            )
            if game_version:
                return game_version

        manifest = await self.fetch_manifest()
        version_info: GameManifest = getattr(manifest, self._game.value)

        version_data = {
            "gi": {"live": manifest.gi.live_version, "latest": manifest.gi.latest_version},
            "hsr": {"live": manifest.hsr.live_version, "latest": manifest.hsr.latest_version},
            "zzz": {"live": manifest.zzz.live_version, "latest": manifest.zzz.latest_version},
            "last_updated": time.time(),
        }

        try:
            await aiofiles.os.makedirs("./.cache/hakushin", exist_ok=True)
            async with aiofiles.open("./.cache/hakushin/version_data.json", "w") as f:
                await f.write(json.dumps(version_data, indent=4))
        except Exception as e:
            logger.warning(f"Failed to write version data to cache: {e}")

        return version_info.live_version if self.use_live else version_info.latest_version

    async def _request(
        self,
        endpoint: str,
        *,
        use_cache: bool,
        static: bool = False,
        in_data: bool = False,
        version: str | None = None,
    ) -> dict[str, Any]:
        if self._session is None:
            msg = "Call `start` before making requests."
            raise RuntimeError(msg)

        if static and in_data:
            msg = "static and data cannot be True at the same time."
            raise RuntimeError(msg)

        game = self._game
        lang = HSR_API_LANG_MAP[self.lang] if game is Game.HSR else self.lang.value
        version = version or await self._get_game_version()

        if static:
            url = f"{self.BASE_URL}/{game.value}/{endpoint}.json"
        elif in_data:
            url = f"{self.BASE_URL}/{game.value}/{version}/{endpoint}.json"
        else:
            url = f"{self.BASE_URL}/{game.value}/{version}/{lang}/{endpoint}.json"

        logger.debug(f"Requesting {url}")

        if not use_cache and isinstance(self._session, CachedSession):
            async with self._session.disabled(), self._session.get(url) as resp:
                if resp.status != 200:
                    self._handle_error(resp.status, url)
                data = await resp.json()
        else:
            async with self._session.get(url) as resp:
                if resp.status != 200:
                    self._handle_error(resp.status, url)
                data = await resp.json()

        # for HSR Memory of Chaos, returns a list
        if isinstance(data, list):
            data = {"level": data}

        return data

    def _handle_error(self, code: int, url: str) -> None:
        match code:
            case 404:
                raise NotFoundError(url)
            case _:
                raise HakushinError(code, "An error occurred while fetching data.", url)

    async def fetch_manifest(self) -> ManifestResponse:
        """Fetch the game manifest from the Hakushin API.

        This method retrieves the latest manifest information for all supported games,
        including available versions and new item IDs.

        Args:
            use_cache: Whether to use cached responses. If False, the cache will be bypassed for this request.

        Returns:
            A ManifestResponse object containing the manifest data.
        """
        if self._session is None:
            msg = "Call `start` before making requests."
            raise RuntimeError(msg)

        async with self._session.get(f"{self.BASE_URL}/manifest.json") as resp:
            if resp.status != 200:
                self._handle_error(resp.status, f"{self.BASE_URL}/manifest.json")
            data = await resp.json()

        return ManifestResponse.model_validate(data)

    async def start(self) -> None:
        """Start the client session.

        Initialize the aiohttp session with caching support if not already provided.
        This method must be called before making any API requests.
        """
        self._session = self._session or CachedSession(headers=self._headers, cache=self._cache)

    async def close(self) -> None:
        """Close the client session.

        Clean up the aiohttp session and release resources. This should be called
        when done with the client to prevent resource leaks.
        """
        if self._session is not None and not self._using_custom_session:
            await self._session.close()
