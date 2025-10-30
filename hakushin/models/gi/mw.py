from __future__ import annotations

from typing import Literal

from pydantic import Field, field_validator

from hakushin.enums import MWCostumeBodyType
from hakushin.models.base import APIModel

__all__ = ("MWCostume", "MWCostumeSet", "MWItem")


class BaseMWCostume(APIModel):
    """Miliastra Wonderland costume base model"""

    id: int = Field(alias="Id")
    name: str = Field(alias="Name")
    description: str = Field(alias="Desc")
    rarity: Literal[5, 4, 3, 2] | None = Field(alias="Rarity")
    icon: str = Field(alias="Icon")

    body_types: list[MWCostumeBodyType] = Field(alias="BodyType")
    colors: list[str] = Field(alias="Color")

    @field_validator("rarity", mode="before")
    @classmethod
    def __convert_rarity(cls, v: Literal["Purple", "Blue", "Green", "None"]) -> int | None:
        mapping = {"Orange": 5, "Purple": 4, "Blue": 3, "Green": 2, "None": None}
        return mapping[v]

    @field_validator("icon", mode="before")
    @classmethod
    def __icon_url(cls, v: str) -> str:
        return f"https://api.hakush.in/gi/UI/{v}.webp"


class MWCostumeSet(BaseMWCostume):
    """Miliastra Wonderland costume set"""


class MWCostume(BaseMWCostume):
    """Miliastra Wonderland costume"""

    slots: list[str] = Field(alias="SlotType")


class MWItem(APIModel):
    """Miliastra Wonderland item"""

    id: int
    name: str = Field(alias="Name")
    description: str = Field(alias="Desc")
    rarity: Literal[5, 4, 3, 2, 1] | None = Field(alias="Rank")
    icon: str = Field(alias="Icon")
    type: str = Field(alias="ItemType")
    sources: list[str] = Field(alias="SourceList")
