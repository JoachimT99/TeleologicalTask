from interTrialScene import InterTrialScene
import pylink
from audioScene import AudioScene
from psychopy import data, visual, gui, core, event
from infoScene import InfoScene
from responseScene import ResponseScene
from feedbackScene import FeedbackScene
import random
import csv
from eyeTracker import EyeTracker
import os
import time
import constants

class ExperimentManager(object):
    def __init__(self, win, dataFile, tracker):
        """
        Initializes experiment
        Params:
            win: window object
            dataFile: a file like object
            tracking: determines wether or not tracker calibration is performed
        Returns:
            None
        """
        self.win = win
        #Fix sequnce
        self.conditions = data.importConditions(dataFile)
        shuffle_sequence(self.conditions)
        self.uniqueConditions = len(self.conditions)
        #Sets necessary variables
        self.eyeTracker = tracker
        self.currentSet = 0
        self.isRunning = True
        self.data = []
        self.dataDict = None
        self.responded = None
        #Configures eyetracker
        self.scene = self.eyeTracker

    def start_experiment(self):
        self.scene = InfoScene(self.win, self, constants.EXPERIMENT_START_TEXT)

    def set_audio_scene(self):
        """
        Sets audio scene
        Params:
            None
        Returns:
            None
        """
        fileName = "data/"+self.conditions[self.currentSet]["wav"]
        cross = visual.ImageStim(self.win, image=constants.FIXATION_CROSS, size=(200, 200), units="pix")
        self.scene = AudioScene(self.win, self, fileName, cross)
        self.eyeTracker.fixation_cross_start()


    def set_response_scene(self):
        """
        Sets the response scene
        Params:
            None
        Returns:
            None
        """
        self.eyeTracker.sound_end()
        self.responded = False
        corAns = self.conditions[self.currentSet]["CorAns"]
        cross = visual.ImageStim(self.win, image=constants.FIXATION_CROSS, size=(200, 200), units="pix")
        self.scene = ResponseScene(self.win, self, corAns, cross)
        self.eyeTracker.response_start()

    def set_feedback_scene(self, response_time, failed=False):
        """
        Sets the visual feedback scene
        Params:
            None
        Returns:
            None
        """
        self.eyeTracker.response_end()
        self.eyeTracker.feedback_start()
        self.responded = True
        self.dataDict["answer"] = 0 if failed else 1
        self.dataDict["response_time"] = response_time
        if failed:
            feedback = visual.ImageStim(self.win, image=constants.NEG_FEEDBACK, size=(200, 200), units="pix")
        else:
            feedback = visual.ImageStim(self.win, image=constants.POS_FEEDBACK, size=(200, 200), units="pix")
        self.scene = FeedbackScene(self.win, self, feedback)

    def update(self):
        """
        Updates the scene
        Params:
            None
        Returns:
            None
        """
        self.scene.update()
        self.win.flip()

    def set_intertrial_scene(self):
        """
        Sets a blank scene to be played between trials
        Params:
            None
        Returns:
            None
        """
        if self.dataDict is not None:
            self.data.append(self.dataDict)
        self.dataDict = {}
        self.dataDict["trial_number"] = self.conditions[self.currentSet]["set"]
        self.dataDict["type"] = self.conditions[self.currentSet]["type"]
        self.eyeTracker.start_recording(self.currentSet)
        self.scene = InterTrialScene(self.win, self, constants.INTERTRIAL_TEXT)

    def end_experiment(self):
        self.isRunning = False

    def next_set(self):
        """
        Goes to the next trial in the list of conditions.
        Ends the experiment if all trials have been answered.
        Params:
            None
        Returns:
            None
        """
        self.eyeTracker.stop_recording()
        if self.responded == False:
            self.eyeTracker.response_end()
            self.dataDict["answer"] = "NA"
            self.dataDict["response_time"] = "NA"
            self.eyeTracker.stop_recording()
            if self.currentSet <= self.uniqueConditions - 1:
                self.conditions.append(self.conditions[self.currentSet])
        if self.currentSet >= len(self.conditions) - 1:
            self.isRunning = False
            if self.dataDict is not None:
                self.data.append(self.dataDict)
        else:
            self.currentSet += 1
            self.set_intertrial_scene()

    def practice_set_feedback(self, float, failed=None):
        """
        Used to bypass the feedback scene for practice trials
        Params:
            float: not used
            failed: not used
        Returns:
            None
        """
        self.responded = True
        self.next_set()

    def save_experiment(self, writer, id):
        """
        Saves information using a writer like object
        Params:
            writer: A writer like object with 'writerows' method
        Returns:
            None
        """
        for dict in self.data:
            dict["ID"] = id
        writer.writerows(self.data)

