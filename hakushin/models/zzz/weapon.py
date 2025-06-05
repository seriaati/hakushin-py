from __future__ import annotations

from typing import Any, Literal

from pydantic import Field, computed_field, field_validator, model_validator

from ...constants import ZZZ_SAB_RARITY_CONVERTER
from ...enums import ZZZSpecialty
from ...utils import cleanup_text
from ..base import APIModel

__all__ = (
    "Weapon",
    "WeaponDetail",
    "WeaponLevel",
    "WeaponProp",
    "WeaponRefinement",
    "WeaponStar",
    "WeaponType",
)


class Weapon(APIModel):
    """Represent a ZZZ weapon (w-engine).

    Attributes:
        id: ID of the weapon.
        icon: Icon URL of the weapon.
        name: Name of the weapon.
        names: Dictionary of names in different languages.
        specialty: Specialty of the weapon.
        rarity: Rarity of the weapon.
    """

    id: int
    icon: str
    name: str = Field("")  # This field doesn't exist in the API response
    names: dict[Literal["EN", "JA", "CHS", "KO"], str]
    specialty: ZZZSpecialty = Field(alias="type")
    rarity: Literal["S", "A", "B"] = Field(alias="rank")

    @field_validator("rarity", mode="before")
    @classmethod
    def __convert_rarity(cls, value: int | None) -> Literal["S", "A", "B"] | None:
        """Convert the rarity value to a string literal."""
        return ZZZ_SAB_RARITY_CONVERTER[value] if value is not None else None

    @field_validator("icon")
    @classmethod
    def __convert_icon(cls, value: str) -> str:
        """Convert the icon path to a full URL."""
        return f"https://api.hakush.in/zzz/UI/{value}.webp"

    @model_validator(mode="before")
    @classmethod
    def __pop_names(cls, values: dict[str, Any]) -> dict[str, Any]:
        """Pop names from the values and assign them to the 'names' field."""
        values["names"] = {
            "EN": values.pop("EN"),
            "KO": values.pop("KO"),
            "CHS": values.pop("CHS"),
            "JA": values.pop("JA"),
        }
        return values


class WeaponType(APIModel):
    """Represent a weapon type classification.

    Defines the specialty and name of weapon types that characters
    can use in Zenless Zone Zero.

    Attributes:
        type: Weapon specialty classification.
        name: Human-readable weapon type name.
    """

    type: ZZZSpecialty
    name: str


class WeaponProp(APIModel):
    """Represent a weapon stat property.

    Contains stat information including names, formatting, and values
    for weapon statistics like attack, crit rate, etc.

    Attributes:
        name: Primary property name.
        name2: Secondary property name.
        format: Value formatting specification.
        value: Numerical property value.
    """

    name: str = Field(alias="Name")
    name2: str = Field(alias="Name2")
    format: str = Field(alias="Format")
    value: float = Field(alias="Value")

    @computed_field
    @property
    def formatted_value(self) -> str:
        """Get the formatted value of this property."""
        if "%" in self.format:
            return f"{self.value / 100:.0%}%"
        return str(round(self.value))


class WeaponLevel(APIModel):
    """Represent weapon leveling information.

    Contains experience requirements and stat scaling rates
    for weapon level progression.

    Attributes:
        exp: Experience points required.
        rate: Primary stat scaling rate.
        rate2: Secondary stat scaling rate.
    """

    exp: int = Field(alias="Exp")
    rate: int = Field(alias="Rate")
    rate2: int = Field(alias="Rate2")


class WeaponStar(APIModel):
    """Represent weapon star ranking information.

    Contains star rating data and randomization rates
    for weapon rarity and quality assessment.

    Attributes:
        star_rate: Star rating value.
        rand_rate: Randomization rate factor.
    """

    star_rate: int = Field(alias="StarRate")
    rand_rate: int = Field(alias="RandRate")


class WeaponRefinement(APIModel):
    """Represent weapon refinement level data.

    Contains information about weapon refinement stages
    and their associated names or effects.

    Attributes:
        name: Refinement level name or description.
    """

    name: str = Field(alias="Name")
    description: str = Field(alias="Desc")

    @field_validator("description")
    @classmethod
    def __cleanup_text(cls, value: str) -> str:
        """Clean up the description text."""
        return cleanup_text(value)


class WeaponDetail(APIModel):
    """Represent detailed information about a ZZZ weapon.

    Attributes:
        id: ID of the weapon.
        code_name: Code name of the weapon.
        name: Name of the weapon.
        description: Description of the weapon.
        description2: Second description of the weapon.
        short_description: Short description of the weapon.
        rarity: Rarity of the weapon.
        icon: Icon URL of the weapon.
        type: Type of the weapon.
        base_property: Base property of the weapon.
        rand_property: Random property of the weapon.
        levels: Dictionary of weapon levels.
        stars: Dictionary of weapon stars.
        materials: Materials required for the weapon.
        refinements: Dictionary of weapon refinements.
    """

    id: int = Field(alias="Id")
    code_name: str = Field(alias="CodeName")
    name: str = Field(alias="Name")
    description: str = Field(alias="Desc")
    description2: str = Field(alias="Desc2")
    short_description: str = Field(alias="Desc3")
    rarity: Literal["S", "A", "B"] | None = Field(alias="Rarity")
    icon: str = Field(alias="Icon")
    type: WeaponType = Field(alias="WeaponType")
    base_property: WeaponProp = Field(alias="BaseProperty")
    rand_property: WeaponProp = Field(alias="RandProperty")
    levels: dict[str, WeaponLevel] = Field(alias="Level")
    stars: dict[str, WeaponStar] = Field(alias="Stars")
    materials: str = Field(alias="Materials")
    refinements: dict[str, WeaponRefinement] = Field(alias="Talents")  # {'1': ..., '2': ...}
    """Dictionary of refinements, key starts from 1."""

    @field_validator("type", mode="before")
    @classmethod
    def __convert_type(cls, value: dict[str, str]) -> WeaponType:
        """Convert the weapon type data to a WeaponType object."""
        first_item = next(iter(value.items()))
        return WeaponType(type=ZZZSpecialty(int(first_item[0])), name=first_item[1])

    @field_validator("icon")
    @classmethod
    def __convert_icon(cls, value: str) -> str:
        """Convert the icon path to a full URL."""
        value = value.rsplit("/", maxsplit=1)[-1].split(".", maxsplit=1)[0]
        return f"https://api.hakush.in/zzz/UI/{value}.webp"

    @field_validator("rarity", mode="before")
    @classmethod
    def __convert_rarity(cls, value: int | None) -> Literal["S", "A", "B"] | None:
        """Convert the rarity value to a string literal."""
        return ZZZ_SAB_RARITY_CONVERTER[value] if value is not None else None
