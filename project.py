import pygame
from sys import exit
from random import randint, choice

GROUND_Y = 340
GRAVITY_CONSTANT = -20

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.player_walk = [
            pygame.image.load('graphics/player/v2.walking.spear.png').convert_alpha(), 
            pygame.image.load('graphics/player/v2.walking.spear.png').convert_alpha()]
        self.player_walk_index = 0
        self.player_jump = pygame.image.load('graphics/player/v2.walking.spear.png').convert_alpha()
        
        self.image = self.player_walk[self.player_walk_index]
        self.rect = self.image.get_rect(midbottom = (80, GROUND_Y))
        self.gravity = 0

        self.jump_sound = pygame.mixer.Sound('audio/jump.mp3')
        self.jump_sound.set_volume(0.5)

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= GROUND_Y:
            self.gravity = GRAVITY_CONSTANT
            self.jump_sound.play()

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
                pygame.image.load('graphics/snail/snail1.png').convert_alpha(), 
                pygame.image.load('graphics/snail/snail2.png').convert_alpha()]
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
        self.screen = pygame.display.set_mode((800, 400))
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
        self.sky_surface = pygame.image.load('graphics/Sky.png').convert()
        self.sky_rect = self.sky_surface.get_rect(topleft = (0, -330))
        self.ground_surface = pygame.image.load('graphics/mayanbg1.png').convert_alpha()

        # Enemies
        self.snail_frame_1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
        self.snail_frame_2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
        self.snail_frames = [self.snail_frame_1, self.snail_frame_2]
        self.snail_frame_index = 0
        self.snail_surf = self.snail_frames[self.snail_frame_index]

        self.fly_frame_1 = pygame.image.load('graphics/fly/fly1.png').convert_alpha()
        self.fly_frame_2 = pygame.image.load('graphics/fly/fly2.png').convert_alpha()
        self.fly_frames = [self.fly_frame_1, self.fly_frame_2]
        self.fly_frame_index = 0
        self.fly_surf = self.fly_frames[self.fly_frame_index]

        self.obstacle_rect_list = []

        self.player_walk_1 = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
        self.player_walk_2 = pygame.image.load('graphics/player/player_walk_2.png').convert_alpha()
        self.player_walk = [self.player_walk_1, self.player_walk_2]
        self.player_walk_index = 0
        self.player_jump = pygame.image.load('graphics/player/jump.png').convert_alpha()

        self.player_surf = self.player_walk[self.player_walk_index]
        self.player_rect = self.player_surf.get_rect(midbottom = (80, GROUND_Y))
        self.player_gravity = 0

        # Intro screen
        self.player_stand = pygame.image.load('graphics/player/player_stand.png').convert_alpha()
        self.player_stand = pygame.transform.rotozoom(self.player_stand,0,2)
        self.player_stand_rect = self.player_stand.get_rect(center = (400, 200))

        self.game_name = self.game_font.render('Pixel Runner', False, (111, 196, 169))
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

    def display_score(self):
        current_time = int(pygame.time.get_ticks() / 1000) - self.start_time
        self.score_surf = self.game_font.render(f'Score: {current_time}', False, (64, 64, 64))
        self.score_rect = self.score_surf.get_rect(center = (400, 50))
        self.screen.blit(self.score_surf, self.score_rect)
        return current_time

    def collision_sprite(self):
        if pygame.sprite.spritecollide(self.player.sprite, self.obstacle_group, False): 
            self.obstacle_group.empty()
            return False
        else: return True

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if self.game_active:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if self.player_rect.bottom >= GROUND_Y and self.player_rect.collidepoint(event.pos): self.player_gravity = -25

                    if event.type == pygame.KEYDOWN:
                        if self.player_rect.bottom >= GROUND_Y and event.key == pygame.K_SPACE: self.player_gravity = -25

                else:
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                        self.start_time = int(pygame.time.get_ticks() / 1000)
                        self.game_active = True

                if self.game_active:
                    if event.type == self.enemy_timer:
                        self.obstacle_group.add(Enemy(choice(['fly', 'snail', 'snail', 'snail'])))

                    if event.type == self.snail_animation_timer:
                        if self.snail_frame_index == 0: self.snail_frame_index = 1
                        else: self.snail_frame_index = 0
                        self.snail_surf = self.snail_frames[self.snail_frame_index]

                    if event.type == self.fly_animation_timer:
                        if self.fly_frame_index == 0: self.fly_frame_index = 1
                        else: self.fly_frame_index = 0
                        self.fly_surf = self.fly_frames[self.fly_frame_index]

            if self.game_active:
                self.screen.blit(self.sky_surface, (0, 0))
                self.screen.blit(self.ground_surface, (0, 0))
                self.screen.blit(self.ground_surface, (500, 0))
                self.score = self.display_score()

                self.player.draw(self.screen)
                self.player.update()

                self.obstacle_group.draw(self.screen)
                self.obstacle_group.update()

                self.game_active = self.collision_sprite()

            else:
                self.screen.fill((94, 129, 162))
                self.screen.blit(self.player_stand, self.player_stand_rect)
                self.obstacle_rect_list.clear()
                self.player_rect.midbottom = (80, GROUND_Y)
                self.player_gravity = 0

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
