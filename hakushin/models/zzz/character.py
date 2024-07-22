from typing import Any, Final, Literal

from pydantic import Field, field_validator, model_validator

from ...enums import ZZZAttackType, ZZZElement, ZZZSpecialty
from ...utils import cleanup_text
from ..base import APIModel

RARITY_CONVERTER: Final[dict[int, Literal["A", "S"]]] = {3: "A", 4: "S"}


class ZZZCharacter(APIModel):
    """ZZZ character (agent)."""

    name: str = Field(alias="code")
    rarity: Literal["S", "A"] = Field(alias="rank")
    specialty: ZZZSpecialty = Field(alias="type")
    element: ZZZElement
    attack_type: ZZZAttackType = Field(alias="hit")
    icon: str
    en_description: str = Field(alias="desc")
    names: dict[Literal["EN", "KO", "CHS", "JA"], str]

    @field_validator("rarity")
    @classmethod
    def __convert_rarity(cls, value: int) -> Literal["S", "A"]:
        return RARITY_CONVERTER[value]

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
