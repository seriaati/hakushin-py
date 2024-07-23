from typing import Any, Final, Literal

from pydantic import Field, field_validator, model_validator

from ...enums import ZZZAttackType, ZZZElement, ZZZSkillType, ZZZSpecialty
from ...utils import cleanup_text
from ..base import APIModel

RARITY_CONVERTER: Final[dict[int, Literal["A", "S"]]] = {3: "A", 4: "S"}

__all__ = (
    "Character",
    "MindscapeCinema",
    "ZZZAscensionMaterial",
    "ZZZCharaSkillDesc",
    "ZZZCharaSkillDescParam",
    "ZZZCharaSkillDescParamProp",
    "ZZZCharacterAscension",
    "ZZZCharacterDetail",
    "ZZZCharacterExtraAscension",
    "ZZZCharacterInfo",
    "ZZZCharacterPassive",
    "ZZZCharacterPassiveLevel",
    "ZZZCharacterProp",
    "ZZZCharacterSkill",
    "ZZZExtraAscensionProp",
)


class Character(APIModel):
    """ZZZ character (agent)."""

    id: int
    name: str = Field(alias="code")
    rarity: Literal["S", "A"] | None = Field(alias="rank")
    specialty: ZZZSpecialty = Field(alias="type")
    element: ZZZElement | None
    attack_type: ZZZAttackType | None = Field(alias="hit")
    icon: str
    en_description: str = Field(alias="desc")
    names: dict[Literal["EN", "KO", "CHS", "JA"], str]

    @field_validator("rarity", mode="before")
    @classmethod
    def __convert_rarity(cls, value: int | None) -> Literal["S", "A"] | None:
        return RARITY_CONVERTER[value] if value is not None else None

    @field_validator("attack_type", mode="before")
    @classmethod
    def __convert_attack_type(cls, value: int) -> ZZZAttackType | None:
        try:
            return ZZZAttackType(value)
        except ValueError:
            return None

    @field_validator("icon")
    @classmethod
    def __convert_icon(cls, value: str) -> str:
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


class ZZZCharacterProp(APIModel):
    """ZZZ character property."""

    id: int
    name: str

    @model_validator(mode="before")
    @classmethod
    def __transform(cls, values: dict[str, Any]) -> dict[str, Any]:
        first_item = next(iter(values.items()))
        return {"id": first_item[0], "name": first_item[1]}


class ZZZCharacterInfo(APIModel):
    """ZZZ character detail info."""

    birthday: str = Field(alias="Birthday")
    full_name: str = Field(alias="FullName")
    gender: str = Field(alias="Gender")
    female_impression: str = Field(alias="ImpressionF")
    male_impression: str = Field(alias="ImpressionM")
    name: str
    outlook_desc: str = Field(alias="OutlookDesc")
    profile_desc: str = Field(alias="ProfileDesc")
    faction: ZZZCharacterProp = Field(alias="Race")
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


class ZZZAscensionMaterial(APIModel):
    """ZZZ character ascension material."""

    id: int
    amount: int


class ZZZCharacterAscension(APIModel):
    """A ZZZ character ascension object."""

    max_hp: int = Field(alias="HpMax")
    attack: int = Field(alias="Attack")
    defense: int = Field(alias="Defence")
    max_level: int = Field(alias="LevelMax")
    min_level: int = Field(alias="LevelMin")
    materials: list[ZZZAscensionMaterial] = Field(alias="Materials")

    @field_validator("materials")
    @classmethod
    def __convert_materials(cls, value: dict[str, int]) -> list[ZZZAscensionMaterial]:
        return [ZZZAscensionMaterial(id=int(k), amount=v) for k, v in value.items()]


class ZZZExtraAscensionProp(APIModel):
    """ZZZ character extra ascension property."""

    id: int = Field(alias="Prop")
    name: str = Field(alias="Name")
    format: str = Field(alias="Format")
    value: int = Field(alias="Value")


class ZZZCharacterExtraAscension(APIModel):
    """ZZZ character extra ascension object."""

    max_level: int = Field(alias="MaxLevel")
    props: list[ZZZExtraAscensionProp] = Field(alias="Extra")

    @field_validator("props")
    @classmethod
    def __convert_props(cls, value: dict[str, dict[str, Any]]) -> list[ZZZExtraAscensionProp]:
        return [ZZZExtraAscensionProp(**data) for data in value.values()]


class ZZZCharaSkillDescParamProp(APIModel):
    """ZZZ character skill description parameter property."""

    main: int = Field(alias="Main")
    growth: int = Field(alias="Growth")
    format: str


class ZZZCharaSkillDescParam(APIModel):
    """ZZZ character skill description parameter."""

    name: str = Field(alias="Name")
    description: str = Field(alias="Desc")
    params: dict[str, ZZZCharaSkillDescParamProp] = Field(alias="Param")


class ZZZCharaSkillDesc(APIModel):
    """ZZZ character skill description."""

    name: str = Field(alias="Name")
    description: str | None = Field(None, alias="Desc")
    params: list[ZZZCharaSkillDescParam] = Field(alias="Param")


