from psychopy import event
import constants
import random
import math
import time

class ResponseScene(object):
    def __init__(self, win, manager, corAns, fixationCross):
        self.win = win
        self.manager = manager
        self.corAns = True if corAns == 'Yes' else False
        self.fixationCross = fixationCross
        self.max_frame = constants.MAX_DECISION_TIME * constants.FRAME_RATE
        self.response_wait = math.ceil(random.randrange(constants.MIN_RESPONSE_DELAY * 10, constants.MAX_RESPONSE_DELAY * 10, 2) / 10) 
        event.clearEvents()
        self.current_frame = 0
        self.failed = None
        self.startTime = time.time()

    def check_input(self):
        keys = event.getKeys()
        if constants.TRUE_KEY in keys and self.failed is None:
            self.elapsedTime = time.time() - self.startTime
            self.current_frame = 0
            self.max_frame = self.response_wait * constants.FRAME_RATE
            self.failed = self.corAns ^ True
        elif constants.FALSE_KEY in keys and self.failed is None:
            self.elapsedTime = time.time() - self.startTime
            self.current_frame = 0
            self.max_frame = self.response_wait * constants.FRAME_RATE
            self.failed = self.corAns ^ False


    def update(self):
        self.current_frame += 1
        if self.current_frame >= self.max_frame and self.failed is None:
            self.manager.next_set()
        elif self.current_frame >= self.max_frame and self.failed is not None:
            self.manager.set_feedback_scene(self.elapsedTime, failed=self.failed)
        self.check_input()
        self.draw()

    def draw(self):
        self.fixationCross.draw()