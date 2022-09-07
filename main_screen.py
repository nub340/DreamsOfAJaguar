from turtle import width
import pygame
import os
from threading import Thread
import pygame
from PIL import Image, ImageFilter

from ai_unit_import import get_units, import_unit
from stable_diffusion.dream import regenerate_unit, ensure_api_key
from ai_unit import AIUnit

class MainScreen:
    def __init__(self, screen, font, large_font, tip_font):
        self.screen = screen
        self.font = font
        self.large_font = large_font
        self.tip_font = tip_font

        self.intro_background = pygame.image.load('graphics/map2.png').convert_alpha()
        self.intro_background_offset = 0
        self.intro_background_fwd = True

        self.player_stand = pygame.image.load('graphics/player/player_stand.png').convert_alpha()
        self.player_stand = pygame.transform.rotozoom(self.player_stand,0,2)
        self.player_stand_rect = self.player_stand.get_rect(center = (400, 220))

        self.init_units()

    def init_units(self):
        self.air_units_group = pygame.sprite.Group()
        self.air_units = get_units('air')
        air_units_x = 125
        for i, air_unit_image_path in enumerate(sorted(self.air_units)):
            self.air_units_group.add(
                AIUnit(
                    'air', 
                    air_unit_image_path, 
                    (air_units_x, ((i + 1) * 80)+100)))
            if i % 2 == 0: air_units_x -= 40
            else: air_units_x += 40

        self.ground_units_group = pygame.sprite.Group()
        self.ground_units = get_units('ground')
        ground_units_x = 675
        for i, ground_unit in enumerate(self.ground_units):
            self.ground_units_group.add(
                AIUnit(
                    'ground', 
                    ground_unit, 
                    (ground_units_x, ((i + 1) * 80)+100)))
            if i % 2 == 0: ground_units_x += 40
            else: ground_units_x -= 40

    def mouse_clicked(self):
        mouse_pos = pygame.mouse.get_pos()

        for i, air_unit in enumerate(self.air_units_group):
            if air_unit.rect.collidepoint(mouse_pos):
                
                ensure_api_key()
                unit_no = os.path.basename(air_unit.image_path).replace('.png', '')

                def replace_air_unit():
                    print(f'Dreaming up new air unit', unit_no)
                    path = regenerate_unit('air', unit_no)
                    import_unit('air', unit_no)
                    self.init_units()
                    print(f'new air unit manifested:', path)
                    pygame.mixer.Sound('audio/bump2.mp3').play()

                Thread(target=replace_air_unit, name=f'aworker{i}').start()
                
        for i, ground_unit in enumerate(self.ground_units_group):
            if ground_unit.rect.collidepoint(mouse_pos):

                ensure_api_key()
                unit_no = os.path.basename(ground_unit.image_path).replace('.png', '')
                
                # use closure to access state
                def replace_ground_unit():
                    print(f'Dreaming up new ground unit', unit_no)
                    regenerate_unit('ground', unit_no)
                    import_unit('ground', unit_no)
                    self.init_units()
                    print(f'new ground unit manifested')

                Thread(target=replace_ground_unit, name=f'gworker{i}').start()

    #  attempt at Bloom Layer Via CV
    # def create_neon(self , surf):
    #     surf_alpha = surf.convert_alpha()
    #     rgb = pygame.surfarray.array3d(surf_alpha)
    #     alpha = pygame.surfarray.array_alpha(surf_alpha).reshape((*rgb.shape[:2], 1))
    #     image = numpy.concatenate((rgb, alpha), 2)
    #     cv2.GaussianBlur(image, ksize=(11, 11), sigmaX=5, sigmaY=5, dst=image)
    #     cv2.blur(image, ksize=(5, 5), dst=image)
    #     bloom_surf = pygame.image.frombuffer(image.flatten(), image.shape[1::-1], 'RGBA')
    #     return bloom_surf

        
    def draw(self, prev_score, score, high_score, konami):
        pygame.mouse.set_cursor(pygame.cursors.arrow)
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

        self.game_name = self.large_font.render('Dream of the Jaguar', False, (113, 6, 115))
        self.game_name_rect = self.game_name.get_rect(center = (400, 50))

        blurred_game_name = self.large_font.render('Dream of the Jaguar', False, (255, 255, 255))
        raw = pygame.image.tostring(blurred_game_name, 'RGBA')
        blurred = Image.frombytes("RGBA", self.game_name.get_size(), raw).filter(ImageFilter.GaussianBlur(2)).filter(ImageFilter.GaussianBlur(2))
        blurred = pygame.image.fromstring(blurred.tobytes("raw", 'RGBA'), self.game_name.get_size(), 'RGBA')
        
        self.screen.blit(blurred, self.game_name_rect)
        self.screen.blit(self.game_name, self.game_name_rect)
        
        # self.game_name = self.create_neon(self.game_name)
        # self.screen.blit(self.game_name, self.game_name_rect)
        
        self.high_score_msg = self.font.render(f'High score: {high_score}', False, (113, 6, 115))
        self.high_score_rect = self.high_score_msg.get_rect(center = (400, 95))
        self.screen.blit(self.high_score_msg, self.high_score_rect)

        # self.game_message = self.font.render('Press space to run', False, (156, 35, 158))
        # self.start_rect = self.game_message.get_rect(center = (400, 340))

        if konami > 0:
            print('Konami activated!', konami)
            player_stand = pygame.transform.rotate(self.player_stand, konami)
            self.screen.blit(player_stand, player_stand.get_rect(center = (400, 25)))
            konami += 10
            if konami >= 360:
                konami = 0
        else:
            self.screen.blit(self.player_stand, self.player_stand_rect)

        if prev_score > 0: game_message = f'Your score: {prev_score}'
        else: game_message = 'Press space to continue...'

        game_message_surf = self.font.render(game_message, False, (0, 0, 0))
        bottom_bar = pygame.Surface((800 , 40))
        bottom_bar.set_alpha(220)
        bottom_bar.fill((200, 200, 200))
        bottom_bar.blit(game_message_surf, game_message_surf.get_rect(center = (400, 23)))
        self.screen.blit(bottom_bar, bottom_bar.get_rect(bottomleft = (0, 400))) 

        self.air_units_group.draw(self.screen)
        self.air_units_group.update()

        self.ground_units_group.draw(self.screen)
        self.ground_units_group.update()

        mouse_pos = pygame.mouse.get_pos()
        for i, sprite in enumerate(self.air_units_group.sprites()):
            if sprite.rect.collidepoint(mouse_pos):
                
                tip = self.tip_font.render(f'REGENERATE AIR UNIT {i+1}', False, (0, 0, 0))

                tip_surf = pygame.Surface(tip.get_size())
                tip_surf.fill((200, 200, 200))
                tip_surf.blit(tip, (2, 2))

                self.screen.blit(tip_surf, tip_surf.get_rect(midleft = mouse_pos))
                pygame.mouse.set_cursor((8,8),(0,0),(0,0,0,0,0,0,0,0),(0,0,0,0,0,0,0,0))

        for i, sprite in enumerate(self.ground_units_group.sprites()):
            if sprite.rect.collidepoint(mouse_pos):

                tip = self.tip_font.render(f'REGENERATE GROUND UNIT {i+1}', False, (0, 0, 0))

                tip_surf = pygame.Surface(tip.get_size())
                tip_surf.fill((200, 200, 200))
                tip_surf.blit(tip, (2, 2))

                self.screen.blit(tip_surf, tip_surf.get_rect(midright = mouse_pos)) 
                pygame.mouse.set_cursor((8,8),(0,0),(0,0,0,0,0,0,0,0),(0,0,0,0,0,0,0,0))
            
            