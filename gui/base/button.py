import pygame

from gui.base.gui_element import GUIElement


class Button(GUIElement):
    """
    Button class for creating buttons in the GUI.
    Inherits from GUIElement.
    """

    color_active = (200, 50, 50)
    color_inactive = (150, 100, 150)
    font_color = (10, 10, 10)

    pygame.font.init()
    text_font = pygame.font.SysFont("consolas", 28)

    def __init__(self, setup, text="Button"):
        super().__init__(setup)

        self.text = text

        self.text_surface = self.text_font.render(text, True, self.font_color)

    def draw(self):
        """
        Draws the button on the screen.
        :return: None
        """
        self.surface.fill(self.color_active if self.is_active else self.color_inactive)
        self.surface.blit(self.text_surface, (5, 8))
        self.screen.blit(self.surface, (self.x+3, self.y+3) if self.is_active else (self.x, self.y))
        self.is_active = False
