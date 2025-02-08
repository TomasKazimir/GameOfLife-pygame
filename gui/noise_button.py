import random

from gui.base.button import Button


class NoiseButton(Button):
    """
    Button class for creating a noise button in the GUI.
    Inherits from Button.

    Upon clicking, the button fills the board with random noise.
    """
    def __init__(self, setup, text):
        super().__init__(setup, text)

    def process_mouseclick(self, event) -> bool:
        clicked = super().process_mouseclick(event)

        if clicked:
            self.game.board = [[random.randint(0, 1)
                                for _ in range(self.game.board_size[0])]
                               for _ in range(self.game.board_size[1])]

        return clicked
