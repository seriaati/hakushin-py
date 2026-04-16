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


class PotentialMaterial(APIModel):
    """Represent a material required for character potential upgrades.

    Attributes:
        id: ID of the material.
        number: Quantity of the material needed? Or maybe it's just a number...
    """

    id: int = Field(alias="item_id")
    number: int


class CharacterPotential(APIModel):
    """Represent a character potential upgrade in Zenless Zone Zero.

    Attributes:
        id: Unique potential identifier.
        name: Potential upgrade name.
        short_name: Short display name for the potential.
        description: Description of the potential's effect.
        image: Image URL representing the potential.
        level: Level of the potential upgrade.
        affected_skills: List of skill IDs affected by this potential.
        materials: List of materials required to unlock or upgrade this potential.
    """

    id: int
    name: str
    short_name: str = Field(alias="level_show_name")
    description: str = Field(alias="desc")
    image: str
    level: int
    affected_skills: list[int] = Field(alias="ability_list")
    materials: list[PotentialMaterial] = Field(alias="potential_materials")

    @field_validator("image", mode="after")
    @classmethod
    def __convert_image(cls, value: str) -> str:
        return f"https://static.nanoka.cc/zzz/UI/AvatarSpecialAwakenBg_{value}.webp"


class CharacterSkin(APIModel):
    """Represent a character skin in Zenless Zone Zero.

    Contains information about character skins including IDs, names,
    and image URLs.

    Attributes:
        id: Unique skin identifier.
        name: Skin name.
        description: Skin description.
        image: Skin image URL.
    """

    id: int
    name: str
    description: str = Field(alias="desc")
    image: str

    @field_validator("image")
    @classmethod
    def __convert_image(cls, value: str) -> str:
        return f"https://static.nanoka.cc/zzz/UI/{value}.webp"


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
    names: dict[Literal["en", "ko", "zh", "ja"], str]
    skins: list[CharacterSkin] = Field(alias="skin", default_factory=list)

    @computed_field
    @property
    def phase_3_cinema_art(self) -> str:
        """Agent phase 3 mindscape cinema art.

        Example: https://static.nanoka.cc/zzz/UI/Mindscape_1041_3.webp
        """
        return f"https://static.nanoka.cc/zzz/UI/Mindscape_{self.id}_3.webp"

    @computed_field
    @property
    def phase_2_cinema_art(self) -> str:
        """Agent phase 2 mindscape cinema art.

        Example: https://static.nanoka.cc/zzz/UI/Mindscape_1041_2.webp
        """
        return f"https://static.nanoka.cc/zzz/UI/Mindscape_{self.id}_2.webp"

    @computed_field
    @property
    def phase_1_cinema_art(self) -> str:
        """Agent phase 1 mindscape cinema art.

        Example: https://static.nanoka.cc/zzz/UI/Mindscape_1041_1.webp
        """
        return f"https://static.nanoka.cc/zzz/UI/Mindscape_{self.id}_1.webp"

    @computed_field
    @property
    def icon(self) -> str:
        """Agent icon.

        Example: https://static.nanoka.cc/zzz/UI/IconRoleSelect01.webp
        """
        return self.image.replace("Role", "RoleSelect")

    @computed_field
    @property
    def cropped_icon(self) -> str:
        """Agent cropped icon.

        Example: https://static.nanoka.cc/zzz/UI/IconRoleCrop01.webp
        """
        return self.image.replace("Role", "RoleCrop")

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
        return f"https://static.nanoka.cc/zzz/UI/{value}.webp"

    @model_validator(mode="before")
    @classmethod
    def __pop_names(cls, values: dict[str, Any]) -> dict[str, Any]:
        values["names"] = {
            "en": values.pop("en"),
            "ko": values.pop("ko"),
            "zh": values.pop("zh"),
            "ja": values.pop("ja"),
        }
        return values

    @field_validator("skins", mode="before")
    @classmethod
    def __convert_skins(cls, value: dict[str, dict[str, Any]]) -> list[CharacterSkin]:
        return [CharacterSkin(id=int(k), **v) for k, v in value.items()]


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

    birthday: str
    full_name: str
    gender: str
    female_impression: str = Field(alias="impression_f")
    male_impression: str = Field(alias="impression_m")
    outlook_desc: str | None = None
    profile_desc: str
    faction: str | None = Field(alias="race", default=None)
    unlock_conditions: list[str] = Field(alias="unlock_condition")

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

    level: int
    name: str
    description: str = Field(alias="desc")
    description2: str = Field(alias="desc2")

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

    max_hp: int = Field(alias="hp_max")
    attack: int
    defense: int = Field(alias="defence")
    max_level: int = Field(alias="level_max")
    min_level: int = Field(alias="level_min")
    materials: list[ZZZMaterial]

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

    max_level: int = Field(alias="max_level")
    props: list[ZZZExtraProp] = Field(alias="extra")

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

    main: int
    growth: int
    format: str


