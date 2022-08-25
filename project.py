import pygame
from sys import exit
from random import randint, choice
from os.path import exists

GROUND_Y = 340
GRAVITY_CONSTANT = -20
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 400
BG_ANIMATION_SPEED_MAGNITUDE = 2
PLAYER_VELOCITY = 5

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.player_walk = [
            pygame.image.load('graphics/player/player_walk_1.png').convert_alpha(), 
            pygame.image.load('graphics/player/player_walk_2.png').convert_alpha()]
        self.player_walk_index = 0

        self.player_crouch = [
            pygame.image.load('graphics/player/player_crouch.png').convert_alpha(), 
            pygame.image.load('graphics/player/player_crouch.png').convert_alpha()]
        self.player_crouch_index = 0
        
        self.player_walk_attack = [
            pygame.image.load('graphics/player/player_attack_1.png').convert_alpha(), 
            pygame.image.load('graphics/player/player_attack_2.png').convert_alpha()]
        self.player_walk_attack_index = 0

        self.player_crouch_attack = [
            pygame.image.load('graphics/player/player_crouch_attack.png').convert_alpha(), 
            pygame.image.load('graphics/player/player_crouch_attack.png').convert_alpha()]
        self.player_crouch_attack_index = 0

        self.player_attack_effect = [
            pygame.image.load('graphics/player/attack_effect_1.png').convert_alpha(),
            pygame.image.load('graphics/player/attack_effect_2.png').convert_alpha(),
            pygame.image.load('graphics/player/attack_effect_3.png').convert_alpha(),
            pygame.image.load('graphics/player/attack_effect_4.png').convert_alpha()
        ]
        self.player_attack_effect_index = 0
        
        self.player_jump = pygame.image.load('graphics/player/player_jump.png').convert_alpha()
        self.player_jump_attack = pygame.image.load('graphics/player/player_jump_attack.png').convert_alpha()
        
        self.image = self.player_walk[self.player_walk_index]
        self.goto_start_pos()
        
        self.jump_sound = pygame.mixer.Sound('audio/sfx_jump_07-80241.mp3')
        self.jump_sound.set_volume(0.1)

        self.death_sound = pygame.mixer.Sound('audio/gasp-uuh-85993.mp3')
        self.death_sound.set_volume(0.2)

        self.swish_sound = pygame.mixer.Sound('audio/slash-whoosh.mp3')
        self.swish_sound.set_volume(0.2)
        self.swish_sound_start_time = 0

        #hit sound
        self.hit_sound = pygame.mixer.Sound('audio/slash.mp3')
        self.hit_sound.set_volume(1)
        self.hit_sound_start_time = 0

    def goto_start_pos(self):
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

        #arm example question
        else:
            # walking...
            if self.attack:
                if self.crouch: 
                    self.player_crouch_attack_index += 0.1
                    if self.player_crouch_attack_index >= len(self.player_crouch_attack): 
                        self.player_crouch_attack_index = 0
                    self.image = self.player_crouch_attack[int(self.player_crouch_attack_index)]
                else:
                    self.player_walk_attack_index += 0.1
                    if self.player_walk_attack_index >= len(self.player_walk_attack): 
                        self.player_walk_attack_index = 0
                    self.image = self.player_walk_attack[int(self.player_walk_attack_index)]
            else:
                if self.crouch:
                    self.player_crouch_index += 0.1
                    if self.player_crouch_index >= len(self.player_crouch): 
                        self.player_crouch_index = 0
                    self.image = self.player_crouch[int(self.player_crouch_index)]
                else:
                    self.player_walk_index += 0.1
                    if self.player_walk_index >= len(self.player_walk): 
                        self.player_walk_index = 0
                    self.image = self.player_walk[int(self.player_walk_index)]


        now = pygame.time.get_ticks()
        if now - self.attack_time < 100:
            attack_effect_surface = self.player_attack_effect[randint(0, 3)]
            attack_rect = attack_effect_surface.get_rect(midleft = self.rect.midright)
            pygame.display.get_surface().blit(attack_effect_surface, attack_rect)

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animate()

class Enemy(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()

        if type == 'bug':
            self.frames = [
                pygame.image.load('graphics/bug/bug1.png').convert_alpha(), 
                pygame.image.load('graphics/bug/bug2.png').convert_alpha()]
            y_pos = 210
        else:
            self.frames = [
                pygame.image.load('graphics/howler_monkey/monkey1.png').convert_alpha(), 
                pygame.image.load('graphics/howler_monkey/monkey2.png').convert_alpha()]
            y_pos = GROUND_Y

        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom = (randint(900, 1100), y_pos))

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

class Game():
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.screen_rect = self.screen.get_rect(topleft = (0, 0))
        pygame.display.set_caption('Jaguar Run')
        self.clock = pygame.time.Clock()
        self.game_font = pygame.font.Font('font/Pixeltype.ttf', 50)
        self.game_active = False
        self.start_time = 0
        # pygame.mixer.Sound('audio/music.wav').play(loops = -1)

        self.score = 0
        self.prev_score = 0
        if exists('save.txt'):
            self.prev_score = int(open('save.txt', 'r').readline())

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
        self.player_stand = pygame.image.load('graphics/player/player_stand.png').convert_alpha()
        self.player_stand = pygame.transform.rotozoom(self.player_stand,0,2)
        self.player_stand_rect = self.player_stand.get_rect(center = (400, 200))

        self.game_name = self.game_font.render('Jaguar Run', False, (111, 196, 169))
        self.game_name_rect = self.game_name.get_rect(center = (400, 80))

        self.game_message = self.game_font.render('Press space to run', False, (111, 196, 169))
        self.start_rect = self.game_message.get_rect(center = (400, 330))

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

    def save_score(self, score):
        save_file = open('save.txt', 'w')
        save_file.write(f'{score}')
        save_file.close()

    def run(self):
        wait = False
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if self.game_active:
                    if event.type == self.enemy_timer:
                        self.obstacle_group.add(Enemy(choice(['bug', 'monkey', 'monkey', 'monkey'])))

                    elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                        self.save_score(self.score)
                        pygame.quit()
                        exit()

                else:
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
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

            else:
                self.screen.fill((94, 129, 162))
                self.screen.blit(self.player_stand, self.player_stand_rect)

                self.score_message = self.game_font.render(f'Your score: {self.score}', False, (111, 196, 169))
                self.score_message_rect = self.score_message.get_rect(center = (400, 330))
                self.screen.blit(self.game_name,self.game_name_rect)

                if self.score == 0: self.screen.blit(self.game_message,self.start_rect)
                else: self.screen.blit(self.score_message,self.score_message_rect)

                self.__player__.goto_start_pos()
                if self.score > 0: 
                    self.save_score(0)
                    self.prev_score = 0
                wait = True
                
            pygame.display.update()
            self.clock.tick(60)
            if wait:
                pygame.time.wait(800)
                wait = False

def main():
    game = Game()
    game.run()

if __name__ == '__main__':
    main()
