from __future__ import annotations

from typing import Any, Literal

from pydantic import Field, field_validator, model_validator

from ...constants import ZZZ_SA_RARITY_CONVERTER
from ...utils import cleanup_text
from ..base import APIModel
from .common import ZZZExtraProp, ZZZMaterial

__all__ = ("Bangboo", "BangbooAscension", "BangbooDetail", "BangbooSkill")


class Bangboo(APIModel):
    """Represent a Zenless Zone Zero bangboo companion.

    Bangboos are AI companions that assist agents in combat and exploration.
    They have different rarities, skills, and can be leveled up.

    Attributes:
        id: Unique bangboo identifier.
        icon: Bangboo icon image URL.
        rarity: Bangboo rarity rank (S or A).
        code_name: Bangboo code designation.
        description: Bangboo description text.
        name: Bangboo display name (may be empty).
        names: Bangboo names in different languages.
    """

    id: int
    icon: str
    rarity: Literal["S", "A"] | None = Field(alias="rank")
    code_name: str = Field(alias="codename")
    description: str = Field(alias="desc")
    name: str = Field("")  # This field doesn't exist in the API response
    names: dict[Literal["en", "ja", "zh", "ko"], str]

    @field_validator("icon")
    @classmethod
    def __convert_icon(cls, value: str) -> str:
        value = value.rsplit("/", maxsplit=1)[-1].split(".", maxsplit=1)[0]
        return f"https://static.nanoka.cc/zzz/UI/{value}.webp"

    @field_validator("rarity", mode="before")
    @classmethod
    def __convert_rarity(cls, value: int | None) -> Literal["S", "A"] | None:
        return ZZZ_SA_RARITY_CONVERTER[value] if value is not None else None

    @model_validator(mode="before")
    @classmethod
    def __pop_names(cls, values: dict[str, Any]) -> dict[str, Any]:
        values["names"] = {
            "en": values.pop("en"),
            "ko": values.pop("ko"),
            "zh": values.pop("zh"),
            "ja": values.pop("ja"),
        }
        return values


class BangbooAscension(APIModel):
    """Represent bangboo ascension phase data.

    Contains stat bonuses, level requirements, and materials needed
    for each bangboo ascension phase.

    Attributes:
        max_hp: Maximum HP bonus at this phase.
        attack: Attack stat bonus.
        defense: Defense stat bonus.
        max_level: Maximum level achievable in this phase.
        min_level: Minimum level for this phase.
        materials: Required materials for ascension.
        extra_props: Additional properties gained.
    """

    max_hp: int = Field(alias="hp_max")
    attack: int
    defense: int = Field(alias="defence")
    max_level: int = Field(alias="level_max")
    min_level: int = Field(alias="level_min")
    materials: list[ZZZMaterial]
    extra_props: list[ZZZExtraProp] = Field(alias="extra")

    @field_validator("extra_props", mode="before")
    @classmethod
    def __convert_extra_props(cls, value: dict[str, dict[str, Any]]) -> list[ZZZExtraProp]:
        return [ZZZExtraProp(**prop) for prop in value.values()]

    @field_validator("materials", mode="before")
    @classmethod
    def __convert_materials(cls, value: dict[str, int]) -> list[ZZZMaterial]:
        return [ZZZMaterial(id=int(id_), amount=amount) for id_, amount in value.items()]


class BangbooSkill(APIModel):
    """Represent a bangboo skill or ability.

    Each bangboo has multiple skills that provide different effects
    and bonuses during gameplay.

    Attributes:
        name: Skill name.
        description: Skill effect description.
        properties: List of skill properties.
        parameter: Skill parameter values.
    """

    name: str
    description: str = Field(alias="desc")
    properties: list[str] = Field(alias="property")
    parameter: str = Field(alias="param")

    @field_validator("description")
    @classmethod
    def __cleanup_text(cls, value: str) -> str:
        return cleanup_text(value)


class BangbooDetail(APIModel):
    """Provide comprehensive bangboo information and progression data.

    Contains complete bangboo details including stats, ascension data,
    skills, and all progression information.

    Attributes:
        id: Unique bangboo identifier.
        code_name: Bangboo code designation.
        name: Bangboo display name.
        description: Bangboo description text.
        rarity: Bangboo rarity rank (S or A).
        icon: Bangboo icon image URL.
        stats: Base stats dictionary.
        ascensions: Ascension data by level (key starts from 1).
        skills: Skills organized by type (A, B, C).
    """

    id: int
    code_name: str = Field(alias="code_name")
    name: str
    description: str = Field(alias="desc")
    rarity: Literal["S", "A"]
    icon: str
    stats: dict[str, float]
    ascensions: dict[str, BangbooAscension] = Field(alias="level")
    skills: dict[Literal["a", "b", "c"], dict[str, BangbooSkill] | None] = Field(alias="skill")

    @field_validator("skills", mode="before")
    @classmethod
    def __unnest_level(
        cls, value: dict[Literal["a", "b", "c"], dict[str, Any] | None]
    ) -> dict[Literal["a", "b", "c"], dict[str, BangbooSkill] | None]:
        return {
            key: (value[key].get("level") or value[key].get("Level")) if value.get(key) else None
            for key in value
        }

    @field_validator("icon")
    @classmethod
    def __convert_icon(cls, value: str) -> str:
        value = value.rsplit("/", maxsplit=1)[-1].split(".", maxsplit=1)[0]
        return f"https://static.nanoka.cc/zzz/UI/{value}.webp"

    @field_validator("rarity", mode="before")
    @classmethod
    def __convert_rarity(cls, value: int) -> Literal["S", "A"]:
        return ZZZ_SA_RARITY_CONVERTER[value]
