from gui.input_box import InputBox
import save


class SaveInputBox(InputBox):
    def __init__(self, setup, title):
        super().__init__(setup, title)

    def process_keypress(self, event):
        enter_pressed = super().process_keypress(event)

        if enter_pressed:
            save.save_board(self.game, self.value)
