import pygame

from gui.gui_element_setup import GUIElementInfo


class GUIElement:
    """
    Base class for GUI elements.
    """
    def __init__(self, setup: GUIElementInfo):
        """
        Initializes a GUIElement with the given setup information.

        :param setup: GUIElementInfo object containing setup information
        """
        (self.screen,
         self.game,
         self.x, self.y,
         self.width, self.height) = setup.unpack()

        self.is_active = False

        self.surface = pygame.Surface((self.width, self.height))

    @property
    def collision_rect(self):
        """
        Returns a pygame.Rect object representing the collision rectangle of the element.
        """
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def is_mouseclick_inside(self, mouse_pos):
        """
        Checks if a mouse click is inside the element's collision rectangle.

        :param mouse_pos: Tuple containing the x and y coordinates of the mouse position
        :return: True if the mouse click is inside the element, False otherwise
        """
        if self.collision_rect.collidepoint(mouse_pos):
            return True
        return False

    def draw(self):
        """
        Draws the GUI element. Must be implemented by subclasses.
        """
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
        print(f"Clicked on {self.__repr__().split(" at")[0].replace("<", "")}")
        self.is_active = True
        return True

    def process_keypress(self, event):
        """
        Processes a key press event. Must be implemented by subclasses.

        :param event: pygame event - should be a KEYDOWN event
        """
        raise NotImplementedError
