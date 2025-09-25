from __future__ import annotations

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
    "SetDetailSetEffects",
)


class Relic(APIModel):
    """Represent an HSR relic.

    Attributes:
        id: The ID of the relic.
        name: The name of the relic.
        description: The description of the relic.
        story: The story of the relic.
    """

    id: int = Field(0)  # This field is not present in the API response.
    name: str = Field(alias="Name")
    description: str | None = Field(alias="Desc", default=None)
    story: str | None = Field(alias="Story", default=None)

    @computed_field
    @property
    def icon(self) -> str:
        """Get the relic's icon URL."""
        relic_id = str(self.id)[1:4]
        part_id = str(self.id)[-1]
        return f"https://api.hakush.in/hsr/UI/relicfigures/IconRelic_{relic_id}_{part_id}.webp"


class SetDetailSetEffect(APIModel):
    """Represent a relic set detail's set effect.

    Attributes:
        description: The description of the set effect.
        parameters: A list of parameters for the set effect.
    """

    description: str = Field(alias="Desc")
    parameters: list[float] = Field(alias="ParamList")

    @model_validator(mode="after")
    def __format_parameters(self) -> Self:
        self.description = replace_placeholders(self.description, self.parameters)
        return self


class SetDetailSetEffects(APIModel):
    """Represent relic set detail's set effects.

    Attributes:
        two_piece: The two-piece set effect.
        four_piece: The four-piece set effect, if available.
    """

    two_piece: SetDetailSetEffect
    four_piece: SetDetailSetEffect | None = None


class RelicSetDetail(APIModel):
    """Represent an HSR relic set detail.

    Attributes:
        name: The name of the relic set.
        icon: The icon URL of the relic set.
        parts: A dictionary of relic parts.
        set_effects: The set effects of the relic set.
    """

    name: str = Field(alias="Name")
    icon: str = Field(alias="Icon")
    parts: dict[str, Relic] = Field(alias="Parts")
    set_effects: SetDetailSetEffects = Field(alias="RequireNum")

    @field_validator("icon", mode="before")
    @classmethod
    def __convert_icon(cls, value: str) -> str:
        icon_id = value.rsplit("/", maxsplit=1)[-1].split(".", maxsplit=1)[0]
        return f"https://api.hakush.in/hsr/UI/itemfigures/{icon_id}.webp"

    @field_validator("set_effects", mode="before")
    @classmethod
    def __assign_set_effects(cls, value: dict[str, Any]) -> dict[str, Any]:
        return {"two_piece": value["2"], "four_piece": value.get("4")}

    @field_validator("parts", mode="before")
    @classmethod
    def __convert_parts(cls, value: dict[str, Any]) -> dict[str, Any]:
        return {key: Relic(id=int(key), **value[key]) for key in value}


class RelicSetEffect(APIModel):
    """Represent a relic set effect.

    Attributes:
        descriptions: A dictionary of descriptions in different languages.
        description: The description of the relic set effect.
        parameters: A list of parameters for the relic set effect.
    """

    descriptions: dict[Literal["en", "cn", "kr", "jp"], str]
    description: str = Field("")  # The value of this field is assigned in post processing.
    parameters: list[float] = Field(alias="ParamList")

    @model_validator(mode="before")
    @classmethod
    def __assign_descriptions(cls, value: dict[str, Any]) -> dict[str, Any]:
        value["descriptions"] = {
            "en": value.pop("en"),
            "cn": value.pop("cn"),
            "kr": value.pop("kr"),
            "jp": value.pop("jp"),
        }
        return value


class RelicSetEffects(APIModel):
    """Represent a relic set's set effects.

    Attributes:
        two_piece: The two-piece set effect.
        four_piece: The four-piece set effect, if available.
    """

    two_piece: RelicSetEffect
    four_piece: RelicSetEffect | None = None


class RelicSet(APIModel):
    """Represent an HSR relic set.

    Attributes:
        id: The ID of the relic set.
        icon: The icon URL of the relic set.
        names: A dictionary of names in different languages.
        name: The name of the relic set.
        set_effect: The set effects of the relic set.
    """

    id: int  # This field is not present in the API response.
    icon: str
    names: dict[Literal["en", "cn", "kr", "jp"], str]
    name: str = Field("")  # The value of this field is assigned in post processing.
    set_effect: RelicSetEffects = Field(alias="set")

    @field_validator("icon", mode="before")
    @classmethod
    def __convert_icon(cls, value: str) -> str:
        icon_id = value.rsplit("/", maxsplit=1)[-1].split(".", maxsplit=1)[0]
        return f"https://api.hakush.in/hsr/UI/itemfigures/{icon_id}.webp"

    @field_validator("set_effect", mode="before")
    @classmethod
    def __assign_set_effect(cls, value: dict[str, Any]) -> dict[str, Any]:
        return {"two_piece": value["2"], "four_piece": value.get("4")}

    @model_validator(mode="before")
    @classmethod
    def __assign_names(cls, value: dict[str, Any]) -> dict[str, Any]:
        value["names"] = {
            "en": value.pop("en"),
            "cn": value.pop("cn"),
            "kr": value.pop("kr"),
            "jp": value.pop("jp"),
        }
        return value
