"""Genshin Impact Stygian Onslaught models."""

from __future__ import annotations

import datetime
import re
from typing import Any, Literal

from pydantic import Field, field_validator, model_validator

from hakushin.models.base import APIModel

__all__ = (
    "Stygian",
    "StygianDetail",
    "StygianDifficultyConfig",
    "StygianEnemy",
    "StygianEnemyBuff",
    "StygianEnemyRecommendation",
    "StygianLevel",
)


class StygianDifficultyConfig(APIModel):
    """Configuration for a Stygian Onslaught difficulty.

    Attributes:
        level: The difficulty level.
        name: The name of the difficulty.
        descriptions: A list of descriptions for the difficulty.
    """

    level: int = Field(alias="Level")
    name: str = Field(alias="Name")
    descriptions: list[str] = Field(alias="DescList")


class StygianEnemyBuff(APIModel):
    """A buff associated with a Stygian Abyss enemy.

    Attributes:
        name: The buff name.
        description: The buff description.
    """

    name: str
    description: str


class StygianEnemyRecommendation(APIModel):
    """Recommendations for dealing with a Stygian Abyss enemy.

    Attributes:
        recommend: Recommended strategies or characters.
        dont_recommend: Strategies or characters to avoid.
    """

    recommend: str
    dont_recommend: str | None = None

    @field_validator("recommend", "dont_recommend", mode="after")
    @classmethod
    def __remove_color_tags(cls, v: str | None) -> str | None:
        # Remove <Color=#FFFFFF40> and </Color> tags
        if v is not None:
            v = re.sub(r"<Color=#[0-9A-Fa-f]{8}>", "", v)
            v = re.sub(r"</Color>", "", v)
        return v


class StygianEnemy(APIModel):
    """A Stygian Onslaught enemy.

    Attributes:
        id: The enemy ID.
        name: The enemy name.
        description: The enemy description.
        icon: The enemy icon URL.
        buffs: A list of buffs associated with the enemy.
        recommendation: Recommendations for dealing with the enemy.
    """

    id: int
    name: str = Field(alias="Name")
    description: str = Field(alias="Desc")
    icon: str = Field(alias="Icon")

    buffs: list[StygianEnemyBuff] = Field(default_factory=list)
    recommendation: StygianEnemyRecommendation | None = None

    @field_validator("icon", mode="after")
    @classmethod
    def __process_icon(cls, v: str) -> str:
        return f"https://api.hakush.in/gi/UI/{v}.webp"

    @model_validator(mode="before")
    @classmethod
    def __process_model(cls, v: dict[str, Any]) -> dict[str, Any]:
        if "MonsterBuffNameList" in v and "MonsterBuffDetailList" in v:
            names = v.pop("MonsterBuffNameList", [])
            descs = v.pop("MonsterBuffDetailList", [])
            v["buffs"] = [
                StygianEnemyBuff(name=name, description=desc)
                for name, desc in zip(names, descs, strict=False)
            ]
        if "RecommendList" in v:
            recs = v.pop("RecommendList", [])
            v["recommendation"] = StygianEnemyRecommendation(
                recommend=recs[0], dont_recommend=recs[1] if len(recs) > 1 else None
            )
        return v


class StygianLevel(APIModel):
    """A Stygian Onslaught level.

    Attributes:
        id: The level ID.
        enemy_level: The enemy level.
        difficulty_config: The difficulty configuration.
        enemies: A mapping of enemy IDs to enemy details.
    """

    id: int
    enemy_level: int = Field(alias="MonsterLevel")
    difficulty_config: StygianDifficultyConfig = Field(alias="DifficultyConfig")
    enemies: dict[int, StygianEnemy] = Field(alias="LevelConfig")

    @field_validator("enemies", mode="before")
    @classmethod
    def __process_enemies(cls, v: dict[str, Any]) -> dict[int, StygianEnemy]:
        return {
            int(enemy_id): StygianEnemy(id=int(enemy_id), **enemy_data)
            for enemy_id, enemy_data in v.items()
        }


class StygianDetail(APIModel):
    """Details of a Stygian Onslaught entry.

    Attributes:
        id: The Stygian ID.
        name: The name of the Stygian.
        start_at: The start datetime of the Stygian event.
        end_at: The end datetime of the Stygian event.
        levels: A mapping of level IDs to StygianLevel objects.
    """

    id: int = Field(alias="Id")
    name: str = Field(alias="Name")
    start_at: datetime.datetime = Field(alias="BeginTime")
    end_at: datetime.datetime = Field(alias="EndTime")
    levels: dict[int, StygianLevel] = Field(alias="Level")

    @field_validator("levels", mode="before")
    @classmethod
    def __process_levels(cls, v: dict[str, Any]) -> dict[int, StygianLevel]:
        return {
            int(level_id): StygianLevel(id=int(level_id), **level_data)
            for level_id, level_data in v.items()
        }


class Stygian(APIModel):
    """A Stygian Onslaught entry.

    Attributes:
        id: The Stygian ID.
        names: A dictionary of names in different languages.
        beta_start_at: The start datetime of the beta period, if applicable.
        beta_end_at: The end datetime of the beta period, if applicable.
        live_start_at: The start datetime of the live period, if applicable.
        live_end_at: The end datetime of the live period, if applicable.
        name: The name of the Stygian (added in post-processing).
    """

    id: int
    names: dict[Literal["EN", "CHS", "KR", "JP"], str]

    beta_start_at: datetime.datetime | None = Field(default=None, alias="begin")
    beta_end_at: datetime.datetime | None = Field(default=None, alias="begin")
    live_start_at: datetime.datetime | None = Field(default=None, alias="live_begin")
    live_end_at: datetime.datetime | None = Field(default=None, alias="live_end")

    # Added in post-processing
    name: str = ""

    @model_validator(mode="before")
    @classmethod
    def __transform_names(cls, values: dict[str, Any]) -> dict[str, Any]:
        values["names"] = {
            "EN": values.pop("EN"),
            "CHS": values.pop("CHS"),
            "KR": values.pop("KR"),
            "JP": values.pop("JP"),
        }
        return values
