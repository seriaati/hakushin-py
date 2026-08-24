"""Genshin Impact Spiral Abyss models."""

from __future__ import annotations

import datetime
from typing import Any, Literal

from pydantic import Field, field_validator, model_validator

from hakushin.constants import GI_ICON_URL_PREFIX
from hakushin.models.base import APIModel

__all__ = (
    "SpiralAbyss",
    "SpiralAbyssBlessing",
    "SpiralAbyssChamber",
    "SpiralAbyssDetail",
    "SpiralAbyssEnemy",
    "SpiralAbyssFloor",
)


class SpiralAbyssBlessing(APIModel):
    """A Spiral Abyss Blessing of the Abyssal Moon.

    Attributes:
        icon: The blessing icon URL.
        name: The blessing name.
        description: The blessing description.
    """

    icon: str
    name: str
    description: str = Field(alias="desc")

    @field_validator("icon", mode="after")
    @classmethod
    def __process_icon(cls, v: str) -> str:
        return f"{GI_ICON_URL_PREFIX}/{v}.webp"


class SpiralAbyssEnemy(APIModel):
    """A Spiral Abyss enemy.

    Attributes:
        id: The enemy ID.
        hp: The enemy HP.
        name: The enemy name.
        icon: The enemy icon URL.
    """

    id: int
    hp: float
    name: str
    icon: str

    @field_validator("icon", mode="after")
    @classmethod
    def __process_icon(cls, v: str) -> str:
        return f"{GI_ICON_URL_PREFIX}/{v}.webp"


class SpiralAbyssChamber(APIModel):
    """A Spiral Abyss chamber.

    Attributes:
        id: The chamber ID.
        enemy_level: The enemy level.
        challenge_conditions: The star challenge conditions, one entry per star; the entry format depends on the condition type.
        condition_type: The challenge condition type.
        first_half: The enemies in the first half.
        second_half: The enemies in the second half.
    """

    id: int
    enemy_level: int = Field(alias="level")
    challenge_conditions: list[list[int]] = Field(alias="cond")
    condition_type: str = Field(alias="type")
    first_half: list[SpiralAbyssEnemy] = Field(alias="first")
    second_half: list[SpiralAbyssEnemy] = Field(alias="second")


class SpiralAbyssFloor(APIModel):
    """A Spiral Abyss floor.

    Attributes:
        id: The floor ID.
        buffs: The Ley Line Disorders of the floor.
        chambers: A mapping of chamber IDs to chambers.
        hp_ability: The internal enemy HP scaling ability name.
        first_half_buff: The buff for the first half, if any.
        second_half_buff: The buff for the second half, if any.
    """

    id: int
    buffs: list[str] = Field(alias="buff")
    chambers: dict[int, SpiralAbyssChamber] = Field(alias="room")
    hp_ability: str
    first_half_buff: str | None = None
    second_half_buff: str | None = None

    @field_validator("chambers", mode="before")
    @classmethod
    def __process_chambers(cls, v: dict[str, Any]) -> dict[int, SpiralAbyssChamber]:
        return {
            int(chamber_id): SpiralAbyssChamber(id=int(chamber_id), **chamber_data)
            for chamber_id, chamber_data in v.items()
        }


class SpiralAbyssDetail(APIModel):
    """Details of a Spiral Abyss phase.

    Attributes:
        id: The Spiral Abyss phase ID.
        start_at: The start datetime of the phase.
        end_at: The end datetime of the phase.
        blessing: The Blessing of the Abyssal Moon.
        floors: A mapping of floor IDs to floors.
    """

    id: int
    start_at: datetime.datetime = Field(alias="open")
    end_at: datetime.datetime = Field(alias="close")
    blessing: SpiralAbyssBlessing = Field(alias="leyline")
    floors: dict[int, SpiralAbyssFloor] = Field(alias="floor")

    @field_validator("floors", mode="before")
    @classmethod
    def __process_floors(cls, v: dict[str, Any]) -> dict[int, SpiralAbyssFloor]:
        return {
            int(floor_id): SpiralAbyssFloor(id=int(floor_id), **floor_data)
            for floor_id, floor_data in v.items()
        }


class SpiralAbyss(APIModel):
    """A Spiral Abyss phase.

    Attributes:
        id: The Spiral Abyss phase ID.
        names: A dictionary of blessing names in different languages.
        icon: The blessing icon URL.
        description: The blessing description.
        start_at: The start datetime of the phase.
        end_at: The end datetime of the phase.
        live_start_at: The start datetime of the live period, if applicable.
        live_end_at: The end datetime of the live period, if applicable.
        name: The blessing name (added in post-processing).
    """

    id: int
    names: dict[Literal["en", "zh", "ko", "ja"], str]
    icon: str
    description: str = Field(alias="desc")

    start_at: datetime.datetime = Field(alias="begin")
    end_at: datetime.datetime = Field(alias="end")
    live_start_at: datetime.datetime | None = Field(default=None, alias="live_begin")
    live_end_at: datetime.datetime | None = Field(default=None, alias="live_end")

    # Added in post-processing
    name: str = ""

    @field_validator("icon", mode="after")
    @classmethod
    def __process_icon(cls, v: str) -> str:
        return f"{GI_ICON_URL_PREFIX}/{v}.webp"

    @model_validator(mode="before")
    @classmethod
    def __transform_names(cls, values: dict[str, Any]) -> dict[str, Any]:
        values["names"] = {
            "en": values.pop("en"),
            "zh": values.pop("zh"),
            "ko": values.pop("ko"),
            "ja": values.pop("ja"),
        }
        return values
