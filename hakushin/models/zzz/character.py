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
    """ZZZ character (agent)."""

    id: int
    name: str = Field(alias="code")
    rarity: Literal["S", "A"] | None = Field(alias="rank")
    specialty: ZZZSpecialty = Field(alias="type")
    element: ZZZElement | None
    attack_type: ZZZAttackType | None = Field(alias="hit")
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
    """ZZZ character property."""

    id: int
    name: str

    @model_validator(mode="before")
    @classmethod
    def __transform(cls, values: dict[str, Any]) -> dict[str, Any]:
        first_item = next(iter(values.items()))
        return {"id": first_item[0], "name": first_item[1]}


class CharacterInfo(APIModel):
    """ZZZ character detail info."""

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
    """ZZZ character mindscape cinema (constellation)."""

    level: int = Field(alias="Level")
    name: str = Field(alias="Name")
    description: str = Field(alias="Desc")
    description2: str = Field(alias="Desc2")

    @field_validator("description", "description2")
    @classmethod
    def __cleanup_text(cls, value: str) -> str:
        return cleanup_text(value)


class CharacterAscension(APIModel):
    """A ZZZ character ascension object."""

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
    """ZZZ character extra ascension object."""

    max_level: int = Field(alias="MaxLevel")
    props: list[ZZZExtraProp] = Field(alias="Extra")

    @field_validator("props", mode="before")
    @classmethod
    def __convert_props(cls, value: dict[str, dict[str, Any]]) -> list[ZZZExtraProp]:
        return [ZZZExtraProp(**data) for data in value.values()]


class CharaSkillDescParamProp(APIModel):
    """ZZZ character skill description parameter property."""

    main: int = Field(alias="Main")
    growth: int = Field(alias="Growth")
    format: str = Field(alias="Format")


class CharaSkillDescParam(APIModel):
    """ZZZ character skill description parameter."""

    name: str = Field(alias="Name")
    description: str = Field(alias="Desc")
    params: dict[str, CharaSkillDescParamProp] | None = Field(None, alias="Param")


class CharacterSkillDesc(APIModel):
    """ZZZ character skill description."""

    name: str = Field(alias="Name")
    description: str | None = Field(None, alias="Desc")
    params: list[CharaSkillDescParam] | None = Field(None, alias="Param")


class CharacterSkill(APIModel):
    """ZZZ character skill."""

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
    """One level of a ZZZ character core skill."""

    level: int = Field(alias="Level")
    id: int = Field(alias="Id")
    names: list[str] = Field(alias="Name")
    descriptions: list[str] = Field(alias="Desc")

    @field_validator("descriptions")
    @classmethod
    def __cleanup_text(cls, value: list[str]) -> list[str]:
        return [cleanup_text(v) for v in value]


class CharacterCoreSkill(APIModel):
    """ZZZ character core skill."""

    levels: dict[int, CharaCoreSkillLevel] = Field(alias="Level")
    """Key is the level of the core skill."""
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
        return {int(k): CharaCoreSkillLevel(**v) for k, v in value.items()}


class CharacterDetail(APIModel):
    """ZZZ character detail."""

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
