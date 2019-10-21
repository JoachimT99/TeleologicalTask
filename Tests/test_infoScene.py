from infoScene import InfoScene
from unittest.mock import Mock, patch
import pytest
import constants

@pytest.fixture
@patch("infoScene.visual.TextStim")
def scene(mock):
    return InfoScene(Mock(), Mock(), Mock())

@patch("infoScene.visual.TextStim")
def test_create_infoScene(text_mock):
    win = Mock()
    manager = Mock()
    text = Mock()

    scene = InfoScene(win, manager, text)

    assert win == scene.win
    assert manager == scene.manager
    assert scene.text == text_mock.return_value
    text_mock.assert_called_once_with(win, text=text, wrapWidth=constants.WINDOW_SIZE[0] )



def test_update(scene):
    scene.draw = Mock()
    scene.check_input = Mock()
    scene.update()

    scene.draw.assert_called_once()
    scene.check_input.assert_called_once()

def test_draw(scene):
    scene.draw()
    scene.text.draw.assert_called_once()

@patch("infoScene.event.getKeys")
def test_check_input(mock_keys, scene):
    mock_keys.return_value = ['d']
    scene.manager.set_intertrial_scene = Mock()

    scene.check_input()

    scene.manager.set_intertrial_scene.assert_called_once()