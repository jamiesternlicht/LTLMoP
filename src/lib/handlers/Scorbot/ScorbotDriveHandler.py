

""" 
===================
ScorbotDrive.py - DriveHandler for Scorbot
===================

""" 
import time, logging
import lib.handlers.handlerTemplates as handlerTemplates
class ScorbotDriveHandler(handlerTemplates.DriveHandler): 

    def __init__(self,executor,shared_data): 
        self.stopped=True

        self.loco = executor.hsub.getHandlerInstanceByType(handlerTemplates.LocomotionCommandHandler)
        self.pose_handler = executor.hsub.getHandlerInstanceByType(handlerTemplates.PoseHandler)
        try: 
            self.scorbotSer = shared_data["ScorbotSer"]
        except: 
            logging.error("(MOTION) ERROR: No connection to Scorbot")
            
    def setVelocity(self,x,y):
        """
        Dummy function
        """
        pass
        
    def nextMove(self, XY, optional_cmd=None):
        """
        Sets next movement 
        """
        starttime = time.clock()

        pose = self.pose_handler.getPose(cached = True)
        """
        print XY
        
        Xmove = XY[0]-pose[0] # Use these Xmove and Y move for RRT
        Ymove = XY[1]-pose[1]
        """
        Xmove = XY[0]*200 # Ammount the gripper is going to move (X direction) in milimeters
        Ymove = XY[1]*200 # (Y direction)  USE THIS ONE FOR SCORBOTMOTIONCONTROL
        
        Zmove = 0 # (Z direction)
        Pmove = 0 # (Pitch)
        Rmove = 0 # (Roll)
        

        self.scorbotSer.flushInput()
        self.scorbotSer.write('teachr oset\r')
        line6 = self.scorbotSer.readline() 
        self.scorbotSer.write('%d' % Xmove + '\r') 
        line = self.scorbotSer.readline()
        self.scorbotSer.write('%d' % Ymove + '\r')
        line1 = self.scorbotSer.readline()
        self.scorbotSer.write('%d' % Zmove + '\r')
        line2 = self.scorbotSer.readline()
        self.scorbotSer.write('%d' % Pmove + '\r')
        line3 = self.scorbotSer.readline()
        self.scorbotSer.write('%d' % Rmove + '\r')
        line4 = self.scorbotSer.readline()
        line4 = self.scorbotSer.readline()


        if optional_cmd == None:
            self.loco.sendCommand('move oset\r') # Sends command to locomotionCommand

        tottime = (time.clock()-starttime)
        #print "This is the ammount of time for drive: {}s".format(tottime)