# This is a specification definition file for the LTLMoP toolkit.
# Format details are described at the beginning of each section below.


======== SETTINGS ========

Actions: # List of action propositions and their state (enabled = 1, disabled = 0)
pick_up, 1
drop_off, 1

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
Ring, 1


======== SPECIFICATION ========

RegionMapping: # Mapping between region names and their decomposed counterparts
others = p1
RingRegion1 = p4
Goal = p5
RingRegion3 = p2
RingRegion2 = p3

Spec: # Specification in structured English
go to RingRegion1
go to Goal
go to RingRegion2
go to Goal
go to RingRegion3
go to Goal

#if you are in T1 or T2 or T3 then do Lower_Close_Raise
#if you are in T4 then do Open
#if you are sensing Ring and in RingRoom1, RingRoom2, RingRoom3 then pick_up

# More descriptive names (RingRoom1, RingRoom2,...)

