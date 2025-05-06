from __future__ import annotations

from pydantic import Field

from ..base import APIModel

__all__ = ("New",)


class New(APIModel):
    """Represent new Genshin Impact data.

    Attributes:
        character_ids: A list of character IDs.
        weapon_ids: A list of weapon IDs.
        artifact_set_ids: A list of artifact set IDs.
        monster_ids: A list of monster IDs.
        item_ids: A list of item IDs.
        version: The current version.
    """

    character_ids: list[str | int] = Field(alias="character")
    weapon_ids: list[int] = Field(alias="weapon")
    artifact_set_ids: list[int] = Field(alias="artifact")
    monster_ids: list[int] = Field(alias="monster")
    item_ids: list[int] = Field(alias="item")
    version: str
