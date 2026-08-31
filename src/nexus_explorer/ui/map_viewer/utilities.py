
import math

from ...constants import HALF_MAP, MAP_SCALE


def hex_to_world_coordinates(hex_x: int, hex_y: int) -> tuple[float, float]:
    """Convert hex coordinates to world coordinates."""
    hex_width = 32
    hex_height = hex_width * math.sqrt(3) / 2

    world_x = ((hex_x - 3) * 1.5) * hex_width - HALF_MAP
    world_z = ((hex_y - 2) * 2) * hex_height - HALF_MAP

    return world_x, world_z

def screen_to_world_coordinates(screen_x, screen_y) -> tuple[int, int]:
    """Map coords to world coords"""
    world_x = -int(HALF_MAP - (screen_x / MAP_SCALE))
    world_y = -int(HALF_MAP - (screen_y / MAP_SCALE))

    return world_x, world_y

def world_to_screen_pos(world_x, world_y) -> tuple[float, float]:
    """World coords to map coords"""
    screen_x = (HALF_MAP + world_x) * MAP_SCALE
    screen_y = (HALF_MAP + world_y) * MAP_SCALE

    return screen_x, screen_y
