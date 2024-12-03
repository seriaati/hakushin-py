from __future__ import annotations

from enum import IntEnum, StrEnum

__all__ = ("Game", "Language")


class Game(StrEnum):
    """Games supported by the Hakushin API."""

    GI = "gi"
    """Genshin Impact."""
    HSR = "hsr"
    """Honkai: Star Rail."""
    ZZZ = "zzz"
    """Zenless Zone Zero."""


class Language(StrEnum):
    """Lanauges supported by the Hakushin API."""

    EN = "en"
    """English."""
    ZH = "zh"
    """Simple Chinese."""
    KO = "ko"
    """Korean."""
    JA = "ja"
    """Japanese."""


class GIElement(StrEnum):
    """Genshin Impact element."""

    HYDRO = "Hydro"
    PYRO = "Pyro"
    CRYO = "Cryo"
    ELECTRO = "Electro"
    ANEMO = "Anemo"
    GEO = "Geo"
    DENDRO = "Dendro"


class HSRElement(StrEnum):
    """HSR element."""

    ICE = "Ice"
    FIRE = "Fire"
    THUNDER = "Thunder"
    WIND = "Wind"
    PHYSICAL = "Physical"
    QUANTUM = "Quantum"
    IMAGINARY = "Imaginary"


class HSRPath(StrEnum):
    """HSR character path."""

    PRESERVATION = "Knight"
    THE_HUNT = "Rogue"
    DESTRUCTION = "Warrior"
    ERUDITION = "Mage"
    HARMONY = "Shaman"
    NIHILITY = "Warlock"
    ABUNDANCE = "Priest"
    REMEMBRANCE = "Memory"


class ZZZSpecialty(IntEnum):
    """ZZZ character specialty."""

    ATTACK = 1
    STUN = 2
    ANOMALY = 3
    SUPPORT = 4
    DEFENSE = 5


class ZZZElement(IntEnum):
    """ZZZ character element."""

    PHYSICAL = 200
    FIRE = 201
    ICE = 202
    ELECTRIC = 203
    ETHER = 205


class ZZZAttackType(IntEnum):
    """ZZZ character attack type."""

    SLASH = 101
    STRIKE = 102
    PIERCE = 103


class ZZZSkillType(StrEnum):
    """ZZZ character skill type."""

    BASIC = "Basic"
    DODGE = "Dodge"
    SPECIAL = "Special"
    CHAIN = "Chain"
    ASSIST = "Assist"
