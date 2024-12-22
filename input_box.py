import sys

import pygame


class InputBox:
    color_active = (200, 150, 150)
    color_inactive = (150, 150, 150)

    pygame.font.init()
    base_font = pygame.font.SysFont("consolas", 28)

    def __init__(self, screen, pos, width=200, height=70, title="InputBox:"):
        self.screen = screen
        self.pos = pos
        self.width = width
        self.height = height
        self.title = title

        self.value = ""
        self.is_active = False

        self.surface = pygame.Surface((self.width, self.height))
        self.title_surface = self.base_font.render(self.title, True, (10, 10, 10), (255, 255, 255))

    @property
    def collision_rect(self):
        return pygame.Rect(self.pos[0], self.pos[1], self.width, self.height)

    def is_mouseclick_inside(self, mouse_pos):
        if self.collision_rect.collidepoint(mouse_pos):
            return True
        return False

    def process_mouseclick(self, event):
        assert event.type == pygame.MOUSEBUTTONDOWN, "Not a mouse button event"
        mouse_pos = event.pos
        button = event.button
        if not self.is_mouseclick_inside(mouse_pos):
            self.is_active = False
            return
        if button != 1:
            return
        self.is_active = True

    def process_keypress(self, event) -> bool:
        assert event.type == pygame.KEYDOWN, "Not a keydown event"
        if not self.is_active:
            return False

        key = event.key
        if key == pygame.K_RETURN or key == pygame.K_KP_ENTER:
            self.is_active = False
            # todo: text entered, should now be loaded by other code
        if key == pygame.K_ESCAPE:
            self.is_active = False
        elif key == pygame.K_BACKSPACE:
            self.value = self.value[:-1]
        else:
            self.value += event.unicode

        return True

    def draw(self):
        self.surface.fill(self.color_active if self.is_active else self.color_inactive)
        self.surface.blit(self.title_surface, (5, 5))
        text_surface = self.base_font.render(self.value, True, (10, 10, 10))
        self.surface.blit(text_surface, (5, self.height//2 + 5))
        self.screen.blit(self.surface, (self.pos[0], self.pos[1]))


if __name__ == "__main__":
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode([400, 200])

    input_box = InputBox(screen, (100, 85))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                input_box.process_mouseclick(event)

            if event.type == pygame.KEYDOWN:
                input_box.process_keypress(event)

        screen.fill((255, 255, 255))

        input_box.draw()
        pygame.display.flip()
        clock.tick(60)
