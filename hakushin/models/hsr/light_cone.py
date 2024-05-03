from typing import Any, Literal

from pydantic import Field, field_validator, model_validator

from ...constants import HSR_LIGHT_CONE_RARITY_MAP
from ..base import APIModel

__all__ = ("LightConeDetail", "SuperimposeInfo")


class SuperimposeInfo(APIModel):
    """Light cone's superimpose information."""

    name: str = Field(alias="Name")
    description: str = Field(alias="Desc")
    parameters: dict[str, list[float]] = Field(alias="Level")

    @model_validator(mode="before")
    def _flatten_parameters(cls, values: dict[str, Any]) -> dict[str, Any]:
        level = values["Level"]
        for key in level:
            level[key] = level[key]["ParamList"]

        return values


class LightConeDetail(APIModel):
    """HSR light cone detail."""

    id: int = Field(alias="Id")
    name: str = Field(alias="Name")
    description: str = Field(alias="Desc")
    rarity: Literal[4, 5] = Field(alias="Rarity")
    superimpose_info: SuperimposeInfo = Field(alias="Refinements")

    @field_validator("rarity", mode="before")
    def _convert_rarity(cls, value: str) -> Literal[4, 5]:
        return HSR_LIGHT_CONE_RARITY_MAP[value]

    @model_validator(mode="before")
    def _extract_id(cls, values: dict[str, Any]) -> dict[str, Any]:
        """Use a hacky way to extract character ID from relic recommendation.

        I don't understand why the API doesn't have the character ID in the response.
        """
        values["Id"] = values["Stats"][0]["EquipmentID"]
        return values

    @property
    def icon(self) -> str:
        """Light cone's icon URL."""
        return f"https://api.hakush.in/hsr/UI/lightconemediumicon/{self.id}.webp"

    @property
    def image(self) -> str:
        """Light cone's image URL."""
        return self.icon.replace("lightconemediumicon", "lightconemaxfigures")
