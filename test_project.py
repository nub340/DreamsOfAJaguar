from unittest.mock import MagicMock
from game import Game
from player import Player
from enemy import Enemy
import config
import pygame

def test_config_defined():
    assert config.SCREEN_WIDTH > 0
    assert config.SCREEN_HEIGHT > 0
    assert config.BG_ANIMATION_SPEED_MAGNITUDE > 0
    assert config.GRAVITY_CONSTANT < 0
    assert config.GROUND_Y > 0
    assert config.PLAYER_VELOCITY > 0

def test_game_init():
    game = Game()
    assert game
    assert game.score == 0

def test_player_init():
    player = Player()
    assert player

def test_enemy_init():
    enemy = Enemy('bug')
    assert enemy 
    enemy = Enemy('monkey')
    assert enemy 

#def konami