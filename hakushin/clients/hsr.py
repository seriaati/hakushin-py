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
        self._elite_groups_cache: dict[int, hsr.EliteGroup] | None = None
        self._hard_level_groups_cache: dict[tuple[int, int], hsr.HardLevelGroup] | None = None

    async def fetch_elite_groups(self, use_cache: bool = True) -> dict[int, hsr.EliteGroup]:
        """
        Download and structure EliteGroup.json into a dict keyed by EliteGroup ID.
        """
        if self._elite_groups_cache is not None and use_cache:
            return self._elite_groups_cache

        url = (
            "https://gitlab.com/Dimbreath/turnbasedgamedata/-/raw/main/ExcelOutput/EliteGroup.json"
        )
        raw = await self._download_gitlab_json(url, use_cache)

        self._elite_groups_cache = {
            item["EliteGroup"]: hsr.EliteGroup(**item) for item in raw if "EliteGroup" in item
        }

        return self._elite_groups_cache

    async def fetch_hard_level_groups(
        self, use_cache: bool = True
    ) -> dict[tuple[int, int], hsr.HardLevelGroup]:
        """
        Download and structure HardLevelGroup.json into a dict keyed by (HardLevelGroup, Level).
        """
        if self._hard_level_groups_cache is not None and use_cache:
            return self._hard_level_groups_cache

        url = "https://gitlab.com/Dimbreath/turnbasedgamedata/-/raw/main/ExcelOutput/HardLevelGroup.json"
        raw = await self._download_gitlab_json(url, use_cache)

        self._hard_level_groups_cache = {
            (item["HardLevelGroup"], item["Level"]): hsr.HardLevelGroup(**item)
            for item in raw
            if "HardLevelGroup" in item and "Level" in item
        }

        return self._hard_level_groups_cache

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

    async def fetch_moc_detail(
        self, moc_id: int, *, use_cache: bool = True
    ) -> hsr.MemoryOfChaosDetail:
        endpoint = f"maze/{moc_id}"
        data: list[dict[str, Any]] = await self._request(endpoint, use_cache)

        stages = [hsr.EndgameStage(**item) for item in data]

        return hsr.MemoryOfChaosDetail(id=moc_id, stages=stages)

    async def fetch_pf_detail(self, pf_id: int, *, use_cache: bool = True) -> hsr.PureFictionDetail:
        endpoint = f"story/{pf_id}"
        data: dict[str, Any] = await self._request(endpoint, use_cache)

        return hsr.PureFictionDetail(**data)

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

    def _calculate_hsr_enemy_stats(
        self,
        enemy_id: int,
        enemy_info: hsr.MonsterDetail,
        eg: hsr.EliteGroup,
        hlg: hsr.HardLevelGroup,
    ) -> hsr.HSREnemy | None:
        """
        Calculate the combat stats for a specific enemy instance in Memory of Chaos.

        Args:
            enemy_id: The unique ID of the enemy (can include phase/variant identifiers).
            enemy_info: The base monster details fetched from the monster database.
            eg: The elite group data used to scale the monster's stats.
            hlg: The hard level group data used to scale the monster's stats.

        Returns:
            An `HSREnemy` object containing the enemy's calculated stats, or None if no matching variant is found.
        """
        base_hp = 0
        speed = None
        toughness = None
        effect_res = None

        child = next((m for m in enemy_info.monster_types if m.id == enemy_id), None)

        if child:
            base_hp = round(enemy_info.hp_base * child.hp_modify_ratio * eg.hp_ratio * hlg.hp_ratio)
            if enemy_info.spd_base:
                speed = round(
                    enemy_info.spd_base * child.spd_modify_ratio * eg.spd_ratio * hlg.spd_ratio
                )
            if enemy_info.stance_base:
                toughness = round(
                    enemy_info.stance_base
                    * child.stance_modify_value
                    * eg.stance_ratio
                    * hlg.stance_ratio
                    / 3
                )
            if enemy_info.status_resistance_base:
                effect_res = enemy_info.status_resistance_base + hlg.status_resistance
        else:
            return None

        return hsr.HSREnemy(
            id=enemy_id,
            name=enemy_info.name,
            weaknesses=child.stance_weak_list,
            level=hlg.level,
            base_hp=base_hp,
            speed=speed,
            toughness=toughness,
            effect_res=effect_res,
        )

    async def calculate_hsr_moc_enemy_stats(
        self, moc_id: int, stage_num: int = 12
    ) -> list[list[list[hsr.HSREnemy]]]:
        """
        Fetch and calculate enemy stats for both halves of a Memory of Chaos stage.

        This function retrieves Memory of Chaos stage data using the provided client,
        extracts the relevant EliteGroup and HardLevelGroup multipliers, and computes
        full enemy stats (including HP, speed, toughness, and effect resistance) for
        each wave of both halves of the specified stage.

        Args:
            client: An initialized HSRClient instance used to fetch MoC and monster data.
            moc_id: The ID of the Memory of Chaos event to analyze.
            stage_num: The 1-indexed stage number within the MoC (defaults to 12).

        Returns:
            A list containing two elements—one for each half of the stage.
            Each half is a list of waves, and each wave is a list of `HSREnemy` objects
            (or None if a matching child monster variant cannot be found).

            The structure is:
                [
                    [  # First half
                        [HSREnemy, HSREnemy, ...],  # Wave 1
                        [HSREnemy, HSREnemy, ...],  # Wave 2
                    ],
                    [  # Second half
                        ...
                    ]
                ]
        """
        if not (1 <= stage_num <= 12):
            msg = "stage_num must be between 1 and 12 (inclusive)."
            raise ValueError(msg)

        moc: hsr.MemoryOfChaosDetail = await self.fetch_moc_detail(moc_id)
        stage: hsr.EndgameStage = moc.stages[stage_num - 1]

        egs: dict[int, hsr.EliteGroup] = await self.fetch_elite_groups()
        hlgs: dict[tuple[int, int], hsr.HardLevelGroup] = await self.fetch_hard_level_groups()

        result = []

        for half in (stage.first_half, stage.second_half):
            specific_eg: hsr.EliteGroup = egs[half.eg_id]
            specific_hlg: hsr.HardLevelGroup = hlgs[(half.hlg_id, half.hlg_level)]

            half_enemies: list[list[hsr.HSREnemy]] = []

            for wave in half.waves:
                wave_enemies: list[hsr.HSREnemy] = []
                for enemy_id in wave.enemies:
                    fetch_id = int(str(enemy_id)[:7]) if enemy_id > 9999999 else enemy_id
                    enemy_info = await self.fetch_monsters_detail(fetch_id)
                    enemy_stats = self._calculate_hsr_enemy_stats(
                        enemy_id=enemy_id, enemy_info=enemy_info, eg=specific_eg, hlg=specific_hlg
                    )
                    if enemy_stats:
                        wave_enemies.append(enemy_stats)
                half_enemies.append(wave_enemies)

            result.append(half_enemies)

        return result
