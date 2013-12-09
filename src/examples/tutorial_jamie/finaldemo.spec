# This is a specification definition file for the LTLMoP toolkit.
# Format details are described at the beginning of each section below.


======== SETTINGS ========

Actions: # List of action propositions and their state (enabled = 1, disabled = 0)
pick_up, 1
drop_off, 1

CompileOptions:
convexify: True
parser: structured
fastslow: False
decompose: True
use_region_bit_encoding: True

CurrentConfigName:
test

Customs: # List of custom propositions
carrying_ring

RegionFile: # Relative path of region description file
jamie_scorbot.regions

Sensors: # List of sensor propositions and their state (enabled = 1, disabled = 0)
Ring, 1


======== SPECIFICATION ========

RegionMapping: # Mapping between region names and their decomposed counterparts
others = p6, p7, p8, p9, p10
RingRegion1 = p4
Goal = p5
RingRegion3 = p2
RingRegion2 = p3

Spec: # Specification in structured English
#Initial conditions
Env starts with false
Robot starts with false

# Assumptions about the environment
If you were in Goal then do not Ring

# Define rules on how to pick up and drop off rings
Do pick_up if and only if you are sensing Ring and you are not activating carrying_ring
If you are activating pick_up then stay there
carrying_ring is set on pick_up and reset on drop_off
Do drop_off if and only if you are in Goal and you are activating carrying_ring

If you did not activate carrying_ring then always not Goal

# Patrol regions
Group regions is RingRegion1, RingRegion2, RingRegion3
If you are not activating carrying_ring then visit all regions
If you are activating carrying_ring then visit Goal

