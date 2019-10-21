from interTrialScene import InterTrialScene
from unittest.mock import Mock, patch
import pytest

@pytest.fixture
@patch("interTrialScene.visual.TextStim")
def scene(mock):
    return InterTrialScene(Mock(), Mock(), Mock())

@patch("interTrialScene.event.getKeys")
def test_update(mock_keys, scene):
    scene.draw = Mock()
    scene.check_input = Mock()
    
    scene.update()


    scene.draw.assert_called_once()
    scene.check_input.assert_called_once()
    

def test_draw(scene):

    scene.draw()
    
    scene.text.draw.assert_called_once()


@patch("interTrialScene.event.getKeys")
def test_check_input(key_mock, scene):
    key_mock.return_value = ['space']

    scene.check_input()

    scene._manager.set_audio_scene.assert_called_once()



