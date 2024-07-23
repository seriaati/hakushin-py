from typing import Any, Final, Literal

from pydantic import field_validator, model_validator

from ...enums import ZZZSpecialty
from ..base import APIModel

RARITY_CONVERTER: Final[dict[int, Literal["B", "A", "S"]]] = {2: "B", 3: "A", 4: "S"}


class Weapon(APIModel):
    """ZZZ weapon (w-engine) model."""

    id: int
    icon: str
    name: str
    names: dict[Literal["EN", "JA", "CHS", "KO"], str]
    specialty: ZZZSpecialty
    rarity: Literal["S", "A", "B"]

    @field_validator("rarity", mode="before")
    @classmethod
    def __convert_rarity(cls, value: int | None) -> Literal["S", "A", "B"] | None:
        return RARITY_CONVERTER[value] if value is not None else None

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
