from psychopy import visual, event
import constants

class InfoScene(object):
    def __init__(self, win, manager, text):
        self.win = win
        self.manager = manager
        self.text = visual.TextStim(self.win,
                                    text=text,
                                    wrapWidth=constants.WINDOW_SIZE[0])


    def check_input(self):
        if 'd' in event.getKeys():
            self.manager.set_intertrial_scene()

    def draw(self):
        self.text.draw()
    
    def update(self):
        self.check_input()
        self.draw()