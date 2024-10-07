from __future__ import annotations

from typing import Any, Literal

from pydantic import Field, field_validator, model_validator

from ..base import APIModel

__all__ = (
    "Artifact",
    "ArtifactSet",
    "ArtifactSetDetail",
    "ArtifactSetDetailSetEffects",
    "ArtifactSetEffect",
    "ArtifactSetEffects",
    "SetEffect",
)


class SetEffect(APIModel):
    """Artifact set's set effect."""

    id: int
    affix_id: int = Field(alias="affixId")
    name: str = Field(alias="Name")
    description: str = Field(alias="Desc")
    parameters: list[float] = Field(alias="paramList")


class ArtifactSetDetailSetEffects(APIModel):
    """Artifact set's set effects."""

    two_piece: SetEffect
    four_piece: SetEffect | None = None


class Artifact(APIModel):
    """Genshin Impact artifact."""

    icon: str = Field(alias="Icon")
    name: str = Field(alias="Name")
    description: str = Field(alias="Desc")

    @field_validator("icon", mode="before")
    def _convert_icon(cls, value: str) -> str:
        return f"https://api.hakush.in/gi/UI/{value}.webp"


class ArtifactSetDetail(APIModel):
    """Genshin Impact artifact set detail."""

    id: int = Field(alias="Id")
    icon: str = Field(alias="Icon")
    set_effect: ArtifactSetDetailSetEffects = Field(alias="Affix")
    parts: dict[str, Artifact] = Field(alias="Parts")

    @field_validator("icon", mode="before")
    def _convert_icon(cls, value: str) -> str:
        return f"https://api.hakush.in/gi/UI/{value}.webp"

    @field_validator("set_effect", mode="before")
    def _assign_set_effect(cls, value: list[dict[str, Any]]) -> dict[str, Any]:
        return {"two_piece": value[0], "four_piece": value[1] if len(value) > 1 else None}


class ArtifactSetEffect(APIModel):
    """Artifact set effect."""

    names: dict[Literal["EN", "KR", "CHS", "JP"], str]
    name: str = Field(None)  # The value of this field is assigned in post processing.
    descriptions: dict[Literal["EN", "KR", "CHS", "JP"], str] = Field(alias="desc")
    description: str = Field(None)  # The value of this field is assigned in post processing.

    @model_validator(mode="before")
    def _transform_names(cls, values: dict[str, Any]) -> dict[str, Any]:
        values["names"] = values.pop("name")
        return values


class ArtifactSetEffects(APIModel):
    """Artifact set effects."""

    two_piece: ArtifactSetEffect
    four_piece: ArtifactSetEffect | None = None


class ArtifactSet(APIModel):
    """Genshin Impact artifact set."""

    id: int
    icon: str
    rarities: list[int] = Field(alias="rank")
    set_effect: ArtifactSetEffects = Field(alias="set")
    names: dict[Literal["EN", "KR", "CHS", "JP"], str]
    name: str = Field(None)  # The value of this field is assigned in post processing.

    @field_validator("icon", mode="before")
    def _convert_icon(cls, value: str) -> str:
        return f"https://api.hakush.in/gi/UI/{value}.webp"

    @field_validator("set_effect", mode="before")
    def _assign_set_effects(cls, value: dict[str, Any]) -> dict[str, Any]:
        return {
            "two_piece": next(iter(value.values())),
            "four_piece": list(value.values())[1] if len(value) > 1 else None,
        }

    @model_validator(mode="before")
    def _extract_names(cls, values: dict[str, Any]) -> dict[str, Any]:
        values["names"] = next(iter(values["set"].values()))["name"]
        return values
