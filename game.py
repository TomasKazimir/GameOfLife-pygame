import pygame

import load
import logic


class Game:
    def __init__(self, width=1200, height=1200, title="Game of Life", fps=60):
        pygame.init()
        pygame.mouse.set_visible(False)

        self.screen_size = width, height
        self.screen = pygame.display.set_mode(self.screen_size)
        pygame.display.set_caption(title)
        self.clock = pygame.time.Clock()
        self.FPS = fps

        self.background_color = (0, 0, 0)  # Black background
        self.cell_color = (0, 85, 170)
        self.color_step = [3, -3, 3]

        board, size = load.load_board()
        self.board = board
        self.board_size = size

        self.running = True
        self.paused = False

        self.time = 0
        self.sim_speed = 60

        self.pressed = (False, False, False)

    def run(self):
        while self.running:
            self.clear_screen()
            self.handle_events()
            if not self.paused:
                if self.time >= 1 / self.sim_speed:
                    self.update_board_state()
                    self.time = 0
            self.draw_cells()
            self.draw_cursor()
            self.render_screen()
            self.time += self.clock.tick(self.FPS) / 1000

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.paused = not self.paused
                elif event.key == pygame.K_RIGHT:  # one sim step
                    if self.paused:
                        self.update_board_state()
                elif event.key == pygame.K_UP:  # speed up simulation
                    self.sim_speed += 1
                    if self.sim_speed > 244:
                        self.sim_speed = 244
                elif event.key == pygame.K_DOWN:
                    self.sim_speed -= 1
                    if self.sim_speed < 1:
                        self.sim_speed = 1

            if event.type in (pygame.MOUSEBUTTONDOWN,
                              pygame.MOUSEBUTTONUP,
                              pygame.MOUSEMOTION):
                self.handle_mouse_event()

    def handle_mouse_event(self):
        mouse_position = pygame.mouse.get_pos()
        x, y = self.get_mouse_cell(mouse_position)

        if x < 0 or y < 0 or x >= self.board_size[0] or y >= self.board_size[1]:
            return

        self.pressed = pygame.mouse.get_pressed()

        if self.pressed[0] or self.pressed[2]:
            if self.pressed[0]:  # LMB pressed
                self.board[y][x] = 1
            elif self.pressed[2]:  # RMB pressed
                self.board[y][x] = 0

    def get_mouse_cell(self, mouse_position):
        cell_x = mouse_position[0] // (self.screen_size[0] // self.board_size[0])
        cell_y = mouse_position[1] // (self.screen_size[1] // self.board_size[1])
        return cell_x, cell_y

    @property
    def cell_size(self):
        return (max(1, self.screen_size[0] // self.board_size[0]),
                max(1, self.screen_size[1] // self.board_size[1]))

    def draw_cells(self):
        self.change_cell_color()

        cell_width, cell_height = self.cell_size
        for x in range(self.board_size[0]):
            for y in range(self.board_size[1]):
                if self.board[y][x] == 1:
                    cell = pygame.Rect(cell_width * x + 1, cell_height * y + 1, cell_width - 2, cell_height - 2)
                    pygame.draw.rect(self.screen, self.cell_color, cell)

    def update_board_state(self, steps=1):
        while steps > 0:
            steps -= 1
            self.board = logic.get_next_generation(self.board)

    def change_cell_color(self):
        new_color = []
        for i, c in enumerate(self.cell_color):
            c += self.color_step[i]
            if not 0 <= c <= 255:
                self.color_step[i] *= -1
                if c < 0:
                    c = 0
                else:
                    c = 255
            new_color.append(c)
        self.cell_color = tuple(new_color)

    def clear_screen(self):
        self.screen.fill(self.background_color)

    def draw_cursor(self, border_width=1):
        x, y = self.get_mouse_cell(pygame.mouse.get_pos())
        cell = pygame.Rect(self.cell_size[0] * x, self.cell_size[1] * y,
                           self.cell_size[0], self.cell_size[1])
        pygame.draw.rect(self.screen, (255, 0, 0), cell, border_width)

    def render_screen(self):
        pygame.display.update()
