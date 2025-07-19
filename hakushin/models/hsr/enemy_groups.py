from __future__ import annotations

from typing import Any

from pydantic import Field, field_validator

from ..base import APIModel

__all__ = ("EliteGroup", "HardLevelGroup")


class EliteGroup(APIModel):
    """Represent an EliteGroup in HSR.

    All enemies in HSR follow the following formula for ATK, DEF, HP, and SPD:
    Base x BaseModifyRatio x EliteGroup Ratio x HardLevelGroup(Level) Ratio x (1 + HPMultiplier)

    Attributes:
        id: The ID of the group.
        attack_ratio: The ratio to multiply to get final attack.
        defence_ratio: The ratio to multiply to get final defence.
        hp_ratio: The ratio to multiply to get final HP.
        spd_ratio: The ratio to multiply to get final speed.
    """

    id: int = Field(alias="EliteGroup")
    attack_ratio: float = Field(alias="AttackRatio", default=0)
    defence_ratio: float = Field(alias="DefenceRatio", default=0)
    hp_ratio: float = Field(alias="HPRatio", default=0)
    spd_ratio: float = Field(alias="SpeedRatio", default=0)
    stance_ratio: float = Field(alias="StanceRatio", default=0)

    @field_validator(
        "attack_ratio", "defence_ratio", "hp_ratio", "spd_ratio", "stance_ratio", mode="before"
    )
    @classmethod
    def handle_missing_fields(cls, value: Any) -> float:
        return 0 if value is None else value


class HardLevelGroup(APIModel):
    """Represent a HardLevelGroup in HSR.

    All enemies in HSR follow the following formula for ATK, DEF, HP, and SPD:
    Base x BaseModifyRatio x EliteGroup Ratio x HardLevelGroup(Level) Ratio x (1 + HPMultiplier)

    Attributes:
        id: The ID of the group.
        level: The level of the enemy.
        attack_ratio: The ratio to multiply to get final attack.
        defence_ratio: The ratio to multiply to get final defence.
        hp_ratio: The ratio to multiply to get final HP.
        spd_ratio: The ratio to multiply to get final speed.
    """

    id: int = Field(alias="HardLevelGroup")
    level: int = Field(alias="Level")
    attack_ratio: float = Field(alias="AttackRatio", default=0)
    defence_ratio: float = Field(alias="DefenceRatio", default=0)
    hp_ratio: float = Field(alias="HPRatio", default=0)
    spd_ratio: float = Field(alias="SpeedRatio", default=0)
    stance_ratio: float = Field(alias="StanceRatio", default=0)
    status_resistance: float = Field(alias="StatusResistance", default=0)

    @field_validator(
        "attack_ratio",
        "defence_ratio",
        "hp_ratio",
        "spd_ratio",
        "stance_ratio",
        "status_resistance",
        mode="before",
    )
    @classmethod
    def handle_missing_fields(cls, value: Any) -> float:
        return 0 if value is None else value
