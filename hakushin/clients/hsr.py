from __future__ import annotations

from typing import TYPE_CHECKING, Any

from ..constants import HSR_API_LANG_MAP, TRAILBLAZER_NAMES
from ..enums import Game, Language
from ..models import hsr
from ..utils import cleanup_text, remove_ruby_tags, replace_placeholders
from .base import BaseClient

if TYPE_CHECKING:
    from aiohttp import ClientSession

__all__ = ("HSRClient",)


class HSRClient(BaseClient):
    """Client to interact with the Hakushin Honkai Star Rail API."""

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
            Game.HSR,
            lang,
            cache_path=cache_path,
            cache_ttl=cache_ttl,
            headers=headers,
            debug=debug,
            session=session,
        )

    async def fetch_elite_groups(self, use_cache: bool = True) -> dict[int, hsr.EliteGroup]:
        """
        Download and structure EliteGroup.json into a dict keyed by EliteGroup ID.
        """
        url = (
            "https://gitlab.com/Dimbreath/turnbasedgamedata/-/raw/main/ExcelOutput/EliteGroup.json"
        )
        raw = await self._download_gitlab_json(url, use_cache)

        return {item["EliteGroup"]: hsr.EliteGroup(**item) for item in raw if "EliteGroup" in item}

    async def fetch_hard_level_groups(
        self, use_cache: bool = True
    ) -> dict[tuple[int, int], hsr.HardLevelGroup]:
        """
        Download and structure HardLevelGroup.json into a dict keyed by (HardLevelGroup, Level).
        """
        url = "https://gitlab.com/Dimbreath/turnbasedgamedata/-/raw/main/ExcelOutput/HardLevelGroup.json"
        raw = await self._download_gitlab_json(url, use_cache)

        return {
            (item["HardLevelGroup"], item["Level"]): hsr.HardLevelGroup(**item)
            for item in raw
            if "HardLevelGroup" in item and "Level" in item
        }

    async def fetch_new(self, *, use_cache: bool = True) -> hsr.New:
        """Fetch the ID of beta items in Honkai Star Rail.

        Args:
            use_cache: Whether to use the response cache.

        Returns:
            A model representing the new items.
        """
        data = await self._request("new", use_cache, static=True)
        return hsr.New(**data)

    async def fetch_monsters(self, *, use_cache: bool = True) -> list[hsr.Monster]:
        """Fetch all Honkai Star Rail monsters.

        Args:
            use_cache: Whether to use the response cache.

        Returns:
            A list of monster objects.
        """
        data = await self._request("monster", use_cache, in_data=True)

        monsters = [
            hsr.Monster(id=int(monster_id), **monster) for monster_id, monster in data.items()
        ]
        for monster in monsters:
            monster.name = remove_ruby_tags(monster.names[HSR_API_LANG_MAP[self.lang]])

        return monsters

    async def fetch_monsters_detail(
        self, monster_id: int, *, use_cache: bool = True
    ) -> hsr.MonsterDetail:
        endpoint = f"monster/{monster_id}"
        data = await self._request(endpoint, use_cache)
        return hsr.MonsterDetail(**data)

    async def fetch_characters(self, *, use_cache: bool = True) -> list[hsr.Character]:
        """Fetch all Honkai Star Rail characters.

        Args:
            use_cache: Whether to use the response cache.

        Returns:
            A list of character objects.
        """
        data = await self._request("character", use_cache, in_data=True)

        characters = [hsr.Character(id=int(char_id), **char) for char_id, char in data.items()]
        for char in characters:
            char.name = remove_ruby_tags(char.names[HSR_API_LANG_MAP[self.lang]])
            if char.name == "{NICKNAME}":
                char.name = TRAILBLAZER_NAMES[self.lang]

        return characters

    async def fetch_character_detail(
        self, character_id: int, *, use_cache: bool = True
    ) -> hsr.CharacterDetail:
        """Fetch the details of a Honkai Star Rail character.

        Args:
            character_id: The character ID.
            use_cache: Whether to use the response cache.

        Returns:
            The character details object.
        """
        endpoint = f"character/{character_id}"
        data = await self._request(endpoint, use_cache)
        return hsr.CharacterDetail(**data)

    async def fetch_light_cones(self, *, use_cache: bool = True) -> list[hsr.LightCone]:
        """Fetch all Honkai Star Rail light cones.

        Args:
            use_cache: Whether to use the response cache.

        Returns:
            A list of light cone objects.
        """
        endpoint = "lightcone"
        data = await self._request(endpoint, use_cache, in_data=True)
        light_cones = [
            hsr.LightCone(id=int(light_cone_id), **light_cone)
            for light_cone_id, light_cone in data.items()
        ]
        for light_cone in light_cones:
            light_cone.name = remove_ruby_tags(light_cone.names[HSR_API_LANG_MAP[self.lang]])
        return light_cones

    async def fetch_light_cone_detail(
        self, light_cone_id: int, *, use_cache: bool = True
    ) -> hsr.LightConeDetail:
        """Fetch the details of a Honkai Star Rail light cone.

        Args:
            light_cone_id: The light cone ID.
            use_cache: Whether to use the response cache.

        Returns:
            The light cone details object.
        """
        endpoint = f"lightcone/{light_cone_id}"
        data = await self._request(endpoint, use_cache)
        return hsr.LightConeDetail(**data)

    async def fetch_relic_sets(self, *, use_cache: bool = True) -> list[hsr.RelicSet]:
        """Fetch all Honkai Star Rail relic sets.

        Args:
            use_cache: Whether to use the response cache.

        Returns:
            A list of relic set objects.
        """
        endpoint = "relicset"
        data = await self._request(endpoint, use_cache, in_data=True)
        sets = [hsr.RelicSet(id=int(set_id), **set_) for set_id, set_ in data.items()]

        for set_ in sets:
            set_.name = remove_ruby_tags(set_.names[HSR_API_LANG_MAP[self.lang]])
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
        """Fetch the details of a Honkai Star Rail relic set.

        Args:
            set_id: The relic set ID.
            use_cache: Whether to use the response cache.

        Returns:
            The relic set details object.
        """
        endpoint = f"relicset/{set_id}"
        data = await self._request(endpoint, use_cache)
        return hsr.RelicSetDetail(**data)
