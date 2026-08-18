
import os

from PIL import Image, ImageOps

from ..constants import MAP_CHUNK_RESOLUTION, MAP_SCALE


def chunk_coords(chunk_name):
    """Parse the minimap chunk name into map coords
    """
    split_name = chunk_name.split('.')[-1]
    x = int(split_name[2:4], 16)
    y = int(split_name[0:2], 16)

    return [x, y]

def generate_map(game_files, world):

    map_path = world.map_path.replace('\\', '/')
    
    cache_path = f'./.cache/{map_path}.png'
    chunk_path = f'{game_files}/{map_path}'
    #If the map was already processed in the past
    if os.path.exists(cache_path):
        im = Image.open(cache_path)
    else:
        #Get chunk images
        chunks = [[chunk_name] + chunk_coords(chunk_name) for chunk_name in os.listdir(chunk_path)]

        scaled_resolution = int(MAP_CHUNK_RESOLUTION * MAP_SCALE)
        max_x = max(chunks, key=lambda x: x[1])[1] * scaled_resolution
        max_y = max(chunks, key=lambda x: x[2])[2] * scaled_resolution
        #Create Image
        im = Image.new('RGB', (max_x, max_y))

        for (chunk_name, chunk_x, chunk_y) in chunks:
            #Load chunk #TODO loading bar
            with Image.open('/'.join([chunk_path, chunk_name, chunk_name + '.png'])) as chunk_image:
                #Scale map and paste at the right postion
                chunk_image = ImageOps.scale(chunk_image, MAP_SCALE)
                im.paste(chunk_image, (chunk_x * scaled_resolution, chunk_y * scaled_resolution))
        #Save map for faster loading
        os.makedirs(os.path.dirname(cache_path), exist_ok=True)
        im.save(cache_path)

    return im
