import pygame
import pyperclip

from gui.base.gui_element import GUIElement


class InputBox(GUIElement):
    color_active = (200, 150, 150)
    color_inactive = (150, 150, 150)
    font_color = (10, 10, 10)

    pygame.font.init()
    title_font = pygame.font.SysFont("consolas", 28)
    value_font = pygame.font.SysFont("consolas", 20)
    cursor = "|" # Cursor character

    def __init__(self, setup, title="Title:"):
        super().__init__(setup)

        self.title = title
        self.text = ""
        self.cursor_pos = 0

        self.title_surface = self.title_font.render(self.title, True, self.font_color, (255, 255, 255))

    def process_keypress(self, event) -> bool:
        """
        Process a keypress event.
        :param event: pygame event
        :return: True if Enter was pressed and the input-box was active, False otherwise
        """
        assert event.type == pygame.KEYDOWN, "Not a keydown event"
        if not self.is_active:
            return False

        key = event.key
        if key == pygame.K_RETURN or key == pygame.K_KP_ENTER:
            self.is_active = False
            return True
        if key == pygame.K_ESCAPE:
            self.is_active = False
        elif key == pygame.K_BACKSPACE:
            self.backspace()
        elif key == pygame.K_DELETE:
            self.clear_input()
        elif key == pygame.K_LEFT:
            self.decrement_cursor()
        elif key == pygame.K_RIGHT:
            self.increment_cursor()
        elif event.mod & pygame.KMOD_CTRL:
            if key == pygame.K_c:
                pyperclip.copy(self.text)
                return False
            elif key == pygame.K_v:
                self.text += pyperclip.paste()
                return False
        else:
            self.add_char(event.unicode)

        return False

    def increment_cursor(self) -> None:
        """
        Increment the cursor position by 1 - shift to the right.
        :return: None
        """
        self.cursor_pos = min(self.cursor_pos + 1, len(self.text))

    def decrement_cursor(self) -> None:
        """
        Decrement the cursor position by 1 - shift to the left.
        :return: None
        """
        self.cursor_pos = max(self.cursor_pos - 1, 0)

    def move_cursor_to_end(self) -> None:
        """
        Move the cursor to the end of the text.
        :return: None
        """
        self.cursor_pos = len(self.text)

    def backspace(self) -> None:
        """
        Remove the character before the cursor.
        :return: None
        """
        if self.cursor_pos == 0:
            return
        v1 = self.text[:self.cursor_pos - 1]
        v2 = self.text[self.cursor_pos:]
        self.text = v1 + v2
        self.decrement_cursor()

    def add_char(self, char) -> None:
        """
        Add a character at the cursor position.
        :param char: str
        :return: None
        """
        v1 = self.text[:self.cursor_pos]
        v2 = self.text[self.cursor_pos:]
        self.text = v1 + char + v2
        self.cursor_pos += len(char)


    def clear_input(self) -> None:
        """
        Clear the input box.
        :return: None
        """
        self.text = ""
        self.cursor_pos = 0


    def draw(self):
        """
        Draw the input box on the screen.
        :return: None
        """
        self.surface.fill(self.color_active if self.is_active else self.color_inactive)
        self.surface.blit(self.title_surface, (5, 5))
        text_surface = self.value_font.render(self.text, True, self.font_color)
        self.surface.blit(text_surface, (5, self.height // 2 + 3))
        if self.is_active:
            cursor_string = " " * self.cursor_pos + self.cursor
            cursor_surface = self.value_font.render(cursor_string, True, (255, 255, 255))
            self.surface.blit(cursor_surface, (0, self.height // 2))
        self.screen.blit(self.surface, (self.x + 3, self.y + 3) if self.is_active else (self.x, self.y))
