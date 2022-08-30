import pygame
from sys import exit
from random import choice
from os.path import exists

from config import *
from player import Player
from enemy import Enemy

class Game():
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.screen_rect = self.screen.get_rect(topleft = (0, 0))
        pygame.display.set_caption('Jaguar Run')
        self.clock = pygame.time.Clock()
        self.game_font_large = pygame.font.Font('font/Pixeltype.ttf', 80)
        self.game_font = pygame.font.Font('font/Pixeltype.ttf', 50)
        self.game_active = False
        self.start_time = 0
        pygame.mixer.Sound('audio/legend-of-narmer.mp3').play(loops = -1)

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
        self.intro_background = pygame.image.load('graphics/map2.png').convert_alpha()
        self.intro_background_offset = 0
        self.intro_background_fwd = True

        self.player_stand = pygame.image.load('graphics/player/player_stand.png').convert_alpha()
        self.player_stand = pygame.transform.rotozoom(self.player_stand,0,2)
        self.player_stand_rect = self.player_stand.get_rect(center = (400, 230))

        self.game_name = self.game_font_large.render('Jaguar Run', False, (0, 0, 0))
        self.game_name_rect = self.game_name.get_rect(center = (400, 80))

        self.high_score_msg = self.game_font.render(f'High score: {self.high_score}', False, (0, 0, 0))
        self.high_score_rect = self.high_score_msg.get_rect(center = (400, 130))

        self.game_message = self.game_font.render('Press space to run', False, (0, 0, 0))
        self.start_rect = self.game_message.get_rect(center = (400, 340))

        # Timer
        self.enemy_timer = pygame.USEREVENT + 1
        pygame.time.set_timer(self.enemy_timer, 1500)

    def display_score(self):
        current_time = (int(pygame.time.get_ticks() / 1000) - self.start_time) + self.prev_score
        self.score_surf = self.game_font.render(f'Score: {current_time}', False, (64, 64, 64))
        self.score_rect = self.score_surf.get_rect(center = (400, 50))
        self.screen.blit(self.score_surf, self.score_rect)
        return current_time
   
    def collision_sprite(self):
        #return True
        colliding = pygame.sprite.spritecollide(self.player.sprite, self.obstacle_group, False)
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
        konomi = 0
        konomi_index = 0
        konami_code = [
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
                        self.obstacle_group.add(Enemy(choice(['bug', 'monkey', 'monkey', 'monkey'])))

                    elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                        self.save_score(self.score, self.high_score)
                        pygame.quit()
                        exit()

                else:
                    if event.type == pygame.KEYDOWN:

                        if konomi == 0 and event.key == konami_code[konomi_index]:
                            konomi_index += 1
                            print('konamicode'[konomi_index-1:konomi_index])
                            if konomi_index == len(konami_code):
                                konomi = 10
                                self.player.sprites()[0].death_sound.play()
                                konomi_index = 0
                        else:
                            konomi_index = 0

                        if event.key == pygame.K_SPACE:
                            self.start_time = int(pygame.time.get_ticks() / 1000)
                            self.game_active = True

            if self.game_active:
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
                self.screen.fill((94, 129, 162))
                if self.intro_background_fwd:
                    if self.intro_background_offset < -1000:
                        self.intro_background_fwd = False
                    else:
                        self.intro_background_offset -= 1
                else: 
                    if self.intro_background_offset < 0:
                        self.intro_background_offset += 1
                    else:
                        self.intro_background_fwd = True

                self.screen.blit(self.intro_background, (self.intro_background_offset, 0))
                self.screen.blit(self.game_name, self.game_name_rect)
                
                self.high_score_msg = self.game_font.render(f'High score: {self.high_score}', False, (0, 0, 0))
                self.high_score_rect = self.high_score_msg.get_rect(center = (400, 130))
                self.screen.blit(self.high_score_msg, self.high_score_rect)

                if konomi > 0:
                    print('Konami activated!', konomi)
                    player_stand = pygame.transform.rotate(self.player_stand, konomi)
                    self.screen.blit(player_stand, player_stand.get_rect(center = (400, 250)))
                    konomi += 10
                    if konomi >= 360:
                        konomi = 0
                else:
                    self.screen.blit(self.player_stand, self.player_stand_rect)

                self.score_message = self.game_font.render(f'Your score: {self.score}', False, (0, 0, 0))
                self.score_message_rect = self.score_message.get_rect(center = (400, 340))

                if self.prev_score > 0: game_message = 'Press space to continue...'
                else: game_message = 'Press space to run' 
                self.game_message = self.game_font.render(game_message, False, (0, 0, 0))
                self.start_rect = self.game_message.get_rect(center = (400, 350))
                
                if self.score == 0: self.screen.blit(self.game_message, self.start_rect)
                else: self.screen.blit(self.score_message, self.score_message_rect)
                
            pygame.display.update()
            self.clock.tick(60)

def main():
    game = Game()
    game.run()

if __name__ == '__main__':
    main()
