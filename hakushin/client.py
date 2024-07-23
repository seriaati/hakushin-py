from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any, Literal, overload

from hakushin.enums import Game, Language

from .clients import GIClient, HSRClient, ZZZClient

if TYPE_CHECKING:
    from aiohttp import ClientSession

__all__ = ("HakushinAPI",)

LOGGER_ = logging.getLogger(__name__)


class HakushinAPI:
    """Client to interact with the Hakushin API."""

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
    ) -> GIClient: ...
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
    ) -> HSRClient: ...
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
    ) -> ZZZClient: ...
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
        """Initializes the Hakushin API client."""
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
