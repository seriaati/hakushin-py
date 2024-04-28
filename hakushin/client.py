import logging
from typing import Any, Final, Literal, Self, overload

from aiohttp_client_cache.backends.sqlite import SQLiteBackend
from aiohttp_client_cache.session import CachedSession

from hakushin.enums import Game, Language
from hakushin.errors import HakushinError, NotFoundError

from .constants import HSR_LANG_MAP
from .models import gi, hsr

__all__ = ("HakushinAPI",)

LOGGER_ = logging.getLogger(__name__)


class HakushinAPI:
    """Client to interact with the Hakushin API."""

    BASE_URL: Final[str] = "https://api.hakush.in"

    def __init__(
        self,
        lang: Language = Language.EN,
        *,
        cache_path: str = "./.cache/hakushin/aiohttp-cache.db",
        cache_ttl: int = 3600,
        headers: dict[str, Any] | None = None,
        debug: bool = False,
    ) -> None:
        """Initializes the Hakushin API client.

        Args:
            lang (Language): The language to fetch data in.
            cache_path (str): The path to the cache database.
            cache_ttl (int): The time-to-live for cache entries.
            headers (dict): The headers to pass with the request.
            debug (bool): Whether to enable debug logging.
        """
        self.lang = lang
        self.cache_ttl = cache_ttl

        self._session: CachedSession | None = None
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

    async def _request(
        self, endpoint: str, game: Game, use_cache: bool, *, static: bool = False
    ) -> dict[str, Any]:
        """A helper function to make requests to the API.

        Args:
            endpoint (str): The endpoint to request.
            game (Game): The game to fetch data for.
            use_cache (bool): Whether to use the cache.
            static (bool): Whether the endpoint is static data (not language specific), defaults to False.

        Returns:
            dict: The response data.
        """
        if self._session is None:
            msg = "Call `start` before making requests."
            raise RuntimeError(msg)

        lang = HSR_LANG_MAP[self.lang] if game is Game.HSR else self.lang.value

        url = (
            f"{self.BASE_URL}/{game.value}/{endpoint}.json"
            if static
            else f"{self.BASE_URL}/{game.value}/data/{lang}/{endpoint}.json"
        )
        LOGGER_.debug("Requesting %s...", url)

        if not use_cache:
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
        """Handles API errors based on the status code.

        Args:
            code (int): The status code.
            url (str): The URL that caused the error.
        """
        match code:
            case 404:
                raise NotFoundError(url)
            case _:
                raise HakushinError(code, "An error occurred while fetching data.", url)

    async def start(self) -> None:
        """Starts the client session."""
        self._session = CachedSession(headers=self._headers, cache=self._cache)

    async def close(self) -> None:
        """Closes the client session."""
        if self._session is not None:
            await self._session.close()

    @overload
    async def fetch_new(self, game: Literal[Game.GI], *, use_cache: bool = True) -> gi.New: ...
    @overload
    async def fetch_new(self, game: Literal[Game.HSR], *, use_cache: bool = True) -> hsr.New: ...
    async def fetch_new(self, game: Game, *, use_cache: bool = True) -> gi.New | hsr.New:
        """Fetches the IDs of new stuff in the game.

        Args:
            game (Game): The game to fetch data for.
            use_cache (bool): Whether to use the cache.

        Returns:
            New: The new stuff object.
        """
        endpoint = "new"
        data = await self._request(endpoint, game, use_cache, static=True)
        return gi.New(**data) if game is Game.GI else hsr.New(**data)

    @overload
    async def fetch_character(
        self, character_id: int, game: Literal[Game.GI], *, use_cache: bool = True
    ) -> gi.GICharacter: ...
    @overload
    async def fetch_character(
        self, character_id: int, game: Literal[Game.HSR], *, use_cache: bool = True
    ) -> hsr.HSRCharacter: ...
    async def fetch_character(
        self, character_id: int, game: Game, *, use_cache: bool = True
    ) -> gi.GICharacter | hsr.HSRCharacter:
        """Fetches a character.

        Args:
            character_id (int): The character ID.
            game (Game): The game to fetch data for.
            use_cache (bool): Whether to use the cache.

        Returns:
            Character: The character object.
        """
        endpoint = f"character/{character_id}"
        data = await self._request(endpoint, game, use_cache)
        return gi.GICharacter(**data) if game is Game.GI else hsr.HSRCharacter(**data)

    async def fetch_weapon(self, weapon_id: int, *, use_cache: bool = True) -> gi.Weapon:
        """Fetches a Genshin Impact weapon.

        Args:
            weapon_id (int): The weapon ID.
            use_cache (bool): Whether to use the cache.

        Returns:
            Weapon: The weapon object.
        """
        endpoint = f"weapon/{weapon_id}"
        data = await self._request(endpoint, Game.GI, use_cache)
        return gi.Weapon(**data)

    async def fetch_light_cone(
        self, light_cone_id: int, *, use_cache: bool = True
    ) -> hsr.LightCone:
        """Fetches a HSR light cone.

        Args:
            light_cone_id (int): The light cone ID.
            use_cache (bool): Whether to use the cache.

        Returns:
            LightCone: The light cone object.
        """
        endpoint = f"lightcone/{light_cone_id}"
        data = await self._request(endpoint, Game.HSR, use_cache)
        return hsr.LightCone(**data)

    async def fetch_artifact_set(self, set_id: int, *, use_cache: bool = True) -> gi.ArtifactSet:
        """Fetches an artifact set.

        Args:
            set_id (int): The artifact set ID.
            use_cache (bool): Whether to use the cache.

        Returns:
            ArtifactSet: The artifact set object.
        """
        endpoint = f"artifact/{set_id}"
        data = await self._request(endpoint, Game.GI, use_cache)
        return gi.ArtifactSet(**data)

    async def fetch_relic_set(self, set_id: int, *, use_cache: bool = True) -> hsr.RelicSet:
        """Fetches a relic set.

        Args:
            set_id (int): The relic set ID.
            use_cache (bool): Whether to use the cache.

        Returns:
            RelicSet: The relic set object.
        """
        endpoint = f"relicset/{set_id}"
        data = await self._request(endpoint, Game.HSR, use_cache)
        return hsr.RelicSet(**data)