class ZZZCharacterSkill(APIModel):
    """ZZZ character skill."""

    descriptions: list[ZZZCharaSkillDesc] = Field(alias="Description")
    materials: list[ZZZAscensionMaterial] = Field(alias="Material")
    type: ZZZSkillType = Field(alias="Type")

    @field_validator("materials")
    @classmethod
    def __convert_materials(cls, value: dict[str, int]) -> list[ZZZAscensionMaterial]:
        return [ZZZAscensionMaterial(id=int(k), amount=v) for k, v in value.items()]


class ZZZCharacterPassiveLevel(APIModel):
    """One level of a ZZZ character passive skill."""

    level: int = Field(alias="Level")
    id: int = Field(alias="Id")
    names: list[str] = Field(alias="Name")
    descriptions: list[str] = Field(alias="Desc")

    @field_validator("descriptions")
    @classmethod
    def __cleanup_text(cls, value: list[str]) -> list[str]:
        return [cleanup_text(v) for v in value]


class ZZZCharacterPassive(APIModel):
    """ZZZ character passive skill."""

    levels: dict[int, ZZZCharacterPassiveLevel] = Field(alias="Level")
    """Key is the level of the passive skill."""
    level_up_materials: dict[str, list[ZZZAscensionMaterial]] = Field(alias="Material")

    @field_validator("level_up_materials")
    @classmethod
    def __convert_materials(
        cls, value: dict[str, dict[str, int]]
    ) -> dict[str, list[ZZZAscensionMaterial]]:
        return {
            k: [ZZZAscensionMaterial(id=int(k), amount=v) for k, v in data.items()]
            for k, data in value.items()
        }

    @field_validator("levels")
    @classmethod
    def __intify_keys(cls, value: dict[str, dict[str, Any]]) -> dict[int, ZZZCharacterPassiveLevel]:
        return {int(k): ZZZCharacterPassiveLevel(**v) for k, v in value.items()}


class ZZZCharacterDetail(APIModel):
    """ZZZ character detail."""

    id: int = Field(alias="Id")
    icon: str = Field(alias="Icon")
    name: str = Field(alias="Name")
    code_name: str = Field(alias="CodeName")
    rarity: Literal["S", "A"] = Field(alias="Rank")
    specialty: ZZZCharacterProp = Field(alias="WeaponType")
    element: ZZZCharacterProp = Field(alias="Element")
    attack_type: ZZZCharacterProp = Field(alias="HitType")
    faction: ZZZCharacterProp = Field(alias="Camp")
    gender: Literal["M", "F"]
    info: ZZZCharacterInfo = Field(alias="PartnerInfo")
    stats: dict[str, float] = Field(alias="Stats")
    mindscape_cinemas: list[MindscapeCinema] = Field(alias="Talent")
    ascension: list[ZZZCharacterAscension] = Field(alias="Level")
    extra_ascension: list[ZZZCharacterExtraAscension] = Field(alias="ExtraLevel")
    skills: dict[ZZZSkillType, ZZZCharacterSkill] = Field(alias="Skill")
    passive: ZZZCharacterPassive = Field(alias="Passive")

    @field_validator("skills")
    @classmethod
    def __convert_skills(
        cls, value: dict[str, dict[str, Any]]
    ) -> dict[ZZZSkillType, ZZZCharacterSkill]:
        return {
            ZZZSkillType(k): ZZZCharacterSkill(Type=ZZZSkillType(k), **v) for k, v in value.items()
        }

    @field_validator("extra_ascension")
    @classmethod
    def __convert_extra_ascension(
        cls, value: dict[str, dict[str, Any]]
    ) -> list[ZZZCharacterExtraAscension]:
        return [ZZZCharacterExtraAscension(**data) for data in value.values()]

    @field_validator("ascension")
    @classmethod
    def __convert_ascension(cls, value: dict[str, dict[str, Any]]) -> list[ZZZCharacterAscension]:
        return [ZZZCharacterAscension(**data) for data in value.values()]

    @field_validator("mindscape_cinemas")
    @classmethod
    def __dict_to_list(cls, value: dict[str, dict[str, Any]]) -> list[MindscapeCinema]:
        return [MindscapeCinema(**data) for data in value.values()]

    @field_validator("stats")
    @classmethod
    def __pop_tags(cls, value: dict[str, Any]) -> dict[str, float]:
        value.pop("Tags")
        return value

    @field_validator("gender")
    @classmethod
    def __transform_gender(cls, value: int) -> Literal["M", "F"]:
        # Hope I don't get cancelled for this.
        # Female is '2' btw.
        return "M" if value == 1 else "F"

    @field_validator("rarity")
    @classmethod
    def __convert_rarity(cls, value: int) -> Literal["S", "A"]:
        return RARITY_CONVERTER[value]

    @field_validator("icon")
    @classmethod
    def __convert_icon(cls, value: str) -> str:
        return f"https://api.hakush.in/zzz/UI/{value}.webp"
