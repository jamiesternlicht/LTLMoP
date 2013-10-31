# This is a specification definition file for the LTLMoP toolkit.
# Format details are described at the beginning of each section below.


======== SETTINGS ========

Actions: # List of action propositions and their state (enabled = 1, disabled = 0)
Lower_Close_Raise, 1
Open, 1

CompileOptions:
convexify: False
parser: structured
fastslow: False
decompose: True
use_region_bit_encoding: True

CurrentConfigName:
test

Customs: # List of custom propositions

RegionFile: # Relative path of region description file
jamie_scorbot.regions

Sensors: # List of sensor propositions and their state (enabled = 1, disabled = 0)


======== SPECIFICATION ========

RegionMapping: # Mapping between region names and their decomposed counterparts
T4 = p2
T1 = p5
T2 = p4
T3 = p3
others = p1

Spec: # Specification in structured English
Environment starts with True
Robot starts in T1 with Open

visit T1, T2, T3, infinitely often

if you are sensing Ring in T1 or T2 or T3 then do Lower_Close_Raise then go to T4 
if you are in T4 then do Open

