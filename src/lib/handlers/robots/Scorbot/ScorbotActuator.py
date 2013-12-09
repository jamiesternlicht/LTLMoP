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

            pose = self.pose_handler.getPose()
            pose = pose[:2]
            region1 = [2590, -3709]
            region2 = [1114, -4581]
            region3 = [1420, -3603]

            dist1 = math.hypot(pose[0] - region1[0], pose[1] - region1[1])
            dist2 = math.hypot(pose[0] - region2[0], pose[1] - region2[1])
            dist3 = math.hypot(pose[0] - region3[0], pose[1] - region3[1])

            for x in range(0,3): 
                goal = dist1 
                oset = region1 - pose

                if dist2 < goal: 
                    goal = dist2
                    oset = region2 - pose

                if dist3 < goal: 
                    goal = dist3
                    oset = region3 - pose

            print "This is region 1 and current pose", region1, pose
            Xmove = oset[0]
            Ymove = oset[1]
            print "Xmove ", Xmove 
            print "Ymove ", Ymove 

            Zmove = 0 # (Z direction)
            Pmove = 0 # (Pitch)
            Rmove = 0 # (Roll)

            self.scorbotSer.flushInput()
            self.scorbotSer.write('teachr oset\r')
            self.scorbotSer.readline() 
            self.scorbotSer.write('%d' % Xmove + '\r') 
            line = self.scorbotSer.readline()
            print line
            self.scorbotSer.write('%d' % Ymove + '\r')
            line = self.scorbotSer.readline()
            print line
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
            time.sleep(5)

            print "Passing move oset"

            self.scorbotSer.write("move O0\r")
            self.scorbotSer.read()
            self.scorbotSer.read()
            time.sleep(5)
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