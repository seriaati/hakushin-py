from typing import Final

from .enums import Language

__all__ = ("GI_CHARA_RARITY_MAP", "HSR_CHARA_RARITY_MAP", "HSR_LIGHT_CONE_RARITY_MAP")

GI_CHARA_RARITY_MAP: Final[dict[str, int]] = {
    "QUALITY_PURPLE": 4,
    "QUALITY_ORANGE": 5,
    "QUALITY_ORANGE_SP": 5,
}

HSR_CHARA_RARITY_MAP: Final[dict[str, int]] = {
    "CombatPowerAvatarRarityType4": 4,
    "CombatPowerAvatarRarityType5": 5,
}

HSR_LIGHT_CONE_RARITY_MAP: Final[dict[str, int]] = {
    "CombatPowerLightconeRarity4": 4,
    "CombatPowerLightconeRarity5": 5,
}

HSR_LANG_MAP: Final[dict[Language, str]] = {
    Language.EN: "en",
    Language.JA: "jp",
    Language.KO: "kr",
    Language.ZH: "cn",
}
"""Map to convert language enum for GI to for HSR."""
