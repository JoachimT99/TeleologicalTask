from psychopy import visual

FRAME_RATE = 60 # refreshrate of the monitor used
WINDOW_SIZE = (1280, 1024)

WINDOW = visual.Window(WINDOW_SIZE, units="pix", fullscr=True)


INTERTRIAL_TEXT = "Press 'space' to initiate the next trial"

EXPERIMENT_START_TEXT = "This is information about the experiment. Press 'd' to continue."
FIXATION_CROSS = "fixation_cross.png"

PRACTICE_START_TEXT = "Practice trials. Press 'enter' to calibrate or 'escape' to exit"
PRACTICE_END_TEXT = "Do you want to redo the practice trials? Press 'd' for yes and 'k' for no"

END_TEXT = "Thank you for participating"

TRUE_KEY = 'd'
FALSE_KEY = 'k'

PRACTICE_TRIALS = "test.xlsx"
TRIALS = "test.xlsx"
EDF_FILENAME = "test"

NEG_FEEDBACK = visual.Rect(WINDOW, width=200, height=200, fillColor=(1, -1, -1), lineColor=(1, -1, -1))
POS_FEEDBACK = visual.Rect(WINDOW, width=200, height=200, fillColor=(-1, 1, -1), lineColor=(-1, 1, -1))


DUMMY_MODE = True

AUDIO_DELAY = 0.2 #seconds

#Sets the wait after the resonse
MIN_RESPONSE_DELAY = 1.8 #seconds
MAX_RESPONSE_DELAY = 2.4 #seconds non-inclusive


MIN_FEEDBACK_JITTER = 4.0 #seconds
MAX_FEEDBACKJITTER = 6.2 # seconds non-inclusive


MAX_DECISION_TIME = 4

