from responseScene import ResponseScene
from unittest.mock import Mock, patch
import pytest
import constants

@pytest.fixture
def scene():
    return ResponseScene(Mock(), Mock(), 'Yes', Mock())

def test_update(scene):
    scene.draw = Mock()
    scene.check_input = Mock()

    scene.update()

    assert scene.current_frame == 1
    scene.draw.assert_called_once()
    scene.check_input.assert_called_once()

def test_update_time_ran_out(scene):
    scene.draw = Mock()

    [scene.update() for _ in range(constants.FRAME_RATE * 4)]
    scene.manager.set_feedback_scene.assert_called_once_with(failed=True)
    assert scene.draw.call_count == constants.FRAME_RATE * 4

@patch("responseScene.event.getKeys")
def test_check_input_incorrect(mock, scene):
    mock.return_value = ['k']

    scene.check_input()

    scene.manager.set_feedback_scene.assert_called_once_with(failed=True)

@patch("responseScene.event.getKeys")
def test_check_input_correct(mock, scene):
    mock.return_value = ['d']

    scene.check_input()

    scene.manager.set_feedback_scene.assert_called_once_with(failed=False)

def test_draw(scene):
    scene.draw()
    scene.fixationCross.draw.assert_called_once()