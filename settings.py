"""Shared configuration for the ray-casting demo."""

from __future__ import annotations

import math

# Display
WINDOW_WIDTH = 1024
WINDOW_HEIGHT = 640
FPS = 60
TITLE = "RayCast 3D"

# World and camera
TILE_SIZE = 64
# Keep the old spelling available for code built against the first prototype.
TILESIZE = TILE_SIZE
FIELD_OF_VIEW = math.radians(60)
RAY_WIDTH = 2
NUM_RAYS = WINDOW_WIDTH // RAY_WIDTH
MAX_DEPTH = 32 * TILE_SIZE
PROJECTION_PLANE_DISTANCE = (WINDOW_WIDTH / 2) / math.tan(FIELD_OF_VIEW / 2)

# Player
PLAYER_RADIUS = 10
MOVE_SPEED = 185.0
ROTATION_SPEED = math.radians(125)

# Colours
CEILING_TOP = (28, 39, 62)
CEILING_BOTTOM = (66, 80, 105)
FLOOR_TOP = (55, 50, 47)
FLOOR_BOTTOM = (20, 20, 22)
HUD_COLOUR = (238, 242, 248)
ACCENT_COLOUR = (247, 195, 72)
