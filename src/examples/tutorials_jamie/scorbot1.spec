# This is a specification definition file for the LTLMoP toolkit.
# Format details are described at the beginning of each section below.


======== SETTINGS ========

Actions: # List of action propositions and their state (enabled = 1, disabled = 0)
Lower_Close_Raise, 1
Open, 1

CompileOptions:
convexify: True
parser: structured
fastslow: False
decompose: True
use_region_bit_encoding: True

CurrentConfigName:
jamie_tutorial

Customs: # List of custom propositions

RegionFile: # Relative path of region description file
../hideandseek/jamie_scorbot.regions

Sensors: # List of sensor propositions and their state (enabled = 1, disabled = 0)


======== SPECIFICATION ========

Spec: # Specification in structured English
go to Ring1
go to Goal 
go to Ring2
go to Goal 
go to Ring3
go to Goal

if Ring1 or Ring2 or Ring3 then Lower_Close_Raise
if Goal then Open

