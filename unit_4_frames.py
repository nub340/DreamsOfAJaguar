import pygame
from random import randint
from config import *

class Unit4Frames(pygame.sprite.Sprite):
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