"""Genshin Impact weapon models."""

from __future__ import annotations

from typing import Any, Literal

from pydantic import Field, field_validator, model_validator

from ..base import APIModel

__all__ = ("Weapon", "WeaponDetail", "WeaponProperty", "WeaponRefinement", "WeaponStatModifier")


class WeaponProperty(APIModel):
    """Represent a weapon's property.

    Attributes:
        type: Type of the property.
        init_value: Initial value of the property.
        growth_type: Growth type of the property.
    """

    type: str = Field(alias="propType")
    init_value: float = Field(alias="initValue")
    growth_type: str = Field(alias="type")


class WeaponStatModifier(APIModel):
    """Represent a weapon's stat modifier.

    Attributes:
        base: Base value of the stat modifier.
        levels: Dictionary of level-based stat modifiers.
    """

    base: float = Field(alias="Base")
    levels: dict[str, float] = Field(alias="Levels")


class WeaponRefinement(APIModel):
    """Represent a weapon's refinement.

    Attributes:
        name: Name of the refinement.
        description: Description of the refinement.
        parameters: List of parameters for the refinement.
    """

    name: str = Field(alias="Name")
    description: str = Field(alias="Desc")
    parameters: list[float] = Field(alias="ParamList")


class WeaponDetail(APIModel):
    """Represent a Genshin Impact weapon detail.

    Attributes:
        name: Name of the weapon.
        description: Description of the weapon.
        rarity: Rarity of the weapon.
        icon: Icon URL of the weapon.
        stat_modifiers: Dictionary of stat modifiers for the weapon.
        xp_requirements: Dictionary of XP requirements for the weapon.
        ascension: Dictionary of ascension data for the weapon.
        refinments: Dictionary of refinements for the weapon.
    """

    name: str = Field(alias="Name")
    description: str = Field(alias="Desc")
    rarity: Literal[1, 2, 3, 4, 5] = Field(alias="Rarity")
    icon: str = Field(alias="Icon")

    stat_modifiers: dict[str, WeaponStatModifier] = Field(alias="StatsModifier")
    xp_requirements: dict[str, float] = Field(alias="XPRequirements")
    ascension: dict[str, dict[str, float]] = Field(alias="Ascension")
    refinments: dict[str, WeaponRefinement] = Field(alias="Refinement")

    @field_validator("icon", mode="before")
    @classmethod
    def __convert_icon(cls, value: str) -> str:
        return f"https://api.hakush.in/gi/UI/{value}.webp"


class Weapon(APIModel):
    """Represent a Genshin Impact weapon.

    Attributes:
        id: ID of the weapon.
        icon: Icon URL of the weapon.
        rarity: Rarity of the weapon.
        description: Description of the weapon.
        names: Dictionary of names in different languages.
        name: Name of the weapon.
    """

    id: int
    icon: str
    rarity: Literal[1, 2, 3, 4, 5] = Field(alias="rank")
    description: str = Field(alias="desc")
    names: dict[Literal["EN", "CHS", "KR", "JP"], str]
    name: str = Field("")

    @field_validator("icon", mode="before")
    @classmethod
    def __convert_icon(cls, value: str) -> str:
        return f"https://api.hakush.in/gi/UI/{value}.webp"

    @model_validator(mode="before")
    @classmethod
    def __transform_names(cls, values: dict[str, Any]) -> dict[str, Any]:
        values["names"] = {
            "EN": values.pop("EN"),
            "CHS": values.pop("CHS"),
            "KR": values.pop("KR"),
            "JP": values.pop("JP"),
        }
        return values
