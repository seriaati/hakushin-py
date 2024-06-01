from __future__ import annotations

import re
from typing import TYPE_CHECKING, Final

from .enums import Game

if TYPE_CHECKING:
    from .models import gi

__all__ = (
    "cleanup_text",
    "format_num",
    "replace_layout",
    "replace_params",
    "replace_placeholders",
)


def format_num(digits: int, calculation: float) -> str:
    """Format a number to a string with a fixed number of digits after the decimal point.

    Args:
        digits (int): Number of digits after the decimal point.
        calculation (float): Number to format.

    Returns:
        str: The formatted number.
    """
    return f"{calculation:.{digits}f}"


def replace_layout(text: str) -> str:
    """Replace the layout in a string with the corresponding word.

    Args:
        text (str): The text to format.

    Returns:
        str: The formatted text.
    """
    if "LAYOUT" in text:
        brackets = re.findall(r"{LAYOUT.*?}", text)
        word_to_replace = re.findall(r"{LAYOUT.*?#(.*?)}", brackets[0])[0]
        text = text.replace("".join(brackets), word_to_replace)
    return text


def replace_params(text: str, param_list: list[float]) -> list[str]:
    """Replace parameters in a string with the corresponding values.

    Args:
        text (str): The text to replace the parameters in.
        param_list (list[float]): The list of parameters to replace the values with.

    Returns:
        list[str]: The list of strings with the replaced parameters.
    """
    params: list[str] = re.findall(r"{[^}]*}", text)

    for item in params:
        if "param" not in item:
            continue

        param_text = re.findall(r"{param(\d+):([^}]*)}", item)[0]
        param, value = param_text

        if value in {"F1P", "F2P"}:
            result = format_num(int(value[1]), param_list[int(param) - 1] * 100)
            text = re.sub(re.escape(item), f"{result}%", text)
        elif value in {"F1", "F2"}:
            result = format_num(int(value[1]), param_list[int(param) - 1])
            text = re.sub(re.escape(item), result, text)
        elif value == "P":
            result = format_num(0, param_list[int(param) - 1] * 100)
            text = re.sub(re.escape(item), f"{result}%", text)
        elif value == "I":
            result = int(param_list[int(param) - 1])
            text = re.sub(re.escape(item), str(round(result)), text)

    text = replace_layout(text)
    text = text.replace("{NON_BREAK_SPACE}", "")
    text = text.replace("#", "")
    return text.split("|")


def cleanup_text(text: str) -> str:
    """Remove HTML tags and sprite presets from a string.

    Args:
        text (str): The text to clean.

    Returns:
        str: The cleaned text.
    """
    clean = re.compile(r"<.*?>|\{SPRITE_PRESET#[^\}]+\}")
    return re.sub(clean, "", text).replace("\\n", "\n")


def replace_placeholders(text: str, param_list: list[float]) -> str:
    """Replaces placeholders in the given text with values from the parameter list.

    Args:
        text (str): The text containing placeholders to be replaced.
        param_list (list[float]): The list of parameter values.

    Returns:
        str: The text with placeholders replaced by their corresponding values.
    """
    placeholders: list[str] = re.findall(r"#\d+\[i\]%?", text)

    for placeholder in placeholders:
        index = int(placeholder[1])
        format_ = placeholder[-1]
        value = param_list[index - 1]
        if format_ == "%":
            value *= 100
        text = text.replace(placeholder, f"{round(value)}{'%' if format_ == '%' else ''}")

    return text


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


def get_ascension_from_level(level: int, ascended: bool, game: Game) -> int:
    if not ascended and level in NOT_ASCENDED_LEVEL_TO_ASCENSION[game]:
        return NOT_ASCENDED_LEVEL_TO_ASCENSION[game][level]

    for (start, end), ascension in ASCENDED_LEVEL_TO_ASCENSION[game].items():
        if start <= level <= end:
            return ascension

    return 0


FIGHT_PROP_TO_STAT: Final[dict[str, str]] = {
    "FIGHT_PROP_BASE_HP": "BaseHP",
    "FIGHT_PROP_BASE_DEFENSE": "BaseDEF",
    "FIGHT_PROP_BASE_ATTACK": "BaseATK",
}


def calc_upgrade_stat_values(
    character: gi.CharacterDetail,
    level: int,
    ascended: bool,
    game: Game,
) -> dict[str, float]:
    result: dict[str, float] = {}

    if game is Game.GI:
        result["BaseHP"] = character.base_hp * character.stats_modifier.hp[str(level)]
        result["BaseATK"] = character.base_atk * character.stats_modifier.atk[str(level)]
        result["BaseDEF"] = character.base_def * character.stats_modifier.def_[str(level)]

        ascension = get_ascension_from_level(level, ascended, game)
        ascension = character.stats_modifier.ascension[ascension - 1]
        for fight_prop, value in ascension.items():
            stat = FIGHT_PROP_TO_STAT.get(fight_prop, fight_prop)
            if stat not in result:
                result[stat] = 0
            result[stat] += value
    else:
        raise NotImplementedError

    return result
