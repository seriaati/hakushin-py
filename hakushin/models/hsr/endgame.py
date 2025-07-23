from __future__ import annotations

from typing import Any, Literal

from pydantic import Field, field_validator, model_validator

from ...enums import HSRElement, HSREndgameType
from ..base import APIModel

__all__ = (
    "ApocBuff",
    "ApocDetail",
    "EndgameBaseModel",
    "EndgameBuffOptions",
    "EndgameHalf",
    "EndgameStage",
    "EndgameSummary",
    "EndgameWave",
    "FullApocDetail",
    "FullEndgameBaseModel",
    "FullEndgameHalf",
    "FullEndgameStage",
    "FullEndgameWave",
    "FullMOCDetail",
    "FullPFDetail",
    "MOCDetail",
    "ProcessedEnemy",
    "PFDetail",
)


class ProcessedEnemy(APIModel):
    """Represents a processed enemy instance in a HSR endgame stage.

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
    """Represents a wave of enemies in an endgame half.

    Attributes:
        enemies: A list of enemy IDs.
        hp_multiplier: Multiplier applied to enemy HP in this wave.
    """

    enemies: list[int] = Field(default_factory=list)
    hp_multiplier: float = Field(alias="HPMultiplier", default=0)

    @field_validator("hp_multiplier", mode="before")
    @classmethod
    def __handle_missing_hp(cls, value: Any) -> float:
        return 0 if value is None else value

    @model_validator(mode="before")
    @classmethod
    def __extract_monster_ids(cls, values: dict[str, Any]) -> dict[str, Any]:
        """
        If this model is being parsed from a raw dictionary with Monster1, Monster2... keys,
        extract them into the 'enemies' list. Otherwise, assume enemies is already provided.
        """
        if "enemies" not in values:
            enemies = []
            for key, val in values.items():
                if key.startswith("Monster") and isinstance(val, int):
                    enemies.append(val)
            values["enemies"] = enemies
        return values


class FullEndgameWave(EndgameWave):
    """Represents a wave of processed enemies in an endgame half.

    Attributes:
        enemies: A list of fully processed enemy instances.
    """

    enemies: list[ProcessedEnemy] = Field(default_factory=list)  # type: ignore


class EndgameHalf(APIModel):
    """Represents one half of an endgame stage (first or second).

    Attributes:
        hlg_id: ID of the HardLevelGroup used to determine difficulty scaling.
        hlg_level: Level of the HardLevelGroup (affects enemy stats).
        eg_id: ID of the EliteGroup (affects enemy traits).
        waves: List of enemy waves in this half.
    """

    hlg_id: int = Field(alias="HardLevelGroup", default=1)
    hlg_level: int = Field(alias="Level", default=1)
    eg_id: int = Field(alias="EliteGroup", default=1)
    waves: list[EndgameWave] = Field(alias="MonsterList")


class FullEndgameHalf(EndgameHalf):
    """Represents one half of an endgame stage (first or second) with processed enemies.

    Attributes:
        waves: List of enemy waves in this half with processed enemies.
    """

    waves: list[FullEndgameWave] = Field(alias="MonsterList")


class EndgameStage(APIModel):
    """Represents a stage in an endgame mode.

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
    second_half: EndgameHalf | None = Field(alias="EventIDList2")

    @model_validator(mode="before")
    @classmethod
    def __unwrap_event_lists(cls, values: dict[str, Any]) -> dict[str, Any]:
        if "EventIDList1" in values and isinstance(values["EventIDList1"], list):
            values["EventIDList1"] = values["EventIDList1"][0]

        if "EventIDList2" in values:
            if isinstance(values["EventIDList2"], list) and values["EventIDList2"]:
                values["EventIDList2"] = values["EventIDList2"][0]
            elif not values["EventIDList2"]:
                values["EventIDList2"] = None  # Let Pydantic handle it as optional
        else:
            values["EventIDList2"] = None

        return values


class FullEndgameStage(EndgameStage):
    """Represents a stage in an endgame mode with processed enemies.

    Attributes:
        first_half: The first half of the stage with processed enemies.
        second_half: The second half of the stage with processed enemies.
    """

    first_half: FullEndgameHalf = Field(alias="EventIDList1")
    second_half: FullEndgameHalf | None = Field(alias="EventIDList2")


class EndgameBaseModel(APIModel):
    """Abstract base class for all HSR endgame modes.

    Attributes:
        id: Unique ID of the endgame event.
        name: Display name of the event.
        begin_time: Event start timestamp.
        end_time: Event end timestamp.
        stages: List of stages in this endgame mode.
    """

    id: int = Field(alias="Id")
    name: str = Field(alias="Name", default="")
    begin_time: str = Field(alias="BeginTime", default="")
    end_time: str = Field(alias="EndTime", default="")
    stages: list[EndgameStage] = Field(alias="Level")

    @field_validator("name", "begin_time", "end_time", mode="before")
    @classmethod
    def __handle_missing_fields(cls, value: Any) -> str:
        return "" if value is None else value


class FullEndgameBaseModel(EndgameBaseModel):
    """Endgame base model with fully processed enemies.

    Attributes:
        stages: List of stages in this endgame mode with processed enemies.
    """

    stages: list[FullEndgameStage] = Field(alias="Level")


