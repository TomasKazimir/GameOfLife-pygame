Board = list[list[int]]

def get_next_generation(board: Board, rule: dict = None):
    """
    Returns the next generation of the board based on the rule provided.
    (If there is no rule, the default rule is used)

    The rule is a dictionary with the following keys:
    - R: radius in which cells are considered neighbours
    - B: how many neighbours are required for a dead cell to become alive
    - S: how many neighbours are required for a live cell to remain alive

    R1/B3/S23 is the default rule for the game of life.

    :param board: 2D list of integers representing the board
    :param rule: dictionary with keys R, B, S
    :return: 2D list of integers representing the next generation of the board
    """
    m, n = len(board), len(board[0])
    next_gen = [[0 for _ in range(n)] for _ in range(m)]

    if rule is None:  # default game of life rule
        rule = {
            "R": [1],
            "B": [3],
            "S": [2, 3]
        }

    for i in range(m):
        for j in range(n):
            cell = board[i][j]
            num_of_live_neighs = 0 if cell == 0 else -1
            # NEIGHBOURS
            for di in range(
                    max(0, i - rule["R"][0]), min(m, (i + rule["R"][0]) + 1)):
                for dj in range(
                        max(0, j - rule["R"][0]), min(n, (j + rule["R"][0]) + 1)):
                    if board[di % m][dj % n] == 1:
                        num_of_live_neighs += 1
            if cell == 1 and num_of_live_neighs in rule["S"]:
                next_gen[i][j] = 1
            elif cell == 0 and num_of_live_neighs in rule["B"]:
                next_gen[i][j] = 1
    return next_gen
