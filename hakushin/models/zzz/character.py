from __future__ import annotations

from typing import Any, Literal

from pydantic import Field, computed_field, field_validator, model_validator

from ...constants import ZZZ_SA_RARITY_CONVERTER
from ...enums import ZZZAttackType, ZZZElement, ZZZSkillType, ZZZSpecialty
from ...utils import cleanup_text
from ..base import APIModel
from .common import ZZZExtraProp, ZZZMaterial

__all__ = (
    "CharaCoreSkillLevel",
    "CharaSkillDescParam",
    "CharaSkillDescParamProp",
    "Character",
    "CharacterAscension",
    "CharacterCoreSkill",
    "CharacterDetail",
    "CharacterExtraAscension",
    "CharacterInfo",
    "CharacterProp",
    "CharacterSkill",
    "CharacterSkillDesc",
    "MindscapeCinema",
)


class Character(APIModel):
    """Represent a Zenless Zone Zero character (agent).

    Contains basic character information including stats, element, specialty,
    and visual assets. Agents are the playable characters in ZZZ.

    Attributes:
        id: Unique character identifier.
        name: Character name/code.
        rarity: Character rarity rank (S or A).
        specialty: Character specialty type.
        element: Elemental attribute of the character.
        attack_type: Combat attack type.
        image: Character portrait image URL.
        en_description: English description text.
        names: Character names in different languages.
    """

    id: int
    name: str = Field(alias="code")
    rarity: Literal["S", "A"] | None = Field(alias="rank")
    specialty: ZZZSpecialty = Field(alias="type")
    element: ZZZElement | None = None
    attack_type: ZZZAttackType | None = Field(None, alias="hit")
    image: str = Field(alias="icon")
    en_description: str = Field(alias="desc")
    names: dict[Literal["EN", "KO", "CHS", "JA"], str]

    @computed_field
    @property
    def phase_3_cinema_art(self) -> str:
        """Agent phase 3 mindscape cinema art.

        Example: https://api.hakush.in/zzz/UI/Mindscape_1041_3.webp
        """
        return f"https://api.hakush.in/zzz/UI/Mindscape_{self.id}_3.webp"

    @computed_field
    @property
    def phase_2_cinema_art(self) -> str:
        """Agent phase 2 mindscape cinema art.

        Example: https://api.hakush.in/zzz/UI/Mindscape_1041_2.webp
        """
        return f"https://api.hakush.in/zzz/UI/Mindscape_{self.id}_2.webp"

    @computed_field
    @property
    def phase_1_cinema_art(self) -> str:
        """Agent phase 1 mindscape cinema art.

        Example: https://api.hakush.in/zzz/UI/Mindscape_1041_1.webp
        """
        return f"https://api.hakush.in/zzz/UI/Mindscape_{self.id}_1.webp"

    @computed_field
    @property
    def icon(self) -> str:
        """Agent icon.

        Example: https://api.hakush.in/zzz/UI/IconRoleSelect01.webp
        """
        return self.image.replace("Role", "RoleSelect")

    @field_validator("rarity", mode="before")
    @classmethod
    def __convert_rarity(cls, value: int | None) -> Literal["S", "A"] | None:
        return ZZZ_SA_RARITY_CONVERTER[value] if value is not None else None

    @field_validator("attack_type", mode="before")
    @classmethod
    def __convert_attack_type(cls, value: int) -> ZZZAttackType | None:
        try:
            return ZZZAttackType(value)
        except ValueError:
            return None

    @field_validator("image")
    @classmethod
    def __convert_image(cls, value: str) -> str:
        return f"https://api.hakush.in/zzz/UI/{value}.webp"

    @model_validator(mode="before")
    @classmethod
    def __pop_names(cls, values: dict[str, Any]) -> dict[str, Any]:
        values["names"] = {
            "EN": values.pop("EN"),
            "KO": values.pop("KO"),
            "CHS": values.pop("CHS"),
            "JA": values.pop("JA"),
        }
        return values


class CharacterProp(APIModel):
    """Represent a character property in Zenless Zone Zero.

    Properties include elements, weapon types, attack types, and other
    character attributes that are referenced by ID and name.

    Attributes:
        id: Unique property identifier.
        name: Human-readable property name.
    """

    id: int
    name: str

    @model_validator(mode="before")
    @classmethod
    def __transform(cls, values: dict[str, Any] | Literal[0]) -> dict[str, Any]:
        if values == 0:
            return {"id": 0, "name": "Unknown"}
        first_item = next(iter(values.items()))
        return {"id": first_item[0], "name": first_item[1]}


