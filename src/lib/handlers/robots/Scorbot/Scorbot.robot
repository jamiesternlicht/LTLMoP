DriveHandler: # Robot default drive handler with default argument values
ScorbotDrive()

InitHandler: # Robot default init handler with default argument values
ScorbotInit(port ='/dev/ttyUSB0')

LocomotionCommandHandler: # Robot default locomotion command handler with default argument values
ScorbotLocomotionCommand()

MotionControlHandler: # Robot default motion control handler with default argument values
ScorbotMotionControl()

PoseHandler: # Robot default pose handler with default argument values
#viconPose(host='10.0.0.102',port=800,x_VICON_name="Nao:Nao <t-X>",y_VICON_name="Nao:Nao <t-Y>",theta_VICON_name="Nao:Nao <a-Z>")
scorbotPose()

RobotName: # Robot Name
Ralph

Type: # Robot type
Scorbot

SensorHandler: # Robot default sensor handler with default argument values
ScorbotSensor()

ActuatorHandler: # Robot default actuator handler with default argument values
ScorbotActuator()
