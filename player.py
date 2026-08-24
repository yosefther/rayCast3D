"""Player movement and collision handling."""

from __future__ import annotations

import math

import pygame

from settings import MOVE_SPEED, PLAYER_RADIUS, ROTATION_SPEED, TILE_SIZE


class Player:
    """Store the player pose and apply collision-safe movement."""

    def __init__(self, world_map: object | None = None) -> None:
        """Place the player at the map's starting position."""
        # This tile is guaranteed to be an open area in the supplied map.
        self.x = 14.5 * TILE_SIZE
        self.y = 7.5 * TILE_SIZE
        self.radius = PLAYER_RADIUS
        self.rotation_angle = 0.0
        self.move_speed = MOVE_SPEED
        self.rotation_speed = ROTATION_SPEED
        self.world_map = world_map

        # Names retained for users of the original prototype.
        self.turnDirection = 0
        self.walkDirection = 0

    @property
    def direction(self) -> pygame.Vector2:
        """Return the unit vector for the current view angle."""
        return pygame.Vector2(
            math.cos(self.rotation_angle), math.sin(self.rotation_angle)
        )

    @property
    def rotationAngle(self) -> float:
        """Expose the original rotation-angle attribute name."""
        return self.rotation_angle

    @rotationAngle.setter
    def rotationAngle(self, value: float) -> None:
        """Update the view angle through the compatibility property."""
        self.rotation_angle = value

    def update(self, dt: float = 1 / 60, world_map: object | None = None) -> None:
        """Read keyboard state and move, using seconds for frame independence."""
        keys = pygame.key.get_pressed()
        forward = float(keys[pygame.K_w] or keys[pygame.K_UP]) - float(
            keys[pygame.K_s] or keys[pygame.K_DOWN]
        )
        strafe = float(keys[pygame.K_d]) - float(keys[pygame.K_a])
        turn = float(keys[pygame.K_RIGHT] or keys[pygame.K_e]) - float(
            keys[pygame.K_LEFT] or keys[pygame.K_q]
        )

        self.turnDirection = int(turn)
        self.walkDirection = int(forward)
        self.rotation_angle = (
            self.rotation_angle + turn * self.rotation_speed * dt
        ) % (2 * math.pi)

        movement = self.direction * forward
        if strafe:
            movement += pygame.Vector2(-self.direction.y, self.direction.x) * strafe
        if movement.length_squared() > 1:
            movement.normalize_ip()

        level = world_map or self.world_map
        delta = movement * self.move_speed * min(dt, 0.05)
        self.move(delta.x, delta.y, level)

    def move(self, dx: float, dy: float, world_map: object | None = None) -> None:
        """Move along each axis separately so the player slides along walls."""
        level = world_map or self.world_map
        if level is None:
            self.x += dx
            self.y += dy
            return

        next_x = self.x + dx
        if self._position_is_clear(next_x, self.y, level):
            self.x = next_x

        next_y = self.y + dy
        if self._position_is_clear(self.x, next_y, level):
            self.y = next_y

    def _position_is_clear(self, x: float, y: float, world_map: object) -> bool:
        """Check the player's four corners against nearby walls."""
        padding = self.radius
        return not any(
            world_map.has_wall_at(check_x, check_y)
            for check_x, check_y in (
                (x - padding, y - padding),
                (x + padding, y - padding),
                (x - padding, y + padding),
                (x + padding, y + padding),
            )
        )

    def player_render(self, screen: pygame.Surface) -> None:
        """Draw the player marker for top-down compatibility."""
        pygame.draw.circle(
            screen, (243, 77, 77), (round(self.x), round(self.y)), self.radius
        )
        endpoint = pygame.Vector2(self.x, self.y) + self.direction * 50
        pygame.draw.line(screen, (255, 220, 130), (self.x, self.y), endpoint, 2)
