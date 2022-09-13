import pygame
from sys import exit
from random import choice
from os.path import exists
from config import * 

from player import Player
from enemy import Enemy
from import_unit import get_dynamic_units, get_static_units
from main_screen import MainScreen
from effects import make_dreamy

class Game():
    def __init__(self, dream_mode):
        pygame.init()
        self.dream_mode = dream_mode
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.screen_rect = self.screen.get_rect(topleft = (0, 0))
        icon = pygame.image.load('graphics/Player/player_icon.png')
        pygame.display.set_icon(icon)
        pygame.display.set_caption('Dream of the Jaguar')
        self.clock = pygame.time.Clock()
        self.game_font_large = pygame.font.Font('font/Pixeltype.ttf', 80)
        self.game_font = pygame.font.Font('font/Pixeltype.ttf', 50)
        self.tip_font = pygame.font.Font('font/Pixeltype.ttf', 25)
        self.game_active = False
        self.start_time = 0
        pygame.mouse.set_cursor(pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_CROSSHAIR))
        self.game_music = None 
        self.paused = False

        self.score = 0
        self.prev_score = 0
        self.high_score = 0
        if exists('save.txt'):
            file = open('save.txt', 'r')
            self.prev_score = int(file.readline() or 0)
            self.high_score = int(file.readline() or 0)

        self.__player__ = Player()
        self.player = pygame.sprite.GroupSingle()
        self.player.add(self.__player__)

        self.obstacle_group = pygame.sprite.Group()
        if get_dynamic_units('air'):
            self.units = {
                'air': get_dynamic_units('air'), 
                'ground': get_dynamic_units('ground')
            }
        else:
            self.units = {
                'air': get_static_units('air'), 
                'ground': get_static_units('ground')
            }

        # Background, ground
        self.bg_ground_surface = pygame.image.load('graphics/mayanbg1.png').convert_alpha()
        self.bg_ground_offset = 0
        self.bg_trees_surface = pygame.image.load('graphics/mayanbg2.png').convert_alpha()
        self.bg_trees_offset = 0
        self.bg_temple_surface = pygame.image.load('graphics/mayanbg3.png').convert_alpha()
        self.bg_temple_offset = 0
        self.bg_hills_surface = pygame.image.load('graphics/mayanbg4.png').convert_alpha()
        self.bg_hills_offset = 0
        self.bg_sky_surface = pygame.image.load('graphics/mayanbg5.png').convert_alpha()
        self.bg_sky_offset = 0

        # Intro screen
        self.main_screen = None

        # Timer
        self.enemy_timer = pygame.USEREVENT + 1
        pygame.time.set_timer(self.enemy_timer, 1500)

    def set_game_music(self, track):
        if track == 'intro' and self.game_music != 'intro':
            self.game_music = track
            pygame.mixer.music.load('audio/legend-of-narmer.mp3')
            pygame.mixer.music.play(-1)
        elif track == 'in_game' and self.game_music != 'in_game':
            self.game_music = track
            pygame.mixer.music.load('audio/music.wav')
            pygame.mixer.music.play(-1)

    def display_score(self):
        current_time = (int(pygame.time.get_ticks() / 1000) - self.start_time) + self.prev_score
        self.score_surf = make_dreamy(self.game_font.render(f'Score: {current_time}', False, (113, 6, 115)), 'pink', 2, 0)
        self.score_rect = self.score_surf.get_rect(center = (400, 50))
        self.screen.blit(self.score_surf, self.score_rect)
        return current_time
   
    def collision_sprite(self):
        #return True
        colliding = (
            pygame.sprite.spritecollide(self.player.sprite, self.obstacle_group, False) and 
            pygame.sprite.spritecollide(self.player.sprite, self.obstacle_group, False, pygame.sprite.collide_mask)
        )
        if colliding:
            player = self.player.sprites()[0]
            for object in colliding:
                if (player.attack):
                    player.attack_time = pygame.time.get_ticks()
                    object.kill() 
                    player.hit_sound.play()
                else:
                    self.obstacle_group.empty()
                    player.death_sound.play()
                    return False
            return True
        else: return True

    def draw_environment_layers(self):
        if self.bg_ground_offset <= -499: self.bg_ground_offset = 0
        else: self.bg_ground_offset -= 1 * BG_ANIMATION_SPEED_MAGNITUDE
        
        if self.bg_trees_offset <= -499: self.bg_trees_offset = 0
        else: self.bg_trees_offset -= 0.25 * BG_ANIMATION_SPEED_MAGNITUDE
        
        if self.bg_temple_offset <= -499: self.bg_temple_offset = 0
        else: self.bg_temple_offset -= 0.0625 * BG_ANIMATION_SPEED_MAGNITUDE
        
        if self.bg_hills_offset <= -499: self.bg_hills_offset = 0
        else: self.bg_hills_offset -= 0.015625 * BG_ANIMATION_SPEED_MAGNITUDE
        
        if self.bg_sky_offset <= -499: self.bg_sky_offset = 0
        else: self.bg_sky_offset -= 0.00390625 * BG_ANIMATION_SPEED_MAGNITUDE

        self.screen.blit(self.bg_sky_surface, (self.bg_sky_offset, 0))
        self.screen.blit(self.bg_sky_surface, (self.bg_sky_offset+500, 0))
        self.screen.blit(self.bg_sky_surface, (self.bg_sky_offset+1000, 0))

        self.screen.blit(self.bg_hills_surface, (self.bg_hills_offset, 125))
        self.screen.blit(self.bg_hills_surface, (self.bg_hills_offset+500, 125))
        self.screen.blit(self.bg_hills_surface, (self.bg_hills_offset+1000, 125))

        self.screen.blit(self.bg_temple_surface, (self.bg_temple_offset, 100))
        self.screen.blit(self.bg_temple_surface, (self.bg_temple_offset+500, 100))
        self.screen.blit(self.bg_temple_surface, (self.bg_temple_offset+1000, 100))

        self.screen.blit(self.bg_trees_surface, (self.bg_trees_offset, 0))
        self.screen.blit(self.bg_trees_surface, (self.bg_trees_offset+500, 0))
        self.screen.blit(self.bg_trees_surface, (self.bg_trees_offset+1000, 0))

        self.screen.blit(self.bg_ground_surface, (self.bg_ground_offset, 0))
        self.screen.blit(self.bg_ground_surface, (self.bg_ground_offset+500, 0))
        self.screen.blit(self.bg_ground_surface, (self.bg_ground_offset+1000, 0))

    def save_score(self, score, high_score, file_name = 'save.txt'):
        save_file = open(file_name, 'w')
        save_file.writelines(list([f'{score}','\n',f'{high_score}']))
        save_file.close()

    def run(self):
        code_idx = 0
        code = [
            pygame.K_UP, pygame.K_UP, 
            pygame.K_DOWN, pygame.K_DOWN, 
            pygame.K_LEFT, pygame.K_RIGHT, 
            pygame.K_LEFT, pygame.K_RIGHT,
            pygame.K_b, pygame.K_a]

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if self.game_active:
                    if event.type == self.enemy_timer:
                        unit_types = []
                        if self.units['air']: unit_types.append('air')
                        if self.units['ground']: unit_types.append('ground')
                        type = choice(unit_types)
                        imported_units = self.units[type]
                        self.obstacle_group.add(Enemy(type, choice(imported_units), None, -6))                    

                    elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                        self.save_score(self.score, self.high_score)
                        pygame.quit()
                        exit()

                else: 
                    if event.type == pygame.KEYDOWN:

                        if event.key == code[code_idx]:
                            code_idx += 1
                            if code_idx == len(code):
                                self.player.sprites()[0].death_sound.play()
                                self.main_screen.trigger_easter_egg()
                                code_idx = 0
                        else:
                            code_idx = 0

                        if event.key == pygame.K_SPACE:
                            self.start_time = int(pygame.time.get_ticks() / 1000)
                            self.game_active = True
                            self.main_screen = None

                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        self.main_screen.mouse_clicked()

            if self.game_active:
                self.set_game_music('intro')
                self.draw_environment_layers()
                self.score = self.display_score()

                self.obstacle_group.draw(self.screen)
                self.obstacle_group.update()

                self.player.draw(self.screen)
                self.player.update()

                self.game_active = self.collision_sprite()
                if not self.game_active: 

                    self.__player__.reset_start_pos()
                    if self.score > 0:
                        self.prev_score = 0
                        if self.score > self.high_score:
                            self.high_score = self.score
                    self.save_score(0, self.high_score)

            else:
                self.set_game_music('intro')

                if not self.main_screen:
                    self.main_screen = MainScreen(self.screen, self.dream_mode, self.game_font, self.game_font_large, self.tip_font, self.high_score, self.score, self.prev_score, True)
                self.main_screen.draw()
                
            pygame.display.update()
            self.clock.tick(60)