from typing import Any, Literal

from pydantic import Field, model_validator

from ..base import APIModel

__all__ = ("Weapon", "WeaponDetail", "WeaponProperty", "WeaponRefinement", "WeaponStatModifier")


class WeaponProperty(APIModel):
    """Weapon's property."""

    type: str = Field(alias="propType")
    init_value: float = Field(alias="initValue")
    growth_type: str = Field(alias="type")


class WeaponStatModifier(APIModel):
    """Weapon's stat modifier."""

    base: float = Field(alias="Base")
    levels: dict[str, float] = Field(alias="Levels")


class WeaponRefinement(APIModel):
    """Weapon's refinement."""

    name: str = Field(alias="Name")
    description: str = Field(alias="Desc")
    parameters: list[float] = Field(alias="ParamList")


class WeaponDetail(APIModel):
    """Genshin Impact weapon detail."""

    name: str = Field(alias="Name")
    description: str = Field(alias="Desc")
    rarity: Literal[4, 5] = Field(alias="Rarity")
    icon: str = Field(alias="Icon")

    stat_modifiers: dict[str, WeaponStatModifier] = Field(alias="StatsModifier")
    xp_requirements: dict[str, float] = Field(alias="XPRequirements")
    ascension: dict[str, dict[str, float]] = Field(alias="Ascension")
    refinments: dict[str, WeaponRefinement] = Field(alias="Refinement")


class Weapon(APIModel):
    """Genshin Impact weapon."""

    id: int  # This field is not present in the API response.
    icon: str
    rarity: Literal[4, 5] = Field(alias="rank")
    description: str = Field(alias="desc")
    names: dict[Literal["EN", "CHS", "KR", "JP"], str]
    name: str = Field(None)  # This value of this field is assigned in post processing.

    @model_validator(mode="before")
    def _transform_names(cls, values: dict[str, Any]) -> dict[str, Any]:
        values["names"] = {
            "EN": values.pop("EN"),
            "CHS": values.pop("CHS"),
            "KR": values.pop("KR"),
            "JP": values.pop("JP"),
        }
        return values
