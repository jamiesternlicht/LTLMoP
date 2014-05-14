#!/usr/bin/env python
"""
=========================================
ScorbotActuator.py - Scorbot Actuator Handler
=========================================

The actions for the scorbot, pick_up and drop_off (open gripper?)
"""
import time, math
import logging, globalConfig

import lib.handlers.handlerTemplates as handlerTemplates

class ScorbotActuatorHandler(handlerTemplates.ActuatorHandler):
    
    def __init__(self, executor, shared_data): 

        self.proj = executor.proj

        self.pose_handler = executor.hsub.getHandlerInstanceByType(handlerTemplates.PoseHandler)   
        self.drive_handler = executor.hsub.getHandlerInstanceByType(handlerTemplates.DriveHandler)


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

            time.sleep(1) # Sleep is used to ensure that actuator gets pose before proceeding
            pose = self.pose_handler.getPose()
            self._gotoCenter(pose)

            self.scorbotSer.write("open\r") 
            self.scorbotSer.read()
            self.scorbotSer.read() 
            time.sleep(3) #This sleep is here to ensure that it completes opening before proceeding

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


            self.scorbotSer.write("move O0\r")
            self.scorbotSer.read()
            self.scorbotSer.read()
            time.sleep(6) # This sleep is here to ensure the gripper fully drops before closing

            self.scorbotSer.write("close\r")
            self.scorbotSer.read()
            self.scorbotSer.read()
            time.sleep(3) # This sleep is here to ensure the gripper fully closes before raising 

            self.scorbotSer.write("move O1\r")
            self.scorbotSer.read()
            self.scorbotSer.read()
            time.sleep(3) # This sleep is here to ensure the gripper fully raises before beginning to navigate again



    def _getCurrentRegionFromPose(self, pose):
        rfi = self.proj.rfi

        
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
        time.sleep(3) #This sleep is here to ensure that the Scorbot moves to the centroid
