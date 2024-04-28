from pydantic import Field

from ..base import APIModel

__all__ = ("Artifact", "ArtifactSet", "SetEffect")


class SetEffect(APIModel):
    """Artifact set's set effect."""

    id: int = Field(alias="id")
    affix_id: int = Field(alias="AffixId")
    name: str = Field(alias="Name")
    description: str = Field(alias="Desc")
    parameters: list[float] = Field(alias="paramList")


class Artifact(APIModel):
    """Genshin Impact artifact."""

    icon: str = Field(alias="Icon")
    name: str = Field(alias="Name")
    description: str = Field(alias="Desc")


class ArtifactSet(APIModel):
    """Genshin Impact artifact set."""

    id: int = Field(alias="Id")
    icon: str = Field(alias="Icon")
    effects: list[SetEffect] = Field(alias="Affix")
    parts: dict[str, Artifact] = Field(alias="Parts")
