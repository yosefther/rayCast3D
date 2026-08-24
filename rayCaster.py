"""Ray collection and first-person projection renderer."""

from __future__ import annotations

from typing import ClassVar

from ray import Ray
from settings import (
    FIELD_OF_VIEW,
    NUM_RAYS,
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
