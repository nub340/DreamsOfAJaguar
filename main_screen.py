
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


    def make_dreamy(self, input_surf, color = (255, 255, 255), border_width = 2, blur_radius = 2):
        
        # create mask surface from mask of input_surf, set black pixels to be transparent
        input_mask_surf = pygame.mask.from_surface(input_surf).to_surface()
        input_mask_surf.set_colorkey((0,0,0))

        # change color of all non-black pixels
        input_w, input_h = input_mask_surf.get_size()
        for x in range(input_w):
            for y in range(input_h):
                if input_mask_surf.get_at((x, y))[0] != 0:
                    input_mask_surf.set_at((x, y), color)

        # calculate some needed dimensions. Square the blur radius to avoid clipping.
        padding = (border_width * blur_radius)
        output_w = input_w + (padding * 2) + (blur_radius**2)
        output_h = input_h + (padding * 2) + (blur_radius**2)

        # draw border/background...
        # blit mask surface 9 times, each offset in a different direction relative to the center: 
        # topleft, left, bottomleft, up, center, down, topright, right, bottomright. 
        input_mask_centered_rect = input_mask_surf.get_rect(center = (output_w/2, output_h/2))
        output_surface = pygame.Surface((output_w, output_h))
        output_surface.blit(input_mask_surf, (input_mask_centered_rect.x - padding, input_mask_centered_rect.y-padding))
        output_surface.blit(input_mask_surf, (input_mask_centered_rect.x - padding, input_mask_centered_rect.y))
        output_surface.blit(input_mask_surf, (input_mask_centered_rect.x - padding, input_mask_centered_rect.y+padding))

        output_surface.blit(input_mask_surf, (input_mask_centered_rect.x, input_mask_centered_rect.y-padding))
        output_surface.blit(input_mask_surf, (input_mask_centered_rect.x, input_mask_centered_rect.y))
        output_surface.blit(input_mask_surf, (input_mask_centered_rect.x, input_mask_centered_rect.y+padding))

        output_surface.blit(input_mask_surf, (input_mask_centered_rect.x + padding, input_mask_centered_rect.y-padding))
        output_surface.blit(input_mask_surf, (input_mask_centered_rect.x + padding, input_mask_centered_rect.y))
        output_surface.blit(input_mask_surf, (input_mask_centered_rect.x + padding, input_mask_centered_rect.y+padding))

        # blur the resulting border/background via PIL and then convert it back to a surface
        image = Image.frombytes(
            "RGBA", 
            output_surface.get_size(), 
            pygame.image.tostring(output_surface, 'RGBA')).filter(
                ImageFilter.GaussianBlur(blur_radius))

        output_surface = pygame.image.fromstring(
            image.tobytes("raw", 'RGBA'), 
            output_surface.get_size(), 
            'RGBA')

        # finally, blit the original unaltered input surface centered onto the output_surface
        output_surface.blit(input_surf, input_surf.get_rect(center = (output_w/2, output_h/2)))
        return output_surface

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

        dreamy_color = '#f786f9'
        self.game_name = self.make_dreamy(self.game_name, dreamy_color, 0, 4)
        self.screen.blit(self.game_name, self.game_name.get_rect(center = (400, 50)))
        
        self.high_score_msg = self.font.render(f'High score: {high_score}', False, (113, 6, 115))
        self.high_score_msg = self.make_dreamy(self.high_score_msg, dreamy_color, 0, 4)
        self.high_score_rect = self.high_score_msg.get_rect(center = (400, 95))
        self.screen.blit(self.high_score_msg, self.high_score_rect)

        if konami > 0:
            print('Konami activated!', konami)
            player_stand = pygame.transform.rotate(self.player_stand, konami)
            self.screen.blit(player_stand, player_stand.get_rect(center = (400, 25)))
            konami += 10
            if konami >= 360:
                konami = 0
        else:
            #player_stand = self.make_dreamy(self.player_stand, 'white', 0, 4)
            self.screen.blit(self.player_stand, self.player_stand_rect)

        if prev_score > 0: game_message = f'Your score: {prev_score}'
        else: game_message = 'Press space to continue...'

        game_message_surf = self.font.render(game_message, False, (0, 0, 0))
        bottom_bar = pygame.Surface((800 , 40))
        bottom_bar.set_alpha(220)
        bottom_bar.fill((200, 200, 200))
        game_message_surf = self.make_dreamy(game_message_surf, 'white', 0, 4)
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
            
            