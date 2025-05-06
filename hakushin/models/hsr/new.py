from __future__ import annotations

from pydantic import Field

from ..base import APIModel

__all__ = ("New",)


class New(APIModel):
    """Represent new Honkai Star Rail data.

    Attributes:
        character_ids: A list of character IDs.
        light_cone_ids: A list of light cone IDs.
        relic_set_ids: A list of relic set IDs.
        monster_ids: A list of monster IDs.
        item_ids: A list of item IDs.
        version: The current version.
    """

    character_ids: list[int] = Field(alias="character")
    light_cone_ids: list[int] = Field(alias="lightcone")
    relic_set_ids: list[int] = Field(alias="relicset")
    monster_ids: list[int] = Field(alias="monster")
    item_ids: list[int] = Field(alias="item")
    version: str
