
"""
================================================================================
ScorbotLocomotionCommand.py - The Scorbot's Locomotion Command Handler
================================================================================
"""

import time, logging

class locomotionCommandHandler:    
    
    def __init__(self, proj, shared_data): 
        """
        This class will tell the Scorbot which region to move to.
        """

        try: 
            self.scorbotSer = shared_data["ScorbotSer"]
        except: 
            logging.error("(LOCO) ERROR: No connection to Scorbot")

    def sendCommand(self, cmd): 
        
        try:
            self.scorbotSer.write(cmd) # Writes movement command to serial port.
            # This command comes from ScorbotDrive
            self.scorbotSer.readline()
            self.scorbotSer.readline()
        except: 
            logging.error("(LOCO) ERROR: Didn't perform movement")




        
