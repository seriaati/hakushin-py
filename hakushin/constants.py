from __future__ import annotations

from typing import Final, Literal

from .enums import Game, HSRPath, Language

__all__ = (
    "ASCENDED_LEVEL_TO_ASCENSION",
    "ASCENSION_TO_MAX_LEVEL",
    "GI_CHARA_RARITY_MAP",
    "GI_LANG_MAP",
    "HSR_API_LANG_MAP",
    "HSR_CHARA_RARITY_MAP",
    "HSR_LIGHT_CONE_RARITY_MAP",
    "HSR_PATH_NAMES",
    "NOT_ASCENDED_LEVEL_TO_ASCENSION",
    "PERCENTAGE_FIGHT_PROPS",
    "STAT_TO_FIGHT_PROP",
    "TRAILBLAZER_NAMES",
    "ZZZ_LANG_MAP",
    "ZZZ_SAB_RARITY_CONVERTER",
    "ZZZ_SA_RARITY_CONVERTER",
)

GI_CHARA_RARITY_MAP: Final[dict[str, Literal[4, 5]]] = {
    "QUALITY_PURPLE": 4,
    "QUALITY_ORANGE": 5,
    "QUALITY_ORANGE_SP": 5,
}
"""Map GI character rarity strings to integer values."""

HSR_CHARA_RARITY_MAP: Final[dict[str, Literal[4, 5]]] = {
    "CombatPowerAvatarRarityType4": 4,
    "CombatPowerAvatarRarityType5": 5,
}
"""Map HSR character rarity strings to integer values."""

HSR_LIGHT_CONE_RARITY_MAP: Final[dict[str, Literal[3, 4, 5]]] = {
    "CombatPowerLightconeRarity3": 3,
    "CombatPowerLightconeRarity4": 4,
    "CombatPowerLightconeRarity5": 5,
}
"""Map HSR light cone rarity strings to integer values."""

HSR_API_LANG_MAP: Final[dict[Language, Literal["en", "jp", "kr", "cn"]]] = {
    Language.EN: "en",
    Language.JA: "jp",
    Language.KO: "kr",
    Language.ZH: "cn",
}
"""Map Language enum to HSR API language strings."""

GI_LANG_MAP: Final[dict[Language, Literal["EN", "JP", "KR", "CHS"]]] = {
    Language.EN: "EN",
    Language.JA: "JP",
    Language.KO: "KR",
    Language.ZH: "CHS",
}
"""Map Language enum to GI data language strings."""

ZZZ_LANG_MAP: Final[dict[Language, Literal["EN", "KO", "CHS", "JA"]]] = {
    Language.EN: "EN",
    Language.JA: "JA",
    Language.KO: "KO",
    Language.ZH: "CHS",
}
"""Map Language enum to ZZZ API language strings."""

PERCENTAGE_FIGHT_PROPS: Final[set[str]] = {
    "FIGHT_PROP_HP_PERCENT",
    "FIGHT_PROP_ATTACK_PERCENT",
    "FIGHT_PROP_DEFENSE_PERCENT",
    "FIGHT_PROP_SPEED_PERCENT",
    "FIGHT_PROP_CRITICAL",
    "FIGHT_PROP_CRITICAL_HURT",
    "FIGHT_PROP_CHARGE_EFFICIENCY",
    "FIGHT_PROP_ADD_HURT",
    "FIGHT_PROP_HEAL_ADD",
    "FIGHT_PROP_HEALED_ADD",
    "FIGHT_PROP_FIRE_ADD_HURT",
    "FIGHT_PROP_WATER_ADD_HURT",
    "FIGHT_PROP_GRASS_ADD_HURT",
    "FIGHT_PROP_ELEC_ADD_HURT",
    "FIGHT_PROP_ICE_ADD_HURT",
    "FIGHT_PROP_WIND_ADD_HURT",
    "FIGHT_PROP_PHYSICAL_ADD_HURT",
    "FIGHT_PROP_ROCK_ADD_HURT",
    "FIGHT_PROP_SKILL_CD_MINUS_RATIO",
    "FIGHT_PROP_ATTACK_PERCENT_A",
    "FIGHT_PROP_DEFENSE_PERCENT_A",
    "FIGHT_PROP_HP_PERCENT_A",
    "criticalChance",
    "criticalDamage",
    "breakDamageAddedRatio",
    "breakDamageAddedRatioBase",
    "healRatio",
    "sPRatio",
    "statusProbability",
    "statusResistance",
    "criticalChanceBase",
    "criticalDamageBase",
    "healRatioBase",
    "sPRatioBase",
    "statusProbabilityBase",
    "statusResistanceBase",
    "physicalAddedRatio",
    "physicalResistance",
    "fireAddedRatio",
    "fireResistance",
    "iceAddedRatio",
    "iceResistance",
    "thunderAddedRatio",
    "thunderResistance",
    "windAddedRatio",
    "windResistance",
    "quantumAddedRatio",
    "quantumResistance",
    "imaginaryAddedRatio",
    "imaginaryResistance",
    "hPAddedRatio",
    "attackAddedRatio",
    "defenceAddedRatio",
    "healTakenRatio",
    "physicalResistanceDelta",
    "fireResistanceDelta",
    "iceResistanceDelta",
    "thunderResistanceDelta",
    "windResistanceDelta",
    "quantumResistanceDelta",
    "imaginaryResistanceDelta",
}
"""Set of fight prop keys that represent percentage values."""

