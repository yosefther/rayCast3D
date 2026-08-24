"""Application entry point for RayCast 3D."""

from __future__ import annotations

import pygame

from map import Map
from player import Player
from rayCaster import Raycaster
from settings import (
    ACCENT_COLOUR,
    FPS,
    HUD_COLOUR,
    TITLE,
    WINDOW_HEIGHT,
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
        if self.top_down_view:
            self._render_top_down()
        else:
            self.raycaster.render_3d(self.screen)
            if self.show_minimap:
                self._render_minimap()
        self._render_hud()
        pygame.display.flip()

    def _render_top_down(self) -> None:
        """Draw the full map and its sampled rays."""
        self.screen.fill((10, 13, 18))
        tile_size = min(
            (WINDOW_WIDTH - 48) / self.map.columns,
            (WINDOW_HEIGHT - 72) / self.map.rows,
        )
        map_width = self.map.columns * tile_size
        map_height = self.map.rows * tile_size
        origin = (
            round((WINDOW_WIDTH - map_width) / 2),
            round((WINDOW_HEIGHT - map_height) / 2),
        )
        self.map.render_top_down(
            self.screen,
            self.player,
            self.raycaster.rays,
            origin=origin,
            tile_size=tile_size,
        )

    def _render_minimap(self) -> None:
        """Draw the compact map overlay."""
        tile_size = 10
        width = self.map.columns * tile_size
        height = self.map.rows * tile_size
        panel = pygame.Surface((width + 12, height + 12), pygame.SRCALPHA)
        panel.fill((4, 7, 11, 205))
        self.map.render_top_down(
            panel,
            self.player,
            self.raycaster.rays,
            origin=(6, 6),
            tile_size=tile_size,
            background=(16, 20, 27),
        )
        self.screen.blit(panel, (14, 14))
        pygame.draw.rect(
            self.screen, (158, 174, 194), (14, 14, width + 12, height + 12), 1
        )

    def _render_hud(self) -> None:
        """Draw performance, view, and control information."""
        fps_text = self.small_font.render(
            f"{self.clock.get_fps():.0f} FPS", True, ACCENT_COLOUR
        )
        self.screen.blit(fps_text, (WINDOW_WIDTH - fps_text.get_width() - 14, 12))

        view_name = "TOP-DOWN" if self.top_down_view else "3D VIEW"
        view_text = self.font.render(view_name, True, HUD_COLOUR)
        self.screen.blit(
            view_text,
            (WINDOW_WIDTH // 2 - view_text.get_width() // 2, 12),
        )

        if self.show_help:
            help_text = "W/S move  A/D strafe  Q/E or arrows turn  TAB view  M map  H help  ESC quit"
            rendered = self.small_font.render(help_text, True, HUD_COLOUR)
            box = pygame.Surface((rendered.get_width() + 20, 30), pygame.SRCALPHA)
            box.fill((3, 6, 10, 175))
            box.blit(rendered, (10, 7))
            self.screen.blit(
                box,
                (
                    WINDOW_WIDTH // 2 - box.get_width() // 2,
                    WINDOW_HEIGHT - box.get_height() - 10,
                ),
            )

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
