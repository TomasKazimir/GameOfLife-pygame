from gui.base.input_box import InputBox
import save


class SaveInputBox(InputBox):
    """
    Input box for saving a board.
    Inherits from InputBox.

    Upon pressing enter, saves the board to a file with the name given in the input box.
    """

    def __init__(self, setup, title):
        super().__init__(setup, title)

    def process_keypress(self, event):
        """
        Upon pressing enter, saves the board to a file with the name given in the input box.
        The input box must be active for the save to happen.
        The input box is deactivated after the save.

        :param event: pygame event
        :return: None
        """
        enter_pressed_and_element_active = super().process_keypress(event)

        if enter_pressed_and_element_active:
            save.save_board(self.game.board,
                            self.game.board_size,
                            self.game.rule,
                            filename=self.text)

            print("Board saved")
