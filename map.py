"""Grid map and its top-down renderer."""

from __future__ import annotations

import pygame

from settings import TILE_SIZE


class Map:
    """A small maze. Zero is walkable and positive values are wall materials."""

    def __init__(self) -> None:
        """Build and validate the default tile grid."""
        self.grid = [
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 1, 1, 1, 0, 1, 0, 2, 0, 1, 1, 1, 3, 3, 3, 0, 1, 0, 1],
            [1, 0, 1, 0, 0, 0, 1, 0, 2, 0, 0, 0, 0, 0, 0, 3, 0, 1, 0, 1],
            [1, 0, 1, 0, 1, 1, 1, 0, 2, 2, 2, 2, 0, 1, 0, 3, 0, 1, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 1, 0, 3, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 2, 0, 1, 1, 3, 3, 3, 0, 1],
            [1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 2, 0, 0, 0, 0, 0, 3, 0, 1],
            [1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 0, 2, 2, 2, 2, 2, 0, 3, 0, 1],
            [1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 2, 0, 3, 0, 1],
            [1, 0, 1, 0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 1, 0, 2, 0, 3, 0, 1],
            [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 2, 0, 0, 0, 1],
            [1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 1, 0, 1, 0, 2, 2, 2, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        ]
        self.rows = len(self.grid)
        self.columns = len(self.grid[0])
        if any(len(row) != self.columns for row in self.grid):
            raise ValueError("Every map row must have the same number of columns")

    @property
    def width(self) -> int:
        """Return the map width in world pixels."""
        return self.columns * TILE_SIZE

    @property
    def height(self) -> int:
        """Return the map height in world pixels."""
        return self.rows * TILE_SIZE

    def tile_at(self, column: int, row: int) -> int:
        """Return a tile value; outside the level behaves as a solid wall."""
        if row < 0 or row >= self.rows or column < 0 or column >= self.columns:
            return 1
        return self.grid[row][column]

    def has_wall_at(self, x: float, y: float, *_: object) -> bool:
        """Report whether a world position is solid."""
        if x < 0 or y < 0 or x >= self.width or y >= self.height:
            return True
        return self.tile_at(int(x // TILE_SIZE), int(y // TILE_SIZE)) > 0

    def render_top_down(
        self,
        screen: pygame.Surface,
        player: object | None = None,
        rays: list[object] | None = None,
        *,
        origin: tuple[int, int] = (0, 0),
        tile_size: float = 32,
        background: tuple[int, int, int] = (12, 15, 20),
    ) -> None:
        """Draw the map, optional rays, and player at any requested scale."""
        offset_x, offset_y = origin
        map_rect = pygame.Rect(
            offset_x,
            offset_y,
            round(self.columns * tile_size),
            round(self.rows * tile_size),
        )
        pygame.draw.rect(screen, background, map_rect)

        wall_colours = {1: (88, 112, 142), 2: (138, 92, 78), 3: (87, 132, 102)}
        for row, tiles in enumerate(self.grid):
            for column, tile in enumerate(tiles):
                if not tile:
                    continue
                rect = pygame.Rect(
                    round(offset_x + column * tile_size),
                    round(offset_y + row * tile_size),
                    max(1, round(tile_size)),
                    max(1, round(tile_size)),
                )
                pygame.draw.rect(screen, wall_colours.get(tile, wall_colours[1]), rect)
                if tile_size >= 12:
                    pygame.draw.rect(screen, (26, 31, 39), rect, 1)

        if player is None:
            return

        scale = tile_size / TILE_SIZE
        player_position = (
            round(offset_x + player.x * scale),
            round(offset_y + player.y * scale),
        )
        if rays:
            # A subset keeps the overlay readable and inexpensive.
            step = max(1, len(rays) // 60)
            for ray in rays[::step]:
                endpoint = (
                    round(offset_x + ray.hit_x * scale),
                    round(offset_y + ray.hit_y * scale),
                )
                pygame.draw.line(screen, (224, 179, 65), player_position, endpoint, 1)

        radius = max(3, round(player.radius * scale))
        pygame.draw.circle(screen, (243, 77, 77), player_position, radius)
        facing = (
            round(player_position[0] + 28 * scale * player.direction.x),
            round(player_position[1] + 28 * scale * player.direction.y),
        )
        pygame.draw.line(screen, (255, 236, 167), player_position, facing, 2)

    def map_render(self, screen: pygame.Surface) -> None:
        """Compatibility wrapper for the original prototype API."""
        self.render_top_down(screen, tile_size=TILE_SIZE)
