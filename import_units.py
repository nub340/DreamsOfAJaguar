from PIL import Image
from config import *
import uuid
import os
from sys import argv, exit

def get_imported_units_list(type='air'):
    dir = f'graphics/units/{type}/'
    return list(map(lambda p: dir + p, os.listdir(dir)))

def extract_frame(img, frame):
    w, h = img.size
    half_w = int(w/2)
    half_h = int(h/2)
    frame_boxes = [
        (0, 0, half_w, half_h),
        (half_w, 0, w, half_h),
        (0, half_h, half_w, h),
        (half_w, half_h, w, h)]
    
    tile_size = (half_w, half_h)
    img_frame = img.crop(frame_boxes[frame-1])
    frame_box = img_frame.getbbox()
    img_frame = img_frame.crop(frame_box)
    img_out = Image.new(mode="RGBA", size=tile_size)
    img_out.paste(img_frame, (
        int((tile_size[0]-img_frame.size[0])/2), 
        int((tile_size[1]-img_frame.size[1])/2)))
    img_out.thumbnail((64, 64), Image.ANTIALIAS)
    return img_out

def process_image(type='air', image_path = None):
    # build a list of images to process
    queue = []
    if image_path:
        queue = [image_path]
    else:
        queue = list(map(lambda p: f'import_units/{type}/' + p, os.listdir(f'import_units/{type}/')))

    # process each image in the list...
    for image_path in queue:
        img = Image.open(image_path)
        img = img.convert("RGBA")

        # convert the background to alpha 
        datas = img.getdata()
        newData = []
        for item in datas:
            if (item[0] >= 240 and item[1] >= 240 and item[2] >= 240):
                newData.append((255, 255, 255, 0))
            else:
                newData.append(item)
        img.putdata(newData)
        
        # extract and normalize each of the 4 frames from the source image
        frame1 = extract_frame(img, 1)
        frame2 = extract_frame(img, 2)
        frame3 = extract_frame(img, 3)
        frame4 = extract_frame(img, 4)

        # combine the 4 frames back into a single image in a format suitable for the game to use
        image_out = Image.new(mode="RGBA", size=(128, 128))
        image_out.paste(frame1, (0,0))
        image_out.paste(frame2, (64,0))
        image_out.paste(frame3, (0,64))
        image_out.paste(frame4, (64,64))
        image_out.save(f'graphics/units/{type}/{uuid.uuid4()}.png', "PNG")

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
