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
        self.scorbotSer.write('here pose\r')
        self.scorbotSer.write('listpv pose\r')

        if self.starting:
            time.sleep(5)
            self.scorbotSer.write('here pose\r')
            self.scorbotSer.write('listpv pose\r')
            self.scorbotSer.starting = False


        gotPose = False
        for i in range(50):
            line = self.scorbotSer.readline()[1:]
            if line == "":
                continue

            print "line: ", i
            print line

            if line[0][0] == "X":
                gotPose = True
                break;

        print "No more waiting!"

        #return array([1,1,1])

        if not gotPose:
            return array([])

        fullpose = map(int, re.findall(r'-?\d+', line))
        pose = fullpose[:3]

        print "fullpose: ", fullpose
        print "pose: ", pose 

        return array(pose).astype(float)[:2]









