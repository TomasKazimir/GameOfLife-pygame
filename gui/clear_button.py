from gui.button import Button


class ClearButton(Button):
    def __init__(self, setup, text):
        super().__init__(setup, text)

    def process_mouseclick(self, event) -> bool:
        clicked = super().process_mouseclick(event)

        if clicked:
            self.game.board = [[0 for _ in range(self.game.board_size[0])]
                               for _ in range(self.game.board_size[1])]

        return clicked
