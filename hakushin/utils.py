import re

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
