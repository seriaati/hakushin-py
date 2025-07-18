from __future__ import annotations

from typing import Any

from attr import dataclass
from pydantic import Field, model_validator

from ...enums import HSRElement
from ..base import APIModel

__all__ = (
    "EndgameBuffOptions",
    "EndgameHalf",
    "EndgameStage",
    "EndgameWave",
    "HSREnemy",
    "MemoryOfChaosDetail",
    "PureFictionDetail",
)


@dataclass(kw_only=True)
class HSREnemy:
    id: int
    name: str = ""
    weaknesses: list[HSRElement]
    level: int
    base_hp: int
    speed: int | None
    toughness: int | None
    effect_res: float | None


class EndgameWave(APIModel):
    enemies: list[int] = Field(default_factory=list)

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
    hlg_id: int = Field(alias="HardLevelGroup")
    hlg_level: int = Field(alias="Level")
    eg_id: int = Field(alias="EliteGroup", default=1)
    waves: list[EndgameWave] = Field(alias="MonsterList")


class EndgameStage(APIModel):
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


class MemoryOfChaosDetail(APIModel):
    id: int
    stages: list[EndgameStage]


class EndgameBuffOptions(APIModel):
    name: str = Field(alias="Name")
    desc: str = Field(alias="Desc")
    params: list[float] = Field(alias="Param")


class PureFictionDetail(APIModel):
    id: int = Field(alias="Id")
    name: str = Field(alias="Name")

    buff_options: list[EndgameBuffOptions] = Field(alias="Option")
    buff_suboptions: list[EndgameBuffOptions] = Field(alias="SubOption")

    begin_time: str = Field(alias="BeginTime")
    end_time: str = Field(alias="EndTime")

    stages: list[EndgameStage] = Field(alias="Level")
