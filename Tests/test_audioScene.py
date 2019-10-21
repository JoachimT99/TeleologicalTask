from audioScene import AudioScene
from unittest.mock import Mock, patch
from psychopy.sound import Sound
import pytest
import time
import constants

@pytest.fixture
def fileMock():
    return Mock()

@pytest.fixture
@patch("audioScene.Sound")
def scene(sound_mock, fileMock):
    sound_mock.return_value = Sound()
    sound_mock.return_value.duration = 1
    return AudioScene(Mock(), Mock(), sound_mock, Mock())


def test_create_audioScene(scene):

    assert isinstance(scene.sound, Sound)
    assert scene.sound.getDuration() == 1
    assert scene.max_frame == 60 + constants.FRAME_RATE * constants.AUDIO_DELAY
    assert scene.current_frame == 0
    assert scene.sound.status == 0

def test_audioScene_delay(scene):
    [scene.update() for _ in range(11)]
    assert scene.sound.status == 0   
    scene.update() 
    assert scene.sound.status == 1


@patch("audioScene.Sound")
def test_update(sound_mock):
    manager = Mock()
    sound_mock.return_value = Sound()
    sound_mock.return_value.duration = 1
    scene = AudioScene(Mock(), manager, Mock(), Mock())
    scene.draw = Mock()

    #Act
    scene.update()
    #Assert
    manager.set_response_scene.assert_not_called()
    #Act
    [scene.update() for _ in range(71)]
    #Assert
    manager.set_response_scene.assert_called_once()
    assert scene.draw.call_count == 72

def test_draw(scene):
    scene.draw()

    scene.fixationCross.draw.assert_called_once()

    