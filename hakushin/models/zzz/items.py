from __future__ import annotations

from typing import Literal

from pydantic import Field, field_validator

from ..base import APIModel

__all__ = ("Item",)


class Item(APIModel):
    """Represent a ZZZ item.

    Attributes:
        icon: Icon URL of the item.
        rarity: Rarity of the item.
        class_: Class of the item.
        name: Name of the item.
        id: ID of the item.
    """

    icon: str
    rarity: Literal[1, 2, 3, 4, 5] = Field(alias="rank")
    class_: int = Field(alias="class")
    name: str
    id: int

    @field_validator("icon", mode="before")
    @classmethod
    def __convert_icon(cls, value: str) -> str:
        icon = value.split("/")[-1].split(".")[0]
        return f"https://api.hakush.in/zzz/UI/{icon}.webp"
