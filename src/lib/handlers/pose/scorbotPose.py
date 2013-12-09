#!/usr/bin/env python
"""
=======================================
scorbotPose.py - Scorbot Pose Handler
=======================================

Get data from serial

"""


from numpy import *
import logging, time
import serial 
import re


class poseHandler:
    def __init__(self, proj, shared_data):
        """
        Pose Handler for Scorbot robot
        """
        try: 
            self.scorbotSer = shared_data["ScorbotSer"]
        except: 
            print "(POSE) ERROR: No connection to Scorbot"
            return

        self.starting = True
        self.lastPose = self.getPose()

        pass
    def getPose(self, cached=False):
        """ Pose returned from encoders on Scorbot """   
        if cached: 
            return self.lastPose

        starttime = time.clock()
        #logging.debug("Pose start")
        self.scorbotSer.flushInput()    
        
        self.scorbotSer.write('here pose\r') # Setting Pose
        self.scorbotSer.readline()
        self.scorbotSer.readline()
        self.scorbotSer.write('listpv pose\r') # Listing Pose
        self.scorbotSer.readline()
        self.scorbotSer.readline()
        self.scorbotSer.readline()
        line = self.scorbotSer.readline()
        
        fullpose = map(int, re.findall(r'-?\d+', line)) # This recieves X,Y,Z,Pitch,Roll
        pose = fullpose[:3] # This limits the pose communication to X,Y,Z 

        #logging.debug("Pose end")
        #print "Pose: ", pose 

        tottime = (time.clock()-starttime)
        #print "This is the ammount of time for pose: {}s".format(tottime)
        
        self.lastPose = array(pose).astype(float)

        return self.lastPose #[:2]
        
        #return array([3478,-3051,0]) # 1556






