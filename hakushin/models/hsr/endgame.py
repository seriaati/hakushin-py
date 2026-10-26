from __future__ import annotations

import re
from typing import Any, Literal

from pydantic import Field, field_validator, model_validator

from ...enums import HSRElement, HSREndgameType
from ...utils import cleanup_text, replace_placeholders
from ..base import APIModel

__all__ = (
    "ApocBuff",
    "ApocDetail",
    "EndgameBaseModel",
    "EndgameBuffOptions",
    "EndgameChallenge",
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
    "PFDetail",
    "ProcessedEnemy",
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
    hp_multiplier: float = Field(alias="hp_multiplier", default=0)

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
                if (key.startswith(("Monster", "monster"))) and isinstance(val, int):
                    enemies.append(val)
            values["enemies"] = enemies
        return values


class FullEndgameWave(EndgameWave):
    """Represents a wave of processed enemies in an endgame half.

    Attributes:
        enemies: A list of processed enemy instances.
        hp_multiplier: Multiplier applied to enemy HP in this wave.
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

    hlg_id: int = Field(alias="hard_level_group", default=1)
    hlg_level: int = Field(alias="level", default=1)
    eg_id: int = Field(alias="elite_group", default=1)
    waves: list[EndgameWave] = Field(alias="monster_list")


class FullEndgameHalf(EndgameHalf):
    """Represents one half of an endgame stage (first or second) with processed enemies.

    Attributes:
        hlg_id: ID of the HardLevelGroup used to determine difficulty scaling.
        hlg_level: Level of the HardLevelGroup (affects enemy stats).
        eg_id: ID of the EliteGroup (affects enemy traits).
        waves: List of enemy waves in this half with processed enemies.
    """

    waves: list[FullEndgameWave] = Field(alias="monster_list")


class EndgameChallenge(APIModel):
    """Represents a star requirement of an endgame stage.

    Attributes:
        name: The formatted requirement text.
        param: The value substituted into the requirement text.
    """

    name: str
    param: int = 0

    @model_validator(mode="before")
    @classmethod
    def __format_name(cls, values: dict[str, Any]) -> dict[str, Any]:
        values["name"] = re.sub(
            r"#1(\[[^\]]*\])?", str(values.get("param") or 0), values.get("name") or ""
        )
        return values


class EndgameStage(APIModel):
    """Represents a stage in an endgame mode.

    A stage with `pre_id` set is the single-half extra node that follows the stage
    with that ID (e.g. node 3 of the last Memory of Chaos stage).

    Attributes:
        id: Unique ID of the stage.
        name: Stage name, empty for extra nodes.
        pre_id: ID of the stage this extra node follows, if any.
        first_half_weaknesses: Elements that enemies in the first half are weak to.
        second_half_weaknesses: Elements that enemies in the second half are weak to.
        first_half: The first half of the stage.
        second_half: The second half of the stage.
        challenges: The star requirements of the stage.
        special_challenge: The extra requirement of an extra node, if any.
        cycle_limit: The raw countdown value; the number of cycles available in Memory of Chaos.
    """

    id: int
    name: str = ""
    pre_id: int | None = None

    first_half_weaknesses: list[HSRElement] = Field(alias="damage_type1")
    second_half_weaknesses: list[HSRElement] = Field(alias="damage_type2", default_factory=list)

    first_half: EndgameHalf = Field(alias="event_id_list1")
    second_half: EndgameHalf | None = Field(alias="event_id_list2")

    challenges: list[EndgameChallenge] = Field(alias="challenge", default_factory=list)
    special_challenge: EndgameChallenge | None = Field(alias="challenge_special", default=None)
    cycle_limit: int | None = Field(alias="countdown", default=None)

    @field_validator("name", mode="before")
    @classmethod
    def __handle_missing_name(cls, value: str | None) -> str:
        return "" if value is None else value

    @model_validator(mode="before")
    @classmethod
    def __unwrap_event_lists(cls, values: dict[str, Any]) -> dict[str, Any]:
        # Extra nodes have a single half under unnumbered keys
        for key in ("event_id_list", "damage_type"):
            if key in values and f"{key}1" not in values:
                values[f"{key}1"] = values.pop(key)

        for key in ["event_id_list1", "event_id_list2", "EventIDList1", "EventIDList2"]:
            if key in values:
                new_key = key.lower()
                if isinstance(values[key], list) and values[key]:
                    values[new_key] = values[key][0]
                elif not values[key]:
                    values[new_key] = None

        if "event_id_list2" not in values:
            values["event_id_list2"] = None

        return values


class FullEndgameStage(EndgameStage):
    """Represents a stage in an endgame mode with processed enemies.

    Attributes:
        first_half: The first half of the stage with processed enemies.
        second_half: The second half of the stage with processed enemies.
    """

    first_half: FullEndgameHalf = Field(alias="event_id_list1")
    second_half: FullEndgameHalf | None = Field(alias="event_id_list2")


class EndgameBaseModel(APIModel):
    """Abstract base class for all HSR endgame modes.

    Attributes:
        id: Unique ID of the endgame event.
        name: Display name of the event.
        begin_time: Event start timestamp.
        end_time: Event end timestamp.
        stages: List of stages in this endgame mode.
    """

    id: int
    name: str = Field(default="")
    begin_time: str = Field(alias="begin_time", default="")
    end_time: str = Field(alias="end_time", default="")
    stages: list[EndgameStage] = Field(alias="level")

    @field_validator("name", "begin_time", "end_time", mode="before")
    @classmethod
    def __handle_missing_fields(cls, value: Any) -> str:
        return "" if value is None else value

    @field_validator("stages", mode="before")
    @classmethod
    def __handle_invalid_stages(cls, value: list[dict[str, Any]]) -> list[dict[str, Any]]:
        return [stage for stage in value if "name" in stage or "pre_id" in stage]


class FullEndgameBaseModel(EndgameBaseModel):
    """Endgame base model with processed enemies.

    Attributes:
        id: Unique ID of the endgame event.
        name: Display name of the event.
        begin_time: Event start timestamp.
        end_time: Event end timestamp.
        stages: List of stages in this endgame mode with processed enemies.
    """

    stages: list[FullEndgameStage] = Field(alias="level")


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
    names: dict[Literal["en", "zh", "ko", "ja"], str]
    name: str = Field("")  # The value of this field is assigned in post processing.
    begin: str = ""
    end: str = ""

    @model_validator(mode="before")
    @classmethod
    def __transform_names(cls, values: dict[str, Any]) -> dict[str, Any]:
        values["names"] = {
            "en": values.pop("en", "") or "",
            "zh": values.pop("zh", "") or "",
            "ko": values.pop("ko", "") or "",
            "ja": values.pop("ja", "") or "",
        }
        return values


class MOCBase(APIModel):
    memory_turbulence: str = Field(alias="memory_turbulence")

    @model_validator(mode="before")
    @classmethod
    def __transform_data(cls, data: dict[str, Any]) -> dict[str, Any]:
        levels = data.get("level") or data.get("Level")
        if levels and len(levels) > 0:
            first_level = levels[0]
            data["name"] = first_level.get("group_name") or first_level.get("GroupName")
            data["memory_turbulence"] = replace_placeholders(
                cleanup_text(first_level.get("desc") or first_level.get("Desc") or ""),
                first_level.get("param") or [],
            )
            data["begin_time"] = first_level.get("begin_time") or first_level.get("BeginTime")
            data["end_time"] = first_level.get("end_time") or first_level.get("EndTime")
        return data


class MOCDetail(EndgameBaseModel, MOCBase):
    """Memory of Chaos event details.

    Attributes:
        memory_turbulence: Global modifier for the current MoC rotation.
    """


class FullMOCDetail(FullEndgameBaseModel, MOCBase):
    """Memory of Chaos event details with processed enemies.

    Attributes:
        memory_turbulence: Global modifier for the current MoC rotation.
    """


class EndgameBuffOptions(APIModel):
    """Represents a selectable buff modifier in endgame.

    Attributes:
        name: Name of the buff.
        desc: Description of the buff effect.
        params: List of parameters applied by the buff.
    """

    name: str
    desc: str
    params: list[float] = Field(alias="param")


class ApocBuff(APIModel):
    """Represents the fixed global buff in Apocalyptic Shadow.

    Attributes:
        name: Name of the buff.
        desc: Description of the effect.
    """

    name: str = Field(default="")
    desc: str = Field(default="")

    @field_validator("name", "desc", mode="before")
    @classmethod
    def __handle_missing_fields(cls, value: Any) -> str:
        return "" if value is None else value


class ApocBase(APIModel):
    buff: ApocBuff

    buff_list_1: list[EndgameBuffOptions] = Field(alias="buff_list1")
    buff_list_2: list[EndgameBuffOptions] = Field(alias="buff_list2")


class ApocDetail(EndgameBaseModel, ApocBase):
    """Apocalyptic Shadow event details.

    Attributes:
        buff: The static global buff applied in all stages.
        buff_list_1: Selectable buffs for first half.
        buff_list_2: Selectable buffs for second half.
    """


class FullApocDetail(FullEndgameBaseModel, ApocBase):
    """Apocalyptic Shadow event details with processed enemies.

    Attributes:
        buff: The static global buff applied in all stages.
        buff_list_1: Selectable buffs for first half.
        buff_list_2: Selectable buffs for second half.
    """


class PFBase(APIModel):
    buff_options: list[EndgameBuffOptions] = Field(alias="option")
    buff_suboptions: list[EndgameBuffOptions] = Field(alias="sub_option")


class PFDetail(EndgameBaseModel, PFBase):
    """Pure Fiction event details.

    Attributes:
        buff_options: First tier of optional buffs.
        buff_suboptions: Second tier of optional buffs.
    """


class FullPFDetail(FullEndgameBaseModel, PFBase):
    """Pure Fiction event details with processed enemies.

    Attributes:
        buff_options: First tier of optional buffs.
        buff_suboptions: Second tier of optional buffs.
    """

    @model_validator(mode="before")
    @classmethod
    def __transform_level_data(cls, data: dict[str, Any]) -> dict[str, Any]:
        levels = data.get("level") or data.get("Level", [])
        transformed_stages = []

        for raw_stage in levels:
            # Suffix "" is the single half of an extra node
            for suffix in ("1", "2", ""):
                infinite_list = raw_stage.get(f"infinite_list{suffix}") or raw_stage.get(
                    f"InfiniteList{suffix}"
                )
                event_id_list = raw_stage.get(f"event_id_list{suffix}") or raw_stage.get(
                    f"EventIDList{suffix}"
                )
                if not (infinite_list and event_id_list):
                    continue

                infinite_list_stage = list(infinite_list.values())
                event_id_list[0]["elite_group"] = infinite_list_stage[0].get(
                    "elite_group"
                ) or infinite_list_stage[0].get("EliteGroup")
                event_id_list[0]["monster_list"] = []

                for wave in infinite_list_stage:
                    monster_group_id_list = wave.get("monster_group_id_list") or wave.get(
                        "MonsterGroupIDList"
                    )
                    unique_wave_enemies = list(set(monster_group_id_list))
                    enemies_dict = {
                        f"monster{i}": enemy for i, enemy in enumerate(unique_wave_enemies)
                    }
                    param_list = wave.get("param_list") or wave.get("ParamList", [])
                    enemies_dict["hp_multiplier"] = param_list[1] if len(param_list) > 1 else 0.0
                    event_id_list[0]["monster_list"].append(enemies_dict)

            transformed_stages.append(raw_stage)

        data["level"] = transformed_stages
        return data
