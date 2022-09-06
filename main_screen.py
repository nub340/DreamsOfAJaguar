import pygame
import os
from threading import Thread

from ai_unit_import import get_units, import_unit
from stable_diffusion.dream import regenerate_unit, ensure_api_key
from ai_unit import AIUnit

class MainScreen:
    def __init__(self, screen, font, large_font):
        self.screen = screen
        self.font = font
        self.large_font = large_font

        self.intro_background = pygame.image.load('graphics/map2.png').convert_alpha()
        self.intro_background_offset = 0
        self.intro_background_fwd = True

        self.player_stand = pygame.image.load('graphics/player/player_stand.png').convert_alpha()
        self.player_stand = pygame.transform.rotozoom(self.player_stand,0,2)
        self.player_stand_rect = self.player_stand.get_rect(center = (400, 230))

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
                    (air_units_x, ((i + 1) * 80)+120)))
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
                    (ground_units_x, ((i + 1) * 80)+120)))
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


    def draw(self, prev_score, score, high_score, konami):
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

        self.game_name = self.large_font.render('Dream of the Jaguar', False, (0, 0, 0))
        self.game_name_rect = self.game_name.get_rect(center = (400, 80))
        self.screen.blit(self.game_name, self.game_name_rect)
        
        self.high_score_msg = self.font.render(f'High score: {high_score}', False, (0, 0, 0))
        self.high_score_rect = self.high_score_msg.get_rect(center = (400, 130))
        self.screen.blit(self.high_score_msg, self.high_score_rect)

        self.game_message = self.font.render('Press space to run', False, (0, 0, 0))
        self.start_rect = self.game_message.get_rect(center = (400, 340))

        if konami > 0:
            print('Konami activated!', konami)
            player_stand = pygame.transform.rotate(self.player_stand, konami)
            self.screen.blit(player_stand, player_stand.get_rect(center = (400, 250)))
            konami += 10
            if konami >= 360:
                konami = 0
        else:
            self.screen.blit(self.player_stand, self.player_stand_rect)

        self.score_message = self.font.render(f'Your score: {score}', False, (0, 0, 0))
        self.score_message_rect = self.score_message.get_rect(center = (400, 340))

        if prev_score > 0: game_message = 'Press space to continue...'
        else: game_message = 'Press space to run' 
        self.game_message = self.font.render(game_message, False, (0, 0, 0))
        self.start_rect = self.game_message.get_rect(center = (400, 350))
        
        if score == 0: self.screen.blit(self.game_message, self.start_rect)
        else: self.screen.blit(self.score_message, self.score_message_rect)

        self.air_units_group.draw(self.screen)
        self.air_units_group.update()

        self.ground_units_group.draw(self.screen)
        self.ground_units_group.update()
            
            