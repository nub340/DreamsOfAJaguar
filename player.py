import pygame
from config import *
from random import randint

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.player_walk = [
            pygame.image.load('graphics/player/player_walk_1.png').convert_alpha(), 
            pygame.image.load('graphics/player/player_walk_2.png').convert_alpha()]
        self.player_walk_index = 0

        self.player_crouch = [
            pygame.image.load('graphics/player/player_crouch.png').convert_alpha(), 
            pygame.image.load('graphics/player/player_crouch_2.png').convert_alpha()]
        self.player_crouch_index = 0
        
        self.player_walk_attack = [
            pygame.image.load('graphics/player/player_attack_1.png').convert_alpha(), 
            pygame.image.load('graphics/player/player_attack_2.png').convert_alpha()]
        self.player_walk_attack_index = 0

        self.player_crouch_attack = [
            pygame.image.load('graphics/player/player_crouch_attack.png').convert_alpha(), 
            pygame.image.load('graphics/player/player_crouch_attack_2.png').convert_alpha()]
        self.player_crouch_attack_index = 0

        self.player_attack_effect = [
            pygame.image.load('graphics/player/attack_effect_1.png').convert_alpha(),
            pygame.image.load('graphics/player/attack_effect_2.png').convert_alpha(),
            pygame.image.load('graphics/player/attack_effect_3.png').convert_alpha(),
            pygame.image.load('graphics/player/attack_effect_4.png').convert_alpha()
        ]

        self.player_jump = pygame.image.load('graphics/player/player_jump.png').convert_alpha()
        self.player_jump_attack = pygame.image.load('graphics/player/player_jump_attack.png').convert_alpha()
        
        self.image = self.player_walk[self.player_walk_index]
        self.reset_start_pos()
        
        self.jump_sound = pygame.mixer.Sound('audio/mixkit-player-jumping-in-a-video-game-2043.wav')
        self.jump_sound.set_volume(0.5)

        self.death_sound = pygame.mixer.Sound('audio/gasp-uuh-85993.mp3')
        self.death_sound.set_volume(0.5)

        self.swish_sound = pygame.mixer.Sound('audio/slash-whoosh.mp3')
        self.swish_sound.set_volume(0.2)
        self.swish_sound_start_time = 0

        #hit sound
        self.hit_sound = pygame.mixer.Sound('audio/slash.mp3')
        self.hit_sound.set_volume(1)
        self.hit_sound_start_time = 0

    def reset_start_pos(self):
        self.gravity = 0
        self.velocity = 10
        self.attack = False
        self.crouch = False
        self.attack_time = 0
        self.rect = self.image.get_rect(midbottom = (80, GROUND_Y))

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and self.rect.bottom >= GROUND_Y:
            self.gravity = GRAVITY_CONSTANT
            self.jump_sound.play()

        if keys[pygame.K_DOWN] and self.rect.bottom >= GROUND_Y:
            self.crouch = True
        else: self.crouch = False

        if keys[pygame.K_SPACE]:
            self.attack = True 
            if (pygame.time.get_ticks() - self.swish_sound_start_time) > (self.swish_sound.get_length() * 1000):
                self.swish_sound.play()
                self.swish_sound_start_time = pygame.time.get_ticks()
        else:
            self.attack = False

        if keys[pygame.K_RIGHT]:
            if self.rect.right + PLAYER_VELOCITY > 800: 
                self.rect.right = 800
            else: self.rect.right += PLAYER_VELOCITY

        if keys[pygame.K_LEFT]:
            if self.rect.left - PLAYER_VELOCITY < 0:
                self.rect.left = 0
            else: self.rect.left -= PLAYER_VELOCITY

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= GROUND_Y:
            self.rect.bottom = GROUND_Y

    def animate(self):
        if self.rect.bottom < GROUND_Y: 
            # jumping...
            if self.attack:
                self.image = self.player_jump_attack
            else:
                self.image = self.player_jump

        else:
            # attacking
            if self.attack:
                if self.crouch: 
                    self.player_crouch_attack_index += 0.1
                    if self.player_crouch_attack_index >= len(self.player_crouch_attack): 
                        self.player_crouch_attack_index = 0
                    self.image = self.player_crouch_attack[int(self.player_crouch_attack_index)]
                else: # standing
                    self.player_walk_attack_index += 0.1
                    if self.player_walk_attack_index >= len(self.player_walk_attack): 
                        self.player_walk_attack_index = 0
                    self.image = self.player_walk_attack[int(self.player_walk_attack_index)]
            # walking...
            else:
                if self.crouch:
                    self.player_crouch_index += 0.1
                    if self.player_crouch_index >= len(self.player_crouch): 
                        self.player_crouch_index = 0
                    self.image = self.player_crouch[int(self.player_crouch_index)]
                else: # standing
                    self.player_walk_index += 0.1
                    if self.player_walk_index >= len(self.player_walk): 
                        self.player_walk_index = 0
                    self.image = self.player_walk[int(self.player_walk_index)]
                    self.mask = self.image

            self.mask = pygame.mask.from_surface(self.image)

        now = pygame.time.get_ticks()
        if now - self.attack_time < 100:
            attack_effect_surface = self.player_attack_effect[randint(0, 3)]
            attack_rect = attack_effect_surface.get_rect(midleft = self.rect.midright)
            pygame.display.get_surface().blit(attack_effect_surface, attack_rect)

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animate()