"""Ray collection and first-person projection renderer."""

from __future__ import annotations

import math
from typing import ClassVar

import pygame

from ray import Ray
from settings import (
    CEILING_BOTTOM,
    CEILING_TOP,
    FIELD_OF_VIEW,
    FLOOR_BOTTOM,
    FLOOR_TOP,
    MAX_DEPTH,
    NUM_RAYS,
    PROJECTION_PLANE_DISTANCE,
    RAY_WIDTH,
    TILE_SIZE,
    WINDOW_HEIGHT,
    WINDOW_WIDTH,
)


class Raycaster:
    """Cast the camera rays and draw their 3D projection."""

    WALL_COLOURS: ClassVar[dict[int, tuple[int, int, int]]] = {
        1: (98, 150, 205),
        2: (198, 111, 87),
        3: (93, 177, 119),
    }

    def __init__(self, player: object, world_map: object | None = None) -> None:
        """Connect the renderer to its player and map."""
        self.rays: list[Ray] = []
        self.player = player
        self.world_map = world_map or getattr(player, "world_map", None)

    def cast_rays(self) -> list[Ray]:
        """Rebuild the current view from left to right."""
        self.rays.clear()
        first_angle = self.player.rotation_angle - FIELD_OF_VIEW / 2
        angle_step = FIELD_OF_VIEW / NUM_RAYS
        for index in range(NUM_RAYS):
            angle = first_angle + (index + 0.5) * angle_step
            self.rays.append(Ray(angle, self.player).cast(self.world_map))
        return self.rays

    def RayCaster(self) -> list[Ray]:
        """Compatibility wrapper for the prototype's original method name."""
        return self.cast_rays()

    @staticmethod
    def _lerp_colour(
        start: tuple[int, int, int], end: tuple[int, int, int], amount: float
    ) -> tuple[int, int, int]:
        """Blend two RGB colours by a normalized amount."""
        return tuple(round(a + (b - a) * amount) for a, b in zip(start, end))

    def _draw_background(self, screen: pygame.Surface) -> None:
        """Draw ceiling and floor gradients around the horizon."""
        horizon = WINDOW_HEIGHT // 2
        band_height = 4
        for y in range(0, horizon, band_height):
            amount = y / max(1, horizon)
            colour = self._lerp_colour(CEILING_TOP, CEILING_BOTTOM, amount)
            pygame.draw.rect(screen, colour, (0, y, WINDOW_WIDTH, band_height))
        for y in range(horizon, WINDOW_HEIGHT, band_height):
            amount = (y - horizon) / max(1, horizon)
            colour = self._lerp_colour(FLOOR_TOP, FLOOR_BOTTOM, amount)
            pygame.draw.rect(screen, colour, (0, y, WINDOW_WIDTH, band_height))

    def render_3d(self, screen: pygame.Surface) -> None:
        """Project current ray hits into shaded wall columns."""
        if not self.rays:
            self.cast_rays()
        self._draw_background(screen)

        for column, ray in enumerate(self.rays):
            # Remove fish-eye distortion before projecting the wall slice.
            corrected_distance = max(
                0.001,
                ray.distance * math.cos(ray.ray_angle - self.player.rotation_angle),
            )
            wall_height = min(
                WINDOW_HEIGHT * 2,
                TILE_SIZE * PROJECTION_PLANE_DISTANCE / corrected_distance,
            )
            wall_top = (WINDOW_HEIGHT - wall_height) / 2

            base = self.WALL_COLOURS.get(ray.wall_type, self.WALL_COLOURS[1])
            side_shade = 0.78 if ray.hit_vertical else 1.0
            distance_shade = max(0.24, 1.0 - corrected_distance / MAX_DEPTH)
            texture_shade = (
                0.88 + 0.12 * math.sin(ray.texture_offset * math.pi * 8) ** 2
            )
            shade = side_shade * distance_shade * texture_shade
            colour = tuple(max(0, min(255, round(channel * shade))) for channel in base)

            stripe = pygame.Rect(
                column * RAY_WIDTH,
                round(wall_top),
                RAY_WIDTH + 1,
                max(1, round(wall_height)),
            )
            pygame.draw.rect(screen, colour, stripe)

            # Subtle mortar bands make the procedural walls easier to read.
            if wall_height > 80:
                band_gap = wall_height / 5
                band_colour = tuple(max(0, channel - 18) for channel in colour)
                for band in range(1, 5):
                    y = round(wall_top + band * band_gap)
                    pygame.draw.line(
                        screen,
                        band_colour,
                        (stripe.left, y),
                        (stripe.right, y),
                    )

        self._draw_crosshair(screen)

    @staticmethod
    def _draw_crosshair(screen: pygame.Surface) -> None:
        """Draw a small crosshair at the center of the view."""
        center_x, center_y = WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2
        colour = (238, 242, 248)
        pygame.draw.line(
            screen, colour, (center_x - 7, center_y), (center_x + 7, center_y), 1
        )
        pygame.draw.line(
            screen, colour, (center_x, center_y - 7), (center_x, center_y + 7), 1
        )

    def render(self, screen: pygame.Surface) -> None:
        """Render through the original prototype method."""
        self.render_3d(screen)
