"""One grid-based DDA ray."""

from __future__ import annotations

import math

import pygame

from settings import MAX_DEPTH, TILE_SIZE


def normalized_angle(angle: float) -> float:
    """Wrap an angle into the zero-to-two-pi range."""
    return angle % (2 * math.pi)


# Original public function kept as an alias.
normalizedAngle = normalized_angle


class Ray:
    """Record one ray and its nearest wall intersection."""

    def __init__(self, angle: float, player: object) -> None:
        """Initialize an uncast ray from the player."""
        self.player = player
        self.ray_angle = normalized_angle(angle)
        self.distance = MAX_DEPTH
        self.hit_x = player.x + math.cos(self.ray_angle) * MAX_DEPTH
        self.hit_y = player.y + math.sin(self.ray_angle) * MAX_DEPTH
        self.wall_type = 1
        self.hit_vertical = False
        self.texture_offset = 0.0

    @property
    def rayAngle(self) -> float:
        """Expose the original ray-angle attribute name."""
        return self.ray_angle

    def cast(self, world_map: object | None = None) -> Ray:
        """Find the closest wall with Digital Differential Analysis."""
        level = world_map or getattr(self.player, "world_map", None)
        if level is None:
            return self

        position_x = self.player.x / TILE_SIZE
        position_y = self.player.y / TILE_SIZE
        direction_x = math.cos(self.ray_angle)
        direction_y = math.sin(self.ray_angle)
        map_x = int(position_x)
        map_y = int(position_y)

        delta_x = abs(1 / direction_x) if abs(direction_x) > 1e-12 else math.inf
        delta_y = abs(1 / direction_y) if abs(direction_y) > 1e-12 else math.inf

        if direction_x < 0:
            step_x = -1
            side_x = (position_x - map_x) * delta_x
        else:
            step_x = 1
            side_x = (map_x + 1 - position_x) * delta_x
        if direction_y < 0:
            step_y = -1
            side_y = (position_y - map_y) * delta_y
        else:
            step_y = 1
            side_y = (map_y + 1 - position_y) * delta_y

        max_steps = int(MAX_DEPTH / TILE_SIZE) * 2
        for _ in range(max_steps):
            if side_x < side_y:
                map_x += step_x
                distance_in_tiles = side_x
                side_x += delta_x
                self.hit_vertical = True
            else:
                map_y += step_y
                distance_in_tiles = side_y
                side_y += delta_y
                self.hit_vertical = False

            tile = level.tile_at(map_x, map_y)
            if tile:
                self.distance = min(distance_in_tiles * TILE_SIZE, MAX_DEPTH)
                self.wall_type = tile
                break
        else:
            self.distance = MAX_DEPTH

        self.hit_x = self.player.x + direction_x * self.distance
        self.hit_y = self.player.y + direction_y * self.distance
        wall_coordinate = self.hit_y if self.hit_vertical else self.hit_x
        self.texture_offset = (wall_coordinate % TILE_SIZE) / TILE_SIZE
        return self

    def render(self, screen: pygame.Surface, scale: float = 1.0) -> None:
        """Draw the ray as a top-down debug line."""
        pygame.draw.line(
            screen,
            (232, 72, 72),
            (self.player.x * scale, self.player.y * scale),
            (self.hit_x * scale, self.hit_y * scale),
            1,
        )
