"""Behavior tests for map, movement, ray casting, and rendering."""

import math

import pygame
import pytest

from map import Map
from player import Player
from ray import Ray, normalized_angle
from rayCaster import Raycaster
from settings import NUM_RAYS, TILE_SIZE, WINDOW_HEIGHT, WINDOW_WIDTH


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


def test_player_cannot_cross_wall(level_and_player):
    """Collision blocks movement into a solid tile."""
    _, player = level_and_player
    starting_x = player.x

    player.move(3 * TILE_SIZE, 0)

    assert player.x == starting_x


def test_player_can_move_through_open_floor(level_and_player):
    """Movement succeeds when the destination is open."""
    _, player = level_and_player
    starting_y = player.y

    player.move(0, TILE_SIZE / 4)

    assert player.y == pytest.approx(starting_y + TILE_SIZE / 4)


def test_raycaster_rebuilds_a_fixed_number_of_rays(level_and_player):
    """Each cast replaces the previous fixed-size ray set."""
    level, player = level_and_player
    caster = Raycaster(player, level)

    first_rays = caster.cast_rays()
    second_rays = caster.cast_rays()

    assert len(first_rays) == NUM_RAYS
    assert len(second_rays) == NUM_RAYS
    assert all(ray.distance > 0 for ray in second_rays)


def test_renderer_draws_to_surface(level_and_player):
    """The 3D renderer writes visible pixels to its target."""
    level, player = level_and_player
    caster = Raycaster(player, level)
    surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))

    caster.cast_rays()
    caster.render_3d(surface)

    assert surface.get_at((WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)) != (0, 0, 0, 255)
