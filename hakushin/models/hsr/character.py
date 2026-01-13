from __future__ import annotations

from typing import Any, Literal

from pydantic import Field, computed_field, field_validator, model_validator

from ...constants import HSR_CHARA_RARITY_MAP
from ...enums import HSRElement, HSRPath
from ..base import APIModel

__all__ = ("Character", "CharacterDetail", "Eidolon", "Skill", "SkillLevelInfo")


class SkillLevelInfo(APIModel):
    """Represent a skill's level information.

    Attributes:
        level: The level of the skill.
        parameters: A list of parameters for the skill level.
    """

    level: int = Field(alias="Level")
    parameters: list[float] = Field(alias="ParamList")


class Skill(APIModel):
    """Represent a character's skill.

    Attributes:
        name: The name of the skill.
        description: The description of the skill, if available.
        type: The type of the skill, if available.
        tag: The tag of the skill.
        energy_generation: The energy generation of the skill, if available.
        level_info: A dictionary of skill level information.
    """

    name: str = Field(alias="Name")
    description: str | None = Field(None, alias="Desc")
    type: str | None = Field(None, alias="Type")
    tag: str = Field(alias="Tag")
    energy_generation: int | None = Field(None, alias="SPBase")
    level_info: dict[str, SkillLevelInfo] = Field(alias="Level")

    @computed_field
    @property
    def max_level(self) -> int:
        """Get the skill's maximum level."""
        return max(int(level) for level in self.level_info)


class Eidolon(APIModel):
    """Represent a character's eidolon.

    Attributes:
        id: The ID of the eidolon.
        name: The name of the eidolon.
        description: The description of the eidolon.
        parameters: A list of parameters for the eidolon.
    """

    id: int = Field(alias="Id")
    name: str = Field(alias="Name")
    description: str = Field(alias="Desc")
    parameters: list[float] = Field(alias="ParamList")

    @computed_field
    @property
    def image(self) -> str:
        """Get the eidolon's image URL."""
        character_id = str(self.id)[:4]
        eidolon_index = str(self.id)[-1]
        return f"https://api.hakush.in/hsr/UI/rank/_dependencies/textures/{character_id}/{character_id}_Rank_{eidolon_index}.webp"


class CharacterDetail(APIModel):
    """Represent an HSR character detail.

    Attributes:
        id: The ID of the character.
        name: The name of the character.
        description: The description of the character.
        rarity: The rarity of the character.
        eidolons: A dictionary of eidolons for the character.
        skills: A dictionary of skills for the character.
        ascension_stats: A dictionary of ascension stats for the character.
    """

    id: int = Field(alias="Id")
    name: str = Field(alias="Name")
    description: str = Field(alias="Desc")
    rarity: Literal[4, 5] = Field(alias="Rarity")
    eidolons: dict[str, Eidolon] = Field(alias="Ranks")
    skills: dict[str, Skill] = Field(alias="Skills")
    ascension_stats: dict[str, dict[str, Any]] = Field(alias="Stats")

    @field_validator("rarity", mode="before")
    @classmethod
    def __convert_rarity(cls, value: str) -> Literal[4, 5]:
        return HSR_CHARA_RARITY_MAP[value]

    @field_validator("description", mode="before")
    @classmethod
    def __convert_description(cls, value: str | None) -> str:
        return value or ""

    @field_validator("skills", mode="before")
    @classmethod
    def __remove_invalid_skills(cls, value: dict[str, Any]) -> dict[str, Any]:
        # Remove skills with empty names
        return {k: v for k, v in value.items() if v.get("Name")}

    @model_validator(mode="before")
    @classmethod
    def __extract_id(cls, values: dict[str, Any]) -> dict[str, Any]:
        values["Id"] = values["Relics"]["AvatarID"]
        return values

    @property
    def icon(self) -> str:
        """Get the character's icon URL."""
        return f"https://api.hakush.in/hsr/UI/avatarshopicon/{self.id}.webp"

    @property
    def gacha_art(self) -> str:
        """Get the character's gacha art URL."""
        return self.icon.replace("avatarshopicon", "avatardrawcard")


class Character(APIModel):
    """Represent an HSR character.

    Attributes:
        id: The ID of the character.
        icon: The icon URL of the character.
        rarity: The rarity of the character.
        description: The description of the character.
        path: The path of the character.
        element: The element of the character.
        names: A dictionary of names in different languages.
        name: The name of the character.
    """

    id: int  # This field is not present in the API response.
    icon: str
    rarity: Literal[4, 5] = Field(alias="rank")
    description: str = Field(alias="desc")
    path: HSRPath = Field(alias="baseType")
    element: HSRElement = Field(alias="damageType")
    names: dict[Literal["en", "cn", "kr", "jp"], str]
    name: str = Field("")  # The value of this field is assigned in post processing.

    @field_validator("icon", mode="before")
    @classmethod
    def __convert_icon(cls, value: str) -> str:
        return f"https://api.hakush.in/hsr/UI/avatarshopicon/{value}.webp"

    @field_validator("rarity", mode="before")
    @classmethod
    def __convert_rarity(cls, value: str) -> Literal[4, 5]:
        return HSR_CHARA_RARITY_MAP[value]

    @field_validator("description", mode="before")
    @classmethod
    def __convert_description(cls, value: str | None) -> str:
        return value or ""

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