class EndgameSummary(APIModel):
    """Summary metadata for an HSR endgame event.

    Attributes:
        id: ID of the endgame.
        type: The type/category of the endgame.
        names: Dictionary containing localized names in English (en), Chinese (cn), Korean (kr), and Japanese (jp).
        name: The selected name to display (populated during post-processing).
        begin: Event start timestamp.
        end: Event end timestamp.
    """

    id: int
    type: HSREndgameType
    names: dict[Literal["en", "cn", "kr", "jp"], str]
    name: str = Field("")  # The value of this field is assigned in post processing.
    begin: str = Field(alias="live_begin", default="")
    end: str = Field(alias="live_end", default="")

    @model_validator(mode="before")
    @classmethod
    def __transform_names(cls, values: dict[str, Any]) -> dict[str, Any]:
        values["names"] = {
            "en": values.pop("en", "") or "",
            "cn": values.pop("cn", "") or "",
            "kr": values.pop("kr", "") or "",
            "jp": values.pop("jp", "") or "",
        }
        return values


class MOCMixin:
    @model_validator(mode="before")
    @classmethod
    def __transform_data(cls, data: dict[str, Any]) -> dict[str, Any]:
        first_level = data["Level"][0]
        data["Name"] = first_level["GroupName"]
        data["MemoryTurbulence"] = first_level["Desc"]
        data["BeginTime"] = first_level["BeginTime"]
        data["EndTime"] = first_level["EndTime"]
        return data


class MOCDetail(EndgameBaseModel, MOCMixin):
    """Memory of Chaos event details.

    Attributes:
        memory_turbulence: Global modifier for the current MoC rotation.
    """

    memory_turbulence: str = Field(alias="MemoryTurbulence")


class FullMOCDetail(FullEndgameBaseModel, MOCMixin):
    """Memory of Chaos event details with processed enemies.

    Attributes:
        memory_turbulence: Global modifier for the current MoC rotation.
    """

    memory_turbulence: str = Field(alias="MemoryTurbulence")


class EndgameBuffOptions(APIModel):
    """Represents a selectable buff modifier in endgame.

    Attributes:
        name: Name of the buff.
        desc: Description of the buff effect.
        params: List of parameters applied by the buff.
    """

    name: str = Field(alias="Name")
    desc: str = Field(alias="Desc")
    params: list[float] = Field(alias="Param")


class ApocBuff(APIModel):
    """Represents the fixed global buff in Apocalyptic Shadow.

    Attributes:
        name: Name of the buff.
        desc: Description of the effect.
    """

    name: str = Field(alias="Name", default="")
    desc: str = Field(alias="Desc", default="")

    @field_validator("name", "desc", mode="before")
    @classmethod
    def __handle_missing_fields(cls, value: Any) -> str:
        return "" if value is None else value


class ApocDetail(EndgameBaseModel):
    """Apocalyptic Shadow event details.

    Attributes:
        buff: The static global buff applied in all stages.
        buff_list_1: Selectable buffs for first half.
        buff_list_2: Selectable buffs for second half.
    """

    buff: ApocBuff = Field(alias="Buff")

    buff_list_1: list[EndgameBuffOptions] = Field(alias="BuffList1")
    buff_list_2: list[EndgameBuffOptions] = Field(alias="BuffList2")


class FullApocDetail(FullEndgameBaseModel):
    """Apocalyptic Shadow event details with processed enemies.

    Attributes:
        buff: The static global buff applied in all stages.
        buff_list_1: Selectable buffs for first half.
        buff_list_2: Selectable buffs for second half.
    """

    buff: ApocBuff = Field(alias="Buff")

    buff_list_1: list[EndgameBuffOptions] = Field(alias="BuffList1")
    buff_list_2: list[EndgameBuffOptions] = Field(alias="BuffList2")


class PFDetail(EndgameBaseModel):
    """Pure Fiction event details.

    Attributes:
        buff_options: First tier of optional buffs.
        buff_suboptions: Second tier of optional buffs.
    """

    buff_options: list[EndgameBuffOptions] = Field(alias="Option")
    buff_suboptions: list[EndgameBuffOptions] = Field(alias="SubOption")


class FullPFDetail(FullEndgameBaseModel):
    """Pure Fiction event details with processed enemies.

    Attributes:
        buff_options: First tier of optional buffs.
        buff_suboptions: Second tier of optional buffs.
    """

    buff_options: list[EndgameBuffOptions] = Field(alias="Option")
    buff_suboptions: list[EndgameBuffOptions] = Field(alias="SubOption")

    @model_validator(mode="before")
    @classmethod
    def __transform_level_data(cls, data: dict[str, Any]) -> dict[str, Any]:
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
                param_list = wave.get("ParamList", [])
                enemies_dict["HPMultiplier"] = param_list[1] if len(param_list) > 1 else 0.0
                raw_stage["EventIDList1"][0]["MonsterList"].append(enemies_dict)

            raw_stage["EventIDList2"][0]["MonsterList"] = []

            for wave in infinite_list_stage_2:
                unique_wave_enemies = list(set(wave["MonsterGroupIDList"]))
                enemies_dict = {f"Monster{i}": enemy for i, enemy in enumerate(unique_wave_enemies)}
                param_list = wave.get("ParamList", [])
                enemies_dict["HPMultiplier"] = param_list[1] if len(param_list) > 1 else 0.0
                raw_stage["EventIDList2"][0]["MonsterList"].append(enemies_dict)
            transformed_stages.append(raw_stage)

        data["Level"] = transformed_stages
        return data
