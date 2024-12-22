import pygame

import load
import logic
from input_box import InputBox


class Game:
    WINDOW_WIDTH = 1400
    WINDOW_HEIGHT = 1200

    SIDEPANEL_WIDTH = 200

    pygame.font.init()
    base_font = pygame.font.SysFont("consolas", 28)

    def __init__(self, width=WINDOW_WIDTH, height=WINDOW_HEIGHT, title="Game of Life", fps=60):
        pygame.init()

        # window setup
        self.screen_size = (width, height)
        self.screen = pygame.display.set_mode(self.screen_size)
        pygame.display.set_caption(title)

        # color
        self.background_color = (0, 0, 0)
        self.cell_color = [0, 85, 170]
        self.color_step = [3, -3, 3]

        # cell board
        board, size = load.load_board()
        self.board = board
        self.board_size = size
        self.board_size_px = width - Game.SIDEPANEL_WIDTH, height

        # sidepanel
        self.sidepanel_size = Game.SIDEPANEL_WIDTH, height
        self.sidepanel_pos = (width - self.sidepanel_size[0], 0)
        self.sidepanel = pygame.Surface(self.sidepanel_size)

        self.rulebox = InputBox(self.screen,
                                pos=(self.sidepanel_pos[0], 50))

        # state
        self.running = True
        self.paused = False

        # simulation speed
        self.clock = pygame.time.Clock()
        self.FPS = fps
        self.time = 0        # since last update
        self.sim_speed = 100  # (ideally) in Hz

        # mouse
        self.pressed = (False, False, False)

    @property
    def cell_size(self):
        """
        Returns cell size in pixels.
        (size of screen // cells in grid)
        """
        return (max(1, self.board_size_px[0] // self.board_size[0]),
                max(1, self.board_size_px[1] // self.board_size[1]))

    def run(self):
        while self.running:
            self.handle_events()
            self.update_board_state()

            self.clear_screen()
            self.draw_cells()
            self.draw_cursor()
            self.draw_GUI()
            self.render_screen()
            self.time += self.clock.tick(self.FPS) / 1000

    def handle_events(self):
        events = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT:
                self.running = False
                return

            elif event.type == pygame.KEYDOWN:
                if self.rulebox.process_keypress(event):
                    continue

                if event.key == pygame.K_SPACE:
                    self.paused = not self.paused

                elif event.key == pygame.K_RIGHT:  # step simulation
                    if self.paused:
                        self.update_board_state(forced=True)

                elif event.key == pygame.K_UP:  # speed up simulation
                    self.sim_speed += 1
                    if self.sim_speed > 244:
                        self.sim_speed = 244

                elif event.key == pygame.K_DOWN:  # slow down simulation
                    self.sim_speed -= 1
                    if self.sim_speed < 1:
                        self.sim_speed = 1

            elif event.type in (pygame.MOUSEBUTTONDOWN,
                                pygame.MOUSEBUTTONUP,
                                pygame.MOUSEMOTION):
                self.handle_mouse_event(event)

            # else:
            #     print(event.type, event)

    # region MOUSE

    def handle_mouse_event(self, event):
        self.pressed = pygame.mouse.get_pressed()

        if event.type == pygame.MOUSEBUTTONDOWN:
            self.rulebox.process_mouseclick(event)

        mouse_pos = pygame.mouse.get_pos()
        if self.is_mouse_over_board(mouse_pos):
            pygame.mouse.set_visible(False)
            if sum(self.pressed):  # mouse-button(s) pressed
                cell_x, cell_y = self.get_mouse_cell(mouse_pos)
                self.toggle_cell_state(cell_x, cell_y)
        else:
            pygame.mouse.set_visible(True)

    def toggle_cell_state(self, cell_x, cell_y):
        if self.pressed[0]:  # LMB
            self.set_cell_state(cell_x, cell_y)
        elif self.pressed[2]:  # RMB
            self.set_cell_state(cell_x, cell_y, 0)

    def set_cell_state(self, cell_x, cell_y, state=1):
        self.board[cell_y][cell_x] = state

    def get_mouse_cell(self, mouse_position=None) -> tuple[int, int]:
        """Returns the position of the cell under the mouse cursor."""
        if mouse_position is None:
            mouse_position = pygame.mouse.get_pos()
        cell_x = mouse_position[0] // (self.board_size_px[0] // self.board_size[0])
        cell_y = mouse_position[1] // (self.board_size_px[1] // self.board_size[1])
        return cell_x, cell_y

    def is_mouse_over_board(self, mouse_position=None):
        x, y = self.get_mouse_cell(mouse_position)
        if x < 0 or x >= self.board_size[0] or y < 0 or y >= self.board_size[1]:  # mouse outside board space
            return False
        return True

    # endregion MOUSE

    def update_board_state(self, forced=False, steps=1):
        if self.paused and not forced:
            return

        if self.time >= 1 / self.sim_speed:
            self.time = 0
            while steps > 0:
                steps -= 1
                self.board = logic.get_next_generation(self.board)

    # region DRAWING
    def clear_screen(self):
        self.screen.fill(self.background_color)

    def draw_cells(self):
        self.change_cell_color()

        cell_width, cell_height = self.cell_size
        for x in range(self.board_size[0]):
            for y in range(self.board_size[1]):
                if self.board[y][x] == 1:
                    cell = pygame.Rect(cell_width * x + 1, cell_height * y + 1, cell_width - 2, cell_height - 2)
                    pygame.draw.rect(self.screen, self.cell_color, cell)

                    def change_cell_color(self):
                        for i in range(3):
                            if not 0 <= self.cell_color[i] + self.color_step[i] <= 255:
                                self.color_step[i] *= -1
                            self.cell_color[i] += self.color_step[i]

    def change_cell_color(self):
        for i in range(3):
            if not 0 <= self.cell_color[i] + self.color_step[i] <= 255:
                self.color_step[i] *= -1
            self.cell_color[i] += self.color_step[i]

    def draw_cursor(self, border_width=2):
        mouse_pos = pygame.mouse.get_pos()
        if not self.is_mouse_over_board(mouse_pos):
            return
        x, y = self.get_mouse_cell(mouse_pos)
        cell = pygame.Rect(self.cell_size[0] * x, self.cell_size[1] * y,
                           self.cell_size[0], self.cell_size[1])
        pygame.draw.rect(self.screen, (255, 0, 0), cell, border_width)

    def draw_GUI(self):
        self.sidepanel.fill((50, 50, 50))
        self.screen.blit(self.sidepanel, self.sidepanel_pos)

        self.rulebox.draw()


    # endregion DRAWING

    def render_screen(self):
        pygame.display.update()
