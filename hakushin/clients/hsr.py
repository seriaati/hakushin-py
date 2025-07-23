from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING, Any, Literal, TypeVar, overload

from ..constants import HSR_API_LANG_MAP, TRAILBLAZER_NAMES
from ..enums import Game, HSREndgameType, Language
from ..models import hsr
from ..utils import cleanup_text, remove_ruby_tags, replace_placeholders
from .base import BaseClient

if TYPE_CHECKING:
    from aiohttp import ClientSession

T = TypeVar("T", bound=hsr.EndgameBaseModel)

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

    async def fetch_elite_and_hard_level_groups(
        self, use_cache: bool = True
    ) -> tuple[dict[int, hsr.EliteGroup], dict[tuple[int, int], hsr.HardLevelGroup]]:
        """Download and structure EliteGroup and HardLevelGroup data from a JavaScript module.

        Returns:
            A tuple of:
                - dict[int, EliteGroup]: keyed by EliteGroup ID
                - dict[tuple[int, int], HardLevelGroup]: keyed by (HardLevelGroup, Level)
        """
        if (
            self._elite_groups_cache is not None
            and self._hard_level_groups_cache is not None
            and use_cache
        ):
            return self._elite_groups_cache, self._hard_level_groups_cache

        url = "https://hsr20.hakush.in/_app/immutable/chunks/HardLevelGroup.085b3477.js"
        elite_raw, hlg_raw = await self._download_groups(url)

        self._elite_groups_cache = {
            item["EliteGroup"]: hsr.EliteGroup(**item) for item in elite_raw if "EliteGroup" in item
        }

        self._hard_level_groups_cache = {
            (item["HardLevelGroup"], item["Level"]): hsr.HardLevelGroup(**item)
            for item in hlg_raw
            if "HardLevelGroup" in item and "Level" in item
        }

        return self._elite_groups_cache, self._hard_level_groups_cache

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
        """Fetch the full detail of a specific monster.

        Args:
            monster_id: The ID of the monster to retrieve.
            use_cache: Whether to use the response cache.

        Returns:
            A `MonsterDetail` object containing the full monster stats and metadata.
        """
        endpoint = f"monster/{monster_id}"
        data = await self._request(endpoint, use_cache)
        return hsr.MonsterDetail(**data)

    async def fetch_moc(self, *, use_cache: bool = True) -> list[hsr.EndgameSummary]:
        """Fetch a list of Memory of Chaos (MoC) event summaries.

        Args:
            use_cache: Whether to use the response cache.

        Returns:
            A list of `EndgameSummary` objects for each MoC event.
        """
        data = await self._request("maze", use_cache, in_data=True)

        mocs = [
            hsr.EndgameSummary(type=HSREndgameType.MEMORY_OF_CHAOS, **moc)
            for _, moc in data.items()
        ]
        for moc in mocs:
            moc.name = remove_ruby_tags(moc.names[HSR_API_LANG_MAP[self.lang]])

        return mocs

    @overload
    async def fetch_moc_detail(
        self, moc_id: int, *, full: Literal[False] = ..., use_cache: bool = ...
    ) -> hsr.MOCDetail: ...
    @overload
    async def fetch_moc_detail(
        self, moc_id: int, *, full: Literal[True] = ..., use_cache: bool = ...
    ) -> hsr.FullMOCDetail: ...
    async def fetch_moc_detail(
        self, moc_id: int, *, full: bool = False, use_cache: bool = True
    ) -> hsr.MOCDetail | hsr.FullMOCDetail:
        """Fetch detailed stage and wave data for a specific Memory of Chaos event.

        Args:
            moc_id: The ID of the Memory of Chaos event to retrieve.
            use_cache: If True, use a cached response if available.
            full: If True, automatically resolve and attach `ProcessedEnemy` stats
                     to each wave in the stage data. If False, return raw model data.

        Returns:
            `FullMOCDetail` if `full=True`, otherwise `MOCDetail`.

        Note:
            When `full=True`, this method performs additional stat
            calculation using `calculate_hsr_enemy_stats()` and replaces enemy ID lists
            with `ProcessedEnemy` models directly on the wave objects.
        """
        endpoint = f"maze/{moc_id}"
        data: dict[str, Any] = await self._request(endpoint, use_cache)
        data["Id"] = moc_id

        detail = hsr.MOCDetail(**data)
        if full:
            return await self._replace_enemy_ids_with_enemies(detail)

        return detail

    async def fetch_pf(self, *, use_cache: bool = True) -> list[hsr.EndgameSummary]:
        """Fetch a list of Pure Fiction (PF) event summaries.

        Args:
            use_cache: Whether to use the response cache.

        Returns:
            A list of `EndgameSummary` objects for each Pure Fiction event.
        """
        data = await self._request("maze_extra", use_cache, in_data=True)

        pfs = [hsr.EndgameSummary(type=HSREndgameType.PURE_FICTION, **pf) for _, pf in data.items()]
        for pf in pfs:
            pf.name = remove_ruby_tags(pf.names[HSR_API_LANG_MAP[self.lang]])

        return pfs

    @overload
    async def fetch_pf_detail(
        self, pf_id: int, *, full: Literal[False] = ..., use_cache: bool = ...
    ) -> hsr.PFDetail: ...
    @overload
    async def fetch_pf_detail(
        self, pf_id: int, *, full: Literal[True] = ..., use_cache: bool = ...
    ) -> hsr.FullPFDetail: ...
    async def fetch_pf_detail(
        self, pf_id: int, *, full: bool = False, use_cache: bool = True
    ) -> hsr.PFDetail | hsr.FullPFDetail:
        """Fetch detailed stage and wave data for a specific Pure Fiction event.

        Args:
            pf_id: The ID of the Pure Fiction event.
            use_cache: Whether to use the response cache.
            full: If True, return calculated `ProcessedEnemy` stats instead of the raw model.

        Returns:
            `FullPFDetail` if `full=True`, otherwise `PFDetail`.

        Note:
            When `full=True`, this method performs additional stat
            calculation using `calculate_hsr_enemy_stats()` and replaces enemy ID lists
            with `ProcessedEnemy` models directly on the wave objects.
        """
        endpoint = f"story/{pf_id}"
        data: dict[str, Any] = await self._request(endpoint, use_cache)

        detail = hsr.PFDetail(**data)
        if full:
            return await self._replace_enemy_ids_with_enemies(detail)

        return detail

    async def fetch_apoc(self, *, use_cache: bool = True) -> list[hsr.EndgameSummary]:
        """Fetch a list of Apocalyptic Shadow (Apoc) event summaries.

        Args:
            use_cache: Whether to use the response cache.

        Returns:
            A list of `EndgameSummary` objects for each Apocalyptic Shadow event.
        """
        data = await self._request("maze_boss", use_cache, in_data=True)

        apocs = [
            hsr.EndgameSummary(type=HSREndgameType.APOCALYPTIC_SHADOW, **apoc)
            for _, apoc in data.items()
        ]
        for apoc in apocs:
            apoc.name = remove_ruby_tags(apoc.names[HSR_API_LANG_MAP[self.lang]])

        return apocs

    @overload
    async def fetch_apoc_detail(
        self, apoc_id: int, *, full: Literal[False] = ..., use_cache: bool = ...
    ) -> hsr.ApocDetail: ...
    @overload
    async def fetch_apoc_detail(
        self, apoc_id: int, *, full: Literal[True] = ..., use_cache: bool = ...
    ) -> hsr.FullApocDetail: ...
    async def fetch_apoc_detail(
        self, apoc_id: int, *, full: bool = False, use_cache: bool = True
    ) -> hsr.ApocDetail | hsr.FullApocDetail:
        """Fetch detailed stage and wave data for a specific Apocalyptic Shadow event.

        Args:
            apoc_id: The ID of the Apocalyptic Shadow event.
            use_cache: Whether to use the response cache.
            full: If True, return calculated `ProcessedEnemy` stats instead of the raw model.

        Returns:
            `FullApocDetail` if `full=True`, otherwise `ApocDetail`.

        Note:
            When `full=True`, this method performs additional stat
            calculation using `calculate_hsr_enemy_stats()` and replaces enemy ID lists
            with `ProcessedEnemy` models directly on the wave objects.
        """
        endpoint = f"boss/{apoc_id}"
        data: dict[str, Any] = await self._request(endpoint, use_cache)

        detail = hsr.ApocDetail(**data)
        if full:
            return await self._replace_enemy_ids_with_enemies(detail)

        return detail

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

    async def _replace_enemy_ids_with_enemies(self, detail: T) -> T:
        """
        Replaces enemy ID lists with `ProcessedEnemy` objects for all waves
        in the given endgame detail model.

        Args:
            detail: An endgame detail instance (e.g., MemoryOfChaosDetail).

        Returns:
            The same model with enriched enemy data per wave.
        """
        egs, hlgs = await self.fetch_elite_and_hard_level_groups()

        for stage_num, stage in enumerate(detail.stages):
            enemies = await self.calculate_hsr_enemy_stats(
                detail, egs=egs, hlgs=hlgs, stage_num=stage_num
            )

            first_half_enemies = enemies[0]
            for wave_num, wave_enemies in enumerate(first_half_enemies):
                wave = stage.first_half.waves[wave_num]
                wave.enemies = wave_enemies  # pyright: ignore[reportAttributeAccessIssue]

            if stage.second_half:
                second_half_enemies = enemies[1]
                for wave_num, wave_enemies in enumerate(second_half_enemies):
                    wave = stage.second_half.waves[wave_num]
                    wave.enemies = wave_enemies  # pyright: ignore[reportAttributeAccessIssue]

        return detail

    def _calculate_hsr_enemy_stats(
        self,
        enemy_id: int,
        enemy_info: hsr.MonsterDetail,
        eg: hsr.EliteGroup,
        hlg: hsr.HardLevelGroup,
        hp_multiplier: float = 0,
    ) -> hsr.ProcessedEnemy | None:
        """
        Calculate the combat stats for a specific enemy instance in and endgame mode.

        Formula used:
        Base x BaseModifyRatio x EliteGroup Ratio x HardLevelGroup(Level) Ratio x (1 + HPMultiplier if HP)

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
            base_hp = round(
                enemy_info.hp_base
                * child.hp_modify_ratio
                * eg.hp_ratio
                * hlg.hp_ratio
                * (1 + hp_multiplier)
            )
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

        return hsr.ProcessedEnemy(
            id=enemy_id,
            name=enemy_info.name,
            weaknesses=child.stance_weak_list,
            level=hlg.level,
            base_hp=base_hp,
            speed=speed,
            toughness=toughness,
            effect_res=effect_res,
        )

    async def calculate_hsr_enemy_stats(  # noqa: C901
        self,
        endgame_data: hsr.EndgameBaseModel,
        *,
        egs: dict[int, hsr.EliteGroup],
        hlgs: dict[tuple[int, int], hsr.HardLevelGroup],
        stage_num: int = 0,
    ) -> list[list[list[hsr.ProcessedEnemy]]]:
        """
        Calculate enemy stats for both halves of an Endgame stage from already fetched endgame detail.

        Args:
            endgame_data: The already fetched Endgame detail object (e.g., MemoryOfChaosDetail).
            egs: A dictionary of elite groups keyed by their IDs, get it from [fetch_elite_and_hard_level_groups][hakushin.clients.hsr.HSRClient.fetch_elite_and_hard_level_groups].
            hlgs: A dictionary of hard level groups keyed by (HardLevelGroup ID, Level), get it from [fetch_elite_and_hard_level_groups][hakushin.clients.hsr.HSRClient.fetch_elite_and_hard_level_groups].
            stage_num: The 0-indexed stage number within the endgame (defaults to 0).

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

        if not (0 <= stage_num < len(endgame_data.stages)):
            msg = f"stage_num {stage_num} is out of bounds. Must be between 0 and {len(endgame_data.stages) - 1}."
            raise IndexError(msg)

        stage: hsr.EndgameStage = endgame_data.stages[stage_num]

        # Fetch all the monster details first
        monster_details: dict[int, asyncio.Task[hsr.MonsterDetail]] = {}
        async with asyncio.TaskGroup() as tg:
            for half in (stage.first_half, stage.second_half):
                if half is None:
                    continue
                for wave in half.waves:
                    for enemy_id in wave.enemies:
                        fetch_id = int(str(enemy_id)[:7]) if enemy_id > 9999999 else enemy_id
                        monster_details[fetch_id] = tg.create_task(
                            self.fetch_monsters_detail(fetch_id)
                        )

        result: list[list[list[hsr.ProcessedEnemy]]] = []

        for half in (stage.first_half, stage.second_half):
            if half is None:
                continue

            specific_eg: hsr.EliteGroup = egs[half.eg_id]
            specific_hlg: hsr.HardLevelGroup = hlgs[(half.hlg_id, half.hlg_level)]

            half_enemies: list[list[hsr.ProcessedEnemy]] = []

            for wave in half.waves:
                wave_enemies: list[hsr.ProcessedEnemy] = []
                for enemy_id in wave.enemies:
                    fetch_id = int(str(enemy_id)[:7]) if enemy_id > 9999999 else enemy_id
                    enemy_info = monster_details[fetch_id].result()
                    enemy_stats = self._calculate_hsr_enemy_stats(
                        enemy_id=enemy_id,
                        enemy_info=enemy_info,
                        eg=specific_eg,
                        hlg=specific_hlg,
                        hp_multiplier=wave.hp_multiplier,
                    )
                    if enemy_stats:
                        wave_enemies.append(enemy_stats)
                half_enemies.append(wave_enemies)

            result.append(half_enemies)

        return result
