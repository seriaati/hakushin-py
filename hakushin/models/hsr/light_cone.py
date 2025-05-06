from __future__ import annotations

from typing import Any, Literal

from pydantic import Field, computed_field, field_validator, model_validator

from ...constants import HSR_LIGHT_CONE_RARITY_MAP
from ...enums import HSRPath
from ..base import APIModel

__all__ = ("LightCone", "LightConeDetail", "SuperimposeInfo")


class SuperimposeInfo(APIModel):
    """Represent a light cone's superimpose information.

    Attributes:
        name: The name of the superimpose information.
        description: The description of the superimpose information.
        parameters: A dictionary of parameters for the superimpose information.
    """

    name: str = Field(alias="Name")
    description: str = Field(alias="Desc")
    parameters: dict[str, list[float]] = Field(alias="Level")

    @model_validator(mode="before")
    @classmethod
    def __flatten_parameters(cls, values: dict[str, Any]) -> dict[str, Any]:
        level = values["Level"]
        for key in level:
            level[key] = level[key]["ParamList"]

        return values


class LightConeDetail(APIModel):
    """Represent an HSR light cone detail.

    Attributes:
        id: The ID of the light cone.
        name: The name of the light cone.
        description: The description of the light cone.
        path: The path of the light cone.
        rarity: The rarity of the light cone.
        superimpose_info: Superimpose information for the light cone.
        ascension_stats: A list of ascension stats for the light cone.
    """

    id: int = Field(alias="Id")
    name: str = Field(alias="Name")
    description: str = Field(alias="Desc")
    path: HSRPath = Field(alias="BaseType")
    rarity: Literal[3, 4, 5] = Field(alias="Rarity")
    superimpose_info: SuperimposeInfo = Field(alias="Refinements")
    ascension_stats: list[dict[str, Any]] = Field(alias="Stats")

    @field_validator("rarity", mode="before")
    @classmethod
    def __convert_rarity(cls, value: str) -> Literal[3, 4, 5]:
        return HSR_LIGHT_CONE_RARITY_MAP[value]

    @model_validator(mode="before")
    @classmethod
    def __extract_id(cls, values: dict[str, Any]) -> dict[str, Any]:
        values["Id"] = values["Stats"][0]["EquipmentID"]
        return values

    @computed_field
    @property
    def icon(self) -> str:
        """Get the light cone's icon URL."""
        return f"https://api.hakush.in/hsr/UI/lightconemediumicon/{self.id}.webp"

    @computed_field
    @property
    def image(self) -> str:
        """Get the light cone's image URL."""
        return self.icon.replace("lightconemediumicon", "lightconemaxfigures")


class LightCone(APIModel):
    """Represent an HSR light cone.

    Attributes:
        id: The ID of the light cone.
        rarity: The rarity of the light cone.
        description: The description of the light cone.
        path: The path of the light cone.
        names: A dictionary of names in different languages.
        name: The name of the light cone.
    """

    id: int  # This field is not present in the API response.
    rarity: Literal[3, 4, 5] = Field(alias="rank")
    description: str = Field(alias="desc")
    path: HSRPath = Field(alias="baseType")
    names: dict[Literal["en", "cn", "kr", "jp"], str]
    name: str = Field("")  # The value of this field is assigned in post processing.

    @computed_field
    @property
    def icon(self) -> str:
        """Get the light cone's icon URL."""
        return f"https://api.hakush.in/hsr/UI/lightconemediumicon/{self.id}.webp"

    @field_validator("description", mode="before")
    @classmethod
    def __handle_null_value(cls, value: str | None) -> str:
        return value or "???"

    @field_validator("icon", mode="before")
    @classmethod
    def __convert_icon(cls, value: str) -> str:
        return f"https://api.hakush.in/hsr/UI/avatarshopicon/{value}.webp"

    @field_validator("rarity", mode="before")
    @classmethod
    def __convert_rarity(cls, value: str) -> Literal[3, 4, 5]:
        return HSR_LIGHT_CONE_RARITY_MAP[value]

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
