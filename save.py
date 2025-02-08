import os

import utils

Board = list[list[int]]


def save_board(board: Board, size: tuple, rule: dict[str, list[int]], filename: str) -> None:
    """
    Saves the board to a file with the specified filename.

    :param board: list of lists representing the board
    :param size: size of the board to save
    :param rule: dictionary representing the rule of the board
    :param filename: name of the file to save
    :return: None
    """

    # convert filename to alphanumeric characters only
    filename = "".join(char for char in filename if char.isalnum() or char in "._-")

    with open(os.getcwd() + "\\saved_boards\\" + filename + ".txt", "w", encoding="utf-8") as f:
        rule = utils.parse_dict_to_rule(rule)
        f.write(rule + "\n")
        size = "/".join(map(str, size))
        f.write(size + "\n")
        for line in board:
            line = "".join(["." if char == 0 else "o" for char in line])
            f.write(line + "\n")
