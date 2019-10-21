from psychopy import event
import constants

class ResponseScene(object):
    def __init__(self, win, manager, corAns, fixationCross):
        self.win = win
        self.manager = manager
        self.corAns = True if corAns == 'Yes' else False
        self.fixationCross = fixationCross
        self.max_frame = 4 * constants.FRAME_RATE
        event.clearEvents()
        self.current_frame = 0

    def check_input(self):
        keys = event.getKeys()
        if 'd' in keys:
            self.manager.set_feedback_scene(failed=(self.corAns ^ True))
        elif 'k' in keys:
            self.manager.set_feedback_scene(failed=(self.corAns ^ False))


    def update(self):
        self.current_frame += 1
        if self.current_frame >= self.max_frame:
            self.manager.set_intertrial_scene()
        self.check_input()
        self.draw()

    def draw(self):
        self.fixationCross.draw()