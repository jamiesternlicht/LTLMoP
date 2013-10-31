# This is a specification definition file for the LTLMoP toolkit.
# Format details are described at the beginning of each section below.


======== SETTINGS ========

Actions: # List of action propositions and their state (enabled = 1, disabled = 0)
Open, 1
Close, 1
Raise, 1
Lower, 1

CompileOptions:
convexify: True
parser: structured
fastslow: False
decompose: True
use_region_bit_encoding: True

CurrentConfigName:
scorbot_sim

Customs: # List of custom propositions

RegionFile: # Relative path of region description file
jamie_scorbot.regions

Sensors: # List of sensor propositions and their state (enabled = 1, disabled = 0)


======== SPECIFICATION ========

RegionMapping: # Mapping between region names and their decomposed counterparts
Ring2 = p3
Ring3 = p2
Goal = p5
Ring1 = p4
others = p6, p7, p8, p9, p10, p11, p12, p13, p14, p15, p16, p17, p18, p19, p20, p21, p22, p23, p24

Spec: # Specification in structured English
go to Ring1
go to Goal
go to Ring2
go to Goal
go to Ring3
go to Goal

if Ring1 then Open 
if Ring2 then Open
if Ring3 then Open

Lower if and only if Ring1 and Open
Lower if and only if Ring2 and Open
Lower if and only if Ring3 and Open
Lower if and only if Goal and Close

Close if and only if Ring1 and Lower
Close if and only if Ring2 and Lower
Close if and only if Ring3 and Lower
Open if and only if Goal and Lower

