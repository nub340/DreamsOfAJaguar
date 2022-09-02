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

    #convert background to alpha
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
        
        #split image into 4 images
        w , h = img.size
        tile_size = (int(w/2), int(h/2))

        img1 = img.crop((0, 0, w/2, h/2))
        img1box = img1.getbbox()
        img1 = img1.crop(img1box)
        img1a = Image.new(mode="RGBA", size=tile_size)
        img1a.paste(img1, (int((tile_size[0]-img1.size[0])/2), int((tile_size[1]-img1.size[1])/2)))
        img1a = img1a.resize((64, 64))
        
        img2 = img.crop((w/2, 0, w, h/2))
        img2box = img2.getbbox()
        img2 = img2.crop(img2box)
        img2a = Image.new(mode="RGBA", size=tile_size)
        img2a.paste(img2, (int((tile_size[0]-img2.size[0])/2), int((tile_size[1]-img2.size[1])/2)))
        img2a = img2a.resize((64, 64))

        img3 = img.crop(( 0, h/2, w/2, h))
        img3box = img3.getbbox()
        img3 = img3.crop(img3box)
        img3a = Image.new(mode="RGBA", size=tile_size)
        img3a.paste(img3, (int((tile_size[0]-img3.size[0])/2), int((tile_size[1]-img3.size[1])/2)))
        img3a = img3a.resize((64, 64))

        img4 = img.crop(( w/2, h/2, w, h))
        img4box = img4.getbbox()
        img4 = img4.crop(img4box)
        img4a = Image.new(mode="RGBA", size=tile_size)
        img4a.paste(img4, (int((tile_size[0]-img4.size[0])/2), int((tile_size[1]-img4.size[1])/2)))
        img4a = img4a.resize((64, 64))

        image_out = Image.new(mode="RGBA", size=(128, 128))
        image_out.paste(img1a, (0,0))
        image_out.paste(img2a, (64,0))
        image_out.paste(img3a, (0,64))
        image_out.paste(img4a, (64,64))
        image_out.save(f'graphics/units/{type}/{uuid.uuid4()}.png', "PNG")

        #re-size image
        #newsize = (128, 128)
        #img = img.resize(newsize)
        #img.save(f'graphics/units/{type}/{uuid.uuid4()}.png', "PNG")
        #img.save(f'graphics/units/test.png', "PNG")

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
