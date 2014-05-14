# This is a specification definition file for the LTLMoP toolkit.
# Format details are described at the beginning of each section below.


======== SETTINGS ========

Actions: # List of action propositions and their state (enabled = 1, disabled = 0)
pickup, 1
dropoff, 1

CompileOptions:
convexify: True
parser: structured
symbolic: False
use_region_bit_encoding: True
synthesizer: jtlv
fastslow: True
decompose: True

CurrentConfigName:
test

Customs: # List of custom propositions
carrying_red_ring
carrying_blue_ring

RegionFile: # Relative path of region description file
jamie_scorbot_Spring.regions

Sensors: # List of sensor propositions and their state (enabled = 1, disabled = 0)
red_ring, 1
blue_ring, 1


======== SPECIFICATION ========

RegionMapping: # Mapping between region names and their decomposed counterparts
Space1 = p4
Space2 = p3
Recycling = p5
Trash = p2
others = p6, p7

Spec: # Specification in structured English
# Assumptions about the environment
if you were in (Trash or Recycling) then do not (red_ring or blue_ring)

# Define rules on how to pick up and drop off rings
if you are sensing (red_ring or blue_ring) and you are not activating (carrying_red_ring or carrying_blue_ring) then do pickup

If you are activating pickup then stay there
If you are activating dropoff then stay there

carrying_red_ring is set on (pickup and red_ring) and reset on (dropoff and Trash)
carrying_blue_ring is set on (pickup and blue_ring) and reset on (dropoff and Recycling)


If you are not activating (carrying_red_ring or carrying_blue_ring) then always not (Trash or Recycling)


# Patrol regions
Group regions is Space1,Space2
If you are not activating (carrying_red_ring or carrying_blue_ring) then visit all regions

infinitely often not (carrying_red_ring or carrying_blue_ring)

