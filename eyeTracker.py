import constants
import pylink
from EyeLinkCoreGraphicsPsychoPy import EyeLinkCoreGraphicsPsychoPy
from psychopy import visual, event
from datetime import datetime

class EyeTracker(object):
    def __init__(self, win, fileName, folderName, dummy=False):
        self.win = win
        self.text = visual.TextStim(self.win, text="hello")
        if dummy == False:
            self.tk = pylink.EyeLink("100.1.1.1")
        else:
            self.tk = pylink.EyeLink(None)
        self.dataFileName = fileName
        self.dataFolderName = folderName
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

    def start_recording(self):
        self.tk.startRecording(1,1,1,1)
        self.tk.sendMessage("trial_start")
        self.manager.dataDict["trial_start"] = datetime.now()

    def stop_recording(self):
        self.tk.stopRecording()
    
    def close(self):
        self.tk.setOfflineMode()
        self.tk.closeDataFile()
        self.tk.receiveDataFile(self.dataFileName, self.dataFolderName + self.dataFileName)
        self.tk.close()

    def display_message(self, message):
        self.tk.sendCommand("record_status_message '{}'".format(message))

    def sound_start(self):
        self.tk.sendMessage("sound_start")
        self.manager.dataDict["sound_start"] = datetime.now()

    def sound_end(self):
        self.tk.sendMessage("sound_end")
        self.manager.dataDict["sound_end"] = datetime.now()

    def response_start(self):
        self.tk.sendMessage("response_start")
        self.manager.dataDict["response_start"] = datetime.now()

    def response_given(self):
        self.tk.sendMessage("response_given")
        self.manager.dataDict["response_given"] = datetime.now()

    def response_end(self):
        self.tk.sendMessage("response_end")
        self.manager.dataDict["response_end"] = datetime.now()

    def feedback_start(self):
        self.tk.sendMessage("feedback_start")
        self.manager.dataDict["feedback_start"] = datetime.now()

    def fixation_cross_start(self):
        self.tk.sendMessage("fixation_start")
        self.manager.dataDict["fixation_start"] = datetime.now()
        
    def practice_start(self):
        self.tk.sendMessage("practice_start")
        
        
    def practice_end(self):
        self.tk.sendMessage("practice_end")
        
    def set_manager(self, manager):
        self.manager = manager

    def update(self):
        keys = event.getKeys()
        print("update")
        if 'space' in keys:
            self.manager.start_experiment()

    def draw(self):
        self.text.draw()
    
