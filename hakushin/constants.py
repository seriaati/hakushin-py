from typing import Final, Literal

from .enums import Language

__all__ = ("GI_CHARA_RARITY_MAP", "HSR_CHARA_RARITY_MAP", "HSR_LIGHT_CONE_RARITY_MAP")

GI_CHARA_RARITY_MAP: Final[dict[str, Literal[4, 5]]] = {
    "QUALITY_PURPLE": 4,
    "QUALITY_ORANGE": 5,
    "QUALITY_ORANGE_SP": 5,
}

HSR_CHARA_RARITY_MAP: Final[dict[str, Literal[4, 5]]] = {
    "CombatPowerAvatarRarityType4": 4,
    "CombatPowerAvatarRarityType5": 5,
}

HSR_LIGHT_CONE_RARITY_MAP: Final[dict[str, Literal[4, 5]]] = {
    "CombatPowerLightconeRarity4": 4,
    "CombatPowerLightconeRarity5": 5,
}

HSR_API_LANG_MAP: Final[dict[Language, Literal["en", "jp", "kr", "cn"]]] = {
    Language.EN: "en",
    Language.JA: "jp",
    Language.KO: "kr",
    Language.ZH: "cn",
}
"""Map to convert API language enum to HSR API language."""

GI_LANG_MAP: Final[dict[Language, Literal["EN", "JP", "KR", "CHS"]]] = {
    Language.EN: "EN",
    Language.JA: "JP",
    Language.KO: "KR",
    Language.ZH: "CHS",
}
"""Map to convert API language enum to GI data language."""
