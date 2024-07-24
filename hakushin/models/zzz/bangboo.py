from typing import Any, Literal

from pydantic import Field, field_validator, model_validator

from ...constants import ZZZ_SA_RARITY_CONVERTER
from ...utils import cleanup_text
from ..base import APIModel
from .common import ZZZExtraProp, ZZZMaterial

__all__ = ("Bangboo", "BangbooAscension", "BangbooDetail", "BangbooSkill")


class Bangboo(APIModel):
    """ZZZ bangboo model."""

    id: int
    icon: str
    rarity: Literal["S", "A"] | None = Field(alias="rank")
    code_name: str = Field(alias="codename")
    description: str = Field(alias="desc")
    name: str = Field(None)  # This field doesn't exist in the API response
    names: dict[Literal["EN", "JA", "CHS", "KO"], str]

    @field_validator("icon")
    @classmethod
    def __convert_icon(cls, value: str) -> str:
        value = value.split("/")[-1].split(".")[0]
        return f"https://api.hakush.in/zzz/UI/{value}.webp"

    @field_validator("rarity", mode="before")
    @classmethod
    def __convert_rarity(cls, value: int | None) -> Literal["S", "A"] | None:
        return ZZZ_SA_RARITY_CONVERTER[value] if value is not None else None

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


class BangbooAscension(APIModel):
    """ZZZ bangboo ascension model."""

    max_hp: int = Field(alias="HpMax")
    attack: int = Field(alias="Attack")
    defense: int = Field(alias="Defence")
    max_level: int = Field(alias="LevelMax")
    min_level: int = Field(alias="LevelMin")
    materials: list[ZZZMaterial] = Field(alias="Materials")
    extra_props: list[ZZZExtraProp] = Field(alias="Extra")

    @field_validator("extra_props", mode="before")
    @classmethod
    def __convert_extra_props(cls, value: dict[str, dict[str, Any]]) -> list[ZZZExtraProp]:
        return [ZZZExtraProp(**prop) for prop in value.values()]

    @field_validator("materials", mode="before")
    @classmethod
    def __convert_materials(cls, value: dict[str, int]) -> list[ZZZMaterial]:
        return [ZZZMaterial(id=int(id_), amount=amount) for id_, amount in value.items()]


class BangbooSkill(APIModel):
    """ZZZ bangboo skill model."""

    name: str = Field(alias="Name")
    description: str = Field(alias="Desc")
    properties: list[str] = Field(alias="Property")
    parameter: str = Field(alias="Param")

    @field_validator("description")
    @classmethod
    def __cleanup_text(cls, value: str) -> str:
        return cleanup_text(value)


class BangbooDetail(APIModel):
    """ZZZ bangboo detail model."""

    id: int = Field(alias="Id")
    code_name: str = Field(alias="CodeName")
    name: str = Field(alias="Name")
    description: str = Field(alias="Desc")
    rarity: Literal["S", "A"] = Field(alias="Rarity")
    icon: str = Field(alias="Icon")
    stats: dict[str, float] = Field(alias="Stats")
    ascensions: dict[str, BangbooAscension] = Field(alias="Level")
    """Dictionary of ascension objects, key starts from 1."""
    skills: dict[Literal["A", "B", "C"], dict[str, BangbooSkill]] = Field(alias="Skill")

    @field_validator("skills", mode="before")
    @classmethod
    def __unnest_level(
        cls, value: dict[Literal["A", "B", "C"], dict[Literal["Level"], dict[str, Any]]]
    ) -> dict[Literal["A", "B", "C"], dict[str, BangbooSkill]]:
        return {key: value[key]["Level"] for key in value}

    @field_validator("icon")
    @classmethod
    def __convert_icon(cls, value: str) -> str:
        value = value.split("/")[-1].split(".")[0]
        return f"https://api.hakush.in/zzz/UI/{value}.webp"

    @field_validator("rarity", mode="before")
    @classmethod
    def __convert_rarity(cls, value: int) -> Literal["S", "A"]:
        return ZZZ_SA_RARITY_CONVERTER[value]
