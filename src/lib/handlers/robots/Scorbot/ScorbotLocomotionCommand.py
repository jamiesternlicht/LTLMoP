
"""
================================================================================
ScorbotLocomotionCommand.py - The Scorbot's Locomotion Command Handler
================================================================================
"""

import time
import serial

class locomotionCommandHandler:    
    """
    This class will tell the Scorbot which region to move to.
    """
    
    def __init__(self, proj, shared_data): 
        try: 
            self.scorbotSer = shared_data["ScorbotSer"]
        except: 
            print "(LOCO) ERROR: No connection to Scorbot"
            return

    def sendCommand(self, cmd): 
        # MAKE COMMANDS 
        try:
            self.scorbotSer.write(cmd) # Writes movement command to serial port.
            # This command comes from ScorbotDrive
        except: 
            print "(LOCO) ERROR: Didn't perform movement" 
            return




        
