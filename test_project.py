from unittest.mock import MagicMock
from project import Game
from player import Player
from enemy import Enemy
import config
import pygame
import os

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

def test_save_file():
    try:
        game = Game()
        game.save_score(123, 456, 'test_save.txt')
        save_file = open('test_save.txt')
        assert save_file.readline() == '123'
        assert save_file.readline() == '456'
    finally:
        os.remove("test_save.txt")


#def konami