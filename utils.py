import re


def format_text_to_rule(text: str) -> str:
    """
    Converts given string to rule format.
    Format looks like this:
            +-- dividing slash for clarity
            |
           / \
    >>  R1/B3/S23  <<
        |  |  |
        |  |  +--> S: how many neighbours are required for a live cell to remain alive - followed by a list of integers
        |  +--> B: how many neighbours are required for a dead cell to become alive - followed by a list integer
        +--> R: radius in which cells are considered neighbours - followed by a single integer (single integer not enforced)

    :param text: string to be converted
    :return: formatted rule string
    """
    out = ""
    for char in text:
        char = char.upper()
        if char.isdigit():
            out += char
        elif char in "RBS" and char not in out:
            out += "/" + char

    if len(out) > 0 and out[0] == "/":
        out = out[1:]

    return out


def is_rule_valid(string: str) -> bool:
    """
    Checks if the given string is a valid rule.
    Rule format is defined in format_text_to_rule() function.
    Regex pattern is used to check the validity of the string.

    :param string: string to be checked
    :return: True if the string is a valid rule, False otherwise
    """
    pattern = r"^R[1-9]{1}/B[0-9]+/S[0-9]+$"

    return bool(re.match(pattern, string.upper()))


def parse_rule_to_dict(string_rule: str) -> dict[str, list[int]]:
    """
    Converts given rule from string to a dictionary.
    Rule format is defined in format_text_to_rule() function.
    Inputted string must be a valid rule.

    :param string_rule: string to be converted
    :return: dictionary with keys R, B, S
    """
    assert is_rule_valid(string_rule), "Invalid rule format"

    rule = {}
    last_char = ""
    for char in string_rule:
        if char.isalpha():
            last_char = char
            rule[char] = []
        elif char.isdigit():
            if char not in rule[last_char]:
                rule[last_char].append(int(char))
    return rule


def parse_dict_to_rule(rd: dict[str, list[int]]) -> str:
    """
    Converts given rule from dictionary to a string.
    Rule format is defined in format_text_to_rule() function.
    :param rd: dictionary with keys R, B, S
    :return: string representation of the rule
    """
    return ("R" + "".join(str(_) for _ in rd["R"]) +
            "/B" + "".join(str(_) for _ in rd["B"]) +
            "/S" + "".join(str(_) for _ in rd["S"]))
