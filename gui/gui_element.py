import pygame

from gui.gui_element_setup import GUIElementSetupDataclass


class GUIElement:
    def __init__(self, setup: GUIElementSetupDataclass):
        (self.screen,
         self.game,
         self.x, self.y,
         self.width, self.height) = setup.unpack()

        self.is_active = False

        self.surface = pygame.Surface((self.width, self.height))

    @property
    def collision_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def is_mouseclick_inside(self, mouse_pos):
        if self.collision_rect.collidepoint(mouse_pos):
            return True
        return False

    def draw(self):
        raise NotImplementedError

    def process_mouseclick(self, event) -> bool:
        """
        Process a mouseclick event.
        :param event: pygame event - must be a MOUSEBUTTONDOWN event
        :return: True if the element was clicked, False otherwise
        """
        assert event.type == pygame.MOUSEBUTTONDOWN, "Not a mouseclick event"
        mouse_pos = event.pos
        btn_pressed = event.button

        if not self.is_mouseclick_inside(mouse_pos):
            self.is_active = False
            return False  # user clicked outside element
        if btn_pressed != 1:  # 1 = LMB, 2 = MMB, 3 = RMB
            return False  # it isn't a left-click
        print(f"I ({self}) was clicked!")
        self.is_active = True
        return True

    def process_keypress(self, event):
        raise NotImplementedError
