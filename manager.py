from interTrialScene import InterTrialScene
import pylink
from audioScene import AudioScene
from psychopy import data, visual, gui, core, event
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
        print("shuffling")
        shuffle_sequence(self.conditions)
        print("shuffled")
        self.currentSet = 0
        self.isRunning = True
        dataFolder = os.getcwd() + '/edfData/'
        if not os.path.exists(dataFolder): 
            os.makedirs(dataFolder)
        dataFileName = "test" + '.EDF'
        self.data = []
        self.dataDict = None
        self.eyeTracker = EyeTracker(win, dataFileName, dataFolder, self)
        self.scene = self.eyeTracker
        self.eyeTracker.calibrate()
        self.responded = None

    def start_experiment(self):
        self.scene = InfoScene(self.win, self, constants.EXPERIMENT_START_TEXT)

    def set_audio_scene(self):
        fileName = "data/"+self.conditions[self.currentSet]["wav"]
        cross = visual.ImageStim(self.win, image=constants.FIXATION_CROSS, size=(200, 200), units="pix")
        self.scene = AudioScene(self.win, self, fileName, cross)
        self.eyeTracker.fixation_cross_start()


    def set_response_scene(self):
        self.eyeTracker.sound_end()
        corAns = self.conditions[self.currentSet]["CorAns"]
        cross = visual.ImageStim(self.win, image=constants.FIXATION_CROSS, size=(200, 200), units="pix")
        self.scene = ResponseScene(self.win, self, corAns, cross)
        self.eyeTracker.response_start()

    def set_feedback_scene(self, response_time, failed=False):
        self.eyeTracker.response_end()
        self.eyeTracker.feedback_start()
        self.responded = True
        self.dataDict["answer"] = 0 if failed else 1
        self.dataDict["response_time"] = response_time
        color = (1, -1, -1) if failed else (-1, 1, -1)
        feedback = visual.Rect(self.win, width=200, height=200, fillColor=color, lineColor=color)
        self.scene = FeedbackScene(self.win, self, feedback)

    def update(self):
        self.scene.update()
        self.win.flip()

    def set_intertrial_scene(self):
        if self.responded == False:
            self.eyeTracker.response_end()
        if self.dataDict is not None:
            self.data.append(self.dataDict)
        self.dataDict = {}
        self.dataDict["trial_number"] = self.conditions[self.currentSet]["set"]
        self.dataDict["type"] = self.conditions[self.currentSet]["type"]
        self.eyeTracker.start_recording()
        self.scene = InterTrialScene(self.win, self, constants.INTERTRIAL_TEXT)

    def end_experiment(self):
        self.isRunning = False

    def next_set(self):
        self.eyeTracker.stop_recording()
        if self.currentSet >= len(self.conditions) - 1:
            self.isRunning = False
            self.eyeTracker.close()
            if self.dataDict is not None:
                self.data.append(self.dataDict)
        else:
            self.currentSet += 1
            self.set_intertrial_scene()

    def save_experiment(self, writer):
        writer.writerows(self.data)

def shuffle_sequence(sequence):
    i = 0
    while not check_sequence(sequence):
        random.shuffle(sequence)
        if i > 100000:
            print("Could not shuffle sequence")
            break
        i += 1

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

    visual.TextStim(window, text="Practice trials").draw()
    window.flip()
    practice = True
    while practice == True:
        manager = ExperimentManager(window, "test.xlsx")
        manager.set_feedback_scene = lambda float, failed=None: manager.next_set()
        manager.start_experiment()
        while manager.isRunning:
            manager.update()
        visual.TextStim(window, text="More practice?").draw()
        window.flip()
        if constants.FALSE_KEY in event.waitKeys():
            practice = False

    filename = "{}_{}.csv".format(subjectInfo["SubjectInitials"], subjectInfo["SubjectID"])      
    
    visual.TextStim(window, text="Eyetracker setup").draw()
    window.flip()
    manager = ExperimentManager(window, "test.xlsx")

    while manager.isRunning:
        manager.update()
    with open(filename, mode="w") as csv_file:
        fieldNames = ["trial_number",
                      "type",
                      "answer",
                      "response_time",
                      "trial_start",
                      "fixation_start",
                      "sound_start",
                      "sound_end",
                      "response_start",
                      "response_given",
                      "response_end",
                      "feedback_start"]
        writer = csv.DictWriter(csv_file, fieldnames=fieldNames)
        writer.writeheader()
        manager.save_experiment(writer)

