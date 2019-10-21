from psychopy import event
import constants

class ResponseScene(object):
    def __init__(self, win, manager, corAns, fixationCross):
        self.win = win
        self.manager = manager
        self.corAns = True if corAns == 'Yes' else False
        self.fixationCross = fixationCross
        self.max_frame = constants.MAX_DECISION_TIME * constants.FRAME_RATE
        event.clearEvents()
        self.current_frame = 0
        self.failed = None

    def check_input(self):
        keys = event.getKeys()
        if 'd' in keys and self.failed is None:
            self.current_frame = 0
            self.max_frame = constants.RESPONSE_DELAY * constants.FRAME_RATE
            self.failed = self.corAns ^ True
        elif 'k' in keys and self.failed is None:
            self.current_frame = 0
            self.max_frame = constants.RESPONSE_DELAY * constants.FRAME_RATE
            self.failed = self.corAns ^ False


    def update(self):
        self.current_frame += 1
        if self.current_frame >= self.max_frame and self.failed is None:
            self.manager.next_set()
        elif self.current_frame >= self.max_frame and self.failed is not None:
            self.manager.set_feedback_scene(failed=self.failed)
        self.check_input()
        self.draw()

    def draw(self):
        self.fixationCross.draw()