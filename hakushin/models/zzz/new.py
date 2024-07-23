from pydantic import Field

from ..base import APIModel

__all__ = ("New",)


class New(APIModel):
    """ZZZ new stuff."""

    character_ids: list[int] = Field(alias="character")
    bangboo_ids: list[int] = Field(alias="bangboo")
    weapon_ids: list[int] = Field(alias="weapon")
    equipment_ids: list[int] = Field(alias="equipment")
    item_ids: list[int] = Field(alias="item")
    current_version: str = Field(alias="version")
    previous_versions: list[str] = Field(alias="previous")
