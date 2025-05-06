from __future__ import annotations

from pydantic import Field

from ..base import APIModel

__all__ = ("New",)


class New(APIModel):
    """Represent new Zenless Zone Zero data.

    Attributes:
        character_ids: A list of character IDs.
        bangboo_ids: A list of Bangboo IDs.
        weapon_ids: A list of weapon IDs.
        equipment_ids: A list of equipment IDs.
        item_ids: A list of item IDs.
        current_version: The current version.
        previous_versions: A list of previous versions.
    """

    character_ids: list[int] = Field(alias="character")
    bangboo_ids: list[int] = Field(alias="bangboo")
    weapon_ids: list[int] = Field(alias="weapon")
    equipment_ids: list[int] = Field(alias="equipment")
    item_ids: list[int] = Field(alias="item")
    current_version: str = Field(alias="version")
    previous_versions: list[str] = Field(alias="previous")
