from __future__ import annotations

import os
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game import Game


def save_board(game: Game, filename):
    with open(os.getcwd() + "\\saved_boards\\" + filename + ".txt", "w+") as f:
        size = ";".join(map(str, game.board_size))
        f.write(size + "\n")
        for line in game.board:
            line = "".join(["." if char == 0 else "o" for char in line])
            f.write(line + "\n")
