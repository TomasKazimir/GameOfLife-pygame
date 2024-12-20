type Matrix = list[list]
type Size = tuple[int, int]


def get_next_generation(board) -> tuple[Matrix, Size]:
    m, n = len(board), len(board[0])
    next = [[0 for _ in range(n)] for _ in range(m)]
    for i in range(m):
        for j in range(n):
            count = 0 if board[i][j] == 0 else -1
            for di in range(i - 1, i + 2):
                for dj in range(j - 1, j + 2):
                    if board[di % m][dj % n] == 1:
                        count += 1
            if board[i][j] == 1:
                if count < 2 or count > 3:
                    next[i][j] = 0
                else:
                    next[i][j] = 1
            elif board[i][j] == 0:
                if count == 3:
                    next[i][j] = 1
    return next
