import os

import load

from tkinter import filedialog

import utils
from gui.base.button import Button



class LoadButton(Button):
    """
    Button class for creating a load button in the GUI.
    Inherits from Button.

    Upon clicking, the button opens a file dialog to load a board from a file.
    """
    def __init__(self, setup, text):
        super().__init__(setup, text)

    def process_mouseclick(self, event) -> bool:
        clicked = super().process_mouseclick(event)

        if clicked:
            file = filedialog.askopenfile(initialdir=os.getcwd() + "\\saved_boards")
            if file is not None:
                self.game.rule, self.game.board, _ = load.load_board(filename=file.name)

                rule_string = utils.parse_dict_to_rule(self.game.rule)

                # update rulebox text
                self.game.rule_box.text = rule_string
                self.game.rule_box.move_cursor_to_end()
                # update rulebox label text
                self.game.rule_label.text = "Active rule: " + rule_string
                # load the name of the file into Save input-box
                self.game.save_box.text = file.name.split("/")[-1].split(".")[0]
                self.game.save_box.move_cursor_to_end()
        return clicked
