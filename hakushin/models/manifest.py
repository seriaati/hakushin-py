from __future__ import annotations

from pydantic import BaseModel, Field

__all__ = ("GameManifest", "ManifestResponse")


class GameManifest(BaseModel):
    """Data model for the manifest information of a single game.

    Attributes:
        latest_version: The latest version of the game.
        available_versions: A list of all available versions for the game.
        live_version: The currently live version of the game.
    """

    latest_version: str = Field(alias="latest")
    available_versions: list[str] = Field(alias="available")
    live_version: str = Field(alias="live")


class ManifestResponse(BaseModel):
    """Data model for the manifest response from the Hakushin API.

    Attributes:
        gi: Manifest information for Genshin Impact.
        hsr: Manifest information for Honkai: Star Rail.
        zzz: Manifest information for Zenless Zone Zero.
        wuwa: Manifest information for Wuthering Waves.
    """

    gi: GameManifest
    hsr: GameManifest
    zzz: GameManifest
    wuwa: GameManifest = Field(alias="ww")
