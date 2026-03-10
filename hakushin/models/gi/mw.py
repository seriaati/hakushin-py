"""Miliastra Wonderland costume and item models."""

from __future__ import annotations

from typing import Literal

from pydantic import Field, field_validator

from hakushin.enums import MWCostumeBodyType
from hakushin.models.base import APIModel

__all__ = ("MWCostume", "MWCostumeSet", "MWItem")


class BaseMWCostume(APIModel):
    """Miliastra Wonderland costume base model"""

    id: int
    name: str
    description: str = Field(alias="desc")
    rarity: Literal[5, 4, 3, 2] | None
    icon: str

    body_types: list[MWCostumeBodyType] = Field(alias="body_type")
    colors: list[str] = Field(alias="color")

    @field_validator("rarity", mode="before")
    @classmethod
    def __convert_rarity(cls, v: Literal["Purple", "Blue", "Green", "None"]) -> int | None:
        mapping = {"Orange": 5, "Purple": 4, "Blue": 3, "Green": 2, "None": None}
        return mapping.get(v)

    @field_validator("icon", mode="before")
    @classmethod
    def __icon_url(cls, v: str) -> str:
        return f"https://static.nanoka.cc/gi/UI/{v}.webp"


class MWCostumeSet(BaseMWCostume):
    """Miliastra Wonderland costume set"""


class MWCostume(BaseMWCostume):
    """Miliastra Wonderland costume"""

    slots: list[str] = Field(alias="slot_type")


class MWItem(APIModel):
    """Miliastra Wonderland item"""

    id: int
    name: str
    description: str = Field(alias="desc")
    rarity: Literal[5, 4, 3, 2, 1] | None = Field(alias="rank")
    icon: str | None
    type: str = Field(alias="item_type")
    sources: list[str] = Field(alias="source_list")

    @field_validator("icon", mode="before")
    @classmethod
    def __icon_url(cls, v: str) -> str | None:
        if not v:
            return None
        return f"https://static.nanoka.cc/gi/UI/{v}.webp"
