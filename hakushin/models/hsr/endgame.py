from __future__ import annotations

from abc import ABC
from typing import Any

from attr import dataclass
from pydantic import Field, field_validator, model_validator

from ...enums import HSRElement
from ..base import APIModel

__all__ = (
    "ApocalypticShadowBuff",
    "ApocalypticShadowDetail",
    "EndgameBuffOptions",
    "EndgameHalf",
    "EndgameStage",
    "EndgameWave",
    "HSREndgameBase",
    "HSREnemy",
    "MemoryOfChaosDetail",
    "PureFictionDetail",
)


@dataclass(kw_only=True)
class HSREnemy:
    """
    Represents a processed enemy instance in a HSR endgame stage.

    Attributes:
        id: The unique monster ID.
        name: The name of the enemy.
        weaknesses: A list of elements this enemy is weak to.
        level: The level of the enemy.
        base_hp: The calculated HP of the enemy after all multipliers.
        speed: The calculated speed value.
        toughness: The calculated toughness value.
        effect_res: Total status effect resistance value.
    """

    id: int
    name: str = ""
    weaknesses: list[HSRElement]
    level: int
    base_hp: int
    speed: int | None
    toughness: int | None
    effect_res: float | None


class EndgameWave(APIModel):
    """
    Represents a wave of enemies in an endgame half.

    Attributes:
        enemies: A list of enemy IDs in the wave.
        hp_multiplier: Multiplier applied to enemy HP in this wave.
    """

    enemies: list[int] = Field(default_factory=list)
    hp_multiplier: float = Field(alias="HPMultiplier", default=0)

    @field_validator("hp_multiplier", mode="before")
    @classmethod
    def handle_missing_hp(cls, value: Any) -> float:
        return 0 if value is None else value

    @model_validator(mode="before")
    @classmethod
    def extract_monster_ids(cls, values: dict[str, Any]) -> dict[str, Any]:
        enemies = []

        for key, val in values.items():
            if key.startswith("Monster") and isinstance(val, int):
                enemies.append(val)

        values["enemies"] = enemies
        return values


class EndgameHalf(APIModel):
    """
    Represents one half of an endgame stage (first or second).

    Attributes:
        hlg_id: ID of the HardLevelGroup used to determine difficulty scaling.
        hlg_level: Level of the HardLevelGroup (affects enemy stats).
        eg_id: ID of the EliteGroup (affects enemy traits).
        waves: List of enemy waves in this half.
    """

    hlg_id: int = Field(alias="HardLevelGroup")
    hlg_level: int = Field(alias="Level")
    eg_id: int = Field(alias="EliteGroup")
    waves: list[EndgameWave] = Field(alias="MonsterList")


class EndgameStage(APIModel):
    """
    Represents a complete stage in an endgame mode.

    Attributes:
        id: Unique ID of the stage.
        name: Stage name.
        first_half_weaknesses: Elements that enemies in the first half are weak to.
        second_half_weaknesses: Elements that enemies in the second half are weak to.
        first_half: The first half of the stage.
        second_half: The second half of the stage.
    """

    id: int = Field(alias="Id")
    name: str = Field(alias="Name")

    first_half_weaknesses: list[HSRElement] = Field(alias="DamageType1")
    second_half_weaknesses: list[HSRElement] = Field(alias="DamageType2")

    first_half: EndgameHalf = Field(alias="EventIDList1")
    second_half: EndgameHalf = Field(alias="EventIDList2")

    @model_validator(mode="before")
    @classmethod
    def _unwrap_event_lists(cls, values: dict[str, Any]) -> dict[str, Any]:
        if "EventIDList1" in values and isinstance(values["EventIDList1"], list):
            values["EventIDList1"] = values["EventIDList1"][0]
        if "EventIDList2" in values and isinstance(values["EventIDList2"], list):
            values["EventIDList2"] = values["EventIDList2"][0]
        return values


