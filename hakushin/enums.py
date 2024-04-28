from enum import StrEnum

__all__ = ("Game", "Language")


class Game(StrEnum):
    """Games supported by the Hakushin API."""

    GI = "gi"  # Genshin Impact
    HSR = "hsr"  # Honkai Star Rail


class Language(StrEnum):
    """Lanauges supported by the Hakushin API."""

    EN = "en"  # English
    ZH = "zh"  # Simplified Chinese
    KO = "ko"  # Korean
    JA = "ja"  # Japanese
