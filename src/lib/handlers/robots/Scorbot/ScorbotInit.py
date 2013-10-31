"""
=================================================
ScorbotInit.py -- Scorbot Initialization Handler 
=================================================

"""

import time
import serial

class initHandler:

    def __init__(self, proj, init_region, port ='/dev/ttyUSB0'): 

	"""
        Initialization handler for Scorbot robot. 

        init_region (region): The name of the region where the robot starts
        port (string): The port of scorbot (default = "/dev/tty.usbserial-A1001aew")
        """

        try:
            self.scorbotSer = serial.Serial(port)
        except Exception as e: 
            print("(INIT) ERROR: Couldn't connect to Scorbot") 
            print (e)
            return
        self.init_region = init_region

    def Stop(self): 
        print "(INIT) Shutting down serial port!" 
        self.scorbotSer.close()

    def getSharedData(self):
        return {"ScorbotSer" : self.scorbotSer}



 
