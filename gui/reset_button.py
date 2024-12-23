import load
from gui.button import Button


class ResetButton(Button):
    def __init__(self, setup, text):
        super().__init__(setup, text)

    def process_mouseclick(self, event) -> bool:
        clicked = super().process_mouseclick(event)

        if clicked:
            self.game.board, _ = load.load_board(filename=self.game.default_load,
                                                 size=self.game.board_size)

        return clicked
