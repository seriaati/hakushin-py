from __future__ import annotations

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
    """Base client to interact with the Hakushin API."""

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
        """Initializes the Hakushin API client.

        Args:
            game (Game): The game to fetch data for.
            lang (Language): The language to fetch data in.
            cache_path (str): The path to the cache database.
            cache_ttl (int): The time-to-live for cache entries.
            headers (dict): The headers to pass with the request.
            debug (bool): Whether to enable debug logging.
            session (aiohttp.ClientSession): The client session to use.
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

    async def _request(
        self, endpoint: str, use_cache: bool, *, static: bool = False, in_data: bool = False
    ) -> dict[str, Any]:
        """A helper function to make requests to the API.

        Args:
            endpoint (str): The endpoint to request.
            use_cache (bool): Whether to use the cache.
            static (bool): Whether the endpoint is static data (not language specific), defaults to False.
            in_data (bool): Whether the endpoint is in the data directory, defaults to False.

        Returns:
            dict: The response data.
        """
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
        self._session = self._session or CachedSession(headers=self._headers, cache=self._cache)

    async def close(self) -> None:
        """Closes the client session."""
        if self._session is not None:
            await self._session.close()
