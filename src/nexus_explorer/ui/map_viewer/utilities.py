
from ...constants import HALF_MAP, MAP_SCALE

# def calculateBounds(bounds0, bounds1, bounds2, bounds3):
#     """Calculate the map bounding box
#     """
#     return int(bounds0) * (32 / settings['mapScale']), int(bounds1) * (32 / settings['mapScale']), int(bounds2) * (32 / settings['mapScale']), int(bounds3) * (32 / settings['mapScale'])

def world_to_screen_pos(world_x, world_y):
    """World coords to map coords
    """
    return (HALF_MAP + float(world_x)) * MAP_SCALE, (HALF_MAP + float(world_y)) * MAP_SCALE

def screen_to_world_pos(screen_x, screen_y):
    """Map coords to world coords
    """
    return -int(HALF_MAP - (screen_x / MAP_SCALE)), -int(HALF_MAP - (screen_y / MAP_SCALE))
