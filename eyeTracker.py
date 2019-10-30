import constants
import pylink
from EyeLinkCoreGraphicsPsychoPy import EyeLinkCoreGraphicsPsychoPy
from psychopy import visual, event

class EyeTracker(object):
    def __init__(self, win, fileName, manager):
        self.win = win
        self.text = visual.TextStim(self.win, text="hello")
        self.manager = manager
        if constants.DUMMY_MODE == False:
            self.tk = pylink.EyeLink("100.1.1.1")
        else:
            self.tk = pylink.EyeLink(None)
        self.tk.openDataFile(fileName)
        self.tk.sendCommand("add_file_preamble_text 'Psychopy teleological task'")
        genv = EyeLinkCoreGraphicsPsychoPy(self.tk, win)
        pylink.openGraphicsEx(genv)

    def calibrate(self):
        self.tk.setOfflineMode()
        self.tk.sendCommand('sample_rate 500')
        self.tk.sendCommand("screen_pixel_coords = 0 0 %d %d" % (constants.WINDOW_SIZE[0]-1, constants.WINDOW_SIZE[1]-1))
        self.tk.sendMessage("DISPLAY_COORDS = 0 0 %d %d" % (constants.WINDOW_SIZE[0]-1, constants.WINDOW_SIZE[1]-1)) 
        self.tk.sendCommand("calibration_type = HV9") # self.tk.setCalibrationType('HV9') also works, see the Pylink manual
        eyelinkVer = self.tk.getTrackerVersion()
        #turn off scenelink camera stuff (EyeLink II/I only)
        if eyelinkVer == 2: self.tk.sendCommand("scene_camera_gazemap = NO")
        # Set the tracker to parse Events using "GAZE" (or "HREF") data
        self.tk.sendCommand("recording_parse_type = GAZE")
        if eyelinkVer>=2: 
            self.tk.sendCommand('select_parser_configuration 0')
        # get Host tracking software version
        hostVer = 0
        if eyelinkVer == 3:
            tvstr  = self.tk.getTrackerVersionString()
            vindex = tvstr.find("EYELINK CL")
            hostVer = int(float(tvstr[(vindex + len("EYELINK CL")):].strip()))

        # specify the EVENT and SAMPLE data that are stored in EDF or retrievable from the Link
        # See Section 4 Data Files of the EyeLink user manual
        self.tk.sendCommand("file_event_filter = LEFT,RIGHT,FIXATION,SACCADE,BLINK,MESSAGE,BUTTON,INPUT")
        self.tk.sendCommand("link_event_filter = LEFT,RIGHT,FIXATION,FIXUPDATE,SACCADE,BLINK,BUTTON,INPUT")
        if hostVer>=4: 
            self.tk.sendCommand("file_sample_data  = LEFT,RIGHT,GAZE,AREA,GAZERES,STATUS,HTARGET,INPUT")
            self.tk.sendCommand("link_sample_data  = LEFT,RIGHT,GAZE,GAZERES,AREA,STATUS,HTARGET,INPUT")
        else:          
            self.tk.sendCommand("file_sample_data  = LEFT,RIGHT,GAZE,AREA,GAZERES,STATUS,INPUT")
            self.tk.sendCommand("link_sample_data  = LEFT,RIGHT,GAZE,GAZERES,AREA,STATUS,INPUT")
        self.tk.doTrackerSetup()
        self.manager.start_experiment()

    def update(self):
        keys = event.getKeys()
        if 'space' in keys:
            print("update")
            self.manager.start_experiment()

    def draw(self):
        self.text.draw()
    
