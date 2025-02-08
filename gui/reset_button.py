import load
import utils
from gui.base.button import Button


class ResetButton(Button):
    """
    Button class for creating a reset button in the GUI.
    Inherits from Button.

    Upon clicking, the button resets the game to the initial state.
    """
    def __init__(self, setup, text):
        super().__init__(setup, text)

    def process_mouseclick(self, event) -> bool:
        clicked = super().process_mouseclick(event)

        if clicked:
            self.game.rule, self.game.board, _ = \
                load.load_board(filename=self.game.startup_board_file, size=self.game.board_size)

            rule_string = utils.parse_dict_to_rule(self.game.rule)
            self.game.rule_box.text = rule_string
            self.game.rule_box.move_cursor_to_end()
            self.game.rule_label.text = "Active rule: " + rule_string

        return clicked
