from pydantic import Field

from ..base import APIModel

__all__ = ("New",)


class New(APIModel):
    """Genshin Impact new stuff."""

    character_ids: list[int] = Field(alias="character")
    weapon_ids: list[int] = Field(alias="weapon")
    artifact_set_ids: list[int] = Field(alias="artifact")
    monster_ids: list[int] = Field(alias="monster")
    item_ids: list[int] = Field(alias="item")
    version: str
