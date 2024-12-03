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
    """ZZZ weapon (w-engine) model."""

    id: int
    icon: str
    name: str = Field("")  # This field doesn't exist in the API response
    names: dict[Literal["EN", "JA", "CHS", "KO"], str]
    specialty: ZZZSpecialty = Field(alias="type")
    rarity: Literal["S", "A", "B"] = Field(alias="rank")

    @field_validator("rarity", mode="before")
    @classmethod
    def __convert_rarity(cls, value: int | None) -> Literal["S", "A", "B"] | None:
        return ZZZ_SAB_RARITY_CONVERTER[value] if value is not None else None

    @field_validator("icon")
    @classmethod
    def __convert_icon(cls, value: str) -> str:
        return f"https://api.hakush.in/zzz/UI/{value}.webp"

    @model_validator(mode="before")
    @classmethod
    def __pop_names(cls, values: dict[str, Any]) -> dict[str, Any]:
        values["names"] = {
            "EN": values.pop("EN"),
            "KO": values.pop("KO"),
            "CHS": values.pop("CHS"),
            "JA": values.pop("JA"),
        }
        return values


class WeaponType(APIModel):
    """ZZZ weapon type model."""

    type: ZZZSpecialty
    name: str


class WeaponProp(APIModel):
    """ZZZ weapon property model."""

    name: str = Field(alias="Name")
    name2: str = Field(alias="Name2")
    format: str = Field(alias="Format")
    value: float = Field(alias="Value")

    @computed_field
    @property
    def formatted_value(self) -> str:
        """Formatted value of this prop."""
        if "%" in self.format:
            return f"{self.value / 100:.0%}%"
        return str(round(self.value))


class WeaponLevel(APIModel):
    """ZZZ weapon level model."""

    exp: int = Field(alias="Exp")
    rate: int = Field(alias="Rate")
    rate2: int = Field(alias="Rate2")


class WeaponStar(APIModel):
    """ZZZ weapon star model."""

    star_rate: int = Field(alias="StarRate")
    rand_rate: int = Field(alias="RandRate")


class WeaponRefinement(APIModel):
    """ZZZ weapon refinement model."""

    name: str = Field(alias="Name")
    description: str = Field(alias="Desc")

    @field_validator("description")
    @classmethod
    def __cleanup_text(cls, value: str) -> str:
        return cleanup_text(value)


class WeaponDetail(APIModel):
    """ZZZ weapon (w-engine) detail model."""

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
        first_item = next(iter(value.items()))
        return WeaponType(type=ZZZSpecialty(int(first_item[0])), name=first_item[1])

    @field_validator("icon")
    @classmethod
    def __convert_icon(cls, value: str) -> str:
        value = value.split("/")[-1].split(".")[0]
        return f"https://api.hakush.in/zzz/UI/{value}.webp"

    @field_validator("rarity", mode="before")
    @classmethod
    def __convert_rarity(cls, value: int | None) -> Literal["S", "A", "B"] | None:
        return ZZZ_SAB_RARITY_CONVERTER[value] if value is not None else None
