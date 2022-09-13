import pygame
import os
from threading import Thread
import pygame
from effects import make_dreamy

from import_unit import get_dynamic_units, import_unit, import_all_units, regenerate_all_units
from stable_diffusion.dream import regenerate_unit, ensure_api_key
from enemy import Enemy

class MainScreen:
    def __init__(self, screen, dream_mode, font, large_font, tip_font, high_score, score, prev_score, fade_in = None):
        self.screen = screen
        self.dream_mode = dream_mode
        self.font = font
        self.large_font = large_font
        self.tip_font = tip_font
        self.high_score = high_score
        self.score = score
        self.prev_score = prev_score
        
        if fade_in:
            self.fade_alpha = 255
        else:
            self.fade_alpha = None

        self.intro_background = pygame.image.load('graphics/map2.png').convert_alpha()
        self.intro_background_offset = 0
        self.intro_background_fwd = True

        self.shimmer_start_x = -2480
        self.shimmer_max_x = 3000
        self.shimmer_speed = 7
        self.shimmer_surf = pygame.image.load('graphics/alpha.shimmer.png').convert_alpha()
        self.shimmer_rect = self.shimmer_surf.get_rect(topleft = (self.shimmer_start_x, 10))
        self.shimmer_mask = pygame.mask.from_surface(self.shimmer_surf)

        self.dreamy_color = '#f786f9'
        self.game_title_surf = self.large_font.render('Dreams of a Jaguar', False, (113, 6, 115))
        self.game_title_mask = pygame.mask.from_surface(self.game_title_surf)
        self.game_title_rect = self.game_title_surf.get_rect(center = (400, 50))

        self.high_score_surf = self.font.render(f'High score: {self.high_score}', False, (113, 6, 115))
        self.high_score_surf = make_dreamy(self.high_score_surf, self.dreamy_color, 0, 4)
        self.high_score_rect = self.high_score_surf.get_rect(center = (400, 95))
        self.high_score_mask = pygame.mask.from_surface(self.high_score_surf)

        self.player_raw = pygame.image.load('graphics/player/player_stand.png').convert_alpha()
        self.player_surf = make_dreamy(pygame.transform.rotozoom(self.player_raw,0,2), 'white')
        self.player_surf_mouseover = make_dreamy(pygame.transform.rotozoom(self.player_raw,0,2), 'purple', 0, 4)
        self.player_mask = pygame.mask.from_surface(self.player_surf)
        self.player_rect = self.player_surf.get_rect(center = (400, 220))

        self.bottom_bar_surf = pygame.Surface((800 , 40))#.convert_alpha()
        self.bottom_bar_surf.set_alpha(220)
        self.bottom_bar_surf.fill((200, 200, 200))
        self.bottom_bar_rect = self.bottom_bar_surf.get_rect(bottomleft = (0, 400))

        if prev_score > 0 or score > 0: game_message = f'Your score: {prev_score or score}'
        else: game_message = 'Press space to continue...'

        call_to_action_surf = make_dreamy(
            self.font.render(game_message, False, (0, 0, 0)), 'white', 0, 4)
        self.bottom_bar_surf.blit(call_to_action_surf, call_to_action_surf.get_rect(center = (400, 22)))

        self.angle = 0
        self.bg_task_lock = { 'all': False, 'a0': False, 'a1': False, 'a2': False, 'g0': False, 'g1': False, 'g2': False }
        self.init_units()

    def init_units(self):
        self.air_units_group = pygame.sprite.Group()
        self.ground_units_group = pygame.sprite.Group()

        if self.dream_mode:
            self.air_units = get_dynamic_units('air')
            self.ground_units = get_dynamic_units('ground')
        else:
            self.air_units = []
            self.ground_units = []

        air_units_x = 125
        for i, air_unit_image_path in enumerate(sorted(self.air_units)):
            y = ((i + 1) * 80) + 100
            self.air_units_group.add(
                Enemy('air', air_unit_image_path, (air_units_x, y)))
            if i % 2 == 0: air_units_x -= 40
            else: air_units_x += 40

        ground_units_x = 675    
        for i, ground_unit in enumerate(self.ground_units):
            y = ((i + 1) * 80) + 100
            self.ground_units_group.add(
                Enemy('ground', ground_unit, (ground_units_x, y)))
            if i % 2 == 0: ground_units_x += 40
            else: ground_units_x -= 40

    def mouse_clicked(self):
        mouse_pos = pygame.mouse.get_pos()

        if self.player_rect.collidepoint(mouse_pos) and all(value == False for value in self.bg_task_lock.values()):
            ensure_api_key()

            def replace_all_units():
                print(f'Dreaming up all new units...')
                regenerate_all_units()
                import_all_units()
                self.init_units()
                print(f'new units manifested')
                self.bg_task_lock['all'] = False
                for _ in range(6):
                    pygame.mixer.Sound('audio/mixkit-magic-sweep-game-trophy-257.wav').play()

            if all(value == False for value in self.bg_task_lock.values()):
                self.bg_task_lock['all'] = True
                Thread(target=replace_all_units, name=f'worker_all').start()

        else:
            for i, air_unit in enumerate(self.air_units_group):
                if air_unit.rect.collidepoint(mouse_pos) and not self.bg_task_lock[f'all'] and not self.bg_task_lock[f'a{i}']:
                    
                    ensure_api_key()
                    unit_no = os.path.basename(air_unit.image_path).replace('.png', '')

                    def replace_air_unit():
                        print(f'Dreaming up new air unit', unit_no)
                        path = regenerate_unit('air', unit_no)
                        import_unit('air', unit_no)
                        self.init_units()
                        print(f'new air unit manifested:', path)
                        self.bg_task_lock[f'a{i}'] = False
                        pygame.mixer.Sound('audio/mixkit-magic-sweep-game-trophy-257.wav').play()

                    if not self.bg_task_lock[f'a{i}']:
                        self.bg_task_lock[f'a{i}'] = True
                        Thread(target=replace_air_unit, name=f'aworker{i}').start()
                    
            for i, ground_unit in enumerate(self.ground_units_group):
                if ground_unit.rect.collidepoint(mouse_pos) and not self.bg_task_lock[f'all'] and not self.bg_task_lock[f'g{i}']:

                    ensure_api_key()
                    unit_no = os.path.basename(ground_unit.image_path).replace('.png', '')
                    
                    # use closure to access state
                    def replace_ground_unit():
                        print(f'Dreaming up new ground unit', unit_no)
                        path = regenerate_unit('ground', unit_no)
                        import_unit('ground', unit_no)
                        self.init_units()
                        print(f'new ground unit manifested', path)
                        self.bg_task_lock[f'g{i}'] = False
                        pygame.mixer.Sound('audio/mixkit-magic-sweep-game-trophy-257.wav').play()

                    if not self.bg_task_lock[f'g{i}']:
                        self.bg_task_lock[f'g{i}'] = True
                        Thread(target=replace_ground_unit, name=f'gworker{i}').start()

    def draw(self):
        
        mouse_pos = pygame.mouse.get_pos()
        
        # background  
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
        dreamy_game_title_surf = make_dreamy(self.game_title_surf, self.dreamy_color, 0, 4)
        self.screen.blit(dreamy_game_title_surf, dreamy_game_title_surf.get_rect(center = (400, 50)))
        
        # animate shimmer rect
        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_LEFT]:
            self.shimmer_rect.x -= self.shimmer_speed*2
        elif self.shimmer_rect.x < self.shimmer_max_x:
            self.shimmer_rect.x += self.shimmer_speed
        else:
            #self.shimmer_speed = max(self.shimmer_speed / 2, 1)
            self.shimmer_rect.x = self.shimmer_start_x
            
        # game title shimmer
        offset_x = (self.game_title_rect.x - self.shimmer_rect.left)
        offset_y = (self.game_title_rect.y - self.shimmer_rect.top)
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

            new_surface = make_dreamy(new_surface, 'purple', 2, 2)
            self.screen.blit(new_surface, new_surface.get_rect(topleft = (self.shimmer_rect.left-6, self.shimmer_rect.top-6)))

        # high score 
        self.screen.blit(self.high_score_surf, self.high_score_rect)

        # high score shimmer
        offset_x = (self.high_score_rect.x - self.shimmer_rect.left)
        offset_y = (self.high_score_rect.y - self.shimmer_rect.top)
        if (self.shimmer_rect.colliderect(self.high_score_rect)
            and self.shimmer_mask.overlap(self.high_score_mask, (offset_x, offset_y))):
            new_mask = self.shimmer_mask.overlap_mask(self.high_score_mask, (offset_x, offset_y))
            new_surface = new_mask.to_surface().convert()
            new_surface.set_colorkey((0, 0, 0))
            
            w, h = new_surface.get_size()
            for x in range(w):
                for y in range(h):
                    if new_surface.get_at((x, y))[0] != 0:
                        new_surface.set_at((x, y), 'white')

            new_surface = make_dreamy(new_surface, 'purple', 2, 2)
            self.screen.blit(new_surface, new_surface.get_rect(topleft = (self.shimmer_rect.left-6, self.shimmer_rect.top-6)))

        # player character
        if self.bg_task_lock['all'] and self.angle == 0:
            self.angle = 10
            
        if self.angle > 0:
            player_stand = make_dreamy(pygame.transform.rotate(self.player_surf, self.angle))
            self.screen.blit(player_stand, player_stand.get_rect(center = (400, 220)))
            self.angle += 2
            if self.angle >= 360:
                self.angle = 0

        elif self.dream_mode and self.player_rect.collidepoint(mouse_pos):
            self.screen.blit(self.player_surf_mouseover, (self.player_rect.x - 6, self.player_rect.y - 6))

        else:
            self.screen.blit(self.player_surf, self.player_rect)
            
        # call to action
        self.screen.blit(self.bottom_bar_surf, self.bottom_bar_rect) 

        # ai unit selection
        self.air_units_group.draw(self.screen)
        self.air_units_group.update(mouse_pos=mouse_pos)

        self.ground_units_group.draw(self.screen)
        self.ground_units_group.update(mouse_pos=mouse_pos)

        # show mouse hover tooltip
        if self.dream_mode:
            for i, sprite in enumerate(self.air_units_group.sprites()):
                pos_in_mask = mouse_pos[0] - sprite.rect.x, mouse_pos[1] - sprite.rect.y
                touching = sprite.rect.collidepoint(*mouse_pos) and sprite.mask.get_at(pos_in_mask)
                if touching:

                    if self.bg_task_lock[f'a{i}'] or self.bg_task_lock['all']:
                        tip = self.tip_font.render(f'DREAMING...', False, (0, 0, 0))
                    else:
                        tip = self.tip_font.render(f'REGENERATE AIR UNIT {i+1}', False, (0, 0, 0))

                    tip_surf = pygame.Surface(tip.get_size())
                    tip_surf.fill((200, 200, 200))
                    tip_surf.blit(tip, (2, 2))

                    self.screen.blit(tip_surf, tip_surf.get_rect(midleft = (mouse_pos[0]+10, mouse_pos[1])))

            for i, sprite in enumerate(self.ground_units_group.sprites()):
                pos_in_mask = mouse_pos[0] - sprite.rect.x, mouse_pos[1] - sprite.rect.y
                touching = sprite.rect.collidepoint(*mouse_pos) and sprite.mask.get_at(pos_in_mask)
                if touching:

                    if self.bg_task_lock[f'g{i}'] or self.bg_task_lock['all']:
                        tip = self.tip_font.render(f'DREAMING...', False, (0, 0, 0))
                    else:
                        tip = self.tip_font.render(f'REGENERATE GROUND UNIT {i+1}', False, (0, 0, 0))

                    tip_surf = pygame.Surface(tip.get_size())
                    tip_surf.fill((200, 200, 200))
                    tip_surf.blit(tip, (2, 2))

                    self.screen.blit(tip_surf, tip_surf.get_rect(midright = (mouse_pos[0]-10, mouse_pos[1]))) 

            pos_in_mask = mouse_pos[0] - self.player_rect.x, mouse_pos[1] - self.player_rect.y
            touching = self.player_rect.collidepoint(*mouse_pos) and self.player_mask.get_at(pos_in_mask)
            if touching:
                if all(value == False for value in self.bg_task_lock.values()):
                    tip = self.tip_font.render(f'REGENERATE ALL UNITS', False, (0, 0, 0))
                else:
                    tip = self.tip_font.render(f'DREAMING...', False, (0, 0, 0))
                    
                tip_surf = pygame.Surface(tip.get_size())
                tip_surf.fill((200, 200, 200))
                tip_surf.blit(tip, (2, 2))
                self.screen.blit(tip_surf, tip_surf.get_rect(midleft = (mouse_pos[0]+10, mouse_pos[1]))) 
        
        if self.fade_alpha and self.fade_alpha > 0:
            self.fade_alpha -= 5
            fade_surf = pygame.Surface([800,400], pygame.SRCALPHA, 32).convert_alpha()
            fade_surf.fill((0, 0, 0))
            fade_surf.set_alpha(self.fade_alpha)
            self.screen.blit(fade_surf, (0, 0))

    def trigger_easter_egg(self):
        if self.angle == 0:
            self.angle = 10