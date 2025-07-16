from __future__ import annotations

import json
import logging
from typing import TYPE_CHECKING, Any, Final, Self

from aiohttp_client_cache.backends.sqlite import SQLiteBackend
from aiohttp_client_cache.session import CachedSession
from loguru import logger

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

    BASE_URL: Final[str] = "https://api.hakush.in"

    def __init__(
        self,
        game: Game,
        lang: Language = Language.EN,
        *,
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
            cache_path: The path to the cache database.
            cache_ttl: The time-to-live for cache entries.
            headers: The headers to pass with the request.
            debug: Whether to enable debug logging.
            session: The client session to use.
        """
        self.lang = lang
        self.cache_ttl = cache_ttl

        self._game = game
        self._session = session
        self._cache = SQLiteBackend(cache_path, expire_after=cache_ttl)
        self._headers = headers or {"User-Agent": "hakuashin-py"}
        self._debug = debug
        if self._debug:
            logging.basicConfig(level=logging.DEBUG)

    async def __aenter__(self) -> Self:
        await self.start()
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:  # noqa: ANN001
        await self.close()

    async def _download_gitlab_json(self, url: str, use_cache: bool) -> list[dict[str, Any]]:
        """
        Download a JSON file from GitLab and cache it locally.

        Returns the raw JSON list.
        """
        if self._session is None:
            msg = "Call `start` before making requests."
            raise RuntimeError(msg)

        if not use_cache and isinstance(self._session, CachedSession):
            async with self._session.disabled(), self._session.get(url) as resp:
                if resp.status != 200:
                    self._handle_error(resp.status, url)
                text = await resp.text()
                return json.loads(text)
        else:
            async with self._session.get(url) as resp:
                if resp.status != 200:
                    self._handle_error(resp.status, url)
                text = await resp.text()
                data = json.loads(text)

        return data

    async def _request(
        self, endpoint: str, use_cache: bool, *, static: bool = False, in_data: bool = False
    ) -> dict[str, Any]:
        if self._session is None:
            msg = "Call `start` before making requests."
            raise RuntimeError(msg)

        if static and in_data:
            msg = "static and data cannot be True at the same time."
            raise RuntimeError(msg)

        game = self._game
        lang = HSR_API_LANG_MAP[self.lang] if game is Game.HSR else self.lang.value

        if static:
            url = f"{self.BASE_URL}/{game.value}/{endpoint}.json"
        elif in_data:
            url = f"{self.BASE_URL}/{game.value}/data/{endpoint}.json"
        else:
            url = f"{self.BASE_URL}/{game.value}/data/{lang}/{endpoint}.json"

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

        return data

    def _handle_error(self, code: int, url: str) -> None:
        match code:
            case 404:
                raise NotFoundError(url)
            case _:
                raise HakushinError(code, "An error occurred while fetching data.", url)

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
        if self._session is not None:
            await self._session.close()
