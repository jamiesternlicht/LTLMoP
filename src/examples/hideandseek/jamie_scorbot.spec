# This is a specification definition file for the LTLMoP toolkit.
# Format details are described at the beginning of each section below.


======== SETTINGS ========

Actions: # List of action propositions and their state (enabled = 1, disabled = 0)

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
others = p6, p7, p8, p9, p10, p11, p12, p13, p14, p15, p16, p17, p18, p19, p20, p21, p22, p23, p24
Ring3 = p2
Goal = p5
Ring1 = p4
Ring2 = p3

Spec: # Specification in structured English
go to Goal
go to Ring1
go to Ring2
go to Ring3

