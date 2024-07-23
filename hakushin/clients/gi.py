from __future__ import annotations

from typing import TYPE_CHECKING, Any

from hakushin.enums import Game, Language

from ..constants import GI_LANG_MAP
from ..models import gi
from .base import BaseClient

if TYPE_CHECKING:
    from aiohttp import ClientSession

__all__ = ("GIClient",)


class GIClient(BaseClient):
    """Client to interact with the Hakushin Genshin Impact API."""

    def __init__(
        self,
        lang: Language = Language.EN,
        *,
        cache_path: str = "./.cache/hakushin/aiohttp-cache.db",
        cache_ttl: int = 3600,
        headers: dict[str, Any] | None = None,
        debug: bool = False,
        session: ClientSession | None = None,
    ) -> None:
        super().__init__(
            Game.GI,
            lang,
            cache_path=cache_path,
            cache_ttl=cache_ttl,
            headers=headers,
            debug=debug,
            session=session,
        )

    async def fetch_new(self, *, use_cache: bool = True) -> gi.New:
        """Fetch the ID of beta items in Genshin Impact.

        Args:
            use_cache: Whether to use the response cache.

        Returns:
            A model representing the new items.
        """
        data = await self._request("new", use_cache, static=True)
        return gi.New(**data)

    async def fetch_characters(self, *, use_cache: bool = True) -> list[gi.Character]:
        """Fetch all Genshin Impact characters.

        Args:
            use_cache: Whether to use the response cache.

        Returns:
            A list of character objects.
        """
        data = await self._request("character", use_cache, in_data=True)

        characters = [gi.Character(id=char_id, **char) for char_id, char in data.items()]
        for char in characters:
            char.name = char.names[GI_LANG_MAP[self.lang]]

        return characters

    async def fetch_character_detail(
        self, character_id: str, *, use_cache: bool = True
    ) -> gi.CharacterDetail:
        """Fetch the details of a Genshin Impact character.

        Args:
            character_id: The character ID.
            use_cache: Whether to use the response cache.

        Returns:
            The character details object.
        """
        endpoint = f"character/{character_id}"
        data = await self._request(endpoint, use_cache)
        return gi.CharacterDetail(**data)

    async def fetch_weapons(self, *, use_cache: bool = True) -> list[gi.Weapon]:
        """Fetch all Genshin Impact weapons.

        Args:
            use_cache: Whether to use the response cache.

        Returns:
            A list of weapon objects.
        """
        endpoint = "weapon"
        data = await self._request(endpoint, use_cache, in_data=True)
        weapons = [gi.Weapon(id=int(weapon_id), **weapon) for weapon_id, weapon in data.items()]
        for weapon in weapons:
            weapon.name = weapon.names[GI_LANG_MAP[self.lang]]
        return weapons

    async def fetch_weapon_detail(
        self, weapon_id: int, *, use_cache: bool = True
    ) -> gi.WeaponDetail:
        """Fetch the details of a Genshin Impact weapon.

        Args:
            weapon_id: The weapon ID.
            use_cache: Whether to use the response cache.

        Returns:
            The weapon details object.
        """
        endpoint = f"weapon/{weapon_id}"
        data = await self._request(endpoint, use_cache)
        return gi.WeaponDetail(**data)

    async def fetch_artifact_sets(self, *, use_cache: bool = True) -> list[gi.ArtifactSet]:
        """Fetch all Genshin Impact artifact sets.

        Args:
            use_cache: Whether to use the response cache.

        Returns:
            A list of artifact set objects.
        """
        endpoint = "artifact"
        data = await self._request(endpoint, use_cache, in_data=True)
        sets = [gi.ArtifactSet(**set_) for set_ in data.values()]
        for set_ in sets:
            set_.name = set_.names[GI_LANG_MAP[self.lang]]
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
        """Fetch the details of a Genshin Impact artifact set.

        Args:
            set_id: The artifact set ID.
            use_cache: Whether to use the response cache.

        Returns:
            The artifact set details object.
        """
        endpoint = f"artifact/{set_id}"
        data = await self._request(endpoint, use_cache)
        return gi.ArtifactSetDetail(**data)
