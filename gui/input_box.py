import pygame
import pyperclip

from gui.gui_element import GUIElement


class InputBox(GUIElement):
    color_active = (200, 150, 150)
    color_inactive = (150, 150, 150)
    font_color = (10, 10, 10)

    pygame.font.init()
    title_font = pygame.font.SysFont("consolas", 28)
    value_font = pygame.font.SysFont("consolas", 20)
    cursor = "."

    def __init__(self, setup, title="Title:"):
        super().__init__(setup)

        self.title = title
        self.value = ""
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
                pyperclip.copy(self.value)
                return False
            elif key == pygame.K_v:
                self.value += pyperclip.paste()
                return False
        else:
            self.add_char(event.unicode)

        return False

    def increment_cursor(self):
        self.cursor_pos = min(self.cursor_pos + 1, len(self.value))

    def decrement_cursor(self):
        self.cursor_pos = max(self.cursor_pos - 1, 0)

    def move_cursor_to_end(self):
        self.cursor_pos = len(self.value)

    def backspace(self):
        if self.cursor_pos == 0:
            return
        v1 = self.value[:self.cursor_pos - 1]
        v2 = self.value[self.cursor_pos:]
        self.value = v1 + v2
        self.decrement_cursor()

    def add_char(self, char):
        v1 = self.value[:self.cursor_pos]
        v2 = self.value[self.cursor_pos:]
        self.value = v1 + char + v2
        self.cursor_pos += len(char)

    def clear_input(self):
        self.value = ""
        self.cursor_pos = 0

    def draw(self):
        self.surface.fill(self.color_active if self.is_active else self.color_inactive)
        self.surface.blit(self.title_surface, (5, 5))
        text_surface = self.value_font.render(self.value, True, self.font_color)
        self.surface.blit(text_surface, (5, self.height // 2 + 3))
        if self.is_active:
            cursor_string = " " * self.cursor_pos + self.cursor
            cursor_surface = self.value_font.render(cursor_string, True, (50, 50, 50))
            self.surface.blit(cursor_surface, (0, self.height // 2 + 5))
        self.screen.blit(self.surface, (self.x + 3, self.y + 3) if self.is_active else (self.x, self.y))

#
# if __name__ == "__main__":
#     pygame.init()
#     clock = pygame.time.Clock()
#     screen = pygame.display.set_mode([400, 200])
#
#     input_box = InputBox(screen, (100, 85))
#
#     while True:
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 pygame.quit()
#                 sys.exit()
#
#             if event.type == pygame.MOUSEBUTTONDOWN:
#                 input_box.process_mouseclick(event)
#
#             if event.type == pygame.KEYDOWN:
#                 input_box.process_keypress(event)
#
#         screen.fill((255, 255, 255))
#
#         input_box.draw()
#         pygame.display.flip()
#         clock.tick(60)
