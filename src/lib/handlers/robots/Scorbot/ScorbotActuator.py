#!/usr/bin/env python
"""
=========================================
ScorbotActuator.py - Scorbot Actuator Handler
=========================================

The actions for the scorbot, pick_up and drop_off (open gripper?)
"""
import time, math
import logging, globalConfig

class ScorbotActuatorHandler:
    
    def __init__(self, proj, shared_data): 

        self.proj = proj

        self.pose_handler = proj.h_instance['pose']   
        self.drive_handler = proj.h_instance['drive']


        try: 
            self.scorbotSer = shared_data["ScorbotSer"]
        except: 
            logging.error("(ACTUATOR) ERROR: No connection to Scorbot")
            return
    

    def drop_off(self,actuatorVal,initial=False):
        """
        This actuator opens the gripper
        """
        if initial: 
            return 

        if int(actuatorVal) == 1:

            time.sleep(1)
            pose = self.pose_handler.getPose()
            self._gotoCenter(pose)

            self.scorbotSer.write("move goal\r") 
            self.scorbotSer.read()
            self.scorbotSer.read()
            time.sleep(3)
            self.scorbotSer.write("open\r") 
            self.scorbotSer.read()
            self.scorbotSer.read() #time.sleep(2) # COMMENT SLEEP IF STILL GOING TO USE
            time.sleep(3)

    def pick_up(self,actuatorVal, initial=False): 
        """
        This actuator lowers the gripper over the ring, and closes the gripper
        """

        if initial: 
            return 

        if int(actuatorVal) == 1: 

            time.sleep(1)
            pose = self.pose_handler.getPose()
            self._gotoCenter(pose)

            print "Passing move oset"

            self.scorbotSer.write("move O0\r")
            self.scorbotSer.read()
            self.scorbotSer.read()
            time.sleep(7)
            print "Passing drop down"
            self.scorbotSer.write("close\r")
            self.scorbotSer.read()
            self.scorbotSer.read()
            time.sleep(3)
            print "Passing close"
            self.scorbotSer.write("move O1\r")
            self.scorbotSer.read()
            self.scorbotSer.read()
            time.sleep(3)
            print "Passing raise up"


    def _getCurrentRegionFromPose(self, pose):
        rfi = self.proj.rfi

        tm = self.proj.currentConfig.getRobotByName(self.proj.currentConfig.main_robot).calibrationMatrix
        
        pose = self.proj.coordmap_lab2map(pose)
        
        region = next((r for i, r in enumerate(rfi.regions) if r.name.lower() != "boundary" and \
                        r.objectContainsPoint(*pose)), None)
 
        if region is None:
            logging.warning("Pose of {} not inside any region!".format(pose))

        return region

    def _gotoCenter(self,pose):

        print "I am going to center"

        current_region = self._getCurrentRegionFromPose(pose[:2])
        target = self.proj.coordmap_map2lab(current_region.getCenter())

        Xmove = target[0] - pose[0]
        Ymove = target[1] - pose[1]

        print "Xmove ", Xmove 
        print "Ymove ", Ymove 

        Zmove = 0 # (Z direction)
        Pmove = 0 # (Pitch)
        Rmove = 0 # (Roll)

        self.scorbotSer.flushInput()
        self.scorbotSer.write('teachr oset\r')
        self.scorbotSer.readline() 
        self.scorbotSer.write('%d' % Xmove + '\r') 
        self.scorbotSer.readline()
        self.scorbotSer.write('%d' % Ymove + '\r')
        self.scorbotSer.readline()
        self.scorbotSer.write('%d' % Zmove + '\r')
        self.scorbotSer.readline()
        self.scorbotSer.write('%d' % Pmove + '\r')
        self.scorbotSer.readline()
        self.scorbotSer.write('%d' % Rmove + '\r')
        self.scorbotSer.readline()
        self.scorbotSer.readline()

        self.scorbotSer.write('move oset\r') 
        self.scorbotSer.readline()
        self.scorbotSer.readline()
        time.sleep(3)
