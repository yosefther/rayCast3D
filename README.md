# RayCast 3D

A small, complete ray-casting engine written in Python and Pygame. It turns a
2D tile map into a first-person 3D view using one DDA ray per screen column
group. No image or map assets are required.

## Features

- Real-time 3D wall projection with fish-eye correction
- Fast grid-based DDA ray intersection
- Frame-rate-independent movement, strafing, and wall collision
- Distance, wall-side, material, and procedural texture shading
- Live minimap plus a full top-down ray-debug view
- On-screen controls and FPS counter
- Unit tests for ray math, map bounds, collisions, and renderer behavior

## Run

Python 3.10 or newer is required.

```bash
uv sync
uv run python main.py
```

Without uv, use a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install pygame
python main.py
```

## Controls

| Key | Action |
| --- | --- |
| W / S or up/down arrows | Move forward/back |
| A / D | Strafe left/right |
| Q / E or left/right arrows | Turn |
| Tab | Switch between 3D and top-down debug views |
| M | Toggle the minimap |
| H or F1 | Toggle control help |
| Esc | Quit |

## Test

```bash
uv run pytest
```

The project is intentionally asset-free. Edit Map.grid in map.py to change
the maze; zero is floor and positive values select wall colours.