class CharacterInfo(APIModel):
    """Contain detailed character lore and background information.

    Provides extensive character details including personal information,
    impressions, descriptions, and unlock requirements.

    Attributes:
        birthday: Character birth date.
        full_name: Character's complete name.
        gender: Character gender.
        female_impression: Female player impression text.
        male_impression: Male player impression text.
        outlook_desc: Character outlook description.
        profile_desc: Character profile description.
        faction: Character faction or group.
        unlock_conditions: List of conditions to unlock the character.
    """

    birthday: str = Field(alias="Birthday")
    full_name: str = Field(alias="FullName")
    gender: str = Field(alias="Gender")
    female_impression: str = Field(alias="ImpressionF")
    male_impression: str = Field(alias="ImpressionM")
    outlook_desc: str = Field(alias="OutlookDesc")
    profile_desc: str = Field(alias="ProfileDesc")
    faction: str = Field(alias="Race")
    unlock_conditions: list[str] = Field(alias="UnlockCondition")

    @field_validator("female_impression", "male_impression", "outlook_desc", "profile_desc")
    @classmethod
    def __cleanup_text(cls, value: str) -> str:
        return cleanup_text(value)


class MindscapeCinema(APIModel):
    """Represent a character mindscape cinema level (constellation equivalent).

    Mindscape cinemas are upgrades that enhance character abilities
    and provide new effects when unlocked.

    Attributes:
        level: Cinema level (1-6).
        name: Cinema ability name.
        description: Primary effect description.
        description2: Secondary effect description.
    """

    level: int = Field(alias="Level")
    name: str = Field(alias="Name")
    description: str = Field(alias="Desc")
    description2: str = Field(alias="Desc2")

    @field_validator("description", "description2")
    @classmethod
    def __cleanup_text(cls, value: str) -> str:
        return cleanup_text(value)


class CharacterAscension(APIModel):
    """Represent character ascension phase data.

    Contains stat bonuses and material requirements for each
    character ascension phase.

    Attributes:
        max_hp: Maximum HP bonus at this phase.
        attack: Attack stat bonus.
        defense: Defense stat bonus.
        max_level: Maximum level achievable in this phase.
        min_level: Minimum level for this phase.
        materials: Required materials for ascension.
    """

    max_hp: int = Field(alias="HpMax")
    attack: int = Field(alias="Attack")
    defense: int = Field(alias="Defence")
    max_level: int = Field(alias="LevelMax")
    min_level: int = Field(alias="LevelMin")
    materials: list[ZZZMaterial] = Field(alias="Materials")

    @field_validator("materials", mode="before")
    @classmethod
    def __convert_materials(cls, value: dict[str, int]) -> list[ZZZMaterial]:
        return [ZZZMaterial(id=int(k), amount=v) for k, v in value.items()]


class CharacterExtraAscension(APIModel):
    """Represent character bonus ascension data.

    Contains additional ascension bonuses and properties that are
    granted beyond the standard ascension phases.

    Attributes:
        max_level: Maximum level for this bonus phase.
        props: Additional properties and bonuses gained.
    """

    max_level: int = Field(alias="MaxLevel")
    props: list[ZZZExtraProp] = Field(alias="Extra")

    @field_validator("props", mode="before")
    @classmethod
    def __convert_props(cls, value: dict[str, dict[str, Any]]) -> list[ZZZExtraProp]:
        return [ZZZExtraProp(**data) for data in value.values()]


class CharaSkillDescParamProp(APIModel):
    """Represent skill description parameter properties.

    Contains numerical properties for skill parameter calculations
    including base values, growth rates, and formatting.

    Attributes:
        main: Base parameter value.
        growth: Growth rate per level.
        format: Display formatting specification.
    """

    main: int = Field(alias="Main")
    growth: int = Field(alias="Growth")
    format: str = Field(alias="Format")


