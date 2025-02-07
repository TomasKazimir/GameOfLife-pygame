import pygame

from gui.gui_element import GUIElement


class Label(GUIElement):
    background_color = (80, 10, 80)
    font_color = (200, 200, 200)

    pygame.font.init()
    text_font = pygame.font.SysFont("consolas", 20, bold=False)

    def __init__(self, setup, text="I'm a Label"):
        super().__init__(setup)

        self.text = text

    def draw(self):
        """
        Draws the label on the screen.
        :return:
        """
        text_surface = self.text_font.render(self.text, True, self.font_color, self.background_color)
        self.screen.blit(text_surface, (self.x, self.y))
