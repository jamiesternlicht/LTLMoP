

""" 
===================
ScorbotDrive.py - DriveHandler for Scorbot
===================

""" 
import time

class driveHandler(): 

    def __init__(self,proj,shared_data): 
        self.stopped=True
        self.loco = proj.h_instance['locomotionCommand']
        init_region = proj.h_instance['init']['Ralph'].init_region
        self.setVelocity("move "+init_region+"\r")
        time.sleep(3)

    def setVelocity(self, cmd, optional_cmd=None):
        if optional_cmd == None:
            self.loco.sendCommand(cmd)