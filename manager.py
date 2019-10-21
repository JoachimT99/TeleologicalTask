from interTrialScene import InterTrialScene
from audioScene import AudioScene
from psychopy import data, visual
import constants
from infoScene import InfoScene
from responseScene import ResponseScene
from feedbackScene import FeedbackScene

class ExperimentManager(object):
    def __init__(self, win, dataFile):
        self.win = win
        self.conditions = data.importConditions(dataFile)
        self.currentSet = 0
        self.isRunning = True

    def start_experiment(self):
        self.scene = InfoScene(self.win, self, constants.EXPERIMENT_START_TEXT)

    def set_audio_scene(self):
        fileName = "data/"+self.conditions[self.currentSet]["wav"]
        cross = visual.Circle(self.win, radius=100, fillColor=(0, 0, 1))
        self.scene = AudioScene(self.win, self, fileName, cross)

    def set_response_scene(self):
        corAns = self.conditions[self.currentSet]["CorAns"]
        cross = visual.Circle(self.win, radius=100, fillColor=(0, 0, 1))
        self.scene = ResponseScene(self.win, self, corAns, cross)

    def set_feedback_scene(self, failed=False):
        color = (1, 0, 0) if failed else (0, 1, 0)
        feedback = visual.Rect(self.win, width=50, height=50, fillColor=color)
        self.scene = FeedbackScene(self.win, self, feedback)

    def update(self):
        self.scene.update()
        self.win.flip()

    def set_intertrial_scene(self):
        cross = visual.Circle(self.win, radius=100, fillColor=(1, 1, 1))
        self.scene = InterTrialScene(self, cross)

    def end_experiment(self):
        self.isRunning = False

    def next_set(self):
        self.currentSet += 1
        self.set_intertrial_scene()

if __name__ == "__main__":
    window = visual.Window(constants.WINDOW_SIZE, units="pix")
    manager = ExperimentManager(window, "Teleological_excel__for_programmer.xlsx")
    manager.start_experiment()

    while manager.isRunning:
        manager.update()