def shuffle_sequence(sequence):
    """
    Randomly shuffles a sequence
    Params:
        sequence: A list object
    Returns:
        None
    """
    i = 0
    while not check_sequence(sequence):
        random.shuffle(sequence)
        if i > 100000:
            print("Could not shuffle sequence")
            break
        i += 1

def check_sequence(sequence):
    """
    Checks the sequence for 4 consecutive elements of the same type
    Params:
        sequence: a list of dicionaries with a column named type
    Returns:
        None
    """
    for i, item in enumerate(sequence):
        if i < 3:
            continue
        if item["type"] == sequence[i-1]["type"] and item["type"] == sequence[i-2]["type"] and item["type"] == sequence[i-3]["type"]:
            return False
    return True


def get_subject_info():
    """
    Presents dialogue box to get subject information
    Params:
        None
    Returns:
        dictionary with subject information
    """
    info = {"SubjectID":"00", "SubjectInitials":"TEST"}
    dlg = gui.DlgFromDict(dictionary=info, title="Enter relevant information", order=("SubjectID", "SubjectInitials"))
    if not dlg.OK:
        core.quit()
    else:
        return info


#Starting point of experiment
if __name__ == "__main__":

    subjectInfo = get_subject_info()
    
        
    window = visual.Window(constants.WINDOW_SIZE, units="pix", fullscr=True)


    visual.TextStim(window, text=constants.PRACTICE_START_TEXT).draw()
    window.flip()
    dataFolder = os.getcwd() + '/edfData/'
    if not os.path.exists(dataFolder): 
        os.makedirs(dataFolder)
    dataFileName = constants.EDF_FILENAME + '.EDF'
    tracker = EyeTracker(window, dataFileName, dataFolder, dummy=constants.DUMMY_MODE)
    tracker.calibrate()
    # practice = True
    # tracker.practice_start()
    # while practice == True:
    #     manager = ExperimentManager(window, constants.PRACTICE_TRIALS, tracker)
    #     tracker.set_manager(manager)
    #     manager.start_experiment()
    #     manager.set_feedback_scene = manager.practice_set_feedback
    #     manager.start_experiment()
    #     while manager.isRunning:
    #         manager.update()
    #     visual.TextStim(window, text=constants.PRACTICE_END_TEXT).draw()
    #     window.flip()
    #     if constants.FALSE_KEY in event.waitKeys():
    #         practice = False
    # tracker.practice_end()
    filename = "{}_{}.csv".format(subjectInfo["SubjectInitials"], subjectInfo["SubjectID"])
    
    manager = ExperimentManager(window, constants.TRIALS, tracker)
    tracker.open_file(dataFileName)
    tracker.set_manager(manager)
    manager.start_experiment()

    while manager.isRunning:
        manager.update()
    with open(filename, mode="w") as csv_file:
        fieldNames = ["ID",
                      "trial_number",
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
        manager.save_experiment(writer, subjectInfo["SubjectID"])
    tracker.close_dataFile(dataFileName, dataFolder)
    tracker.close_tracker()
    visual.TextStim(window, text=constants.END_TEXT).draw()
    window.flip()
    event.waitKeys()
