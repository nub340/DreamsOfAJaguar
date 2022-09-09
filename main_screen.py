import pygame
import os
from threading import Thread
import pygame
from PIL import Image, ImageFilter

from ai_unit_import import get_units, import_unit
from stable_diffusion.dream import regenerate_unit, ensure_api_key
from ai_unit import AIUnit

class MainScreen:
    def __init__(self, screen, font, large_font, tip_font, high_score, score, prev_score):
        self.screen = screen
        self.font = font
        self.large_font = large_font
        self.tip_font = tip_font
        self.high_score = high_score
        self.score = score
        self.prev_score = prev_score

        self.intro_background = pygame.image.load('graphics/map2.png').convert_alpha()
        self.intro_background_offset = 0
        self.intro_background_fwd = True

        self.shimmer_surf = pygame.Surface((20, 100), pygame.SRCALPHA)
        self.shimmer_surf.fill('gray')
        self.shimmer_surf = pygame.transform.rotate(self.shimmer_surf, 135)
        self.shimmer_x = -150
        self.shimmer_speed = 1
        self.shimmer_rect = self.shimmer_surf.get_rect(topleft = (self.shimmer_x, 10))
        self.shimmer_mask = pygame.mask.from_surface(self.shimmer_surf)

        self.dreamy_color = '#f786f9'
        self.game_title_surf = self.make_dreamy(
            self.large_font.render('Dream of a Jaguar', False, (113, 6, 115)), 
            self.dreamy_color, 0, 4)
        self.game_title_mask = pygame.mask.from_surface(self.game_title_surf)
        self.game_title_rect = self.game_title_surf.get_rect(center = (400, 50))

        self.high_score_surf = self.font.render(f'High score: {self.high_score}', False, (113, 6, 115))
        self.high_score_surf = self.make_dreamy(self.high_score_surf, self.dreamy_color, 0, 4)
        self.high_score_rect = self.high_score_surf.get_rect(center = (400, 95))
        self.high_score_mask = pygame.mask.from_surface(self.high_score_surf)

        self.player_surf = pygame.image.load('graphics/player/player_stand.png').convert_alpha()
        self.player_surf = pygame.transform.rotozoom(self.player_surf,0,2)
        self.player_rect = self.player_surf.get_rect(center = (400, 220))

        self.bottom_bar_surf = pygame.Surface((800 , 40))#.convert_alpha()
        self.bottom_bar_surf.set_alpha(220)
        self.bottom_bar_surf.fill((200, 200, 200))
        self.bottom_bar_rect = self.bottom_bar_surf.get_rect(bottomleft = (0, 400))

        if prev_score > 0 or score > 0: game_message = f'Your score: {prev_score or score}'
        else: game_message = 'Press space to continue...'

        call_to_action_surf = self.make_dreamy(
            self.font.render(game_message, False, (0, 0, 0)), 'white', 0, 4)
        self.bottom_bar_surf.blit(call_to_action_surf, call_to_action_surf.get_rect(center = (400, 22)))

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

    def make_dreamy(self, input_surf, color = (255, 255, 255), border_width = 2, blur_radius = None):
        
        # create mask surface from mask of input_surf, set black pixels to be transparent
        input_mask_surf = pygame.mask.from_surface(input_surf).to_surface().convert()
        input_mask_surf.set_colorkey((0,0,0))

        # change color of all non-black pixels
        input_w, input_h = input_mask_surf.get_size()
        for x in range(input_w):
            for y in range(input_h):
                if input_mask_surf.get_at((x, y))[0] != 0:
                    input_mask_surf.set_at((x, y), color)

        # calculate some needed dimensions. Square the blur radius to avoid clipping.
        if blur_radius:
            padding = (border_width * blur_radius)
            output_w = input_w + (padding * 2) + (blur_radius**2)
            output_h = input_h + (padding * 2) + (blur_radius**2)
        else:
            padding = (border_width)
            output_w = input_w + (padding * 2) 
            output_h = input_h + (padding * 2)

        # draw border/background...
        # blit mask surface 9 times, each offset in a different direction relative to the center: 
        # topleft, left, bottomleft, up, center, down, topright, right, bottomright. 
        input_mask_centered_rect = input_mask_surf.get_rect(center = (output_w/2, output_h/2))
        output_surface = pygame.Surface((output_w, output_h), pygame.SRCALPHA).convert_alpha()
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
        if blur_radius:
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

    def draw(self, konami):
        
        # background
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

        # game title
        self.game_title_surf = self.make_dreamy(
            self.large_font.render('Dream of a Jaguar', False, (113, 6, 115)), 
            self.dreamy_color, 0, 4)
        self.screen.blit(self.game_title_surf, self.game_title_rect)
        
        # animate shimmer rect
        if self.shimmer_rect.x < 1000:
            self.shimmer_rect.x += self.shimmer_speed
        else:
            self.shimmer_rect.x = -150
            
        # game title shimmer
        offset_x = self.game_title_rect.x - self.shimmer_rect.left
        offset_y = self.game_title_rect.y - self.shimmer_rect.top     
        if (self.shimmer_rect.colliderect(self.game_title_rect)
            and self.shimmer_mask.overlap(self.game_title_mask, (offset_x, offset_y))):
            new_mask = self.shimmer_mask.overlap_mask(self.game_title_mask, (offset_x, offset_y))
            new_surface = new_mask.to_surface().convert()
            new_surface.set_colorkey((0, 0, 0))
            
            w, h = new_surface.get_size()
            for x in range(w):
                for y in range(h):
                    if new_surface.get_at((x, y))[0] != 0:
                        new_surface.set_at((x, y), 'white')

            #new_surface.set_alpha(200)
            new_surface = self.make_dreamy(new_surface, 'purple', 2, 2)
            self.screen.blit(new_surface, (self.shimmer_rect.x-3, self.shimmer_rect.y-3))

        # high score 
        self.screen.blit(self.high_score_surf, self.high_score_rect)

        # player character
        if konami > 0:
            print('Konami activated!', konami)
            player_stand = pygame.transform.rotate(self.player_surf, konami)
            self.screen.blit(player_stand, player_stand.get_rect(center = (400, 25)))
            konami += 10
            if konami >= 360:
                konami = 0
        else:
            self.screen.blit(self.player_surf, self.player_rect)

        # call to action
        self.screen.blit(self.bottom_bar_surf, self.bottom_bar_rect) 

        # ai unit selection
        self.air_units_group.draw(self.screen)
        self.air_units_group.update()

        self.ground_units_group.draw(self.screen)
        self.ground_units_group.update()

        # show mouse hover tooltip
        mouse_pos = pygame.mouse.get_pos()
        for i, sprite in enumerate(self.air_units_group.sprites()):
            if sprite.rect.collidepoint(mouse_pos):
                
                tip = self.tip_font.render(f'REGENERATE AIR UNIT {i+1}', False, (0, 0, 0))

                tip_surf = pygame.Surface(tip.get_size())
                tip_surf.fill((200, 200, 200))
                tip_surf.blit(tip, (2, 2))

                self.screen.blit(tip_surf, tip_surf.get_rect(midleft = mouse_pos))
                #pygame.mouse.set_cursor((8,8),(0,0),(0,0,0,0,0,0,0,0),(0,0,0,0,0,0,0,0))

        for i, sprite in enumerate(self.ground_units_group.sprites()):
            if sprite.rect.collidepoint(mouse_pos):

                tip = self.tip_font.render(f'REGENERATE GROUND UNIT {i+1}', False, (0, 0, 0))

                tip_surf = pygame.Surface(tip.get_size())
                tip_surf.fill((200, 200, 200))
                tip_surf.blit(tip, (2, 2))

                self.screen.blit(tip_surf, tip_surf.get_rect(midright = mouse_pos)) 
                #pygame.mouse.set_cursor((8,8),(0,0),(0,0,0,0,0,0,0,0),(0,0,0,0,0,0,0,0))
            
            