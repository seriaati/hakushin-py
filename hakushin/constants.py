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

GI_ICON_URL_PREFIX: Final[str] = "https://api.hakush.in/gi/UI"
_gi_sprite_preset_map: dict[str, str] = {
    "SPRITE_PRESET#1101": "UI_Gcg_DiceS_Frost",
    "SPRITE_PRESET#1102": "UI_Gcg_DiceS_Water",
    "SPRITE_PRESET#1103": "UI_Gcg_DiceS_Fire",
    "SPRITE_PRESET#1104": "UI_Gcg_DiceS_Elect",
    "SPRITE_PRESET#1105": "UI_Gcg_DiceS_Wind",
    "SPRITE_PRESET#1106": "UI_Gcg_DiceS_Roach",
    "SPRITE_PRESET#1107": "UI_Gcg_DiceS_Grass",
    "SPRITE_PRESET#1108": "UI_Gcg_DiceS_Same",
    "SPRITE_PRESET#1109": "UI_Gcg_DiceS_Diff",
    "SPRITE_PRESET#1110": "UI_Gcg_DiceS_Energy",
    "SPRITE_PRESET#1111": "UI_Gcg_DiceS_Any",
    "SPRITE_PRESET#1112": "UI_Gcg_DiceS_Legend",
    "SPRITE_PRESET#1113": "UI_Gcg_Buff_ElementMastery",
    "SPRITE_PRESET#2100": "UI_Gcg_Buff_Common_Element_Physics",
    "SPRITE_PRESET#2101": "UI_Gcg_Buff_Common_Element_Ice",
    "SPRITE_PRESET#2102": "UI_Gcg_Buff_Common_Element_Water",
    "SPRITE_PRESET#2103": "UI_Gcg_Buff_Common_Element_Fire",
    "SPRITE_PRESET#2104": "UI_Gcg_Buff_Common_Element_Electric",
    "SPRITE_PRESET#2105": "UI_Gcg_Buff_Common_Element_Wind",
    "SPRITE_PRESET#2106": "UI_Gcg_Buff_Common_Element_Rock",
    "SPRITE_PRESET#2107": "UI_Gcg_Buff_Common_Element_Grass",
    "SPRITE_PRESET#3002": "UI_Gcg_Tag_Card_Talent",
    "SPRITE_PRESET#3005": "UI_Gcg_Tag_Card_Talent",
    "SPRITE_PRESET#3003": "UI_Gcg_Tag_Card_Weapon",
    "SPRITE_PRESET#3004": "UI_Gcg_Tag_Card_Relic",
    "SPRITE_PRESET#3006": "UI_Gcg_Tag_Card_Talent",
    "SPRITE_PRESET#3007": "UI_Gcg_Tag_Card_Legend",
    "SPRITE_PRESET#3008": "UI_Gcg_Tag_Card_Vehicle",
    "SPRITE_PRESET#3104": "UI_Gcg_Tag_Card_Location",
    "SPRITE_PRESET#3103": "UI_Gcg_Tag_Card_Ally",
    "SPRITE_PRESET#3102": "UI_Gcg_Tag_Card_Item",
    "SPRITE_PRESET#3105": "UI_Gcg_Tag_Card_Ally",
    "SPRITE_PRESET#3101": "UI_Gcg_Tag_Card_Food",
    "SPRITE_PRESET#3201": "UI_Gcg_Tag_Weapon_Catalyst",
    "SPRITE_PRESET#3202": "UI_Gcg_Tag_Weapon_Bow",
    "SPRITE_PRESET#3203": "UI_Gcg_Tag_Weapon_Claymore",
    "SPRITE_PRESET#3204": "UI_Gcg_Tag_Weapon_Polearm",
    "SPRITE_PRESET#3205": "UI_Gcg_Tag_Weapon_Sword",
    "SPRITE_PRESET#3401": "UI_Gcg_Tag_Faction_Mondstadt",
    "SPRITE_PRESET#3402": "UI_Gcg_Tag_Faction_Liyue",
    "SPRITE_PRESET#3403": "UI_Gcg_Tag_Faction_Inazuma",
    "SPRITE_PRESET#3404": "UI_Gcg_Tag_Faction_Sumeru",
    "SPRITE_PRESET#3405": "UI_Gcg_Tag_Faction_Fontaine",
    "SPRITE_PRESET#3406": "UI_Gcg_Tag_Faction_Natlan",
    "SPRITE_PRESET#3501": "UI_Gcg_Tag_Faction_Fatui",
    "SPRITE_PRESET#3502": "UI_Gcg_Tag_Faction_Hili",
    "SPRITE_PRESET#3503": "UI_Gcg_Tag_Faction_Monster",
    "SPRITE_PRESET#3504": "UI_Gcg_Tag_Faction_Pneuma",
    "SPRITE_PRESET#3505": "UI_Gcg_Tag_Faction_Ousia",
    "SPRITE_PRESET#3506": "UI_Gcg_Tag_Faction_Sacred",
    "SPRITE_PRESET#4001": "UI_Gcg_Buff_Common_Atk_Self",
    "SPRITE_PRESET#4002": "UI_Gcg_Buff_Common_Atk_Up",
    "SPRITE_PRESET#4003": "UI_Gcg_Buff_Common_Barrier",
    "SPRITE_PRESET#4004": "UI_Gcg_Buff_Common_Food",
    "SPRITE_PRESET#4005": "UI_Gcg_Buff_Common_Frozen",
    "SPRITE_PRESET#4006": "UI_Gcg_Buff_Common_Heal",
    "SPRITE_PRESET#4007": "UI_Gcg_Buff_Common_Shield",
    "SPRITE_PRESET#4008": "UI_Gcg_Buff_Common_Special",
    "SPRITE_PRESET#4101": "UI_Gcg_Buff_Kaeya_E",
    "SPRITE_PRESET#4102": "UI_Gcg_Buff_Mona_E",
    "SPRITE_PRESET#4103": "UI_Gcg_Buff_Noel_E",
    "SPRITE_PRESET#4104": "UI_Gcg_Buff_Razor_E",
    "SPRITE_PRESET#4105": "UI_Gcg_Buff_Xiangling_E",
    "SPRITE_PRESET#4106": "UI_Gcg_Buff_Yoimiya_E",
    "SPRITE_PRESET#4201": "UI_Icon_AlchemySim_Type_Small_1",
    "SPRITE_PRESET#4202": "UI_Icon_AlchemySim_Type_Small_2",
    "SPRITE_PRESET#4203": "UI_Icon_AlchemySim_Type_Small_3",
    "SPRITE_PRESET#4204": "UI_Icon_AlchemySim_Type_Small_4",
    "SPRITE_PRESET#4205": "UI_Icon_AlchemySim_Type_Small_5",
    "SPRITE_PRESET#4301": "UI_Icon_LanV5GreetingCard_Friend",
    "SPRITE_PRESET#11001": "UI_Buff_Element02_Frost",
    "SPRITE_PRESET#11002": "UI_Buff_Element02_Water",
    "SPRITE_PRESET#11003": "UI_Buff_Element02_Fire",
    "SPRITE_PRESET#11004": "UI_Buff_Element02_Elect",
    "SPRITE_PRESET#11005": "UI_Buff_Element02_Wind",
    "SPRITE_PRESET#11006": "UI_Buff_Element02_Roach",
    "SPRITE_PRESET#11007": "UI_Buff_Element02_Grass",
    "SPRITE_PRESET#11021": "UI_LeyLineChallenge_Icon_ElectGrass",
    "SPRITE_PRESET#11022": "UI_LeyLineChallenge_Icon_ElectIce",
    "SPRITE_PRESET#11023": "UI_LeyLineChallenge_Icon_ElectRock",
    "SPRITE_PRESET#11024": "UI_LeyLineChallenge_Icon_ElectWind",
    "SPRITE_PRESET#11025": "UI_LeyLineChallenge_Icon_FireElect",
    "SPRITE_PRESET#11026": "UI_LeyLineChallenge_Icon_FireGrass",
    "SPRITE_PRESET#11027": "UI_LeyLineChallenge_Icon_FireIce",
    "SPRITE_PRESET#11028": "UI_LeyLineChallenge_Icon_FireWind",
    "SPRITE_PRESET#11029": "UI_LeyLineChallenge_Icon_GrassWter",
    "SPRITE_PRESET#11030": "UI_LeyLineChallenge_Icon_IceRock",
    "SPRITE_PRESET#11031": "UI_LeyLineChallenge_Icon_IceWater",
    "SPRITE_PRESET#11032": "UI_LeyLineChallenge_Icon_IceWind",
    "SPRITE_PRESET#11033": "UI_LeyLineChallenge_Icon_RockFire",
    "SPRITE_PRESET#11034": "UI_LeyLineChallenge_Icon_WaterElect",
    "SPRITE_PRESET#11035": "UI_LeyLineChallenge_Icon_WaterFire",
    "SPRITE_PRESET#11036": "UI_LeyLineChallenge_Icon_WaterRock",
    "SPRITE_PRESET#11037": "UI_LeyLineChallenge_Icon_WindWater",
    "SPRITE_PRESET#21001": "UI_DisplayItemIcon_410030",
    "SPRITE_PRESET#21002": "UI_Icon_AutoChess_Text_Heal",
}
GI_SPRITE_PRESET_MAP: Final[dict[str, str]] = {
    k: f"{GI_ICON_URL_PREFIX}/{v}.webp" for k, v in _gi_sprite_preset_map.items()
}
