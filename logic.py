def get_next_generation(board):
    m, n = len(board), len(board[0])
    next = [[0 for _ in range(n)] for _ in range(m)]
    brain = {
        "radius": 1,
        "die": (2, 4),
        "live": (3, 3)
    }

    rule = {
        "radius": 1,
        "die": (2, 3),
        "live": (3, 3)
    }

    for i in range(m):
        for j in range(n):
            count = 0 if board[i][j] == 0 else -1
            for di in range((i - rule["radius"]), (i + rule["radius"]) + 1):
                for dj in range((j - rule["radius"]), (j + rule["radius"]) + 1):
                    if board[di % m][dj % n] == 1:
                        count += 1
            if board[i][j] == 1:
                if count < rule["die"][0] or count > rule["die"][1]:
                    next[i][j] = 0
                else:
                    next[i][j] = 1
            elif board[i][j] == 0:
                if rule["live"][0] <= count <= rule["live"][1]:
                    next[i][j] = 1
    return next
