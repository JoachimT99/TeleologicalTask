import pytest
from manager import ExperimentManager
from interTrialScene import InterTrialScene
from audioScene import AudioScene
from unittest.mock import Mock, mock_open, patch, ANY
from psychopy import data
from infoScene import InfoScene
from responseScene import ResponseScene
from feedbackScene import FeedbackScene

@pytest.fixture
def manager():
    mock_func = Mock()
    data.importConditions = mock_func
    mock_func.return_value = [{"Set" : 9, "Type" : "CP", "CorAns" : "No", "wav" : "random_file_name.wav"}]
    return ExperimentManager(Mock(), Mock())

@patch("infoScene.visual.TextStim")
def test_start_experiment(mock, manager):
    #Act
    manager.start_experiment()

    #Assert
    assert isinstance(manager.scene, InfoScene)
    assert manager.isRunning == True



@patch("interTrialScene.visual.TextStim")
def test_set_intertrialScene(text_mock, manager):
    manager.set_intertrial_scene()
    assert isinstance(manager.scene, InterTrialScene)



def test_manager_data(manager):
    #Assert
    assert manager.conditions[0]["Set"] == 9
    assert manager.conditions[0]["Type"] == "CP"
    assert manager.conditions[0]["CorAns"] == "No"
    assert manager.conditions[0]["wav"] == "random_file_name.wav"

@patch("audioScene.Sound")
@patch("manager.visual.ImageStim")
def test_manager_set_audio_scene(sound_mock, circle_mock, manager):
    manager.set_audio_scene()

    assert isinstance(manager.scene, AudioScene)

@patch("manager.visual.ImageStim")
@patch("responseScene.random.randrange")
def test_set_response_scene(circle_mock, random_mock, manager):
    manager.set_response_scene()
    assert isinstance(manager.scene, ResponseScene)


@patch("manager.visual.Rect")
def test_set_feedback_scene(rect_mock, manager):
    manager.set_feedback_scene()
    assert isinstance(manager.scene, FeedbackScene)
    rect_mock.assert_called_once_with(ANY, height=ANY, width=ANY, fillColor=(-1, 1, -1), lineColor=(-1, 1, -1))

@patch("manager.visual.Rect")
def test_set_feedback_scene_failed(rect_mock, manager):
    manager.set_feedback_scene(failed=True)
    assert isinstance(manager.scene, FeedbackScene)
    rect_mock.assert_called_once_with(ANY, height=ANY, width=ANY, fillColor=(1, -1, -1), lineColor=(1, -1, -1))

def test_update(manager):
    manager.scene = Mock()
    #Act
    manager.update()
    #Assert
    manager.scene.update.assert_called_once()

def test_manager_end(manager):
    manager.end_experiment()
    assert manager.isRunning == False
