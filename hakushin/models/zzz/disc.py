from __future__ import annotations

from pydantic import Field, field_validator

from ..base import APIModel

__all__ = ("DriveDisc", "DriveDiscDetail", "DriveDiscInfo")


class DriveDiscInfo(APIModel):
    """Represent drive disc information in a specific language.

    Contains localized drive disc name and set bonus descriptions
    for 2-piece and 4-piece effects.

    Attributes:
        name: Drive disc set name.
        two_piece_effect: Effect when 2 pieces are equipped.
        four_piece_effect: Effect when 4 pieces are equipped.
    """

    name: str
    two_piece_effect: str = Field(alias="desc2")
    four_piece_effect: str = Field(alias="desc4")


class DriveDisc(APIModel):
    """Represent a Zenless Zone Zero drive disc set.

    Drive discs are equipment sets that provide bonuses when multiple
    pieces are equipped. Contains basic info and localized descriptions.

    Attributes:
        id: Unique drive disc set identifier.
        icon: Drive disc icon image URL.
        name: Set name (may be empty if not in API response).
        two_piece_effect: 2-piece effect description (may be empty).
        four_piece_effect: 4-piece effect description (may be empty).
        en_info: English localization data.
        ko_info: Korean localization data.
        chs_info: Chinese Simplified localization data.
        ja_info: Japanese localization data.
    """

    id: int
    icon: str
    name: str = Field("")  # This field doesn't exist in the API response
    two_piece_effect: str = Field("")  # Same here
    four_piece_effect: str = Field("")  # Same here

    en_info: DriveDiscInfo | None = Field(None, alias="EN")
    ko_info: DriveDiscInfo | None = Field(None, alias="KO")
    chs_info: DriveDiscInfo = Field(alias="CHS")
    ja_info: DriveDiscInfo | None = Field(None, alias="JA")

    @field_validator("icon")
    @classmethod
    def __convert_icon(cls, icon: str) -> str:
        filename = icon.rsplit("/", maxsplit=1)[-1].split(".", maxsplit=1)[0]
        return f"https://api.hakush.in/zzz/UI/{filename}.webp"


class DriveDiscDetail(APIModel):
    """Provide comprehensive drive disc set information.

    Contains complete drive disc data including set bonuses, lore,
    and visual assets for a specific drive disc set.

    Attributes:
        id: Unique drive disc set identifier.
        name: Drive disc set name.
        two_piece_effect: Effect when 2 pieces are equipped.
        four_piece_effect: Effect when 4 pieces are equipped.
        story: Background lore and story text.
        icon: Drive disc icon image URL.
    """

    id: int = Field(alias="Id")
    name: str = Field(alias="Name")
    two_piece_effect: str = Field(alias="Desc2")
    four_piece_effect: str = Field(alias="Desc4")
    story: str = Field(alias="Story")
    icon: str = Field(alias="Icon")

    @field_validator("icon")
    @classmethod
    def __convert_icon(cls, icon: str) -> str:
        filename = icon.rsplit("/", maxsplit=1)[-1].split(".", maxsplit=1)[0]
        return f"https://api.hakush.in/zzz/UI/{filename}.webp"
