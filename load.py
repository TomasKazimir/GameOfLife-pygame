import utils

Board = list[list[int]]


def load_board(filename: str, size: tuple = (100, 100)) -> (dict, Board, tuple[int, int]):
    """
    Loads a saved board and its rules from a file.
    The loaded board is converted to the size specified by the size parameter.

    :param filename: name of the file to load
    :param size: size of the board to convert to
    :return: a tuple containing the board's rules, the board itself, and the size of the board
    """
    with open(filename, "r", encoding="utf-8") as save_file:
        file_rule = utils.parse_rule_to_dict(save_file.readline().rstrip())
        x, y = tuple(map(int, save_file.readline().rstrip().split("/")))

        board = []
        while (line := save_file.readline().rstrip()) != "":
            board.append([0 if char == "." else 1 for char in line])

    return file_rule, center_and_resize(board, (x, y), size), size


def center_and_resize(board: Board, size: tuple, target_size: tuple) -> Board:
    """
    Centers the board in the middle of the target_size.

    :param board: board to center
    :param size: size of the board
    :param target_size: size of the target board
    :return: centered board with the target size
    """
    board_x = len(board[0])
    board_y = len(board)

    if board_x == target_size[0] and board_y == target_size[1]:
        return board

    out = []
    # add empty lines to the top
    for i in range((target_size[1] - size[1]) // 2):
        out.append([0] * target_size[0])
    # center the lines of given board
    for i in range(size[1]):
        out.append(center_line(board[i], board_x, target_size[0]))
    # add empty lines to the bottom
    for i in range(target_size[1] - len(out)):
        out.append([0] * target_size[0])

    return out


def center_line(line: list, line_len: int, target_len: int):
    """
    Centers a line in the middle of the target length.
    :param line: line to center
    :param line_len: length of the line
    :param target_len: length of the target line
    :return: centered line with the target length
    """
    return ([0] * ((target_len - line_len) // 2)
            + line
            + [0] * ((target_len - line_len + 1) // 2))
