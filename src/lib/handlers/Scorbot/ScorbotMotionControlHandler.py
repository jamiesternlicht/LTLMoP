"""
=============================
ScorbotMotionControl.py - Motion Controller
=============================

Uses simple predetermined saved locations for movement to regions
"""

import __vectorControllerHelper as vectorControllerHelper
from numpy import *
from __is_inside import *
import time, math, logging
import lib.handlers.handlerTemplates as handlerTemplates
class ScorbotMotionControlHandler(handlerTemplates.MotionControlHandler): 

    def __init__(self,executor,shared_data): 
        """
        Motion control handler for the Scorbot
        """
        self.drive_handler = executor.hsub.getHandlerInstanceByType(handlerTemplates.DriveHandler)
        self.proj = executor.proj
        self.pose_handler = executor.hsub.getHandlerInstanceByType(handlerTemplates.PoseHandler) # Have pose, to verify reached destination

        # Get information about regions
        self.rfi = self.proj.rfi
        self.coordmap_map2lab = self.proj.coordmap_map2lab
        self.last_warning = 0

        try: 
            self.scorbotSer = shared_data["ScorbotSer"]
        except: 
            logging.error("(MOTION) ERROR: No connection to Scorbot")

    def gotoRegion(self,current_reg,next_reg, last = False): 

        """
        If ``last`` is True, we will move to the center of the destination region.

        Returns ``True`` if we've reached the destination region.
        """

        if current_reg == next_reg and not last:  
            # Don't move! 
            return True

        # Find our current configuration
        pose = self.pose_handler.getPose()

        logging.info("Next Region is " + str(self.proj.rfi.regions[next_reg].name))
        logging.info("Current Region is " + str(self.proj.rfi.regions[current_reg].name))

        # NOTE: Information about region geometry can be found in self.rfi.regions:
        pointArray = [x for x in self.rfi.regions[current_reg].getPoints()]
        pointArray = map(self.coordmap_map2lab, pointArray)
        vertices = mat(pointArray).T 

        if last:
            transFaceIdx = None
        else:
            # Find a face to go through
            # TODO: Account for non-determinacy?
            # For now, let's just choose the largest face available, because we are probably using a big clunky robot
            # TODO: Why don't we just store this as the index?
            transFaceIdx = None
            max_magsq = 0
            for i, face in enumerate(self.rfi.regions[current_reg].getFaces()):
                if face not in self.rfi.transitions[current_reg][next_reg]:
                    continue

                tf_pta, tf_ptb = face
                tf_vector = tf_ptb - tf_pta
                magsq = (tf_vector.x)**2 + (tf_vector.y)**2
                if magsq > max_magsq:
                    transFaceIdx = i
                    max_magsq = magsq
                
            if transFaceIdx is None:
                print "ERROR: Unable to find transition face between regions %s and %s.  Please check the decomposition (try viewing projectname_decomposed.regions in RegionEditor or a text editor)." % (self.rfi.regions[current_reg].name, self.rfi.regions[next_reg].name)
         

        # Run algorithm to find a velocity vector (global frame) to take the robot to the next region
        V = vectorControllerHelper.getController([pose[0], pose[1]], vertices, transFaceIdx)

        self.drive_handler.nextMove(V)
        

        departed = not is_inside([pose[0], pose[1]], vertices)
        pointArray = [x for x in self.rfi.regions[next_reg].getPoints()]
        pointArray = map(self.coordmap_map2lab, pointArray)
        vertices = mat(pointArray).T 
        # Figure out whether we've reached the destination region
        arrived = is_inside([pose[0], pose[1]], vertices)

        if departed and (not arrived) and (time.time()-self.last_warning) > 0.5:
            #print "WARNING: Left current region but not in expected destination region"
            # Figure out what region we think we stumbled into
            for r in self.rfi.regions:
                pointArray = [self.coordmap_map2lab(x) for x in r.getPoints()]
                vertices = mat(pointArray).T 

                if is_inside([pose[0], pose[1]], vertices):
                    #print "I think I'm in " + r.name
                    #print pose
                    break
            self.last_warning = time.time()

        return arrived
