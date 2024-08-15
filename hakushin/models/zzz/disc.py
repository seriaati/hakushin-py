from pydantic import Field, field_validator

from ..base import APIModel

__all__ = ("DriveDisc", "DriveDiscDetail", "DriveDiscInfo")


class DriveDiscInfo(APIModel):
    """ZZZ drive disc info model."""

    name: str
    two_piece_effect: str = Field(alias="desc2")
    four_piece_effect: str = Field(alias="desc4")


class DriveDisc(APIModel):
    """ZZZ drive disc model."""

    id: int
    icon: str
    name: str = Field(None)  # This field doesn't exist in the API response
    two_piece_effect: str = Field(None)  # Same here
    four_piece_effect: str = Field(None)  # Same here

    en_info: DriveDiscInfo | None = Field(None, alias="EN")
    ko_info: DriveDiscInfo | None = Field(None, alias="KO")
    chs_info: DriveDiscInfo = Field(alias="CHS")
    ja_info: DriveDiscInfo | None = Field(None, alias="JA")

    @field_validator("icon")
    @classmethod
    def __convert_icon(cls, icon: str) -> str:
        filename = icon.split("/")[-1].split(".")[0]
        return f"https://api.hakush.in/zzz/UI/{filename}.webp"


class DriveDiscDetail(APIModel):
    """ZZZ drive disc detail model."""

    id: int = Field(alias="Id")
    name: str = Field(alias="Name")
    two_piece_effect: str = Field(alias="Desc2")
    four_piece_effect: str = Field(alias="Desc4")
    story: str = Field(alias="Story")
    icon: str = Field(alias="Icon")
    # icon2: str = Field(alias="Icon2")

    @field_validator("icon")
    @classmethod
    def __convert_icon(cls, icon: str) -> str:
        filename = icon.split("/")[-1].split(".")[0]
        return f"https://api.hakush.in/zzz/UI/{filename}.webp"
