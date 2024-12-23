from gui.button import Button

import random

class NoiseButton(Button):
    def __init__(self, setup, text):
        super().__init__(setup, text)

    def process_mouseclick(self, event) -> bool:
        clicked = super().process_mouseclick(event)

        if clicked:
            self.game.board = [[random.randint(0,1) for _ in range(self.game.board_size[0])]
                               for _ in range(self.game.board_size[1])]