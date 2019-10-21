import random
import constants

class FeedbackScene(object):
    def __init__(self, win, manager, feedback):
        self.win = win
        self.manager = manager
        self.feedback = feedback
        self.max_frame = int((random.randrange(constants.MIN_FEEDBACK_JITTER * 10, constants.MAX_FEEDBACKJITTER * 10, 2) / 10) * constants.FRAME_RATE)
        self.current_frame = 0

    def update(self):
        self.current_frame +=1
        if self.current_frame >= self.max_frame:
            self.manager.next_set()
        self.draw()

    def draw(self):
        self.feedback.draw()