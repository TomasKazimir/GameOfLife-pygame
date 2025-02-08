from __future__ import annotations

from dataclasses import dataclass

import pygame


@dataclass
class GUIElementInfo:
    """
    Dataclass for GUIElement setup information.

    Attributes:
        screen: pygame.Surface - the screen to draw the element on
        game: game.Game - the game object
        pos: tuple[int, int] - the position of the element on the screen
        size: tuple[int, int] - the size of the element
    """
    screen: pygame.Surface
    game: game.Game
    pos: tuple[int, int]
    size: tuple[int, int] = (0, 0)

    def unpack(self) -> tuple[pygame.Surface, game.game, int, int, int, int]:
        return self.screen, self.game, self.pos[0], self.pos[1], self.size[0], self.size[1]
