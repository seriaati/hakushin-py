from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any, Final, Literal, Self, overload

from aiohttp_client_cache.backends.sqlite import SQLiteBackend
from aiohttp_client_cache.session import CachedSession

from hakushin.enums import Game, Language
from hakushin.errors import HakushinError, NotFoundError

from .constants import GI_LANG_MAP, HSR_API_LANG_MAP
from .models import gi, hsr
from .utils import cleanup_text, replace_placeholders

if TYPE_CHECKING:
    import aiohttp

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
        session: aiohttp.ClientSession | None = None,
    ) -> None:
        """Initializes the Hakushin API client.

        Args:
            lang (Language): The language to fetch data in.
            cache_path (str): The path to the cache database.
            cache_ttl (int): The time-to-live for cache entries.
            headers (dict): The headers to pass with the request.
            debug (bool): Whether to enable debug logging.
            session (aiohttp.ClientSession): The client session to use.
        """
        self.lang = lang
        self.cache_ttl = cache_ttl

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
        self,
        endpoint: str,
        game: Game,
        use_cache: bool,
        *,
        static: bool = False,
        in_data: bool = False,
    ) -> dict[str, Any]:
        """A helper function to make requests to the API.

        Args:
            endpoint (str): The endpoint to request.
            game (Game): The game to fetch data for.
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

        lang = HSR_API_LANG_MAP[self.lang] if game is Game.HSR else self.lang.value

        if static:
            url = f"{self.BASE_URL}/{game.value}/{endpoint}.json"
        elif in_data:
            url = f"{self.BASE_URL}/{game.value}/data/{endpoint}.json"
        else:
            url = f"{self.BASE_URL}/{game.value}/data/{lang}/{endpoint}.json"

        LOGGER_.debug("Requesting %s...", url)

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
    async def fetch_characters(
        self, game: Literal[Game.GI], *, use_cache: bool = True
    ) -> list[gi.Character]: ...
    @overload
    async def fetch_characters(
        self, game: Literal[Game.HSR], *, use_cache: bool = True
    ) -> list[hsr.Character]: ...
    async def fetch_characters(
        self, game: Game, *, use_cache: bool = True
    ) -> list[gi.Character] | list[hsr.Character]:
        """Fetches all characters in the game.

        Args:
            game (Game): The game to fetch data for.
            use_cache (bool): Whether to use the cache.

        Returns:
            list[Character]: The list of character objects.
        """
        endpoint = "character"
        data = await self._request(endpoint, game, use_cache, in_data=True)

        if game is Game.GI:
            characters = [gi.Character(id=char_id, **char) for char_id, char in data.items()]
            for char in characters:
                char.name = char.names[GI_LANG_MAP[self.lang]]
        else:
            characters = [hsr.Character(id=int(char_id), **char) for char_id, char in data.items()]
            for char in characters:
                char.name = char.names[HSR_API_LANG_MAP[self.lang]]

        return characters

    @overload
    async def fetch_character_detail(
        self, character_id: int, game: Literal[Game.GI], *, use_cache: bool = True
    ) -> gi.CharacterDetail: ...
    @overload
    async def fetch_character_detail(
        self, character_id: int, game: Literal[Game.HSR], *, use_cache: bool = True
    ) -> hsr.CharacterDetail: ...
    async def fetch_character_detail(
        self, character_id: int, game: Game, *, use_cache: bool = True
    ) -> gi.CharacterDetail | hsr.CharacterDetail:
        """Fetches a character with detailed info.

        Args:
            character_id (int): The character ID.
            game (Game): The game to fetch data for.
            use_cache (bool): Whether to use the cache.

        Returns:
            gi.CharacterDetail | hsr.CharacterDetail: The character object.
        """
        endpoint = f"character/{character_id}"
        data = await self._request(endpoint, game, use_cache)
        return gi.CharacterDetail(**data) if game is Game.GI else hsr.CharacterDetail(**data)

    async def fetch_weapons(self, *, use_cache: bool = True) -> list[gi.Weapon]:
        """Fetches all weapons in the game.

        Args:
            use_cache (bool): Whether to use the cache.

        Returns:
            list[Weapon]: The list of weapon objects.
        """
        endpoint = "weapon"
        data = await self._request(endpoint, Game.GI, use_cache, in_data=True)
        return [gi.Weapon(id=int(weapon_id), **weapon) for weapon_id, weapon in data.items()]

    async def fetch_weapon_detail(
        self, weapon_id: int, *, use_cache: bool = True
    ) -> gi.WeaponDetail:
        """Fetches a Genshin Impact weapon with detailed info.

        Args:
            weapon_id (int): The weapon ID.
            use_cache (bool): Whether to use the cache.

        Returns:
            Weapon: The weapon object.
        """
        endpoint = f"weapon/{weapon_id}"
        data = await self._request(endpoint, Game.GI, use_cache)
        return gi.WeaponDetail(**data)

    async def fetch_light_cones(self, *, use_cache: bool = True) -> list[hsr.LightCone]:
        """Fetches all light cones in the game.

        Args:
            use_cache (bool): Whether to use the cache.

        Returns:
            list[LightCone]: The list of light cone objects.
        """
        endpoint = "lightcone"
        data = await self._request(endpoint, Game.HSR, use_cache, in_data=True)
        return [
            hsr.LightCone(id=int(light_cone_id), **light_cone)
            for light_cone_id, light_cone in data.items()
        ]

    async def fetch_light_cone_detail(
        self, light_cone_id: int, *, use_cache: bool = True
    ) -> hsr.LightConeDetail:
        """Fetches a light cone with detailed info.

        Args:
            light_cone_id (int): The light cone ID.
            use_cache (bool): Whether to use the cache.

        Returns:
            LightCone: The light cone object.
        """
        endpoint = f"lightcone/{light_cone_id}"
        data = await self._request(endpoint, Game.HSR, use_cache)
        return hsr.LightConeDetail(**data)

    async def fetch_artifact_sets(self, *, use_cache: bool = True) -> list[gi.ArtifactSet]:
        """Fetches all artifact sets in the game.

        Args:
            use_cache (bool): Whether to use the cache.

        Returns:
            list[ArtifactSet]: The list of artifact set objects.
        """
        endpoint = "artifact"
        data = await self._request(endpoint, Game.GI, use_cache, in_data=True)
        sets = [gi.ArtifactSet(**set_) for set_ in data.values()]
        for set_ in sets:
            set_.set_effect.two_piece.name = set_.set_effect.two_piece.names[GI_LANG_MAP[self.lang]]
            set_.set_effect.two_piece.description = set_.set_effect.two_piece.descriptions[
                GI_LANG_MAP[self.lang]
            ]
            if set_.set_effect.four_piece is not None:
                set_.set_effect.four_piece.name = set_.set_effect.four_piece.names[
                    GI_LANG_MAP[self.lang]
                ]
                set_.set_effect.four_piece.description = set_.set_effect.four_piece.descriptions[
                    GI_LANG_MAP[self.lang]
                ]
        return sets

    async def fetch_artifact_set_detail(
        self, set_id: int, *, use_cache: bool = True
    ) -> gi.ArtifactSetDetail:
        """Fetches an artifact set with detailed info.

        Args:
            set_id (int): The artifact set ID.
            use_cache (bool): Whether to use the cache.

        Returns:
            ArtifactSet: The artifact set object.
        """
        endpoint = f"artifact/{set_id}"
        data = await self._request(endpoint, Game.GI, use_cache)
        return gi.ArtifactSetDetail(**data)

    async def fetch_relic_sets(self, *, use_cache: bool = True) -> list[hsr.RelicSet]:
        """Fetches all relic sets in the game.

        Args:
            use_cache (bool): Whether to use the cache.

        Returns:
            list[RelicSet]: The list of relic set objects.
        """
        endpoint = "relicset"
        data = await self._request(endpoint, Game.HSR, use_cache, in_data=True)
        sets = [hsr.RelicSet(id=int(set_id), **set_) for set_id, set_ in data.items()]

        for set_ in sets:
            set_.name = set_.names[HSR_API_LANG_MAP[self.lang]]
            two_piece = set_.set_effect.two_piece
            two_piece.description = replace_placeholders(
                cleanup_text(two_piece.descriptions[HSR_API_LANG_MAP[self.lang]]),
                two_piece.parameters,
            )
            if (four_piece := set_.set_effect.four_piece) is not None:
                four_piece.description = replace_placeholders(
                    cleanup_text(four_piece.descriptions[HSR_API_LANG_MAP[self.lang]]),
                    four_piece.parameters,
                )

        return sets

    async def fetch_relic_set_detail(
        self, set_id: int, *, use_cache: bool = True
    ) -> hsr.RelicSetDetail:
        """Fetches a relic set with detailed info.

        Args:
            set_id (int): The relic set ID.
            use_cache (bool): Whether to use the cache.

        Returns:
            RelicSet: The relic set object.
        """
        endpoint = f"relicset/{set_id}"
        data = await self._request(endpoint, Game.HSR, use_cache)
        return hsr.RelicSetDetail(**data)
