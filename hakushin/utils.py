from __future__ import annotations

import re
from typing import TYPE_CHECKING, TypeVar

from .constants import (
    ASCENDED_LEVEL_TO_ASCENSION,
    ASCENSION_TO_MAX_LEVEL,
    NOT_ASCENDED_LEVEL_TO_ASCENSION,
    PERCENTAGE_FIGHT_PROPS,
    STAT_TO_FIGHT_PROP,
)
from .enums import Game

if TYPE_CHECKING:
    from .models import gi, hsr


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


def replace_device_params(text: str) -> str:
    """Replace device parameters in a string with the corresponding values."""
    # Replace '{LAYOUT_CONSOLECONTROLLER#stick}' with 'stick/'
    text = re.sub(r"{LAYOUT_CONSOLECONTROLLER#(.*?)}", r"\1/", text)

    # Replace '{LAYOUT_FALLBACK#joystick}' with 'joystick'
    text = re.sub(r"{LAYOUT_FALLBACK#(.*?)}", r"\1", text)

    return text


def cleanup_text(text: str) -> str:
    """Remove HTML tags and sprite presets from a string.

    Args:
        text (str): The text to clean.

    Returns:
        str: The cleaned text.
    """
    clean = re.compile(r"<.*?>|\{SPRITE_PRESET#[^\}]+\}")
    return re.sub(clean, "", text).replace("\\n", "\n").replace("\r\n", "\n")


def replace_placeholders(text: str, param_list: list[float]) -> str:
    """Replaces placeholders in the given text with values from the parameter list.

    Args:
        text (str): The text containing placeholders to be replaced.
        param_list (list[float]): The list of parameter values.

    Returns:
        str: The text with placeholders replaced by their corresponding values.
    """
    placeholders: list[str] = re.findall(r"#\d+\[[^\]]+\]%?", text)

    for placeholder in placeholders:
        index = int(placeholder[1])
        format_ = placeholder[-1]
        value = param_list[index - 1]
        if format_ == "%":
            value *= 100
        text = text.replace(placeholder, f"{round(value)}{'%' if format_ == '%' else ''}")

    return text


def get_ascension_from_level(level: int, ascended: bool, game: Game) -> int:
    """Get the ascension from the level and ascended status."""
    if not ascended and level in NOT_ASCENDED_LEVEL_TO_ASCENSION[game]:
        return NOT_ASCENDED_LEVEL_TO_ASCENSION[game][level]

    for (start, end), ascension in ASCENDED_LEVEL_TO_ASCENSION[game].items():
        if start <= level <= end:
            return ascension

    return 0


def get_max_level_from_ascension(ascension: int, game: Game) -> int:
    """Get the max level from the ascension."""
    return ASCENSION_TO_MAX_LEVEL[game][ascension]


def calc_gi_chara_upgrade_stat_values(
    character: gi.CharacterDetail, level: int, ascended: bool
) -> dict[str, float]:
    """Calculate the stat values of a GI character at a certain level and ascension status.

    Args:
        character: The character to calculate the stats for.
        level: The level of the character.
        ascended: Whether the character is ascended.
    """
    result: dict[str, float] = {}

    result["FIGHT_PROP_BASE_HP"] = character.base_hp * character.stats_modifier.hp[str(level)]
    result["FIGHT_PROP_BASE_ATTACK"] = character.base_atk * character.stats_modifier.atk[str(level)]
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

    return result


def calc_hsr_chara_upgrade_stat_values(
    character: hsr.CharacterDetail, level: int, ascended: bool
) -> dict[str, float]:
    """Calculate the stat values of a HSR character at a certain level and ascension status.

    Args:
        character: The character to calculate the stats for.
        level: The level of the character.
        ascended: Whether the character is ascended.
    """
    result: dict[str, float] = {}

    ascension = get_ascension_from_level(level, ascended, Game.HSR)
    stats = character.ascension_stats[str(ascension)]

    result["baseHP"] = stats["HPBase"] + stats["HPAdd"] * (level - 1)
    result["baseAttack"] = stats["AttackBase"] + stats["AttackAdd"] * (level - 1)
    result["baseDefence"] = stats["DefenceBase"] + stats["DefenceAdd"] * (level - 1)

    result["baseSpeed"] = stats["SpeedBase"]
    result["criticalChanceBase"] = stats["CriticalChance"]
    result["criticalDamageBase"] = stats["CriticalDamage"]

    return result


def calc_weapon_upgrade_stat_values(
    weapon: gi.WeaponDetail, level: int, ascended: bool
) -> dict[str, float]:
    """Calculate the stat values of a GI weapon at a certain level and ascension.

    Args:
        weapon: The weapon to calculate the stats for.
        level: The level of the weapon.
        ascended: Whether the weapon is ascended.
    """
    result: dict[str, float] = {}

    result["FIGHT_PROP_BASE_ATTACK"] = (
        weapon.stat_modifiers["ATK"].base * weapon.stat_modifiers["ATK"].levels[str(level)]
    )

    for fight_prop, value in weapon.stat_modifiers.items():
        if fight_prop == "ATK":
            continue
        result[fight_prop] = value.base * value.levels[str(level)]

    ascension = get_ascension_from_level(level, ascended, Game.GI)
    if ascension == 0:
        ascension = 1
    ascension = weapon.ascension[str(ascension)]
    for fight_prop, value in ascension.items():
        if fight_prop not in result:
            result[fight_prop] = 0
        result[fight_prop] += value

    return result


def calc_light_cone_upgrade_stat_values(
    light_cone: hsr.LightConeDetail, level: int, ascended: bool
) -> dict[str, float]:
    """Calculate the stat values of a HSR light cone at a certain level and ascension status.

    Args:
        light_cone: The light cone to calculate the stats for.
        level: The level of the light cone.
        ascended: Whether the light cone is ascended.
    """
    result: dict[str, float] = {}

    ascension = get_ascension_from_level(level, ascended, Game.HSR)
    stats = light_cone.ascension_stats[ascension]

    result["baseHP"] = stats["BaseHP"] + stats["BaseHPAdd"] * (level - 1)
    result["baseAttack"] = stats["BaseAttack"] + stats["BaseAttackAdd"] * (level - 1)
    result["baseDefence"] = stats["BaseDefence"] + stats["BaseDefenceAdd"] * (level - 1)

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
            result[fight_prop] = f"{value * 100:.1f}%"
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


def get_skill_attributes(descriptions: list[str], params: list[int | float]) -> str:
    """Get the skill attributes from the descriptions.

    Args:
        descriptions (list[str]): The list of descriptions.
        params (list[int | float]): The list of parameters.
    """
    result = ""
    for desc in descriptions:
        try:
            k, v = replace_params(desc, params)
        except ValueError:
            continue
        result += f"{k}: {v}\n"
    return result


def remove_ruby_tags(text: str) -> str:
    """Remove ruby tags from a string."""
    # Remove {RUBY_E#} tags
    text = re.sub(r"\{RUBY_E#\}", "", text)
    # Remove {RUBY_B...} tags
    text = re.sub(r"\{RUBY_B#.*?\}", "", text)
    return text