class CharaSkillDescParam(APIModel):
    """Represent a skill description parameter.

    Contains parameter information for skill descriptions including
    names, descriptions, and numerical properties.

    Attributes:
        name: Parameter name.
        description: Parameter description.
        params: Dictionary of parameter properties.
    """

    name: str = Field(alias="Name")
    description: str = Field(alias="Desc")
    params: dict[str, CharaSkillDescParamProp] | None = Field(None, alias="Param")


class CharacterSkillDesc(APIModel):
    """Represent a character skill description entry.

    Contains detailed information about specific skill effects
    including names, descriptions, and parameters.

    Attributes:
        name: Skill description name.
        description: Skill effect description.
        params: List of skill parameters.
    """

    name: str = Field(alias="Name")
    description: str | None = Field(None, alias="Desc")
    params: list[CharaSkillDescParam] | None = Field(None, alias="Param")


class CharacterSkill(APIModel):
    """Represent a character skill with upgrade information.

    Contains complete skill data including descriptions, upgrade materials,
    and skill type classification.

    Attributes:
        descriptions: List of skill effect descriptions.
        materials: Required materials for skill upgrades by level.
        type: Skill type classification.
    """

    descriptions: list[CharacterSkillDesc] = Field(alias="Description")
    materials: dict[str, list[ZZZMaterial]] = Field(alias="Material")
    type: ZZZSkillType = Field(alias="Type")

    @field_validator("materials", mode="before")
    @classmethod
    def __convert_materials(cls, value: dict[str, dict[str, int]]) -> dict[str, list[ZZZMaterial]]:
        return {
            k: [ZZZMaterial(id=int(k), amount=v) for k, v in data.items()]
            for k, data in value.items()
        }


class CharaCoreSkillLevel(APIModel):
    """Represent a single level of a character core skill.

    Core skills are passive abilities that can be upgraded to provide
    enhanced effects and bonuses.

    Attributes:
        level: Core skill level.
        id: Unique core skill identifier.
        names: Skill names in different contexts.
        descriptions: Skill effect descriptions.
    """

    level: int = Field(alias="Level")
    id: int = Field(alias="Id")
    names: list[str] = Field(alias="Name")
    descriptions: list[str] = Field(alias="Desc")

    @field_validator("descriptions")
    @classmethod
    def __cleanup_text(cls, value: list[str]) -> list[str]:
        return [cleanup_text(v) for v in value]


class CharacterCoreSkill(APIModel):
    """Represent a character's core skill progression system.

    Core skills are passive abilities that provide ongoing benefits
    and can be upgraded through multiple levels.

    Attributes:
        levels: Core skill levels mapped by level number.
        level_up_materials: Materials required for each upgrade level.
    """

    levels: dict[int, CharaCoreSkillLevel] = Field(alias="Level")
    level_up_materials: dict[str, list[ZZZMaterial]] | None = Field(None, alias="Materials")

    @field_validator("level_up_materials", mode="before")
    @classmethod
    def __convert_materials(cls, value: dict[str, dict[str, int]]) -> dict[str, list[ZZZMaterial]]:
        return {
            k: [ZZZMaterial(id=int(k), amount=v) for k, v in data.items()]
            for k, data in value.items()
        }

    @field_validator("levels", mode="before")
    @classmethod
    def __intify_keys(cls, value: dict[str, dict[str, Any]]) -> dict[int, CharaCoreSkillLevel]:
        return {v["Level"]: CharaCoreSkillLevel(**v) for v in value.values()}


