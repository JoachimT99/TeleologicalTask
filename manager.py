from interTrialScene import InterTrialScene
import pylink
from audioScene import AudioScene
from psychopy import data, visual, gui, core
import constants
from infoScene import InfoScene
from responseScene import ResponseScene
from feedbackScene import FeedbackScene
import random
import csv
from eyeTracker import EyeTracker
import os
import time

class ExperimentManager(object):
    def __init__(self, win, dataFile):
        self.win = win
        self.conditions = data.importConditions(dataFile)
        shuffle_sequence(self.conditions)
        self.currentSet = 0
        self.isRunning = True
        dataFolder = os.getcwd() + '/edfData/'
        if not os.path.exists(dataFolder): 
            os.makedirs(dataFolder)
        dataFileName = "test" + '.EDF'
        self.eyeTracker = EyeTracker(win, dataFileName, self)
        self.scene = self.eyeTracker
        self.data = []
        self.dataDict = None
        self.eyeTracker.calibrate()

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

    def set_feedback_scene(self, response_time, failed=False):
        self.dataDict["answer"] = 0 if failed else 1
        self.dataDict["response_time"] = response_time
        color = (1, -1, -1) if failed else (-1, 1, -1)
        feedback = visual.Rect(self.win, width=200, height=200, fillColor=color, lineColor=color)
        self.scene = FeedbackScene(self.win, self, feedback)

    def update(self):
        self.scene.update()
        self.win.flip()

    def set_intertrial_scene(self):
        if self.dataDict is not None:
            self.data.append(self.dataDict)
        self.dataDict = {}
        self.dataDict["trial_number"] = self.currentSet
        self.dataDict["type"] = self.conditions[self.currentSet]["type"]
        self.scene = InterTrialScene(self.win, self, constants.INTERTRIAL_TEXT)

    def end_experiment(self):
        self.isRunning = False

    def next_set(self):
        self.currentSet += 1
        self.set_intertrial_scene()

    def save_experiment(self, writer):
        writer.writeRows(self.data)

def shuffle_sequence(sequence):
    while not check_sequence(sequence):
        random.shuffle(sequence)

def check_sequence(sequence):
    for i, item in enumerate(sequence):
        if i < 3:
            continue
        if item["type"] == sequence[i-1]["type"] and item["type"] == sequence[i-2]["type"] and item["type"] == sequence[i-3]["type"]:
            return False
    return True


def get_subject_info():
        info = {"SubjectID":"00", "SubjectInitials":"TEST"}
        dlg = gui.DlgFromDict(dictionary=info, title="Enter relevant information", order=("SubjectID", "SubjectInitials"))
        if not dlg.OK:
            core.quit()
        else:
            return info

if __name__ == "__main__":

    subjectInfo = get_subject_info()
    window = visual.Window(constants.WINDOW_SIZE, units="pix", fullscr=True)
    filename = f"{subjectInfo['SubjectInitials']}_.csv"       
    
    visual.TextStim(window, text="Eyetracker setup").draw()
    window.flip()
    with open(filename, mode="w") as csv_file:
        fieldNames = ["trial_number", "type", "answer", "response_time"]
        writer = csv.DictWriter(csv_file, fieldnames=fieldNames)
        writer.writeheader()
        manager = ExperimentManager(window, "Teleological_excel__for_programmer.xlsx")

        while manager.isRunning:
            manager.update()

        manager.save_experiment(writer)
