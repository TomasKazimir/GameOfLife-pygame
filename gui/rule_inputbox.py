import pygame

import logic
from gui.base.input_box import InputBox


class RuleInputBox(InputBox):
    """
    InputBox class for creating a rule input box in the GUI.
    Inherits from InputBox.

    Upon pressing Enter, the input box validates the rule and updates the game rule.
    """
    def __init__(self, setup, title, text):
        super().__init__(setup, title)

        self.text = text
        self.valid = logic.is_rule_valid(self.text)

        self.cursor_pos = len(self.text)
        
    def process_keypress(self, event):
        """
        Upon pressing Enter, the input box validates the rule and updates the game rule.
        The input box must be active for the rule to be updated.
        The input box is deactivated after the rule is updated.

        :param event: pygame event
        :return: None
        """
        enter_pressed = super().process_keypress(event)
        
        if enter_pressed:
            new_rule = logic.format_text_to_rule(self.text)
            self.valid = logic.is_rule_valid(self.text)

            if self.valid:
                self.text = new_rule
                self.game.rule = logic.parse_rule_to_dict(new_rule)

                self.game.rule_label.text = "Active rule: " + self.text
            else:
                last_valid_rule = logic.parse_dict_to_rule(self.game.rule)
                self.game.rule_label.text = f"Invalid rule! ({last_valid_rule})"
            self.move_cursor_to_end()





            
        

