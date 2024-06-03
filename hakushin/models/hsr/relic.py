from typing import Any, Literal, Self

from pydantic import Field, computed_field, field_validator, model_validator

from ...utils import replace_placeholders
from ..base import APIModel

__all__ = (
    "Relic",
    "RelicSet",
    "RelicSetDetail",
    "RelicSetEffect",
    "RelicSetEffects",
    "SetDetailSetEffect",
)


class Relic(APIModel):
    """HSR relic."""

    id: int = Field(None)  # This field is not present in the API response.
    name: str = Field(alias="Name")
    description: str = Field(alias="Desc")
    story: str = Field(alias="Story")

    @computed_field
    @property
    def icon(self) -> str:
        """Relic's icon URL."""
        relic_id = str(self.id)[1:4]
        part_id = str(self.id)[-1]
        return f"https://api.hakush.in/hsr/UI/relicfigures/IconRelic_{relic_id}_{part_id}.webp"


class SetDetailSetEffect(APIModel):
    """Relic set detail's set effect."""

    description: str = Field(alias="Desc")
    parameters: list[float] = Field(alias="ParamList")

    @model_validator(mode="after")
    def _format_parameters(self) -> Self:
        self.description = replace_placeholders(self.description, self.parameters)
        return self


class SetDetailSetEffects(APIModel):
    """Relic set detail's set effects."""

    two_piece: SetDetailSetEffect
    four_piece: SetDetailSetEffect | None = None


class RelicSetDetail(APIModel):
    """HSR relic set detail."""

    name: str = Field(alias="Name")
    icon: str = Field(alias="Icon")
    parts: dict[str, Relic] = Field(alias="Parts")
    set_effects: SetDetailSetEffects = Field(alias="RequireNum")

    @field_validator("icon", mode="before")
    def _convert_icon(cls, value: str) -> str:
        icon_id = value.split("/")[-1].split(".")[0]
        return f"https://api.hakush.in/hsr/UI/itemfigures/{icon_id}.webp"

    @field_validator("set_effects", mode="before")
    def _assign_set_effects(cls, value: dict[str, Any]) -> dict[str, Any]:
        return {
            "two_piece": value["2"],
            "four_piece": value.get("4"),
        }

    @field_validator("parts", mode="before")
    def _convert_parts(cls, value: dict[str, Any]) -> dict[str, Any]:
        return {key: Relic(id=int(key), **value[key]) for key in value}


class RelicSetEffect(APIModel):
    """Relic set effect."""

    descriptions: dict[Literal["en", "cn", "kr", "jp"], str]
    description: str = Field(None)  # The value of this field is assigned in post processing.
    parameters: list[float] = Field(alias="ParamList")

    @model_validator(mode="before")
    def _assign_descriptions(cls, value: dict[str, Any]) -> dict[str, Any]:
        value["descriptions"] = {
            "en": value.pop("en"),
            "cn": value.pop("cn"),
            "kr": value.pop("kr"),
            "jp": value.pop("jp"),
        }
        return value


class RelicSetEffects(APIModel):
    """Relic set's set effects."""

    two_piece: RelicSetEffect
    four_piece: RelicSetEffect | None = None


class RelicSet(APIModel):
    """HSR relic set."""

    id: int  # This field is not present in the API response.
    icon: str
    names: dict[Literal["en", "cn", "kr", "jp"], str]
    name: str = Field(None)  # The value of this field is assigned in post processing.
    set_effect: RelicSetEffects = Field(alias="set")

    @field_validator("icon", mode="before")
    def _convert_icon(cls, value: str) -> str:
        icon_id = value.split("/")[-1].split(".")[0]
        return f"https://api.hakush.in/hsr/UI/itemfigures/{icon_id}.webp"

    @field_validator("set_effect", mode="before")
    def _assign_set_effect(cls, value: dict[str, Any]) -> dict[str, Any]:
        return {
            "two_piece": value["2"],
            "four_piece": value.get("4"),
        }

    @model_validator(mode="before")
    def _assign_names(cls, value: dict[str, Any]) -> dict[str, Any]:
        value["names"] = {
            "en": value.pop("en"),
            "cn": value.pop("cn"),
            "kr": value.pop("kr"),
            "jp": value.pop("jp"),
        }
        return value
