from typing import Literal

from pydantic import Field, field_validator

from ..base import APIModel

__all__ = ("Item",)


class Item(APIModel):
    """ZZZ item model."""

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