class CharacterDetail(APIModel):
    """Provide comprehensive character information and progression data.

    Contains complete character details including stats, skills, ascension data,
    mindscape cinemas, and all progression information for a ZZZ agent.

    Attributes:
        id: Unique character identifier.
        image: Character portrait image URL.
        name: Character display name.
        code_name: Character code designation.
        rarity: Character rarity rank (S or A).
        specialty: Character weapon specialty.
        element: Character elemental attribute.
        attack_type: Character combat attack type.
        faction: Character faction or camp.
        gender: Character gender (M or F).
        info: Detailed character background information.
        stats: Base character statistics.
        mindscape_cinemas: Character mindscape cinema upgrades.
        ascension: Character ascension phase data.
        extra_ascension: Additional ascension bonuses.
        skills: Character skills by type.
        passive: Character core passive skill.
    """

    id: int = Field(alias="Id")
    image: str = Field(alias="Icon")
    name: str = Field(alias="Name")
    code_name: str = Field(alias="CodeName")
    rarity: Literal["S", "A"] | None = Field(alias="Rarity")
    specialty: CharacterProp = Field(alias="WeaponType")
    element: CharacterProp = Field(alias="ElementType")
    attack_type: CharacterProp = Field(alias="HitType")
    faction: CharacterProp = Field(alias="Camp")
    gender: Literal["M", "F"] = Field(alias="Gender")
    info: CharacterInfo | None = Field(alias="PartnerInfo")
    stats: dict[str, float] = Field(alias="Stats")
    mindscape_cinemas: list[MindscapeCinema] = Field(alias="Talent")
    ascension: list[CharacterAscension] = Field(alias="Level")
    extra_ascension: list[CharacterExtraAscension] = Field(alias="ExtraLevel")
    skills: dict[ZZZSkillType, CharacterSkill] = Field(alias="Skill")
    passive: CharacterCoreSkill = Field(alias="Passive")

    @computed_field
    @property
    def phase_3_cinema_art(self) -> str:
        """Agent phase 3 mindscape cinema art.

        Example: https://api.hakush.in/zzz/UI/Mindscape_1041_3.webp
        """
        return f"https://api.hakush.in/zzz/UI/Mindscape_{self.id}_3.webp"

    @computed_field
    @property
    def phase_2_cinema_art(self) -> str:
        """Agent phase 2 mindscape cinema art.

        Example: https://api.hakush.in/zzz/UI/Mindscape_1041_2.webp
        """
        return f"https://api.hakush.in/zzz/UI/Mindscape_{self.id}_2.webp"

    @computed_field
    @property
    def phase_1_cinema_art(self) -> str:
        """Agent phase 1 mindscape cinema art.

        Example: https://api.hakush.in/zzz/UI/Mindscape_1041_1.webp
        """
        return f"https://api.hakush.in/zzz/UI/Mindscape_{self.id}_1.webp"

    @computed_field
    @property
    def icon(self) -> str:
        """Character icon.

        Example: https://api.hakush.in/zzz/UI/IconRoleSelect01.webp
        """
        return self.image.replace("Role", "RoleSelect")

    @field_validator("info", mode="before")
    @classmethod
    def __convert_info(cls, value: dict[str, Any]) -> CharacterInfo | None:
        return None if not value else CharacterInfo(**value)

    @field_validator("skills", mode="before")
    @classmethod
    def __convert_skills(
        cls, value: dict[str, dict[str, Any]]
    ) -> dict[ZZZSkillType, CharacterSkill]:
        return {
            ZZZSkillType(k): CharacterSkill(Type=ZZZSkillType(k), **v) for k, v in value.items()
        }

    @field_validator("extra_ascension", mode="before")
    @classmethod
    def __convert_extra_ascension(
        cls, value: dict[str, dict[str, Any]]
    ) -> list[CharacterExtraAscension]:
        return [CharacterExtraAscension(**data) for data in value.values()]

    @field_validator("ascension", mode="before")
    @classmethod
    def __convert_ascension(cls, value: dict[str, dict[str, Any]]) -> list[CharacterAscension]:
        return [CharacterAscension(**data) for data in value.values()]

    @field_validator("mindscape_cinemas", mode="before")
    @classmethod
    def __dict_to_list(cls, value: dict[str, dict[str, Any]]) -> list[MindscapeCinema]:
        return [MindscapeCinema(**data) for data in value.values()]

    @field_validator("stats", mode="before")
    @classmethod
    def __pop_tags(cls, value: dict[str, Any]) -> dict[str, float]:
        value.pop("Tags", None)
        return value

    @field_validator("gender", mode="before")
    @classmethod
    def __transform_gender(cls, value: int) -> Literal["M", "F"]:
        # Hope I don't get cancelled for this.
        # Female is '2' btw.
        return "M" if value == 1 else "F"

    @field_validator("rarity", mode="before")
    @classmethod
    def __convert_rarity(cls, value: int | None) -> Literal["S", "A"] | None:
        return ZZZ_SA_RARITY_CONVERTER[value] if value is not None else None

    @field_validator("image")
    @classmethod
    def __convert_image(cls, value: str) -> str:
        return f"https://api.hakush.in/zzz/UI/{value}.webp"
