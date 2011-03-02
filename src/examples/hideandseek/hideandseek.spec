# This is a specification definition file for the LTLMoP toolkit.
# Format details are described at the beginning of each section below.
# Note that all values are separated by *tabs*.


======== EXPERIMENT CONFIG 0 ========

Calibration: # Coordinate transformation between map and experiment: XScale, XOffset, YScale, YOffset
0.012811806809,-8.07774146808,-0.0185568627189,5.91272155958

InitialRegion: # Initial region number
5

InitialTruths: # List of initially true propositions
seeker

Lab: # Lab configuration file
playerstage.lab

Name: # Name of the experiment
Default

RobotFile: # Relative path of robot description file
HnS_stage.robot


======== SETTINGS ========

Actions: # List of actions and their state (enabled = 1, disabled = 0)
count,1
whistle,1
hide,1

Customs: # List of custom propositions
seeker
playing

RegionFile: # Relative path of region description file
hideandseek.regions

Sensors: # List of sensors and their state (enabled = 1, disabled = 0)
see_player,1
hear_whistle,1
hear_counting,1

currentExperimentName:
Default


======== SPECIFICATION ========

RegionMapping:

Classroom1=p14
Classroom2=p13
Closet=p12
Office=p9,p59,p60
Danger=p61,p62
Wall=p4
Gym=p10
Parking=p7
Tree=p5
SchoolWall=p9,p43,p44,p45,p46,p47,p48,p49,p50,p51,p52,p53,p54,p55,p56,p57,p58
others=p15,p16,p17,p18,p19,p20,p21,p22,p23,p24,p25,p26,p27,p28,p29,p30,p31,p32,p33,p34,p35,p36,p37
between$Tree$and$Wall$=p38,p39,p40,p41,p42

Spec: # Specification in simple English
### Overview ###
# Start in the parking lot.  If you are a seeker, stay there and count until you hear a ready whistle.
# Then search all the hiding spots until you find someone.  Once you've found someone, you are now a hider.
# If you are a hider, go back to the parking lot and wait for counting to start.
# Once that happens, go hide somewhere and whistle.

### Initialization ###
# Allow for the possibility of starting out with other players in view
Environment starts with not hear_whistle and not hear_counting
Robot starts in Parking
# Robot can start as either seeker or hider
Robot starts with not count and not whistle and not hide and not playing

### Restrictions ###
Always not Danger
Always not SchoolWall
Always not Wall
Always not Tree

### Game start and end conditions ###
playing is set on ((seeker and hear_whistle) or (not seeker and hear_counting)) and reset on ((seeker and see_player) or (not seeker and see_player))

If you are not activating playing then go to Parking
If you were not activating playing and you were in Parking then stay there

### Hider/seeker alternation ###
#TODO: Why are the following two not equivalent to the sum of all the statements in this section?
#Do seeker if and only if you were activating seeker or you were activating playing and you are not activating playing and you were not activating seeker
#Do not seeker if and only if you were not activating seeker or you were activating playing and you are not activating playing and you were activating seeker
# Toggle the value of seeker at the end of a game
If you were activating playing and you are not activating playing and you were activating seeker then do not seeker
If you were activating playing and you are not activating playing and you were not activating seeker then do seeker
# Otherwise, don't change anything
If you were activating playing and you are activating playing and you were activating seeker then do seeker
If you were activating playing and you are activating playing and you were not activating seeker then do not seeker
If you were not activating playing and you are not activating playing and you were activating seeker then do seeker
If you were not activating playing and you are not activating playing and you were not activating seeker then do not seeker
If you were not activating playing and you are activating playing and you were activating seeker then do seeker
If you were not activating playing and you are activating playing and you were not activating seeker then do not seeker

### Seeking Behavior ###

Do count if and only if you are activating seeker and you are not activating playing and you are in Parking

If you are activating seeker and you are activating playing then visit Classroom2
If you are activating seeker and you are activating playing then visit Office
If you are activating seeker and you are activating playing then visit Gym
If you are activating seeker and you are activating playing then visit Closet
If you are activating seeker and you are activating playing then visit Classroom1
If you are activating seeker and you are activating playing then visit between Tree and Wall

### Hiding Behavior ###
If you are not activating seeker and you are activating playing then go to ((between Tree and Wall) or Closet or Office)

Do hide if and only if you are not activating seeker and you are activating playing and you are in ((between Tree and Wall) or Closet or Office)

If you were activating hide then stay there
Do whistle if and only if you were not activating hide and you are activating hide


