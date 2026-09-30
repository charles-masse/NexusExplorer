
import os

from PIL import Image, ImageOps

from ..constants import MAP_CHUNK_RESOLUTION, MAP_SCALE


def chunk_coords(chunk_name):
    """Parse the minimap chunk name into map coords"""
    split_name = chunk_name.split('.')[-1]
    x = int(split_name[2:4], 16)
    y = int(split_name[0:2], 16)

    return [x, y]

def generate_map(chunk_path, cache=True):

    map_name = chunk_path.split('/')[-1]
    cache_path = f'.cache/{map_name}.png'
    #If the map was already processed in the past
    if cache and os.path.exists(cache_path):
        im = Image.open(cache_path)
    else:
        #Get chunk images
        chunks = [[chunk_name] + chunk_coords(chunk_name) for chunk_name in os.listdir(chunk_path)]

        max_x = (max(chunks, key=lambda x: x[1])[1] + 1) * MAP_CHUNK_RESOLUTION
        max_y = (max(chunks, key=lambda x: x[2])[2] + 1) * MAP_CHUNK_RESOLUTION
        #Create Image
        im = Image.new('RGB', (max_x, max_y))

        for (chunk_name, chunk_x, chunk_y) in chunks:
            #Load chunk
            with Image.open('/'.join([chunk_path, chunk_name, chunk_name + '.png'])) as chunk_image:
                # Assemble the unscaled map so fractional scaled chunk widths do not accumulate rounding error.
                im.paste(chunk_image, (chunk_x * MAP_CHUNK_RESOLUTION, chunk_y * MAP_CHUNK_RESOLUTION))
        im = ImageOps.scale(im, MAP_SCALE)
        #Save map for faster loading
        if cache:
            os.makedirs(os.path.dirname(cache_path), exist_ok=True)
            im.save(cache_path)

    return im
