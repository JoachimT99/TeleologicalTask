from interTrialScene import InterTrialScene
from unittest.mock import Mock
import pytest

@pytest.fixture
def scene():
    return InterTrialScene(Mock(), Mock())

def test_duration(scene):
    #Act
    for _ in range(60):
        scene.update()
    #Assert
    scene._manager.set_audio_scene.assert_called_once()

def test_blank_duration(scene):
    scene.draw = Mock()
    
    for _ in range(12):
        scene.update()
    
    scene.draw.assert_not_called()

def test_draw(scene):

    scene.draw()
    
    scene.fixationCross.draw.assert_called_once()