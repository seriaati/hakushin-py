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
    """Represent a character's namecard.

    Attributes:
        id: ID of the namecard.
        name: Name of the namecard.
        description: Description of the namecard.
        icon: Icon URL of the namecard.
    """

    id: int = Field(alias="Id")
    name: str = Field(alias="Name")
    description: str = Field(alias="Desc")
    icon: str = Field(alias="Icon")

    @field_validator("icon", mode="before")
    @classmethod
    def __convert_icon(cls, value: str) -> str:
        return f"https://api.hakush.in/gi/UI/{value}.webp"


class CharacterInfo(APIModel):
    """Represent a character's information.

    Attributes:
        namecard: Character's namecard, if available.
    """

    namecard: Namecard | None = Field(None, alias="Namecard")

    @field_validator("namecard", mode="before")
    @classmethod
    def __handle_empty_namecard(cls, value: dict[str, Any] | None) -> dict[str, Any] | None:
        return value or None


class SkillUpgradeInfo(APIModel):
    """Represent a character's skill upgrade information.

    Attributes:
        level: Level of the skill upgrade.
        icon: Icon URL of the skill upgrade.
        attributes: List of attributes for the skill upgrade.
        parameters: List of parameters for the skill upgrade.
    """

    level: int = Field(alias="Level")
    icon: str = Field(alias="Icon")
    attributes: list[str] = Field(alias="Desc")
    parameters: list[float] = Field(alias="Param")

    @field_validator("icon", mode="before")
    @classmethod
    def __convert_icon(cls, value: str) -> str:
        return f"https://api.hakush.in/gi/UI/{value}.webp"

    @field_validator("attributes", mode="before")
    @classmethod
    def __remove_empty_attributes(cls, value: list[str]) -> list[str]:
        return [attr for attr in value if attr]


class CharacterSkill(APIModel):
    """Represent a character's skill.

    Attributes:
        name: Name of the skill.
        description: Description of the skill.
        upgrade_info: Dictionary of skill upgrade information.
    """

    name: str = Field(alias="Name")
    description: str = Field(alias="Desc")
    upgrade_info: dict[str, SkillUpgradeInfo] = Field(alias="Promote")


class CharacterPassive(APIModel):
    """Represent a character's passive talent.

    Attributes:
        name: Name of the passive talent.
        description: Description of the passive talent.
        unlock: Unlock requirement for the passive talent.
        parameters: List of parameters for the passive talent.
        icon: Icon URL of the passive talent.
    """

    name: str = Field(alias="Name")
    description: str = Field(alias="Desc")
    unlock: int = Field(alias="Unlock")
    parameters: list[float] = Field(alias="ParamList")
    icon: str = Field(alias="Icon")

    @field_validator("icon", mode="before")
    @classmethod
    def __convert_icon(cls, value: str) -> str:
        return f"https://api.hakush.in/gi/UI/{value}.webp"


class CharacterConstellation(APIModel):
    """Represent a character's constellation.

    Attributes:
        name: Name of the constellation.
        description: Description of the constellation.
        parameters: List of parameters for the constellation.
        icon: Icon URL of the constellation.
    """

    name: str = Field(alias="Name")
    description: str = Field(alias="Desc")
    parameters: list[float] = Field(alias="ParamList")
    icon: str = Field(alias="Icon")

    @field_validator("icon", mode="before")
    @classmethod
    def __convert_icon(cls, value: str) -> str:
        return f"https://api.hakush.in/gi/UI/{value}.webp"


class UpgradeMaterial(APIModel):
    """Represent a character's upgrade material.

    Attributes:
        name: Name of the material.
        id: ID of the material.
        count: Count of the material.
        rarity: Rarity of the material.
    """

    name: str = Field(alias="Name")
    id: int = Field(alias="Id")
    count: int = Field(alias="Count")
    rarity: Literal[0, 1, 2, 3, 4, 5] = Field(alias="Rank")

    @property
    def icon(self) -> str:
        """Get the material's icon URL."""
        return f"https://api.hakush.in/gi/UI/UI_ItemIcon_{self.id}.webp"


