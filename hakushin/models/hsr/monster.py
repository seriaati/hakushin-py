from __future__ import annotations

from typing import Any, Literal

from pydantic import Field, field_validator, model_validator

from ...enums import HSRElement
from ..base import APIModel

__all__ = ("ChildMonster", "DamageTypeResistance", "HSREnemySkill", "Monster", "MonsterDetail")


class HSREnemySkill(APIModel):
    """Represents an enemy skill's information.

    Attributes:
        id: The id of the skill.
        name: The name of the skill
        desc: The description of what the skill does
        damage_type: The type of damage the skill does (out of the HSRElements or None)
    """

    id: int = Field(alias="Id")
    name: str = Field(alias="SkillName", default="")
    desc: str = Field(alias="SkillDesc", default="")
    damage_type: HSRElement | None = Field(alias="DamageType", default=None)

    @field_validator("name", "desc", mode="before")
    @classmethod
    def default_empty_string(cls, value: str | None) -> str:
        return value if isinstance(value, str) else ""

    @field_validator("damage_type", mode="before")
    @classmethod
    def empty_string_to_none(cls: type[HSREnemySkill], v: str | None) -> str | None:
        if not v:
            return None
        return v


class DamageTypeResistance(APIModel):
    """Represent the damage resistance of an enemy in HSR.

    Attributes:
        element: The element of the resistance.
        value: The value of the resistance.
    """

    element: HSRElement = Field(alias="DamageType")
    value: float = Field(alias="Value")


class ChildMonster(APIModel):
    """Represent the specific details of a monster type.

    Attributes:
        id: The ID of this instance of the monster.
        attack_modify_ratio: Multiplier applied to the monster's base attack.
        defence_modify_ratio: Multiplier applied to the monster's base defense.
        hp_modify_ratio: Multiplier applied to the monster's base HP.
        spd_modify_ratio: Multiplier applied to the monster's base speed.
        spd_modify_value: An optional fixed value added to the monster's speed (can override base speed).
        stance_modify_value: Multiplier applied to the monster's base toughness.
        stance_weak_list: List of elemental types that this monster is weak to (for toughness damage).
        damage_type_resistances: List of resistances the monster has against specific elements.
        skills: List of skills this monster instance can use in combat.
    """

    id: int = Field(alias="Id")
    attack_modify_ratio: float = Field(alias="AttackModifyRatio", default=1)
    defence_modify_ratio: float = Field(alias="DefenceModifyRatio", default=1)
    hp_modify_ratio: float = Field(alias="HPModifyRatio", default=1)
    spd_modify_ratio: float = Field(alias="SpeedModifyRatio", default=1)
    spd_modify_value: float | None = Field(alias="SpeedModifyValue", default=None)
    stance_modify_value: float = Field(alias="StanceModifyRatio", default=1)

    stance_weak_list: list[HSRElement] = Field(alias="StanceWeakList")
    damage_type_resistances: list[DamageTypeResistance] = Field(alias="DamageTypeResistance")
    skills: list[HSREnemySkill] = Field(alias="SkillList")


class MonsterDetail(APIModel):
    """Represent an enemy monster with details in HSR.

    Attributes:
        id: Unique identifier for the monster.
        name: Name of the monster.
        description: The description of the monster.
        attack_base: The base attack stat for this monster.
        defence_base: The base defense stat.
        hp_base: The base HP value.
        spd_base: The base speed stat.
        stance_base: The base toughness value.
        status_resistance_base: The base status resistance (used for debuff resist chance).
        monster_types: A list of `ChildMonster` variants derived from this monster.
    """

    id: int = Field(alias="Id")
    rank: str = Field(alias="Rank")
    name: str = Field(alias="Name", default="")
    description: str = Field(alias="Desc", default="")
    attack_base: float = Field(alias="AttackBase", default=0)
    defence_base: float = Field(alias="DefenceBase", default=1)
    hp_base: float = Field(alias="HPBase", default=0)
    spd_base: float = Field(alias="SpeedBase", default=0)
    stance_base: float = Field(alias="StanceBase", default=0)
    status_resistance_base: float = Field(alias="StatusResistanceBase", default=0)

    monster_types: list[ChildMonster] = Field(alias="Child")

    @field_validator(
        "attack_base",
        "defence_base",
        "hp_base",
        "spd_base",
        "stance_base",
        "status_resistance_base",
        mode="before",
    )
    @classmethod
    def default_zero_if_none(cls, value: int | float | None) -> int | float:
        return value if isinstance(value, (int, float)) else 0

    @property
    def icon(self) -> str:
        """Get the monster's icon URL."""
        return f"https://api.hakush.in/hsr/UI/monsterfigure/Monster_{self.id}.webp"


class Monster(APIModel):
    """
    Represent an enemy monster in HSR.

    Attributes:
        id: The ID of the monster.
        icon: The icon URL of the monster.
        children: A list of child monster IDs associated with this monster.
        weaknesses: List of elements that this monster is weak to (used for breaking toughness).
        names: A dictionary of names in different languages.
        description: The English description of the monster.
        name: The English name of the monster.
    """

    id: int  # This field is not present in the API response.
    icon: str
    children: list[int] = Field(alias="child")
    weaknesses: list[HSRElement] = Field(alias="weak")
    names: dict[Literal["en", "cn", "kr", "jp"], str]
    description: str = Field(alias="desc")
    name: str = Field("")  # The value of this field is assigned in post processing.

    @field_validator("icon", mode="before")
    @classmethod
    def __convert_icon(cls, value: str) -> str:
        filename = value.rsplit("/", 1)[-1]
        filename = filename.replace(".png", ".webp")
        return f"https://api.hakush.in/hsr/UI/monsterfigure/{filename}"

    @model_validator(mode="before")
    @classmethod
    def __transform_names(cls, values: dict[str, Any]) -> dict[str, Any]:
        # This is probably the most questionable API design decision I've ever seen.
        values["names"] = {
            "en": values.pop("en"),
            "cn": values.pop("cn"),
            "kr": values.pop("kr"),
            "jp": values.pop("jp"),
        }
        return values
