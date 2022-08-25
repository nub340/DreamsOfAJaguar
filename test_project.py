from unittest.mock import MagicMock
import config

def test_config_defined():
    assert config.SCREEN_WIDTH > 0
    assert config.SCREEN_HEIGHT > 0
    assert config.BG_ANIMATION_SPEED_MAGNITUDE > 0
    assert config.GRAVITY_CONSTANT < 0
    assert config.GROUND_Y > 0
    assert config.PLAYER_VELOCITY > 0
