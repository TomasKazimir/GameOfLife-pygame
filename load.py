def load_board(filename, size=(100,100)):
    with open(filename, "r", encoding="utf-8") as save_file:
        board = []
        x, y = tuple(map(int, save_file.readline().rstrip().split(";")))

        while (line := save_file.readline().rstrip()) != "":
            board.append([0 if char == "." else 1 for char in line])

    # print("Board loaded:")
    # print(*board, sep="\n")
    return center(board, (x, y), size)


def center(board, size, target_size):
    board_x = len(board[0])
    board_y = len(board)

    assert board_x <= target_size[0]
    assert board_y <= target_size[1]

    out = []
    for i in range((target_size[1] - size[1]) // 2):
        out.append([0] * target_size[0])
    for i in range(size[1]):
        out.append(center_line(board[i], board_x, target_size[0]))
    for i in range(target_size[1] - len(out)):
        out.append([0] * target_size[0])
    # print("Board centered:")
    # print(*out, sep="\n")
    return out, target_size


def center_line(line, line_len, target_len):
    return [0] * ((target_len - line_len) // 2) + line + [0] * ((target_len - line_len + 1) // 2)
