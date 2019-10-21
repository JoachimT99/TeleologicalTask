import constants
from psychopy import visual, event

class InterTrialScene(object):
    def __init__(self, win, manager, text):
        self._manager = manager
        self.text = visual.TextStim(win,
                                    text=text,
                                    wrapWidth=constants.WINDOW_SIZE[0])

    def check_input(self):
        keys = event.getKeys()
        if 'space' in keys:
            self._manager.set_audio_scene()
    
    def update(self):
        self.check_input()
        self.draw()

    def draw(self):
        self.text.draw()