class HSREndgameBase(APIModel, ABC):
    """
    Abstract base class for all HSR endgame modes.

    Attributes:
        id: Unique ID of the endgame event.
        name: Display name of the event.
        begin_time: Event start timestamp.
        end_time: Event end timestamp.
        stages: List of stages in this endgame mode.
    """

    id: int = Field(alias="Id")
    name: str = Field(alias="Name")
    begin_time: str = Field(alias="BeginTime")
    end_time: str = Field(alias="EndTime")
    stages: list[EndgameStage] = Field(alias="Level")


class MemoryOfChaosDetail(HSREndgameBase):
    """
    Memory of Chaos event details.

    Attributes:
        memory_turbulence: Global modifier for the current MoC rotation.
    """

    memory_turbulence: str = Field(alias="MemoryTurbulence")

    @model_validator(mode="before")
    @classmethod
    def transform_data(cls, data: dict[str, Any]) -> dict[str, Any]:
        first_level = data["Level"][1]
        data["Name"] = first_level["GroupName"]
        data["MemoryTurbulence"] = first_level["Desc"]
        data["BeginTime"] = first_level["BeginTime"]
        data["EndTime"] = first_level["EndTime"]
        return data


class EndgameBuffOptions(APIModel):
    """
    Represents a selectable buff modifier in endgame.

    Attributes:
        name: Name of the buff.
        desc: Description of the buff effect.
        params: List of parameters applied by the buff.
    """

    name: str = Field(alias="Name")
    desc: str = Field(alias="Desc")
    params: list[float] = Field(alias="Param")


class ApocalypticShadowBuff(APIModel):
    """
    Represents the fixed global buff in Apocalyptic Shadow.

    Attributes:
        name: Name of the buff.
        desc: Description of the effect.
    """

    name: str = Field(alias="Name")
    desc: str = Field(alias="Desc")


class ApocalypticShadowDetail(HSREndgameBase):
    """
    Apocalyptic Shadow event details.

    Attributes:
        buff: The static global buff applied in all stages.
        buff_list_1: Selectable buffs for first half.
        buff_list_2: Selectable buffs for second half.
    """

    buff: ApocalypticShadowBuff = Field(alias="Buff")

    buff_list_1: list[EndgameBuffOptions] = Field(alias="BuffList1")
    buff_list_2: list[EndgameBuffOptions] = Field(alias="BuffList2")


class PureFictionDetail(HSREndgameBase):
    """
    Pure Fiction event details.

    Attributes:
        buff_options: First tier of optional buffs.
        buff_suboptions: Second tier of optional buffs.
    """

    buff_options: list[EndgameBuffOptions] = Field(alias="Option")
    buff_suboptions: list[EndgameBuffOptions] = Field(alias="SubOption")

    @model_validator(mode="before")
    @classmethod
    def transform_level_data(cls, data: dict[str, Any]) -> dict[str, Any]:
        levels = data.get("Level", [])
        transformed_stages = []

        for raw_stage in levels:
            infinite_list_stage_1 = list(raw_stage["InfiniteList1"].values())
            infinite_list_stage_2 = list(raw_stage["InfiniteList2"].values())
            raw_stage["EventIDList1"][0]["EliteGroup"] = infinite_list_stage_1[0]["EliteGroup"]
            raw_stage["EventIDList2"][0]["EliteGroup"] = infinite_list_stage_2[0]["EliteGroup"]

            raw_stage["EventIDList1"][0]["MonsterList"] = []

            for wave in infinite_list_stage_1:
                unique_wave_enemies = list(set(wave["MonsterGroupIDList"]))
                enemies_dict = {f"Monster{i}": enemy for i, enemy in enumerate(unique_wave_enemies)}
                enemies_dict["HPMultiplier"] = wave["ParamList"][1]
                raw_stage["EventIDList1"][0]["MonsterList"].append(enemies_dict)

            raw_stage["EventIDList2"][0]["MonsterList"] = []

            for wave in infinite_list_stage_2:
                unique_wave_enemies = list(set(wave["MonsterGroupIDList"]))
                enemies_dict = {f"Monster{i}": enemy for i, enemy in enumerate(unique_wave_enemies)}
                enemies_dict["HPMultiplier"] = wave["ParamList"][1]
                raw_stage["EventIDList2"][0]["MonsterList"].append(enemies_dict)
            transformed_stages.append(raw_stage)

        data["Level"] = transformed_stages
        return data