HSR_PATH_NAMES: Final[dict[Language, dict[HSRPath, str]]] = {
    Language.EN: {
        HSRPath.ABUNDANCE: "Abundance",
        HSRPath.DESTRUCTION: "Destruction",
        HSRPath.ERUDITION: "Erudition",
        HSRPath.HARMONY: "Harmony",
        HSRPath.NIHILITY: "Nihility",
        HSRPath.PRESERVATION: "Preservation",
        HSRPath.THE_HUNT: "The Hunt",
        HSRPath.REMEMBRANCE: "Remembrance",
    },
    Language.JA: {
        HSRPath.ABUNDANCE: "豊穣",
        HSRPath.DESTRUCTION: "壊滅",
        HSRPath.ERUDITION: "知恵",
        HSRPath.HARMONY: "調和",
        HSRPath.NIHILITY: "虚無",
        HSRPath.PRESERVATION: "存護",
        HSRPath.THE_HUNT: "巡狩",
        HSRPath.REMEMBRANCE: "記憶",
    },
    Language.ZH: {
        HSRPath.ABUNDANCE: "丰饶",
        HSRPath.DESTRUCTION: "毁灭",
        HSRPath.ERUDITION: "智识",
        HSRPath.HARMONY: "同谐",
        HSRPath.NIHILITY: "虚无",
        HSRPath.PRESERVATION: "存护",
        HSRPath.THE_HUNT: "巡猎",
        HSRPath.REMEMBRANCE: "记忆",
    },
    Language.KO: {
        HSRPath.ABUNDANCE: "풍요",
        HSRPath.DESTRUCTION: "파멸",
        HSRPath.ERUDITION: "지식",
        HSRPath.HARMONY: "화합",
        HSRPath.NIHILITY: "공허",
        HSRPath.PRESERVATION: "보존",
        HSRPath.THE_HUNT: "수렵",
        HSRPath.REMEMBRANCE: "기억",
    },
}
"""Map HSRPath enum to localized path names."""

TRAILBLAZER_NAMES: Final[dict[Language, str]] = {
    Language.EN: "Trailblazer",
    Language.JA: "開拓者",
    Language.ZH: "开拓者",
    Language.KO: "개척자",
}
"""Map Language enum to localized Trailblazer names."""

STAT_TO_FIGHT_PROP: Final[dict[str, str]] = {
    "BaseHP": "FIGHT_PROP_BASE_HP",
    "BaseDEF": "FIGHT_PROP_BASE_DEFENSE",
    "BaseATK": "FIGHT_PROP_BASE_ATTACK",
}
"""Map stat keys to fight prop keys."""

NOT_ASCENDED_LEVEL_TO_ASCENSION: Final[dict[Game, dict[int, int]]] = {
    Game.GI: {80: 5, 70: 4, 60: 3, 50: 2, 40: 1, 20: 0},
    Game.HSR: {70: 5, 60: 4, 50: 3, 40: 2, 30: 1, 20: 0},
}
"""Map non-ascended levels to ascension numbers for each game."""

ASCENDED_LEVEL_TO_ASCENSION: Final[dict[Game, dict[tuple[int, int], int]]] = {
    Game.GI: {(80, 90): 6, (70, 80): 5, (60, 70): 4, (50, 60): 3, (40, 50): 2, (20, 40): 1},
    Game.HSR: {(70, 80): 6, (60, 70): 5, (50, 60): 4, (40, 50): 3, (30, 40): 2, (20, 30): 1},
}
"""Map ascended level ranges to ascension numbers for each game."""

ASCENSION_TO_MAX_LEVEL: Final[dict[Game, dict[int, int]]] = {
    Game.GI: {0: 20, 1: 40, 2: 50, 3: 60, 4: 70, 5: 80, 6: 90},
    Game.HSR: {0: 20, 1: 30, 2: 40, 3: 50, 4: 60, 5: 70, 6: 80},
}
"""Map ascension numbers to maximum levels for each game."""

ZZZ_SAB_RARITY_CONVERTER: Final[dict[int, Literal["B", "A", "S"]]] = {2: "B", 3: "A", 4: "S"}
"""Convert ZZZ S/A/B rarity integer values to string literals."""
ZZZ_SA_RARITY_CONVERTER: Final[dict[int, Literal["A", "S"]]] = {3: "A", 4: "S"}
"""Convert ZZZ S/A rarity integer values to string literals."""
