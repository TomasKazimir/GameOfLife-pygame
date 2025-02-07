from gui.base.button import Button


class ClearButton(Button):
    """
    Button class for creating a clear button in the GUI.
    Inherits from Button.

    Upon clicking, the button clears the board.
    """
    def __init__(self, setup, text):
        super().__init__(setup, text)

    def process_mouseclick(self, event) -> bool:
        clicked = super().process_mouseclick(event)

        if clicked:
            self.game.board = [[0 for _ in range(self.game.board_size[0])]
                               for _ in range(self.game.board_size[1])]

        return clicked
