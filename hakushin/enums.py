from enum import StrEnum

__all__ = ("Game", "Language")


class Game(StrEnum):
    """Games supported by the Hakushin API."""

    GI = "gi"
    """Genshin Impact."""
    HSR = "hsr"
    """Honkai: Star Rail."""


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
