from __future__ import annotations

from enum import IntEnum, StrEnum

__all__ = (
    "GIElement",
    "Game",
    "HSRElement",
    "HSREndgameType",
    "HSRPath",
    "Language",
    "MWCostumeBodyType",
    "ZZZAttackType",
    "ZZZElement",
    "ZZZSkillType",
    "ZZZSpecialty",
)


class Game(StrEnum):
    """Represent games supported by the Hakushin API."""

    GI = "gi"
    """Genshin Impact."""
    HSR = "hsr"
    """Honkai: Star Rail."""
    ZZZ = "zzz"
    """Zenless Zone Zero."""


class Language(StrEnum):
    """Represent languages supported by the Hakushin API."""

    EN = "en"
    """English."""
    ZH = "zh"
    """Simple Chinese."""
    KO = "ko"
    """Korean."""
    JA = "ja"
    """Japanese."""


class GIElement(StrEnum):
    """Represent a Genshin Impact element."""

    HYDRO = "Hydro"
    PYRO = "Pyro"
    CRYO = "Cryo"
    ELECTRO = "Electro"
    ANEMO = "Anemo"
    GEO = "Geo"
    DENDRO = "Dendro"


class HSRElement(StrEnum):
    """Represent an HSR element."""

    ICE = "Ice"
    FIRE = "Fire"
    THUNDER = "Thunder"
    WIND = "Wind"
    PHYSICAL = "Physical"
    QUANTUM = "Quantum"
    IMAGINARY = "Imaginary"


class HSRPath(StrEnum):
    """Represent an HSR character path."""

    PRESERVATION = "Knight"
    THE_HUNT = "Rogue"
    DESTRUCTION = "Warrior"
    ERUDITION = "Mage"
    HARMONY = "Shaman"
    NIHILITY = "Warlock"
    ABUNDANCE = "Priest"
    REMEMBRANCE = "Memory"


class HSREndgameType(StrEnum):
    """Represent an HSR endgame."""

    MEMORY_OF_CHAOS = "maze"
    PURE_FICTION = "story"
    APOCALYPTIC_SHADOW = "boss"


class ZZZSpecialty(IntEnum):
    """Represent a ZZZ character specialty."""

    ATTACK = 1
    STUN = 2
    ANOMALY = 3
    SUPPORT = 4
    DEFENSE = 5
    RUPTURE = 6


class ZZZElement(IntEnum):
    """Represent a ZZZ character element."""

    PHYSICAL = 200
    FIRE = 201
    ICE = 202
    ELECTRIC = 203
    ETHER = 205


class ZZZAttackType(IntEnum):
    """Represent a ZZZ character attack type."""

    SLASH = 101
    STRIKE = 102
    PIERCE = 103


class ZZZSkillType(StrEnum):
    """Represent a ZZZ character skill type."""

    BASIC = "Basic"
    DODGE = "Dodge"
    SPECIAL = "Special"
    CHAIN = "Chain"
    ASSIST = "Assist"


class MWCostumeBodyType(StrEnum):
    """Miliastra Wonderland costume body types"""

    GIRL = "BODY_GIRL"
    BOY = "BODY_BOY"
