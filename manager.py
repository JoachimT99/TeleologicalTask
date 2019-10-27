from interTrialScene import InterTrialScene
import pylink
from audioScene import AudioScene
from psychopy import data, visual
import constants
from infoScene import InfoScene
from responseScene import ResponseScene
from feedbackScene import FeedbackScene
from EyeLinkCoreGraphicsPsychoPy import EyeLinkCoreGraphicsPsychoPy
import random

class ExperimentManager(object):
    def __init__(self, win, dataFile):
        self.win = win
        self.conditions = data.importConditions(dataFile)
        shuffle_sequence(self.conditions)
        self.currentSet = 0
        self.isRunning = True

    def start_experiment(self):
        self.scene = InfoScene(self.win, self, constants.EXPERIMENT_START_TEXT)

    def set_audio_scene(self):
        fileName = "data/"+self.conditions[self.currentSet]["wav"]
        cross = visual.ImageStim(self.win, image=constants.FIXATION_CROSS, size=(200, 200), units="pix")
        self.scene = AudioScene(self.win, self, fileName, cross)


    def set_response_scene(self):
        corAns = self.conditions[self.currentSet]["CorAns"]
        cross = visual.ImageStim(self.win, image=constants.FIXATION_CROSS, size=(200, 200), units="pix")
        self.scene = ResponseScene(self.win, self, corAns, cross)

    def set_feedback_scene(self, failed=False):
        color = (1, -1, -1) if failed else (-1, 1, -1)
        feedback = visual.Rect(self.win, width=200, height=200, fillColor=color, lineColor=color)
        self.scene = FeedbackScene(self.win, self, feedback)

    def update(self):
        self.scene.update()
        self.win.flip()

    def set_intertrial_scene(self):
        self.scene = InterTrialScene(self.win, self, constants.INTERTRIAL_TEXT)

    def end_experiment(self):
        self.isRunning = False

    def next_set(self):
        self.currentSet += 1
        self.set_intertrial_scene()

def shuffle_sequence(sequence):
    while not check_sequence(sequence):
        random.shuffle(sequence)

def check_sequence(sequence):
    for i, item in enumerate(sequence):
        if i < 2:
            continue
        if item["type"] == sequence[i-1]["type"] and item["type"] == sequence[i-2]["type"] and item["type"] == sequence[i-3]["type"]:
            return False
    return True




if __name__ == "__main__":
    window = visual.Window(constants.WINDOW_SIZE, units="pix")

    manager = ExperimentManager(window, "Teleological_excel__for_programmer.xlsx")
    manager.start_experiment()

    while manager.isRunning:
        manager.update()
