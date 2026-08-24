"""Application entry point for RayCast 3D."""

from __future__ import annotations

import pygame

from map import Map
from player import Player
from rayCaster import Raycaster
from settings import (
    FPS,
    TITLE,
    WINDOW_WIDTH,
)


class Game:
    """Coordinate input, simulation, and rendering."""

    def __init__(self) -> None:
        """Initialize Pygame and the engine's core objects."""
        pygame.init()
        pygame.display.set_caption(TITLE)
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 25)
        self.small_font = pygame.font.Font(None, 20)
        self.map = Map()
        self.player = Player(self.map)
        self.raycaster = Raycaster(self.player, self.map)
        self.running = True
        self.top_down_view = False
        self.show_minimap = True
        self.show_help = True

    def handle_events(self) -> None:
        """Handle quitting and display toggle events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_TAB:
                    self.top_down_view = not self.top_down_view
                elif event.key == pygame.K_m:
                    self.show_minimap = not self.show_minimap
                elif event.key in (pygame.K_h, pygame.K_F1):
                    self.show_help = not self.show_help

    def update(self, dt: float) -> None:
        """Advance the player and rebuild the visible rays."""
        self.player.update(dt)
        self.raycaster.cast_rays()

    def render(self) -> None:
        """Draw the active view and present the finished frame."""
        self.raycaster.render_3d(self.screen)
        pygame.display.flip()

    def run(self, max_frames: int | None = None) -> None:
        """Run until closed; max_frames supports automated smoke tests."""
        frame_count = 0
        while self.running and (max_frames is None or frame_count < max_frames):
            dt = self.clock.tick(FPS) / 1000
            self.handle_events()
            self.update(dt)
            self.render()
            frame_count += 1
        pygame.quit()


if __name__ == "__main__":
    Game().run()
