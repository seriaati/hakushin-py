from __future__ import annotations

from typing import Any, Literal

from pydantic import Field, field_validator, model_validator

from ...constants import GI_CHARA_RARITY_MAP
from ...enums import GIElement
from ..base import APIModel

__all__ = (
    "Character",
    "CharacterConstellation",
    "CharacterDetail",
    "CharacterInfo",
    "CharacterPassive",
    "CharacterSkill",
    "CharacterStatsModifier",
    "FightPropGrowthCurve",
    "Namecard",
    "SkillUpgradeInfo",
    "UpgradeMaterial",
    "UpgradeMaterialInfo",
    "UpgradeMaterialInfos",
)


class Namecard(APIModel):
    """Character's namecard."""

    id: int = Field(alias="Id")
    name: str = Field(alias="Name")
    description: str = Field(alias="Desc")
    icon: str = Field(alias="Icon")

    @field_validator("icon", mode="before")
    def _convert_icon(cls, value: str) -> str:
        return f"https://api.hakush.in/gi/UI/{value}.webp"


class CharacterInfo(APIModel):
    """Character's information."""

    namecard: Namecard | None = Field(None, alias="Namecard")

    @field_validator("namecard", mode="before")
    def _handle_empty_namecard(cls, value: dict[str, Any] | None) -> dict[str, Any] | None:
        return value or None


class SkillUpgradeInfo(APIModel):
    """Character's skill upgrade information."""

    level: int = Field(alias="Level")
    icon: str = Field(alias="Icon")
    attributes: list[str] = Field(alias="Desc")
    parameters: list[float] = Field(alias="Param")

    @field_validator("icon", mode="before")
    def _convert_icon(cls, value: str) -> str:
        return f"https://api.hakush.in/gi/UI/{value}.webp"

    @field_validator("attributes", mode="before")
    def _remove_empty_attributes(cls, value: list[str]) -> list[str]:
        return [attr for attr in value if attr]


class CharacterSkill(APIModel):
    """Character's skill."""

    name: str = Field(alias="Name")
    description: str = Field(alias="Desc")
    upgrade_info: dict[str, SkillUpgradeInfo] = Field(alias="Promote")


class CharacterPassive(APIModel):
    """Character's passive talent."""

    name: str = Field(alias="Name")
    description: str = Field(alias="Desc")
    unlock: int = Field(alias="Unlock")
    parameters: list[float] = Field(alias="ParamList")
    icon: str = Field(alias="Icon")

    @field_validator("icon", mode="before")
    def _convert_icon(cls, value: str) -> str:
        return f"https://api.hakush.in/gi/UI/{value}.webp"


class CharacterConstellation(APIModel):
    """Character's constellation."""

    name: str = Field(alias="Name")
    description: str = Field(alias="Desc")
    parameters: list[float] = Field(alias="ParamList")
    icon: str = Field(alias="Icon")

    @field_validator("icon", mode="before")
    def _convert_icon(cls, value: str) -> str:
        return f"https://api.hakush.in/gi/UI/{value}.webp"


class UpgradeMaterial(APIModel):
    """Character's upgrade material."""

    name: str = Field(alias="Name")
    id: int = Field(alias="Id")
    count: int = Field(alias="Count")
    rarity: Literal[1, 2, 3, 4, 5] = Field(alias="Rank")

    @property
    def icon(self) -> str:
        """Material's icon URL."""
        return f"https://api.hakush.in/gi/UI/UI_ItemIcon_{self.id}.webp"


class UpgradeMaterialInfo(APIModel):
    """Character's upgrade material information."""

    materials: list[UpgradeMaterial] = Field(alias="Mats")
    mora_cost: int = Field(alias="Cost")


class UpgradeMaterialInfos(APIModel):
    """Character's upgrade material information."""

    ascensions: list[UpgradeMaterialInfo] = Field(alias="Ascensions")
    talents: list[list[UpgradeMaterialInfo]] = Field(alias="Talents")


class FightPropGrowthCurve(APIModel):
    """Character's stat growth curve data."""

    stat_type: str = Field(alias="type")
    growth_type: str = Field(alias="growCurve")


class CharacterStatsModifier(APIModel):
    """Character's stat modifiers."""

    hp: dict[str, float] = Field(alias="HP")
    atk: dict[str, float] = Field(alias="ATK")
    def_: dict[str, float] = Field(alias="DEF")
    ascension: list[dict[str, float]] = Field(alias="Ascension")
    prop_growth_curves: list[FightPropGrowthCurve] = Field(alias="PropGrowCurves")


class CharacterDetail(APIModel):
    """Genshin Impact character detail."""

    # Info
    name: str = Field(alias="Name")
    description: str = Field(alias="Desc")
    info: CharacterInfo = Field(alias="CharaInfo")
    rarity: Literal[4, 5] = Field(alias="Rarity")
    icon: str = Field(alias="Icon")

    # Combat
    skills: list[CharacterSkill] = Field(alias="Skills")
    passives: list[CharacterPassive] = Field(alias="Passives")
    constellations: list[CharacterConstellation] = Field(alias="Constellations")

    # Props
    stamina_recovery: float = Field(alias="StaminaRecovery")
    base_hp: float = Field(alias="BaseHP")
    base_atk: float = Field(alias="BaseATK")
    base_def: float = Field(alias="BaseDEF")
    crit_rate: float = Field(alias="CritRate")
    crit_dmg: float = Field(alias="CritDMG")

    stats_modifier: CharacterStatsModifier = Field(alias="StatsModifier")
    upgrade_materials: UpgradeMaterialInfos = Field(alias="Materials")

    @property
    def gacha_art(self) -> str:
        """Character's gacha art URL."""
        return self.icon.replace("AvatarIcon", "Gacha_AvatarImg")

    @field_validator("icon", mode="before")
    def _convert_icon(cls, value: str) -> str:
        return f"https://api.hakush.in/gi/UI/{value}.webp"

    @field_validator("rarity", mode="before")
    def _convert_rarity(cls, value: str) -> Literal[4, 5]:
        return GI_CHARA_RARITY_MAP[value]


class Character(APIModel):
    """Genshin Impact character."""

    id: str  # This field is not present in the API response.
    icon: str
    rarity: Literal[4, 5] = Field(alias="rank")
    description: str = Field(alias="desc")
    element: GIElement | None = None
    names: dict[Literal["EN", "CHS", "KR", "JP"], str]
    name: str = Field("")  # This value of this field is assigned in post processing.

    @field_validator("icon", mode="before")
    def _convert_icon(cls, value: str) -> str:
        return f"https://api.hakush.in/gi/UI/{value}.webp"

    @field_validator("rarity", mode="before")
    def _convert_rarity(cls, value: str) -> Literal[4, 5]:
        return GI_CHARA_RARITY_MAP[value]

    @field_validator("element", mode="before")
    def _convert_element(cls, value: str) -> GIElement | None:
        return GIElement(value) if value else None

    @model_validator(mode="before")
    def _transform_names(cls, values: dict[str, Any]) -> dict[str, Any]:
        # This is probably the most questionable API design decision I've ever seen.
        values["names"] = {
            "EN": values.pop("EN"),
            "CHS": values.pop("CHS"),
            "KR": values.pop("KR"),
            "JP": values.pop("JP"),
        }
        return values
