#!/usr/bin/env python
"""
=========================================
ScorbotActuator.py - Scorbot Actuator Handler
=========================================

The actions for the scorbot, will be able to lower close raise and open
"""
import time

class actuatorHandler:
    
    def __init__(self, proj, shared_data):   
        try: 
            self.scorbotSer = shared_data["ScorbotSer"]
        except: 
            print "(ACTUATOR) ERROR: No connection to Scorbot"
            return
    

    def open(self,actuatorVal,initial=False):
        if initial: 
            return 
        if actuatorVal:
            self.scorbotSer.write("open\r") 
            time.sleep(2)
        

    def lower_close_raise(self,actuatorVal, initial=False): 
        if initial: 
            return 
        if actuatorVal: 
            self.scorbotSer.write("move O0\r")
            time.sleep(2)
            self.scorbotSer.write("close\r")
            time.sleep(2)
            self.scorbotSer.write("move O1\r")
            time.sleep(2)