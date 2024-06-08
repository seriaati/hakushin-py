from typing import Final, Literal

from .enums import Game, HSRPath, Language

__all__ = (
    "GI_CHARA_RARITY_MAP",
    "GI_LANG_MAP",
    "HSR_API_LANG_MAP",
    "HSR_CHARA_RARITY_MAP",
    "HSR_LIGHT_CONE_RARITY_MAP",
    "PERCENTAGE_FIGHT_PROPS",
)

GI_CHARA_RARITY_MAP: Final[dict[str, Literal[4, 5]]] = {
    "QUALITY_PURPLE": 4,
    "QUALITY_ORANGE": 5,
    "QUALITY_ORANGE_SP": 5,
}

HSR_CHARA_RARITY_MAP: Final[dict[str, Literal[4, 5]]] = {
    "CombatPowerAvatarRarityType4": 4,
    "CombatPowerAvatarRarityType5": 5,
}

HSR_LIGHT_CONE_RARITY_MAP: Final[dict[str, Literal[3, 4, 5]]] = {
    "CombatPowerLightconeRarity3": 3,
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
"""Set of fight props that should be displayed as percentage value."""

HSR_PATH_NAMES: Final[dict[Language, dict[HSRPath, str]]] = {
    Language.EN: {
        HSRPath.ABUNDANCE: "Abundance",
        HSRPath.DESTRUCTION: "Destruction",
        HSRPath.ERUDITION: "Erudition",
        HSRPath.HARMONY: "Harmony",
        HSRPath.NIHILITY: "Nihility",
        HSRPath.PRESERVATION: "Preservation",
        HSRPath.THE_HUNT: "The Hunt",
    },
    Language.JA: {
        HSRPath.ABUNDANCE: "豊穣",
        HSRPath.DESTRUCTION: "壊滅",
        HSRPath.ERUDITION: "知恵",
        HSRPath.HARMONY: "調和",
        HSRPath.NIHILITY: "虚無",
        HSRPath.PRESERVATION: "存護",
        HSRPath.THE_HUNT: "巡狩",
    },
    Language.ZH: {
        HSRPath.ABUNDANCE: "豐饒",
        HSRPath.DESTRUCTION: "毀滅",
        HSRPath.ERUDITION: "智識",
        HSRPath.HARMONY: "同諧",
        HSRPath.NIHILITY: "虚無",
        HSRPath.PRESERVATION: "存護",
        HSRPath.THE_HUNT: "巡獵",
    },
    Language.KO: {
        HSRPath.ABUNDANCE: "풍요",
        HSRPath.DESTRUCTION: "파멸",
        HSRPath.ERUDITION: "지식",
        HSRPath.HARMONY: "화합",
        HSRPath.NIHILITY: "공허",
        HSRPath.PRESERVATION: "보존",
        HSRPath.THE_HUNT: "수렵",
    },
}

STAT_TO_FIGHT_PROP: Final[dict[str, str]] = {
    "BaseHP": "FIGHT_PROP_BASE_HP",
    "BaseDEF": "FIGHT_PROP_BASE_DEFENSE",
    "BaseATK": "FIGHT_PROP_BASE_ATTACK",
}

NOT_ASCENDED_LEVEL_TO_ASCENSION: Final[dict[Game, dict[int, int]]] = {
    Game.GI: {
        80: 5,
        70: 4,
        60: 3,
        50: 2,
        40: 1,
        20: 0,
    },
    Game.HSR: {
        70: 5,
        60: 4,
        50: 3,
        40: 2,
        30: 1,
        20: 0,
    },
}

ASCENDED_LEVEL_TO_ASCENSION: Final[dict[Game, dict[tuple[int, int], int]]] = {
    Game.GI: {
        (80, 90): 6,
        (70, 80): 5,
        (60, 70): 4,
        (50, 60): 3,
        (40, 50): 2,
        (20, 40): 1,
    },
    Game.HSR: {
        (70, 80): 6,
        (60, 70): 5,
        (50, 60): 4,
        (40, 50): 3,
        (30, 40): 2,
        (20, 30): 1,
    },
}

ASCENSION_TO_MAX_LEVEL: Final[dict[Game, dict[int, int]]] = {
    Game.GI: {
        0: 20,
        1: 40,
        2: 50,
        3: 60,
        4: 70,
        5: 80,
        6: 90,
    },
    Game.HSR: {
        0: 20,
        1: 30,
        2: 40,
        3: 50,
        4: 60,
        5: 70,
        6: 80,
    },
}
