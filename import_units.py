from PIL import Image
from config import *
import uuid
import os
from sys import argv, exit

def get_imported_units_list(type='air'):
    dir = f'graphics/units/{type}/'
    return list(map(lambda p: dir + p, os.listdir(dir)))

def process_image(type='air', image_path = None):
    queue = []
    if image_path:
        queue = [image_path]
    else:
        queue = list(map(lambda p: f'import_units/{type}/' + p, os.listdir(f'import_units/{type}/')))

    for image_path in queue:
        img = Image.open(image_path)
        img = img.convert("RGBA")
        datas = img.getdata()

        newData = []
        for item in datas:
            if (item[0] >= 240 and item[1] >= 240 and item[2] >= 240):
                newData.append((255, 255, 255, 0))
            else:
                newData.append(item)

        img.putdata(newData)
        newsize = (128, 128)
        img = img.resize(newsize)
        img.save(f'graphics/units/{type}/{uuid.uuid4()}.png', "PNG")

if __name__ == '__main__':
    if len(argv) == 3:
        type = argv[1]
        file_path = argv[2]
        process_image(type, file_path)
    elif len(argv) == 2:
        type = argv[1]
        process_image(type)
    else:
        exit('Incorrect number of arguments specified.')
