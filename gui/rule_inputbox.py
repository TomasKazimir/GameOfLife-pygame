from gui.input_box import InputBox

import re

class RuleInputBox(InputBox):
    RULE_PATTERN = r"^R[1-9]{1}/B[0-9]+/S[0-9]+$"

    def __init__(self, setup, title):
        super().__init__(setup, title)

        self.value = "R1/B3/S23"
        self.is_rule_valid = False
        self.validate_rule()

        self.cursor_pos = len(self.value)
        
    def process_keypress(self, event):
        enter_pressed = super().process_keypress(event)
        
        if enter_pressed:
            self.convert_value_to_rule_format()
            self.validate_rule()
            if self.is_rule_valid:
                rule = self.parse_rule_to_dict()
                self.game.set_rule(rule)
                print(self.game.rule)
            self.move_cursor_to_end()


    def convert_value_to_rule_format(self):
        """
        Converts the `value` attribute to a specific format based on defined rules:
        - Digits are added directly to the new string.
        - Characters in "RBS" are prefixed with a '/' before adding.
        - Ensures the result doesn't start with a '/' if the processed string begins with one.

        :return: None
        """
        v = ""
        for char in self.value:
            char = char.upper()
            if char.isdigit():
                v += char.upper()
            elif char in "RBS" and char not in v:
                v += "/" + char.upper()

        if len(v) > 0 and v[0] == "/":
            v = v[1:]
        self.value = v

    def validate_rule(self):
        self.is_rule_valid = re.match(self.RULE_PATTERN, self.value)

    def parse_rule_to_dict(self):
        rule = {}
        last_char = ""
        for char in self.value:
            if char.isalpha():
                last_char = char
                rule[char] = []
            elif char.isdigit():
                if char not in rule[last_char]:
                    rule[last_char].append(int(char))
        return rule






            
        

