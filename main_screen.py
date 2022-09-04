import pygame

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

        self.game_name = self.large_font.render('Jaguar Run', False, (0, 0, 0))
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