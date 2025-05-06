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
    """Represent a set effect.

    Attributes:
        id: ID of the set effect.
        affix_id: Affix ID of the set effect.
        name: Name of the set effect.
        description: Description of the set effect.
        parameters: List of parameters for the set effect.
    """

    id: int
    affix_id: int = Field(alias="affixId")
    name: str = Field(alias="Name")
    description: str = Field(alias="Desc")
    parameters: list[float] = Field(alias="paramList")


class ArtifactSetDetailSetEffects(APIModel):
    """Represent set effects of an artifact set detail.

    Attributes:
        two_piece: Two-piece set effect.
        four_piece: Four-piece set effect, if available.
    """

    two_piece: SetEffect
    four_piece: SetEffect | None = None


class Artifact(APIModel):
    """Represent a Genshin Impact artifact.

    Attributes:
        icon: Icon URL of the artifact.
        name: Name of the artifact.
        description: Description of the artifact.
    """

    icon: str = Field(alias="Icon")
    name: str = Field(alias="Name")
    description: str = Field(alias="Desc")

    @field_validator("icon", mode="before")
    @classmethod
    def __convert_icon(cls, value: str) -> str:
        """Convert the icon path to a full URL."""
        return f"https://api.hakush.in/gi/UI/{value}.webp"


class ArtifactSetDetail(APIModel):
    """Represent a Genshin Impact artifact set detail.

    Attributes:
        id: ID of the artifact set.
        icon: Icon URL of the artifact set.
        set_effect: Set effects of the artifact set.
        parts: Parts of the artifact set.
    """

    id: int = Field(alias="Id")
    icon: str = Field(alias="Icon")
    set_effect: ArtifactSetDetailSetEffects = Field(alias="Affix")
    parts: dict[str, Artifact] = Field(alias="Parts")

    @field_validator("icon", mode="before")
    @classmethod
    def __convert_icon(cls, value: str) -> str:
        """Convert the icon path to a full URL."""
        return f"https://api.hakush.in/gi/UI/{value}.webp"

    @field_validator("set_effect", mode="before")
    @classmethod
    def __assign_set_effect(cls, value: list[dict[str, Any]]) -> dict[str, Any]:
        """Assign the set effect to the appropriate fields."""
        return {"two_piece": value[0], "four_piece": value[1] if len(value) > 1 else None}


class ArtifactSetEffect(APIModel):
    """Represent an artifact set effect.

    Attributes:
        names: Dictionary of names in different languages.
        name: Name of the artifact set effect.
        descriptions: Dictionary of descriptions in different languages.
        description: Description of the artifact set effect.
    """

    names: dict[Literal["EN", "KR", "CHS", "JP"], str]
    name: str = Field("")  # The value of this field is assigned in post processing.
    descriptions: dict[Literal["EN", "KR", "CHS", "JP"], str] = Field(alias="desc")
    description: str = Field("")  # The value of this field is assigned in post processing.

    @model_validator(mode="before")
    @classmethod
    def __transform_names(cls, values: dict[str, Any]) -> dict[str, Any]:
        """Transform the names field."""
        values["names"] = values.pop("name")
        return values


class ArtifactSetEffects(APIModel):
    """Represent artifact set effects.

    Attributes:
        two_piece: Two-piece set effect.
        four_piece: Four-piece set effect, if available.
    """

    two_piece: ArtifactSetEffect
    four_piece: ArtifactSetEffect | None = None


class ArtifactSet(APIModel):
    """Represent a Genshin Impact artifact set.

    Attributes:
        id: ID of the artifact set.
        icon: Icon URL of the artifact set.
        rarities: List of rarities for the artifact set.
        set_effect: Set effects of the artifact set.
        names: Dictionary of names in different languages.
        name: Name of the artifact set.
    """

    id: int
    icon: str
    rarities: list[int] = Field(alias="rank")
    set_effect: ArtifactSetEffects = Field(alias="set")
    names: dict[Literal["EN", "KR", "CHS", "JP"], str]
    name: str = Field("")  # The value of this field is assigned in post processing.

    @field_validator("icon", mode="before")
    @classmethod
    def __convert_icon(cls, value: str) -> str:
        """Convert the icon path to a full URL."""
        return f"https://api.hakush.in/gi/UI/{value}.webp"

    @field_validator("set_effect", mode="before")
    @classmethod
    def __assign_set_effects(cls, value: dict[str, Any]) -> dict[str, Any]:
        """Assign the set effects to the appropriate fields."""
        return {
            "two_piece": next(iter(value.values())),
            "four_piece": list(value.values())[1] if len(value) > 1 else None,
        }

    @model_validator(mode="before")
    @classmethod
    def __extract_names(cls, values: dict[str, Any]) -> dict[str, Any]:
        """Extract names from the set effect."""
        values["names"] = next(iter(values["set"].values()))["name"]
        return values
