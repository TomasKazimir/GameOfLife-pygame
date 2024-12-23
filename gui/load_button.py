import os

import load

from tkinter import filedialog

from gui.button import Button



class LoadButton(Button):
    def __init__(self, setup, text):
        super().__init__(setup, text)

    def process_mouseclick(self, event) -> bool:
        clicked = super().process_mouseclick(event)

        if clicked:
            file = filedialog.askopenfile(initialdir=os.getcwd() + "\\saved_boards")
            if file is not None:
                self.game.board, _ = load.load_board(filename=file.name)
        return clicked
