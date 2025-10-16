from __future__ import annotations

from typing import TYPE_CHECKING, Any

from ..constants import ZZZ_LANG_MAP
from ..enums import Game, Language
from ..models import zzz
from .base import BaseClient

if TYPE_CHECKING:
    from collections.abc import Sequence

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

    async def fetch_characters(
        self, *, version: str | None = None, use_cache: bool = True
    ) -> list[zzz.Character]:
        """Fetch all Zenless Zone Zero characters.

        Args:
            use_cache: Whether to use the response cache.

        Returns:
            A list of character objects.
        """
        data = await self._request("character", use_cache, in_data=True, version=version)

        characters = [
            zzz.Character(id=int(char_id), **char)
            for char_id, char in data.items()
            if char_id not in {"2011", "2021"}  # Exclude MCs
        ]
        for char in characters:
            char.name = char.names[ZZZ_LANG_MAP[self.lang]]

        return characters

    async def fetch_character_detail(
        self, character_id: int, *, version: str | None = None, use_cache: bool = True
    ) -> zzz.CharacterDetail:
        """Fetch the details of a Zenless Zone Zero character.

        Args:
            character_id: The character ID.
            version: The game version to fetch data for.
            use_cache: Whether to use the response cache.

        Returns:
            The character details object.
        """
        endpoint = f"character/{character_id}"
        data = await self._request(endpoint, use_cache, version=version)
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

    async def fetch_bangboos(self, *, use_cache: bool = True) -> list[zzz.Bangboo]:
        """Fetch all Zenless Zone Zero bangboos.

        Args:
            use_cache: Whether to use the response cache.

        Returns:
            A list of bangboo objects.
        """
        data = await self._request("bangboo", use_cache, in_data=True)
        bangboos = [
            zzz.Bangboo(id=int(bangboo_id), **bangboo) for bangboo_id, bangboo in data.items()
        ]
        for bangboo in bangboos:
            bangboo.name = bangboo.names[ZZZ_LANG_MAP[self.lang]]
        return bangboos

    async def fetch_bangboo_detail(
        self, bangboo_id: int, *, use_cache: bool = True
    ) -> zzz.BangbooDetail:
        """Fetch the details of a Zenless Zone Zero bangboo.

        Args:
            bangboo_id: The bangboo ID.
            use_cache: Whether to use the response cache.

        Returns:
            The bangboo details object.
        """
        endpoint = f"bangboo/{bangboo_id}"
        data = await self._request(endpoint, use_cache)
        return zzz.BangbooDetail(**data)

    async def fetch_drive_discs(self, *, use_cache: bool = True) -> list[zzz.DriveDisc]:
        """Fetch all Zenless Zone Zero drive discs.

        Args:
            use_cache: Whether to use the response cache.

        Returns:
            A list of drive disc objects.
        """
        data = await self._request("equipment", use_cache, in_data=True)
        drive_discs = [
            zzz.DriveDisc(id=int(drive_disc_id), **drive_disc)
            for drive_disc_id, drive_disc in data.items()
        ]
        for drive_disc in drive_discs:
            if self.lang is Language.EN:
                info = drive_disc.en_info
            elif self.lang is Language.KO:
                info = drive_disc.ko_info
            elif self.lang is Language.ZH:
                info = drive_disc.chs_info
            else:
                info = drive_disc.ja_info

            if info is None:
                continue

            drive_disc.name = info.name
            drive_disc.two_piece_effect = info.two_piece_effect
            drive_disc.four_piece_effect = info.four_piece_effect

        return drive_discs

    async def fetch_drive_disc_detail(
        self, drive_disc_id: int, *, use_cache: bool = True
    ) -> zzz.DriveDiscDetail:
        """Fetch the details of a Zenless Zone Zero drive disc.

        Args:
            drive_disc_id: The drive disc ID.
            use_cache: Whether to use the response cache.

        Returns:
            The drive disc details object.
        """
        endpoint = f"equipment/{drive_disc_id}"
        data = await self._request(endpoint, use_cache)
        return zzz.DriveDiscDetail(**data)

    async def fetch_items(self, *, use_cache: bool = True) -> Sequence[zzz.Item]:
        """Fetch all Zenless Zone Zero items.

        Args:
            use_cache: Whether to use the response cache.

        Returns:
            A list of item objects.
        """
        data = await self._request("item", use_cache)
        items = [zzz.Item(id=int(item_id), **item) for item_id, item in data.items()]
        return items
