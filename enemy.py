import pygame
from random import randint
from config import *

class Enemy(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()

        self.animation_index = 0
        if type == 'bug':
            self.frames = [
                pygame.image.load('graphics/bug/bug1.png').convert_alpha(), 
                pygame.image.load('graphics/bug/bug2.png').convert_alpha()]
            self.image = self.frames[self.animation_index]
            self.rect = self.image.get_rect(midbottom = (randint(900, 1100), randint(210, 280)))
        else:
            self.frames = [
                pygame.image.load('graphics/howler_monkey/monkey1.png').convert_alpha(), 
                pygame.image.load('graphics/howler_monkey/monkey2.png').convert_alpha()]
            self.image = self.frames[self.animation_index]
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