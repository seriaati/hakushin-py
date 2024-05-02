from typing import Any

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


class CharacterInfo(APIModel):
    """Character's information."""

    namecard: Namecard = Field(alias="Namecard")


class SkillUpgradeInfo(APIModel):
    """Character's skill upgrade information."""

    level: int = Field(alias="Level")
    icon: str = Field(alias="Icon")
    attributes: list[str] = Field(alias="Desc")
    parameters: list[float] = Field(alias="Param")

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


class CharacterConstellation(APIModel):
    """Character's constellation."""

    name: str = Field(alias="Name")
    description: str = Field(alias="Desc")
    parameters: list[float] = Field(alias="ParamList")


class UpgradeMaterial(APIModel):
    """Character's upgrade material."""

    name: str = Field(alias="Name")
    id: int = Field(alias="Id")
    count: int = Field(alias="Count")
    rarity: int = Field(alias="Rank")

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
    stat_type: str = Field(alias="type")
    growth_type: str = Field(alias="growCurve")


class CharacterStatsModifier(APIModel):
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
    rarity: int = Field(alias="Rarity")
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

    @field_validator("rarity", mode="before")
    def _convert_rarity(cls, value: str) -> int:
        return GI_CHARA_RARITY_MAP[value]


class Character(APIModel):
    """Genshin Impact character."""

    id: str  # This field is not present in the API response.
    icon: str
    rarity: int = Field(alias="rank")
    description: str = Field(alias="desc")
    element: GIElement
    names: dict[str, str]
    name: str = Field(None)  # This value of this field is assigned in post processing.

    @field_validator("rarity", mode="before")
    def _convert_rarity(cls, value: str) -> int:
        return GI_CHARA_RARITY_MAP[value]

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
