from __future__ import annotations

from pydantic import Field, field_validator

from ..base import APIModel

__all__ = ("EliteGroup", "HardLevelGroup")


class EliteGroup(APIModel):
    """Represent an EliteGroup in HSR.

    All enemies in HSR follow the following formula for ATK, DEF, HP, and SPD:
    Base x BaseModifyRatio x EliteGroup Ratio x HardLevelGroup(Level) Ratio

    Attributes:
        id: The ID of the group.
        attack_ratio: The ratio to multiply to get final attack.
        defence_ratio: The ratio to multiply to get final defence.
        hp_ratio: The ratio to multiply to get final HP.
        spd_ratio: The ratio to multiply to get final speed.
    """

    id: int = Field(alias="EliteGroup")
    attack_ratio: float = Field(alias="AttackRatio", default=1)
    defence_ratio: float = Field(alias="DefenceRatio", default=1)
    hp_ratio: float = Field(alias="HPRatio", default=1)
    spd_ratio: float = Field(alias="SpeedRatio", default=1)
    stance_ratio: float = Field(alias="StanceRatio", default=1)

    @field_validator(
        "attack_ratio",
        "defence_ratio",
        "hp_ratio",
        "spd_ratio",
        "stance_ratio",
        mode="before",
        check_fields=False,
    )
    @classmethod
    def extract_value(cls, v: dict[str, float]) -> float:
        # Expecting something like {"Value": 2.32}
        if isinstance(v, dict) and "Value" in v:
            return v["Value"]
        msg = "Expected a dict with 'Value' key."
        raise ValueError(msg)


class HardLevelGroup(APIModel):
    """Represent a HardLevelGroup in HSR.

    All enemies in HSR follow the following formula for ATK, DEF, HP, and SPD:
    Base x BaseModifyRatio x EliteGroup Ratio x HardLevelGroup(Level) Ratio

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
    attack_ratio: float = Field(alias="AttackRatio", default=1)
    defence_ratio: float = Field(alias="DefenceRatio", default=1)
    hp_ratio: float = Field(alias="HPRatio", default=1)
    spd_ratio: float = Field(alias="SpeedRatio", default=1)
    stance_ratio: float = Field(alias="StanceRatio", default=1)
    status_resistance: float = Field(alias="StatusResistance", default=0)

    @field_validator(
        "attack_ratio",
        "defence_ratio",
        "hp_ratio",
        "spd_ratio",
        "stance_ratio",
        "status_resistance",
        mode="before",
        check_fields=False,
    )
    @classmethod
    def extract_value(cls, v: dict[str, float]) -> float:
        # Expecting something like {"Value": 2.32}
        if isinstance(v, dict) and "Value" in v:
            return v["Value"]
        msg = "Expected a dict with 'Value' key."
        raise ValueError(msg)
