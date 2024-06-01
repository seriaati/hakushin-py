from __future__ import annotations

import re
from typing import Final, TypeVar

from .constants import PERCENTAGE_FIGHT_PROPS
from .enums import Game
from .models import gi, hsr

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


STAT_TO_FIGHT_PROP: Final[dict[str, str]] = {
    "BaseHP": "FIGHT_PROP_BASE_HP",
    "BaseDEF": "FIGHT_PROP_BASE_DEFENSE",
    "BaseATK": "FIGHT_PROP_BASE_ATTACK",
}


def calc_upgrade_stat_values(
    character: gi.CharacterDetail | hsr.CharacterDetail,
    level: int,
    ascended: bool,
) -> dict[str, float]:
    """Calculate the stat values of a character at a certain level and ascension.

    Args:
        character (gi.CharacterDetail): The character to calculate the stats for.
        level (int): The level of the character.
        ascended (bool): Whether the character is ascended.
    """
    result: dict[str, float] = {}

    if isinstance(character, gi.CharacterDetail):
        result["FIGHT_PROP_BASE_HP"] = character.base_hp * character.stats_modifier.hp[str(level)]
        result["FIGHT_PROP_BASE_ATTACK"] = (
            character.base_atk * character.stats_modifier.atk[str(level)]
        )
        result["FIGHT_PROP_BASE_DEFENSE"] = (
            character.base_def * character.stats_modifier.def_[str(level)]
        )

        ascension = get_ascension_from_level(level, ascended, Game.GI)
        ascension = character.stats_modifier.ascension[ascension - 1]
        for fight_prop, value in ascension.items():
            stat = STAT_TO_FIGHT_PROP.get(fight_prop, fight_prop)
            if stat not in result:
                result[stat] = 0
            result[stat] += value
    else:
        raise NotImplementedError

    return result


def format_stat_values(values: dict[str, float]) -> dict[str, str]:
    """Format the stat values to a human-readable format.

    Percentage values will be rounded to 1 decimal, while others will be rounded to the nearest integer.

    Args:
        values (dict[str, float]): A dictionary of fight prop ID and value.
    """
    result: dict[str, str] = {}

    for fight_prop, value in values.items():
        if fight_prop in PERCENTAGE_FIGHT_PROPS:
            # round to 1 decimal
            result[fight_prop] = f"{value:.1f}%"
        else:
            result[fight_prop] = str(round(value))

    return result


T = TypeVar("T")


def replace_fight_prop_with_name(
    values: dict[str, T], manual_weapon: dict[str, str]
) -> dict[str, T]:
    """Replace the fight prop with the corresponding name.

    Manual weapon example: https://api.ambr.top/v2/cht/manualWeapon

    Args:
        values (dict[str, T]): A dictionary of fight prop ID and value.
        manual_weapon (dict[str, str]): A dictionary from project ambr with fight prop ID and value.
    """
    return {
        manual_weapon.get(fight_prop, fight_prop): value for fight_prop, value in values.items()
    }
