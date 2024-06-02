from typing import Any, Literal

from pydantic import Field, computed_field, field_validator, model_validator

from ...constants import HSR_CHARA_RARITY_MAP
from ...enums import HSRElement, HSRPath
from ..base import APIModel

__all__ = ("Character", "CharacterDetail", "Eidolon", "Skill", "SkillLevelInfo")


class SkillLevelInfo(APIModel):
    """Skill's level info."""

    level: int = Field(alias="Level")
    parameters: list[float] = Field(alias="ParamList")


class Skill(APIModel):
    """Character's skill."""

    name: str = Field(alias="Name")
    description: str = Field(alias="Desc")
    type: str | None = Field(None, alias="Type")
    tag: str = Field(alias="Tag")
    energy_generation: int | None = Field(None, alias="SPBase")
    level_info: dict[str, SkillLevelInfo] = Field(alias="Level")

    @computed_field
    @property
    def max_level(self) -> int:
        """Skill's max level."""
        return max(int(level) for level in self.level_info)


class Eidolon(APIModel):
    """Character's eidolon."""

    id: int = Field(alias="Id")
    name: str = Field(alias="Name")
    description: str = Field(alias="Desc")
    parameters: list[float] = Field(alias="ParamList")


class CharacterDetail(APIModel):
    """HSR character detail."""

    id: int = Field(alias="Id")
    name: str = Field(alias="Name")
    description: str = Field(alias="Desc")
    rarity: Literal[4, 5] = Field(alias="Rarity")
    eidolons: dict[str, Eidolon] = Field(alias="Ranks")
    skills: dict[str, Skill] = Field(alias="Skills")
    ascension_stats: dict[str, dict[str, Any]] = Field(alias="Stats")

    @field_validator("rarity", mode="before")
    def _convert_rarity(cls, value: str) -> Literal[4, 5]:
        return HSR_CHARA_RARITY_MAP[value]

    @model_validator(mode="before")
    def _extract_id(cls, values: dict[str, Any]) -> dict[str, Any]:
        """Use a hacky way to extract character ID from relic recommendation.

        I don't understand why the API doesn't have the character ID in the response.
        """
        values["Id"] = values["Relics"]["AvatarID"]
        return values

    @property
    def icon(self) -> str:
        """Character's icon URL."""
        return f"https://api.hakush.in/hsr/UI/avatarshopicon/{self.id}.webp"

    @property
    def gacha_art(self) -> str:
        """Character's gacha art URL."""
        return self.icon.replace("avatarshopicon", "avatardrawcard")


class Character(APIModel):
    """HSR character."""

    id: int  # This field is not present in the API response.
    icon: str
    rarity: Literal[4, 5] = Field(alias="rank")
    description: str = Field(alias="desc")
    path: HSRPath = Field(alias="baseType")
    element: HSRElement = Field(alias="damageType")
    names: dict[Literal["en", "cn", "kr", "jp"], str]
    name: str = Field(None)  # The value of this field is assigned in post processing.

    @field_validator("icon", mode="before")
    def _convert_icon(cls, value: str) -> str:
        return f"https://api.hakush.in/hsr/UI/avatarshopicon/{value}.webp"

    @field_validator("rarity", mode="before")
    def _convert_rarity(cls, value: str) -> Literal[4, 5]:
        return HSR_CHARA_RARITY_MAP[value]

    @model_validator(mode="before")
    def _transform_names(cls, values: dict[str, Any]) -> dict[str, Any]:
        # This is probably the most questionable API design decision I've ever seen.
        values["names"] = {
            "en": values.pop("en"),
            "cn": values.pop("cn"),
            "kr": values.pop("kr"),
            "jp": values.pop("jp"),
        }
        return values
