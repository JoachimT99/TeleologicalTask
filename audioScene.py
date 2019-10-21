from psychopy.sound import Sound
import math
import constants

class AudioScene(object):
    def __init__(self, win, manager, soundFile, fixationCross):
        self.win = win
        self.manager = manager
        self.sound = Sound(soundFile)
        self.fixationCross = fixationCross
        self.max_frame = math.ceil(self.sound.getDuration() * constants.FRAME_RATE)
        self.current_frame = 0
        self.sound.play()
    
    def update(self):
        self.current_frame += 1
        if self.current_frame >= self.max_frame:
            self.manager.set_response_scene()
        self.draw()

    def draw(self):
        self.fixationCross.draw()