class UpgradeMaterialInfo(APIModel):
    """Represent character's upgrade material information.

    Attributes:
        materials: List of upgrade materials.
        mora_cost: Mora cost for the upgrade.
    """

    materials: list[UpgradeMaterial] = Field(alias="Mats")
    mora_cost: int = Field(alias="Cost")


class UpgradeMaterialInfos(APIModel):
    """Represent character's upgrade material information.

    Attributes:
        ascensions: List of upgrade material information for ascensions.
        talents: List of lists of upgrade material information for talents.
    """

    ascensions: list[UpgradeMaterialInfo] = Field(alias="Ascensions")
    talents: list[list[UpgradeMaterialInfo]] = Field(alias="Talents")


class FightPropGrowthCurve(APIModel):
    """Represent a character's stat growth curve data.

    Attributes:
        stat_type: Type of the stat.
        growth_type: Type of the growth curve.
    """

    stat_type: str = Field(alias="type")
    growth_type: str = Field(alias="growCurve")


class CharacterStatsModifier(APIModel):
    """Represent a character's stat modifiers.

    Attributes:
        hp: HP stat modifiers.
        atk: ATK stat modifiers.
        def_: DEF stat modifiers.
        ascension: List of ascension stat modifiers.
        prop_growth_curves: List of property growth curves.
    """

    hp: dict[str, float] = Field(alias="HP")
    atk: dict[str, float] = Field(alias="ATK")
    def_: dict[str, float] = Field(alias="DEF")
    ascension: list[dict[str, float]] = Field(alias="Ascension")
    prop_growth_curves: list[FightPropGrowthCurve] = Field(alias="PropGrowCurves")


class CharacterDetail(APIModel):
    """Represent a Genshin Impact character detail.

    Attributes:
        name: Name of the character.
        description: Description of the character.
        info: Character information.
        rarity: Rarity of the character.
        icon: Icon URL of the character.
        skills: List of character skills.
        passives: List of character passive talents.
        constellations: List of character constellations.
        stamina_recovery: Stamina recovery rate of the character.
        base_hp: Base HP of the character.
        base_atk: Base ATK of the character.
        base_def: Base DEF of the character.
        crit_rate: Critical rate of the character.
        crit_dmg: Critical damage of the character.
        stats_modifier: Character stat modifiers.
        upgrade_materials: Character upgrade materials.
    """

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
        """Get the character's gacha art URL."""
        return self.icon.replace("AvatarIcon", "Gacha_AvatarImg")

    @field_validator("icon", mode="before")
    @classmethod
    def __convert_icon(cls, value: str) -> str:
        return f"https://api.hakush.in/gi/UI/{value}.webp"

    @field_validator("rarity", mode="before")
    @classmethod
    def __convert_rarity(cls, value: str) -> Literal[4, 5]:
        return GI_CHARA_RARITY_MAP[value]


class Character(APIModel):
    """Represent a Genshin Impact character.

    Attributes:
        id: ID of the character.
        icon: Icon URL of the character.
        rarity: Rarity of the character.
        description: Description of the character.
        element: Element of the character, if available.
        names: Dictionary of names in different languages.
        name: Name of the character.
    """

    id: str
    icon: str
    rarity: Literal[4, 5] = Field(alias="rank")
    description: str = Field(alias="desc")
    element: GIElement | None = None
    names: dict[Literal["EN", "CHS", "KR", "JP"], str]
    name: str = Field("")

    @field_validator("icon", mode="before")
    @classmethod
    def __convert_icon(cls, value: str) -> str:
        return f"https://api.hakush.in/gi/UI/{value}.webp"

    @field_validator("rarity", mode="before")
    @classmethod
    def __convert_rarity(cls, value: str) -> Literal[4, 5]:
        return GI_CHARA_RARITY_MAP[value]

    @field_validator("element", mode="before")
    @classmethod
    def __convert_element(cls, value: str) -> GIElement | None:
        return GIElement(value) if value else None

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
