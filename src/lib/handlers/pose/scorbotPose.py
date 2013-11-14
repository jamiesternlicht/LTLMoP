#!/usr/bin/env python
"""
=======================================
scorbotPose.py - Scorbot Pose Handler
=======================================

Get data from serial

"""


from numpy import *
import time
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

        pass
    def getPose(self, cached=False):
        """ No return for now """   
        
        print "Pose is here"

        self.scorbotSer.flush()
        
        self.scorbotSer.write('here pose\r') # Setting Pose
        self.scorbotSer.write('listpv pose\r') # Listing Pose
        
        
        if self.starting:
            time.sleep(.5)
            print "This is checking whether this turns OFF"
            self.scorbotSer.write('here pose\r')
            self.scorbotSer.write('listpv pose\r')
            print "BEFORE: ", (self.starting)
            #self.starting = False
            print "AFTER: ", (self.starting)
            

        gotPose = False
        for i in range(50):
            line = self.scorbotSer.readline()[1:]
            if line == "":
                continue

            # print "line: ", i
            # print line

            if line[0][0] == "X": # Finding Position line in XYZPR instead of Joints (1-5)
                gotPose = True
                break;

        if not gotPose:
            return array([])

        fullpose = map(int, re.findall(r'-?\d+', line)) # This recieves X,Y,Z,Pitch,Roll
        pose = fullpose[:3] # This limits the pose communication to X,Y,Z 

        print "Pose: ", pose 

        return array(pose).astype(float) #[:2]









