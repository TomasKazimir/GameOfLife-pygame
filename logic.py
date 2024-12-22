def get_next_generation(board, rule=None):
    m, n = len(board), len(board[0])
    next = [[0 for _ in range(n)] for _ in range(m)]

    brain = {
        "radius": 1,
        "die": (2, 4),
        "live": (3, 3)
    }

    if rule is None:
        rule = {
            "R": [1],
            "B": [3],
            "S": [2, 3]
        }

    for i in range(m):
        for j in range(n):
            cell = board[i][j]
            count = 0 if board[i][j] == 0 else -1
            # NEIGHBOURS
            for di in range(
                    max(0, i - rule["R"][0]), min(m, (i + rule["R"][0]) + 1)):
                for dj in range(
                        max(0, j - rule["R"][0]), min(n, (j + rule["R"][0]) + 1)):
                    if board[di % m][dj % n] == 1:
                        count += 1
            if cell == 1 and count in rule["S"]:
                    next[i][j] = 1
            elif cell == 0 and count in rule["B"]:
                    next[i][j] = 1
    return next
