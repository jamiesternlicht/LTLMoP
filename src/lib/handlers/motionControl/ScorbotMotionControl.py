

"""
=============================
ScorbotMotionControl.py - Motion Controller
=============================

Uses simple predetermined saved locations for movement to regions
"""

import time

class motionControlHandler: 

    def __init__(self,proj,shared_data): 
        self.drive_handler = proj.h_instance['drive']
        self.system_print = False
        self.proj = proj
        self.pose_handler = proj.h_instance['pose'] # Have pose, to verify reached destination

    def gotoRegion(self,current_reg,next_reg, last = False): 

        if current_reg == next_reg and not last:  
            return True

        if self.system_print == True: 
            print "Next Region is " + str(self.proj.rfi.regions[next_reg].name)
            print "Current Region is " + str(self.proj.rfi.regions[current_reg].name)

        if last:
            transFace = None
        else: 
            transFace = None

        # Finds point it next wants to go to, sets controller. 
        # Currently this is region names, but in the future will be changed to offset values.
        self.drive_handler.setVelocity("move "+str(self.proj.rfi.regions[next_reg].name)+"\r") 
        time.sleep(3)
        return True