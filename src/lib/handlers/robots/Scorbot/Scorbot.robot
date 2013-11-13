DriveHandler: # Robot default drive handler with default argument values
ScorbotDrive()

InitHandler: # Robot default init handler with default argument values
ScorbotInit(port ='/dev/tty.usbserial-A1001aew')

LocomotionCommandHandler: # Robot default locomotion command handler with default argument values
ScorbotLocomotionCommand()

MotionControlHandler: # Robot default motion control handler with default argument values
ScorbotMotionControl()

PoseHandler: # Robot default pose handler with default argument values
ScorbotPose()

RobotName: # Robot Name
Ralph

Type: # Robot type
Scorbot

SensorHandler: # Robot default sensor handler with default argument values
ScorbotSensor()

ActuatorHandler: # Robot default actuator handler with default argument values
ScorbotActuator()

CalibrationMatrix:
array([[ 1, 0, 0],
       [ 0, 1, 0],
       [ 0, 0, 1]])

