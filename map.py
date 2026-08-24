"""Grid map and its top-down renderer."""

from __future__ import annotations

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
