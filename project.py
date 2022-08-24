import pygame
from sys import exit
from random import randint, choice

GROUND_Y = 340
GRAVITY_CONSTANT = -20
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 400
BG_ANIMATION_SPEED_MAGNITUDE = 2
PLAYER_VELOCITY = 10

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.player_walk = [
            pygame.image.load('graphics/player/v2.walking.spear.png').convert_alpha(), 
            pygame.image.load('graphics/player/v2.walking.spear1.png').convert_alpha()]
        self.player_walk_index = 0
        self.player_jump = pygame.image.load('graphics/player/v2.jump.png').convert_alpha()
        
        self.image = self.player_walk[self.player_walk_index]
        self.rect = self.image.get_rect(midbottom = (80, GROUND_Y))
        self.gravity = 0
        self.velocity = 10

        self.jump_sound = pygame.mixer.Sound('audio/jump.mp3')
        self.jump_sound.set_volume(0.5)

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= GROUND_Y:
            self.gravity = GRAVITY_CONSTANT

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
        if self.rect.bottom < GROUND_Y: self.image = self.player_jump
        else:
            self.player_walk_index += 0.1
            if self.player_walk_index >= len(self.player_walk): self.player_walk_index = 0
            self.image = self.player_walk[int(self.player_walk_index)]

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animate()

class Enemy(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()

        if type == 'fly':
            self.frames = [
                pygame.image.load('graphics/fly/fly1.png').convert_alpha(), 
                pygame.image.load('graphics/fly/fly2.png').convert_alpha()]
            y_pos = 210
        else:
            self.frames = [
                pygame.image.load('graphics/snail/jaguar1.png').convert_alpha(), 
                pygame.image.load('graphics/snail/jaguar2.png').convert_alpha()]
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
        pygame.display.set_caption('PixelRunner')
        self.clock = pygame.time.Clock()
        self.game_font = pygame.font.Font('font/Pixeltype.ttf', 50)
        self.game_active = False
        self.start_time = 0
        self.score = 0
        # bg_music = pygame.mixer.Sound('audio/music.wav')
        # bg_music.play(loops = -1)

        self.player = pygame.sprite.GroupSingle()
        self.player.add(Player())

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

        # Enemies
        self.snail_frames = [
            pygame.image.load('graphics/snail/snail1.png').convert_alpha(), 
            pygame.image.load('graphics/snail/snail2.png').convert_alpha()]
        self.snail_frame_index = 0
        self.snail_surf = self.snail_frames[self.snail_frame_index]

        self.fly_frames = [
            pygame.image.load('graphics/fly/fly1.png').convert_alpha(), 
            pygame.image.load('graphics/fly/fly2.png').convert_alpha()]
        self.fly_frame_index = 0
        self.fly_surf = self.fly_frames[self.fly_frame_index]

        self.player_walk = [
            pygame.image.load('graphics/player/player_walk_1.png').convert_alpha(), 
            pygame.image.load('graphics/player/player_walk_2.png').convert_alpha()]
        self.player_walk_index = 0
        self.player_jump = pygame.image.load('graphics/player/jump.png').convert_alpha()

        self.player_surf = self.player_walk[self.player_walk_index]
        self.player_rect = self.player_surf.get_rect(midbottom = (80, GROUND_Y))

        # Intro screen
        self.player_stand = pygame.image.load('graphics/player/v2.standing.spear.png').convert_alpha()
        self.player_stand = pygame.transform.rotozoom(self.player_stand,0,2)
        self.player_stand_rect = self.player_stand.get_rect(center = (400, 200))

        self.game_name = self.game_font.render('Jaguar Run', False, (111, 196, 169))
        self.game_name_rect = self.game_name.get_rect(center = (400, 80))

        self.game_message = self.game_font.render('Press space to run', False, (111, 196, 169))
        self.start_rect = self.game_message.get_rect(center = (400, 330))

        # Timer
        self.enemy_timer = pygame.USEREVENT + 1
        pygame.time.set_timer(self.enemy_timer, 1500)

        self.snail_animation_timer = pygame.USEREVENT + 2
        pygame.time.set_timer(self.snail_animation_timer, 500)

        self.fly_animation_timer = pygame.USEREVENT + 3
        pygame.time.set_timer(self.fly_animation_timer, 200)

        self.bg_timer = pygame.USEREVENT + 4
        pygame.time.set_timer(self.bg_timer, 16)

    def display_score(self):
        current_time = int(pygame.time.get_ticks() / 1000) - self.start_time
        self.score_surf = self.game_font.render(f'Score: {current_time}', False, (64, 64, 64))
        self.score_rect = self.score_surf.get_rect(center = (400, 50))
        self.screen.blit(self.score_surf, self.score_rect)
        return current_time
   
    def collision_sprite(self):
        return True
        if pygame.sprite.spritecollide(self.player.sprite, self.obstacle_group, False): 
            self.obstacle_group.empty()
            return False
        else: return True

    def draw_environment_layers(self):     
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

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if self.game_active:
                    if event.type == self.enemy_timer:
                        self.obstacle_group.add(Enemy(choice(['fly', 'snail', 'snail', 'snail'])))

                    elif event.type == self.snail_animation_timer:
                        if self.snail_frame_index == 0: self.snail_frame_index = 1
                        else: self.snail_frame_index = 0
                        self.snail_surf = self.snail_frames[self.snail_frame_index]

                    elif event.type == self.fly_animation_timer:
                        if self.fly_frame_index == 0: self.fly_frame_index = 1
                        else: self.fly_frame_index = 0
                        self.fly_surf = self.fly_frames[self.fly_frame_index]

                    elif event.type == self.bg_timer:
                        
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

                else:
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                        self.start_time = int(pygame.time.get_ticks() / 1000)
                        self.game_active = True

            if self.game_active:
                self.draw_environment_layers()
                self.score = self.display_score()

                self.player.draw(self.screen)
                self.player.update()

                self.obstacle_group.draw(self.screen)
                self.obstacle_group.update()

                self.game_active = self.collision_sprite()

            else:
                self.screen.fill((94, 129, 162))
                self.screen.blit(self.player_stand, self.player_stand_rect)
                self.player_rect.midbottom = (80, GROUND_Y)

                self.score_message = self.game_font.render(f'Your score: {self.score}', False, (111, 196, 169))
                self.score_message_rect = self.score_message.get_rect(center = (400, 330))
                self.screen.blit(self.game_name,self.game_name_rect)

                if self.score == 0: self.screen.blit(self.game_message,self.start_rect)
                else: self.screen.blit(self.score_message,self.score_message_rect)
                
            pygame.display.update()
            self.clock.tick(60)

def main():
    game = Game()
    game.run()

if __name__ == '__main__':
    main()
