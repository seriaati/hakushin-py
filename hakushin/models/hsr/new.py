from __future__ import annotations

from pydantic import Field

from ..base import APIModel

__all__ = ("New",)


class New(APIModel):
    """Genshin Impact new stuff."""

    character_ids: list[int] = Field(alias="character")
    light_cone_ids: list[int] = Field(alias="lightcone")
    relic_set_ids: list[int] = Field(alias="relicset")
    monster_ids: list[int] = Field(alias="monster")
    item_ids: list[int] = Field(alias="item")
    version: str
