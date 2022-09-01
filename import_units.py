from PIL import Image, ImageOps
import pygame
from random import randint
from config import *
import uuid
import os
from sys import argv

def list_imported_units():
    return list(map(lambda p: 'graphics/imported_units_ready/' + p, os.listdir('graphics/imported_units_ready')))

def process_image(image_path = None):
    queue = []
    if image_path:
        queue = [image_path]
    else:
        queue = list(map(lambda p: 'graphics/imported_units/' + p, os.listdir('graphics/imported_units')))

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
        img.save(f'graphics/imported_units_ready/{uuid.uuid4()}.png', "PNG")

class ImportedUnit(pygame.sprite.Sprite):
    def __init__(self, type, image_path):
        super().__init__()

        self.type = type
        self.animation_index = 0
        self.source_image = pygame.image.load(image_path).convert_alpha()
        self.frames = [
            self.source_image.subsurface((0, 0, 64, 64)),
            self.source_image.subsurface((64, 0, 64, 64)),
            self.source_image.subsurface((0, 64, 64, 64)),
            self.source_image.subsurface((64, 64, 64, 64))]
        self.image = self.frames[self.animation_index]

        if type == 'air':
            self.rect = self.image.get_rect(midbottom = (randint(900, 1100), randint(210, 280)))
        else:
            self.rect = self.image.get_rect(midbottom = (randint(900, 1100), GROUND_Y))

    def animate(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames): self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def update(self):
        self.animate()
        self.rect.x -= 6
        self.destroy()

    def destroy(self):
        if self.rect.x <= -100:
            self.kill()

if __name__ == '__main__':

    if len(argv) > 1:
        #for one file at each time
        file_path = argv[1]
        process_image(file_path)
    else:
        #for whole folder batch
        process_image()

    #process_image("graphics/imported_units/bird.1.3.png")
