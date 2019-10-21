import constants
from psychopy import visual

class InterTrialScene(object):
    def __init__(self, manager, fixationCross):
        self._manager = manager
        self.fixationCross = fixationCross
        self.max_frame = constants.interTrialBlankDuration + constants.interTrialFixationDuration
        self.current_frame = 0

    def check_input(self):
        pass
    
    def update(self):
        self.current_frame += 1
        if self.current_frame >= self.max_frame:
            self._manager.set_audio_scene()
        if self.current_frame > constants.interTrialBlankDuration:
            self.draw()

    def draw(self):
        self.fixationCross.draw()