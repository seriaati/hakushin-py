from __future__ import annotations

from typing import TYPE_CHECKING, Any, Literal, overload

from hakushin.enums import Game, Language

from .clients import GIClient, HSRClient, ZZZClient

if TYPE_CHECKING:
    from aiohttp import ClientSession

__all__ = ("HakushinAPI",)


class HakushinAPI:
    """Represent a client to interact with the Hakushin API."""

    @overload
    def __new__(
        cls,
        game: Literal[Game.GI],
        lang: Language = Language.EN,
        *,
        cache_path: str = "./.cache/hakushin/aiohttp-cache.db",
        cache_ttl: int = 3600,
        headers: dict[str, Any] | None = None,
        debug: bool = False,
        session: ClientSession | None = None,
    ) -> GIClient:
        """Initialize a new GIClient instance.

        Args:
            game: The game to initialize the client for.
            lang: The language to use for API responses.
            cache_path: The path to the cache database.
            cache_ttl: The time-to-live for cached responses, in seconds.
            headers: Optional custom headers to include in API requests.
            debug: Whether to enable debug mode.
            session: An optional aiohttp ClientSession to use.

        Returns:
            An instance of GIClient.
        """

    @overload
    def __new__(
        cls,
        game: Literal[Game.HSR],
        lang: Language = Language.EN,
        *,
        cache_path: str = "./.cache/hakushin/aiohttp-cache.db",
        cache_ttl: int = 3600,
        headers: dict[str, Any] | None = None,
        debug: bool = False,
        session: ClientSession | None = None,
    ) -> HSRClient:
        """Initialize a new HSRClient instance.

        Args:
            game: The game to initialize the client for.
            lang: The language to use for API responses.
            cache_path: The path to the cache database.
            cache_ttl: The time-to-live for cached responses, in seconds.
            headers: Optional custom headers to include in API requests.
            debug: Whether to enable debug mode.
            session: An optional aiohttp ClientSession to use.

        Returns:
            An instance of HSRClient.
        """

    @overload
    def __new__(
        cls,
        game: Literal[Game.ZZZ],
        lang: Language = Language.EN,
        *,
        cache_path: str = "./.cache/hakushin/aiohttp-cache.db",
        cache_ttl: int = 3600,
        headers: dict[str, Any] | None = None,
        debug: bool = False,
        session: ClientSession | None = None,
    ) -> ZZZClient:
        """Initialize a new ZZZClient instance.

        Args:
            game: The game to initialize the client for.
            lang: The language to use for API responses.
            cache_path: The path to the cache database.
            cache_ttl: The time-to-live for cached responses, in seconds.
            headers: Optional custom headers to include in API requests.
            debug: Whether to enable debug mode.
            session: An optional aiohttp ClientSession to use.

        Returns:
            An instance of ZZZClient.
        """

    def __new__(
        cls,
        game: Game,
        lang: Language = Language.EN,
        *,
        cache_path: str = "./.cache/hakushin/aiohttp-cache.db",
        cache_ttl: int = 3600,
        headers: dict[str, Any] | None = None,
        debug: bool = False,
        session: ClientSession | None = None,
    ) -> GIClient | HSRClient | ZZZClient:
        if game is Game.GI:
            return GIClient(
                lang,
                cache_path=cache_path,
                cache_ttl=cache_ttl,
                headers=headers,
                debug=debug,
                session=session,
            )
        if game is Game.HSR:
            return HSRClient(
                lang,
                cache_path=cache_path,
                cache_ttl=cache_ttl,
                headers=headers,
                debug=debug,
                session=session,
            )
        return ZZZClient(
            lang,
            cache_path=cache_path,
            cache_ttl=cache_ttl,
            headers=headers,
            debug=debug,
            session=session,
        )
