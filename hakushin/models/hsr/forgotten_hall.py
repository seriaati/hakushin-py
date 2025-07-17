from __future__ import annotations

from typing import Any, Literal

from pydantic import Field, computed_field, field_validator, model_validator

from ...constants import HSR_CHARA_RARITY_MAP
from ...enums import HSRElement, HSRPath
from ..base import APIModel

__all__ = ("MemoryOfChaos", "MemoryOfChaosStage", "MemoryOfChaosWave")


class MemoryOfChaosWave(APIModel):
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


class MemoryOfChaosHalf(APIModel):
    hlg_id: int = Field(alias="HardLevelGroup")
    hlg_level: int = Field(alias="Level")
    eg_id: int = Field(alias="EliteGroup")
    waves: list[MemoryOfChaosWave] = Field(alias="MonsterList")


class MemoryOfChaosStage(APIModel):
    id: int = Field(alias="Id")
    name: str = Field(alias="Name")

    first_half_weaknesses: list[HSRElement] = Field(alias="DamageType1")
    second_half_weaknesses: list[HSRElement] = Field(alias="DamageType2")

    first_half: list[MemoryOfChaosHalf] = Field(alias="EventIDList1")
    second_half: list[MemoryOfChaosHalf] = Field(alias="EventIDList2")


class MemoryOfChaos(APIModel):
    id: int
    stages: list[MemoryOfChaosStage]
