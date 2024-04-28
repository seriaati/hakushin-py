from pydantic import Field

from ..base import APIModel

__all__ = ("Weapon", "WeaponProperty", "WeaponRefinement", "WeaponStatModifier")


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


class Weapon(APIModel):
    """Genshin Impact weapon."""

    name: str = Field(alias="Name")
    description: str = Field(alias="Desc")
    rarity: int = Field(alias="Rarity")
    icon: str = Field(alias="Icon")

    stat_modifiers: dict[str, WeaponStatModifier] = Field(alias="StatsModifier")
    xp_requirements: dict[str, float] = Field(alias="XPRequirements")
    ascension: dict[str, dict[str, float]] = Field(alias="Ascension")
    refinments: dict[str, WeaponRefinement] = Field(alias="Refinement")
