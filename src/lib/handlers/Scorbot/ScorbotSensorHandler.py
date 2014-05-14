#!/usr/bin/env python
"""
=========================================
ScorbotSensorHandler.py - Simulated Scorbot Sensor Handler
=========================================

"""
import time
import socket
import struct
import logging
import threading
import numpy as np



import lib.handlers.handlerTemplates as handlerTemplates

class ScorbotSensorHandler(handlerTemplates.SensorHandler):
    def __init__(self, executor, ip, port, shared_data):
        """
        This is the ScorbotKinect sensor handler

        ip (string): the multicast group ip set in C# kinect program (default='239.0.0.222')
        port (int): the multicast port set in C# kinect program (default=2222)
        """

        # we need a data structure to cache detected color value:
        self.color_detected = {'r':[],'b':[]} # {'r':[(x,y),(x,y)], 'b':[(x,y)]}
        if executor is not None:
            self.proj = executor.proj
            self.pose_handler = executor.hsub.getHandlerInstanceByType(handlerTemplates.PoseHandler)
            
        self.sensorListenInitialized = False
        self._running = True
        self.sensorListenThread = None
        self.ip = ip
        self.port = port
        
        
    ###################################
    ### Available Sensor functions: ###
    ###################################

    def color_object_detected(self, color, initial=False):
        """
        Return true if there is an object detected with the provided `color`
        
        color (string): the color of the object red or blue
        """
        
        if initial:
            # start communication
            # Create new thread to communicate with subwindow
            if self.sensorListenThread is None:
                print "(SENS) Starting Kinect listen thread..."
                self.sensorListenThread = threading.Thread(target = self._sensorListen)
                self.sensorListenThread.daemon = True
                self.sensorListenThread.start()
        else:
            # convert color input
            if color.lower() in ['red','r']: color = 'r'
            elif color.lower() in ['blue','b']: color = 'b'
            
            return len(self.color_detected[color]) > 0
            
    def nearby_color_object_detected(self, color, initial=False):
        """
        Return true if there is an object detected with the provided `color` 
        in the same region as the robot
        
        color (string): the color of the object red or blue
        """
        if initial:
            # start communication
            # Create new thread to communicate with subwindow
            if self.sensorListenThread is None:
                print "(SENS) Starting Kinect listen thread..."
                self.sensorListenThread = threading.Thread(target = self._sensorListen)
                self.sensorListenThread.daemon = True
                self.sensorListenThread.start()
        else:
            # convert color input
            if color.lower() in ['red','r']: color = 'r'
            elif color.lower() in ['blue','b']: color = 'b'
            
            # get region of the robot
            pose = self.pose_handler.getPose()
            robot_region = self._getRegionFromPose(pose[:2])
            for p in self.color_detected[color]:
                object_region = self._getRegionFromPose(p)
                if object_region == robot_region:
                    # the object is in the same region as the robot
                    return True
            
            return False
        
        
        
    def _stop(self):
        print >>sys.__stderr__, "(SENS) Terminating dummysensor GUI listen thread..."
        self._running = False
        self.sensorListenThread.join() 
        
    def _sensorListen(self):
        """
        Processes messages from the C# kinect program, and updates our cache appropriately
        """

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        sock.settimeout(0.5)
        
        try:
            sock.bind(('', self.port))
            mreq = struct.pack("4sl", socket.inet_aton(self.ip), socket.INADDR_ANY)

            sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
        except:
            print "ERROR: Cannot bind to port.  Try killing all Python processes and trying again."
            return

        while self._running:
            # Wait for and receive a message from the subwindow
            try:
                receivedMsg = sock.recv(1024)
            except socket.timeout:
                # if nothing is detected, we clear the cache
                self.color_detected = {'r':[],'b':[]}
            else:
                # something is detected, let's parse it and store it in cache
                for ind, val in enumerate(receivedMsg):
                    if val == '\x40' and receivedMsg[ind-1] == '\x21':
                        # we detect a blue color
                        self.color_detected['b'].append(self._decode_color_location(receivedMsg, ind))
                    elif val == '\x54' and receivedMsg[ind-1] == '\x32':
                        # we detect a red color
                        self.color_detected['r'].append(self._decode_color_location(receivedMsg, ind))

    def _decode_color_location(self, msg, ind):
        """
        Decode the location information (x,y) stored in the `msg` starting from index `ind`
        """
        xmsg = msg[ind+1:ind+5]
        ymsg = msg[ind+5:]

        xint = struct.unpack("!i",xmsg)[0]
        yint = struct.unpack("!i",ymsg)[0]

        return (xint,yint)
        

    def _getRegionFromPose(self, pose):
        """
        get the region where the pose (x,y) is located
        """
        
        rfi = self.proj.rfi
        pose = self.proj.coordmap_lab2map(pose)
        region = next((r for i, r in enumerate(rfi.regions) if r.name.lower() != "boundary" and \
                        r.objectContainsPoint(*pose)), None)
        if region is None:
            pass
            #logging.debug("Pose of {} not inside any region!".format(pose))
        return region
          
if __name__ == "__main__":
    h = ScorbotSensorHandler(None,'239.0.0.222',2222,{})
    h.color_object_detected('r',True)
    
    while True:
        print h.color_object_detected('b',False)
        time.sleep(0.2)
    