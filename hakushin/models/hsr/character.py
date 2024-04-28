from typing import Any

from pydantic import Field, field_validator, model_validator

from ...constants import HSR_CHARA_RARITY_MAP
from ..base import APIModel

__all__ = ("Eidolon", "HSRCharacter", "Skill", "SkillLevelInfo")


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


class Eidolon(APIModel):
    """Character's eidolon."""

    id: int = Field(alias="Id")
    name: str = Field(alias="Name")
    description: str = Field(alias="Desc")
    parameters: list[float] = Field(alias="ParamList")


class HSRCharacter(APIModel):
    """HSR character."""

    id: int = Field(alias="Id")
    name: str = Field(alias="Name")
    description: str = Field(alias="Desc")
    rarity: int = Field(alias="Rarity")
    eidolons: dict[str, Eidolon] = Field(alias="Ranks")
    skills: dict[str, Skill] = Field(alias="Skills")

    @field_validator("rarity", mode="before")
    def _convert_rarity(cls, value: str) -> int:
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