class CharaSkillDescParam(APIModel):
    """Represent a skill description parameter.

    Contains parameter information for skill descriptions including
    names, descriptions, and numerical properties.

    Attributes:
        name: Parameter name.
        description: Parameter description.
        params: Dictionary of parameter properties.
    """

    name: str
    description: str = Field(alias="desc")
    params: dict[str, CharaSkillDescParamProp] | None = Field(None, alias="param")


class CharacterSkillDesc(APIModel):
    """Represent a character skill description entry.

    Contains detailed information about specific skill effects
    including names, descriptions, and parameters.

    Attributes:
        name: Skill description name.
        description: Skill effect description.
        params: List of skill parameters.
    """

    name: str
    description: str | None = Field(None, alias="desc")
    params: list[CharaSkillDescParam] | None = Field(None, alias="param")


class CharacterSkill(APIModel):
    """Represent a character skill with upgrade information.

    Contains complete skill data including descriptions, upgrade materials,
    and skill type classification.

    Attributes:
        descriptions: List of skill effect descriptions.
        materials: Required materials for skill upgrades by level.
        type: Skill type classification.
    """

    descriptions: list[CharacterSkillDesc] = Field(alias="description")
    materials: dict[str, list[ZZZMaterial]] = Field(alias="material")
    type: ZZZSkillType

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

    level: int
    id: int
    names: list[str] = Field(alias="name")
    descriptions: list[str] = Field(alias="desc")

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

    levels: dict[int, CharaCoreSkillLevel] = Field(alias="level")
    level_up_materials: dict[str, list[ZZZMaterial]] | None = Field(None, alias="materials")

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
        return {
            int(v.get("level") or v.get("Level") or 0): CharaCoreSkillLevel(**v)
            for v in value.values()
        }


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

    id: int
    image: str = Field(alias="icon")
    name: str
    code_name: str
    rarity: Literal["S", "A"] | None
    specialty: CharacterProp = Field(alias="weapon_type")
    element: CharacterProp = Field(alias="element_type")
    attack_type: CharacterProp = Field(alias="hit_type")
    faction: CharacterProp = Field(alias="camp")
    gender: Literal["M", "F"]
    info: CharacterInfo | None = Field(alias="partner_info")
    stats: dict[str, float]
    mindscape_cinemas: list[MindscapeCinema] = Field(alias="talent")
    ascension: list[CharacterAscension] = Field(alias="level")
    extra_ascension: list[CharacterExtraAscension] = Field(alias="extra_level")
    skills: dict[ZZZSkillType, CharacterSkill] = Field(alias="skill")
    passive: CharacterCoreSkill
    skins: list[CharacterSkin] = Field(alias="skin", default_factory=list)
    potentials: list[CharacterPotential] = Field(alias="potential_detail", default_factory=list)

    @computed_field
    @property
    def phase_3_cinema_art(self) -> str:
        """Agent phase 3 mindscape cinema art.

        Example: https://static.nanoka.cc/zzz/UI/Mindscape_1041_3.webp
        """
        return f"https://static.nanoka.cc/zzz/UI/Mindscape_{self.id}_3.webp"

    @computed_field
    @property
    def phase_2_cinema_art(self) -> str:
        """Agent phase 2 mindscape cinema art.

        Example: https://static.nanoka.cc/zzz/UI/Mindscape_1041_2.webp
        """
        return f"https://static.nanoka.cc/zzz/UI/Mindscape_{self.id}_2.webp"

    @computed_field
    @property
    def phase_1_cinema_art(self) -> str:
        """Agent phase 1 mindscape cinema art.

        Example: https://static.nanoka.cc/zzz/UI/Mindscape_1041_1.webp
        """
        return f"https://static.nanoka.cc/zzz/UI/Mindscape_{self.id}_1.webp"

    @computed_field
    @property
    def icon(self) -> str:
        """Character icon.

        Example: https://static.nanoka.cc/zzz/UI/IconRoleSelect01.webp
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
            ZZZSkillType(k): CharacterSkill(type=ZZZSkillType(k), **v) for k, v in value.items()
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
        value.pop("tags", None)
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
        return f"https://static.nanoka.cc/zzz/UI/{value}.webp"

    @field_validator("skins", mode="before")
    @classmethod
    def __convert_skins(cls, value: dict[str, dict[str, Any]]) -> list[CharacterSkin]:
        return [CharacterSkin(id=int(k), **v) for k, v in value.items()]

    @field_validator("potentials", mode="before")
    @classmethod
    def __flatten_potentials(cls, value: dict[str, dict[str, Any]]) -> list[CharacterPotential]:
        return [CharacterPotential(**data) for data in value.values()]
