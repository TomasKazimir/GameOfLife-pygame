import pygame

import load
import generation
import utils
from gui.base.label import Label
from gui.clear_button import ClearButton
from gui.base.gui_element_setup import GUIElementInfo
from gui.load_button import LoadButton
from gui.noise_button import NoiseButton
from gui.reset_button import ResetButton
from gui.rule_inputbox import RuleInputBox
from gui.save_inputbox import SaveInputBox


class Game:
    BOARD_SIZE = (100, 100)

    WINDOW_WIDTH = 1200
    WINDOW_HEIGHT = 800

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

        # STATE
        self.running = True
        self.paused = False

        # region COLOR
        self.background_color = (0, 0, 0)
        self.cell_color = [0, 85, 170]
        self.color_step = [3, -3, 3]
        # endregion

        # region load BOARD, RULE
        self.startup_board_file = "saved_boards/.default_board.txt"
        rule, board, size = load.load_board(filename=self.startup_board_file, size=Game.BOARD_SIZE)
        self.board = board
        self.board_size = size
        self.board_size_px = width - Game.SIDEPANEL_WIDTH, height
        self.rule = rule
        # endregion

        # region GUI
        self.sidepanel_size = Game.SIDEPANEL_WIDTH, height
        self.sidepanel_pos = (width - self.sidepanel_size[0], 0)
        self.sidepanel = pygame.Surface(self.sidepanel_size)

        offset = 25

        # INPUT BOXES
        self.rule_box = RuleInputBox(
            GUIElementInfo(self.screen, self,
                           pos=(self.sidepanel_pos[0] + offset, 0),
                           size=(350, 70)),
            title="Enter rule:",
            text=utils.parse_dict_to_rule(self.rule))
        self.save_box = SaveInputBox(
            GUIElementInfo(self.screen, self,
                           pos=(self.sidepanel_pos[0] + offset, 200),
                           size=(350, 70)),
            title="Save current board as:")

        self.input_boxes = [
            self.rule_box,
            self.save_box,
        ]

        # BUTTONS
        self.load_button = LoadButton(
            GUIElementInfo(self.screen, self,
                           pos=(self.sidepanel_pos[0] + offset, 300),
                           size=(200, 40)),
            text="Load board...")
        self.reset_button = ResetButton(
            GUIElementInfo(self.screen, self,
                           pos=(self.sidepanel_pos[0] + offset, 500),
                           size=(200, 40)),
            text="Reset game")
        self.noise_button = NoiseButton(
            GUIElementInfo(self.screen, self,
                           pos=(self.sidepanel_pos[0] + offset, 600),
                           size=(200, 40)),
            text="Insert noise")
        self.clear_button = ClearButton(
            GUIElementInfo(self.screen, self,
                           pos=(self.sidepanel_pos[0] + offset, 700),
                           size=(200, 40)),
            text="Clear board")

        self.buttons = [
            self.load_button,
            self.reset_button,
            self.noise_button,
            self.reset_button,
            self.clear_button
        ]

        # LABELS
        self.rule_label = Label(
            GUIElementInfo(self.screen, self,
                           pos=(self.sidepanel_pos[0] + offset, 75)),
            text="Active rule: " + self.rule_box.text)
        self.sim_speed_label = Label(
            GUIElementInfo(self.screen, self,
                           pos=(self.sidepanel_pos[0] + offset, 100)),
            text=f"Simulation speed: {30}")
        self.pause_label = Label(
            GUIElementInfo(self.screen, self,
                           pos=(self.sidepanel_pos[0] + offset, 125)),
            text="Paused" if self.paused else "Running")

        self.labels = [
            self.rule_label,
            self.sim_speed_label,
            self.pause_label
        ]
        # endregion GUI

        # region SIMULATION SPEED CONTROL
        self.clock = pygame.time.Clock()
        self.FPS = fps
        self.time = 0  # since last update
        self.sim_speed = 30  # (ideally) in Hz
        # endregion

        # MOUSE-BUTTONS  LMB    RMB    MMB
        self.pressed = (False, False, False)

    @property
    def cell_size(self):
        """
        Returns cell size in pixels.
        cell_size_x_coor := (width of screen // # of cells in a row)
        cell_size_y_coor := (height of screen // # of cells in a column)
        """
        return (max(1, self.board_size_px[0] // self.board_size[0]),
                max(1, self.board_size_px[1] // self.board_size[1]))

    def clear_board(self) -> None:
        """
        Sets the board to all zeroes.
        """
        self.board = [[0 for _ in range(self.board_size[0])] for _ in range(self.board_size[1])]

    def loop(self) -> None:
        """
        Game loop function.
        """
        while self.running:
            self.handle_events()
            self.update_board_state()
            self.clear_screen()
            self.draw_cells()
            self.draw_cursor()
            self.draw_gui()
            self.render_screen()
            self.time += self.clock.tick(self.FPS) / 1000

    def handle_events(self) -> None:
        """
        Handles pygame events - user interaction with the GUI.
        :return:
        """
        events = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT:
                self.running = False
                return
            elif event.type == pygame.KEYDOWN:
                self.handle_keydown_event(event)
            elif event.type in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEMOTION):
                self.handle_mouse_event(event)

    def handle_keydown_event(self, event) -> None:
        """
        Handles pygame.KEYDOWN events.

        :param event: pygame KEYDOWN event
        :return: None
        """
        for input_box in self.input_boxes:
            input_box.process_keypress(event)

        if event.key == pygame.K_SPACE:
            if not self.rule_box.is_active and not self.save_box.is_active:
                self.paused = not self.paused
                self.pause_label.text = "Paused" if self.paused else "Running"
        elif event.key == pygame.K_RIGHT:  # step simulation
            if self.paused:
                self.update_board_state(forced=True)
        elif event.key == pygame.K_UP:  # speed up simulation
            self.sim_speed = (5 + self.sim_speed) // 5 * 5
            if self.sim_speed > 100:
                self.sim_speed = 100
            self.sim_speed_label.text = f"Simulation speed: {self.sim_speed}"
        elif event.key == pygame.K_DOWN:  # slow down simulation
            self.sim_speed -= 5
            if self.sim_speed < 1:
                self.sim_speed = 1
            self.sim_speed_label.text = f"Simulation speed: {self.sim_speed}"

    # region MOUSE
    def handle_mouse_event(self, event) -> None:
        """
        Handles pygame.MOUSE events.

        :param event: pygame MOUSE event
        :return: None
        """
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

    def toggle_cell_state(self, cell_x: int, cell_y: int) -> None:
        """
        Toggles the state of the cell under the mouse cursor.

        :param cell_x: row coordinate
        :param cell_y: column coordinate
        :return: None
        """
        if self.pressed[0]:  # LMB is down
            self.set_cell_state(cell_x, cell_y, 1)  # 1 = alive
        elif self.pressed[2]:  # RMB is down
            self.set_cell_state(cell_x, cell_y, 0)  # 0 = dead

    def set_cell_state(self, cell_x, cell_y, state=1):
        """
        Sets the state of the cell at (cell_x, cell_y) to the given state.

        :param cell_x: row coordinate
        :param cell_y: column coordinate
        :param state: default is 1 (alive)
        :return: None
        """
        self.board[cell_y][cell_x] = state

    def get_mouse_cell(self, mouse_position: tuple=None) -> tuple[int, int]:
        """
        Returns the position (column, row) of the cell under the mouse cursor.

        :param mouse_position: (x, y) tuple, optional
        :return: (column, row) tuple
        """
        if mouse_position is None:
            mouse_position = pygame.mouse.get_pos()
        cell_x = mouse_position[0] // (self.board_size_px[0] // self.board_size[0])
        cell_y = mouse_position[1] // (self.board_size_px[1] // self.board_size[1])
        return cell_x, cell_y

    def is_mouse_over_board(self, mouse_position:tuple=None) -> bool:
        """
        Returns True if the mouse is over the board space, False otherwise.

        :param mouse_position: (x, y) tuple, optional
        :return: bool
        """
        x, y = self.get_mouse_cell(mouse_position)
        if x < 0 or x >= self.board_size[0] or y < 0 or y >= self.board_size[1]:  # mouse outside board space
            return False
        return True

    # endregion MOUSE

    def update_board_state(self, forced=False, steps=1) -> None:
        """
        Updates the board state by given number of steps.

        :param forced: if True, the simulation will run even if paused
        :param steps: how many steps to simulate
        :return: None
        """
        if self.paused and not forced:
            return

        if self.time >= 1 / self.sim_speed:
            self.time = 0
            while steps > 0:
                steps -= 1
                self.board = generation.get_next_generation(self.board, self.rule)

    # region DRAWING
    def clear_screen(self) -> None:
        """
        Clears the screen by filling it with the background color.
        """
        self.screen.fill(self.background_color)

    def draw_cells(self) -> None:
        """
        Draws the cells on the screen. Cells that are alive (value 1) are drawn as rectangles.
        Changes the color used to draw the cells - makes it more visually interesting.
        """
        self.change_cell_color()

        border_width = 0.0  # visual separation between cells, in pixels

        cell_width, cell_height = self.cell_size
        for x in range(self.board_size[0]):
            for y in range(self.board_size[1]):
                if self.board[y][x] == 1:
                    cell = pygame.Rect(cell_width * x + border_width, cell_height * y + border_width,
                                       cell_width - border_width * 2, cell_height - border_width * 2)
                    pygame.draw.rect(self.screen, self.cell_color, cell)

    def change_cell_color(self) -> None:
        """
        Changes the color of the cells by adjusting the RGB values.
        The color changes direction when it reaches the bounds (0 or 255).
        """
        for i in range(3):
            if not 0 <= self.cell_color[i] + self.color_step[i] <= 255:
                self.color_step[i] *= -1
            self.cell_color[i] += self.color_step[i]

    def draw_cursor(self, border_width=2) -> None:
        """
        Draws a red border around the cell under the mouse cursor.

        :param border_width: The width of the border to draw around the cell.
        """
        mouse_pos = pygame.mouse.get_pos()
        if not self.is_mouse_over_board(mouse_pos):
            return
        x, y = self.get_mouse_cell(mouse_pos)
        cell = pygame.Rect(self.cell_size[0] * x, self.cell_size[1] * y,
                           self.cell_size[0], self.cell_size[1])
        pygame.draw.rect(self.screen, (255, 0, 0), cell, border_width)

    def draw_gui(self) -> None:
        """
        Draws the GUI elements (buttons, input boxes, labels) on the side panel.
        """
        self.sidepanel.fill((50, 50, 50))
        self.screen.blit(self.sidepanel, self.sidepanel_pos)

        for element in self.buttons + self.input_boxes + self.labels:
            element.draw()

    # endregion DRAWING

    def render_screen(self) -> None:
        """
        Updates the contents of the entire display.
        """
        pygame.display.update()
