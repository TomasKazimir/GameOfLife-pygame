from __future__ import annotations

from dataclasses import dataclass

import pygame


@dataclass
class GUIElementSetupDataclass:
    screen: pygame.Surface
    game: game.Game
    pos: tuple[int, int]
    size: tuple[int, int]

    def unpack(self) -> tuple[pygame.Surface, game.game, int, int, int, int]:
        return self.screen, self.game, self.pos[0], self.pos[1], self.size[0], self.size[1]
