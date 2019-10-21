import pytest
import constants
from unittest.mock import Mock, patch
from feedbackScene import FeedbackScene

@pytest.fixture
@patch("feedbackScene.random.randint")
def scene(random_mock):
    random_mock.return_value = 4
    return FeedbackScene(Mock(), Mock(), Mock())

def test_update(scene):
    scene.draw = Mock()

    scene.update()

    scene.draw.assert_called_once()

def test_feedback_duration(scene):

    [scene.update() for _ in range(4 * constants.FRAME_RATE)]
    scene.manager.next_set.assert_called_once()

def test_draw(scene):
    scene.feedback = Mock()

    scene.draw()

    scene.feedback.draw.assert_called_once()
    