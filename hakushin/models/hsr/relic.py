from pydantic import Field

from ..base import APIModel


class Relic(APIModel):
    """HSR relic."""

    name: str = Field(alias="Name")
    description: str = Field(alias="Desc")
    story: str = Field(alias="Story")


class SetEffect(APIModel):
    """Relic set's set effect."""

    description: str = Field(alias="Desc")
    parameters: list[float] = Field(alias="ParamList")


class RelicSetDetail(APIModel):
    """HSR relic set detail."""

    name: str = Field(alias="Name")
    icon: str = Field(alias="Icon")
    parts: dict[str, Relic] = Field(alias="Parts")
    set_effects: dict[str, SetEffect] = Field(alias="RequireNum")
