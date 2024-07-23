from __future__ import annotations

from typing import TYPE_CHECKING, Any

from ..constants import ZZZ_LANG_MAP
from ..enums import Game, Language
from ..models import zzz
from .base import BaseClient

if TYPE_CHECKING:
    from aiohttp import ClientSession

__all__ = ("ZZZClient",)


class ZZZClient(BaseClient):
    """Client to interact with the Hakushin Zenless Zone Zero API."""

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
            Game.ZZZ,
            lang,
            cache_path=cache_path,
            cache_ttl=cache_ttl,
            headers=headers,
            debug=debug,
            session=session,
        )

    async def fetch_new(self, *, use_cache: bool = True) -> zzz.New:
        """Fetch the ID of beta items in Zenless Zone Zero.

        Args:
            use_cache: Whether to use the response cache.

        Returns:
            A model representing the new items.
        """
        data = await self._request("new", use_cache, static=True)
        return zzz.New(**data)

    async def fetch_characters(self, *, use_cache: bool = True) -> list[zzz.Character]:
        """Fetch all Zenless Zone Zero characters.

        Args:
            use_cache: Whether to use the response cache.

        Returns:
            A list of character objects.
        """
        data = await self._request("character", use_cache, in_data=True)

        characters = [
            zzz.Character(id=int(char_id), **char)
            for char_id, char in data.items()
            if char_id not in {"2011", "2021"}  # Exclude MCs
        ]
        for char in characters:
            char.name = char.names[ZZZ_LANG_MAP[self.lang]]

        return characters

    async def fetch_character_detail(
        self, character_id: int, *, use_cache: bool = True
    ) -> zzz.CharacterDetail:
        """Fetch the details of a Zenless Zone Zero character.

        Args:
            character_id: The character ID.
            use_cache: Whether to use the response cache.

        Returns:
            The character details object.
        """
        endpoint = f"character/{character_id}"
        data = await self._request(endpoint, use_cache)
        return zzz.CharacterDetail(**data)

    async def fetch_weapons(self, *, use_cache: bool = True) -> list[zzz.Weapon]:
        """Fetch all Zenless Zone Zero weapons (w-engines).

        Args:
            use_cache: Whether to use the response cache.

        Returns:
            A list of weapon objects.
        """
        data = await self._request("weapon", use_cache, in_data=True)

        weapons = [zzz.Weapon(id=int(weapon_id), **weapon) for weapon_id, weapon in data.items()]
        for weapon in weapons:
            weapon.name = weapon.names[ZZZ_LANG_MAP[self.lang]]

        return weapons

    async def fetch_weapon_detail(
        self, weapon_id: int, *, use_cache: bool = True
    ) -> zzz.WeaponDetail:
        """Fetch the details of a Zenless Zone Zero weapon.

        Args:
            weapon_id: The weapon ID.
            use_cache: Whether to use the response cache.

        Returns:
            The weapon details object.
        """
        endpoint = f"weapon/{weapon_id}"
        data = await self._request(endpoint, use_cache)
        return zzz.WeaponDetail(**data)
