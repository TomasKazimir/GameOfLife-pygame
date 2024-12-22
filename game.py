import pygame

import load
import logic
from gui.clear_button import ClearButton
from gui.gui_element_setup import GUIElementSetupDataclass
from gui.load_button import LoadButton
from gui.noise_button import NoiseButton
from gui.reset_button import ResetButton
from gui.rule_inputbox import RuleInputBox
from gui.save_inputbox import SaveInputBox


class Game:
    BOARD_SIZE = (100, 100)

    WINDOW_WIDTH = 1600
    WINDOW_HEIGHT = 1200

    SIDEPANEL_WIDTH = 400

    pygame.font.init()
    base_font = pygame.font.SysFont("consolas", 28)

    def __init__(self, width=WINDOW_WIDTH, height=WINDOW_HEIGHT, title="Game of Life", fps=60):
        pygame.init()

        # region WINDOW SETUP
        self.screen_size = (width, height)
        self.screen = pygame.display.set_mode(self.screen_size)
        pygame.display.set_caption(title)
        # endregion

        # region COLOR
        self.background_color = (0, 0, 0)
        self.cell_color = [0, 85, 170]
        self.color_step = [3, -3, 3]
        # endregion

        # region CELL-SPACE, RULE
        self.default_load = "saved_boards/.default_board.txt"
        board, size = load.load_board(filename=self.default_load, size=Game.BOARD_SIZE)
        self.board = board
        self.board_size = size
        self.board_size_px = width - Game.SIDEPANEL_WIDTH, height
        self.rule = {"R": [1], "B": [3], "S": [2, 3]}
        # endregion

        # region GUI
        self.sidepanel_size = Game.SIDEPANEL_WIDTH, height
        self.sidepanel_pos = (width - self.sidepanel_size[0], 0)
        self.sidepanel = pygame.Surface(self.sidepanel_size)

        self.rule_box = RuleInputBox(
            GUIElementSetupDataclass(self.screen, self,
                                     pos=(self.sidepanel_pos[0] + 25, 0),
                                     size=(350, 70)),
            title="Rule:")
        self.save_box = SaveInputBox(
            GUIElementSetupDataclass(self.screen, self,
                                     pos=(self.sidepanel_pos[0] + 25, 200),
                                     size=(350, 70)),
            title="Save current board as:")
        self.input_boxes = [
            self.rule_box,
            self.save_box,
        ]

        self.load_button = LoadButton(
            GUIElementSetupDataclass(self.screen, self,
                                     pos=(self.sidepanel_pos[0] + 25, 300),
                                     size=(200, 40)),
            text="Load board...")
        self.reset_button = ResetButton(
            GUIElementSetupDataclass(self.screen, self,
                                     pos=(self.sidepanel_pos[0] + 25, 600),
                                     size=(200, 40)),
            text="Reset board")
        self.random_button = NoiseButton(  # TODO
            GUIElementSetupDataclass(self.screen, self,
                                     pos=(self.sidepanel_pos[0] + 25, 700),
                                     size=(200, 40)),
            text="Insert noise")
        self.clear_button = ClearButton(
            GUIElementSetupDataclass(self.screen, self,
                                     pos=(self.sidepanel_pos[0] + 25, 800),
                                     size=(200, 40)),
            text="Clear board"
        )
        self.buttons = [
            self.load_button,
            self.reset_button,
            self.random_button,
            self.reset_button,
            self.clear_button
        ]
        # endregion GUI

        # region SIMULATION SPEED CONTROL
        self.clock = pygame.time.Clock()
        self.FPS = fps
        self.time = 0  # since last update
        self.sim_speed = 5  # (ideally) in Hz
        # endregion

        # STATE
        self.running = True
        self.paused = False

        # MOUSE-BUTTONS
        self.pressed = (False, False, False)

    @property
    def cell_size(self):
        """
        Returns cell size in pixels.
        (size of screen // cells in grid)
        """
        return (max(1, self.board_size_px[0] // self.board_size[0]),
                max(1, self.board_size_px[1] // self.board_size[1]))

    def clear_board(self):
        self.board = [[0 for _ in range(self.board_size[0])] for _ in range(self.board_size[1])]

    def set_rule(self, rule):
        self.rule = rule

    def run(self):
        while self.running:
            self.handle_events()
            self.update_board_state()

            self.clear_screen()
            self.draw_cells()
            self.draw_cursor()
            self.draw_gui()
            self.render_screen()
            self.time += self.clock.tick(self.FPS) / 1000

    def handle_events(self):
        events = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT:
                self.running = False
                return
            elif event.type == pygame.KEYDOWN:
                self.handle_keydown_event(event)
            elif event.type in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEMOTION):
                self.handle_mouse_event(event)

    def handle_keydown_event(self, event):
        # GUI
        for input_box in self.input_boxes:
            input_box.process_keypress(event)

        if event.key == pygame.K_SPACE:
            if not self.rule_box.is_active and not self.save_box.is_active:
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

    # region MOUSE

    def handle_mouse_event(self, event):
        self.pressed = pygame.mouse.get_pressed()

        if event.type == pygame.MOUSEBUTTONDOWN:
            for button in self.buttons:
                if button.process_mouseclick(event):
                    break  # once a button is clicked, no other can be clicked at the same time
            for input_box in self.input_boxes:  # each must check, can be active!
                input_box.process_mouseclick(event)

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
                self.board = logic.get_next_generation(self.board, self.rule)

    # region DRAWING
    def clear_screen(self):
        self.screen.fill(self.background_color)

    def draw_cells(self):
        self.change_cell_color()

        border_width = 0

        cell_width, cell_height = self.cell_size
        for x in range(self.board_size[0]):
            for y in range(self.board_size[1]):
                if self.board[y][x] == 1:
                    cell = pygame.Rect(cell_width * x + border_width, cell_height * y + border_width,
                                       cell_width - border_width * 2, cell_height - border_width * 2)
                    pygame.draw.rect(self.screen, self.cell_color, cell)

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

    def draw_gui(self):
        self.sidepanel.fill((50, 50, 50))
        self.screen.blit(self.sidepanel, self.sidepanel_pos)

        for element in self.buttons + self.input_boxes:
            element.draw()

    # endregion DRAWING

    def render_screen(self):
        pygame.display.update()
