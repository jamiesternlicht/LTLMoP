"""
=================================================
ScorbotInit.py -- Scorbot Initialization Handler 
=================================================

"""

import serial
import logging 

import lib.handlers.handlerTemplates as handlerTemplates

class ScorbotInitHandler(handlerTemplates.InitHandler):

    def __init__(self, executor, init_region, port): 

        """
        Initialization handler for Scorbot robot. 

        init_region (region): The name of the region where the robot starts
        port (string): The port of scorbot (default = "/dev/tty.usbserial-A1001aew")
        """

        try:
            self.scorbotSer = serial.Serial(port)
        except Exception as e: 
            logging.error("(INIT) ERROR: Couldn't connect to Scorbot") 
            print (e)
            return
        self.init_region = init_region 
        #Initial region is set by user in LTLMoP init config... maybe...

    def _stop(self): 
        logging.info("(INIT) Shutting down serial port!")
        self.scorbotSer.close()

    def getSharedData(self):
        return {"ScorbotSer" : self.scorbotSer}

    def sendCommand(cmd, num_lines):

        self.scorbotSer.write(cmd)
        for x in range(num_lines): 
            self.scorbotSer.readline()


 
