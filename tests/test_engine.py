"""Behavior tests for map, movement, ray casting, and rendering."""

import math

import pytest

from map import Map
from player import Player
from ray import Ray, normalized_angle
from settings import TILE_SIZE


@pytest.fixture
def level_and_player():
    """Return a connected map and player for each test."""
    level = Map()
    return level, Player(level)


def test_angle_normalization():
    """Angles wrap correctly in both directions."""
    assert normalized_angle(-math.pi / 2) == pytest.approx(3 * math.pi / 2)
    assert normalized_angle(5 * math.pi) == pytest.approx(math.pi)


def test_outside_map_is_solid():
    """Map bounds behave as walls while the spawn remains open."""
    level = Map()
    assert level.has_wall_at(-1, 10)
    assert level.has_wall_at(10, level.height)
    assert not level.has_wall_at(14.5 * TILE_SIZE, 7.5 * TILE_SIZE)


def test_ray_hits_nearest_wall(level_and_player):
    """A horizontal ray stops at the first wall tile."""
    level, player = level_and_player
    ray = Ray(0, player).cast(level)

    assert ray.distance == pytest.approx(2.5 * TILE_SIZE)
    assert ray.hit_x == pytest.approx(17 * TILE_SIZE)
    assert ray.wall_type == 3
    assert ray.hit_vertical


def test_vertical_ray_has_stable_math(level_and_player):
    """A vertical ray remains finite and reports the correct side."""
    level, player = level_and_player
    ray = Ray(-math.pi / 2, player).cast(level)

    assert math.isfinite(ray.distance)
    assert ray.distance == pytest.approx(TILE_SIZE / 2)
    assert ray.hit_y == pytest.approx(7 * TILE_SIZE)
    assert not ray.hit_vertical

