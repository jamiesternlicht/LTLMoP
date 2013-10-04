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
jamie_tutorial

Customs: # List of custom propositions

RegionFile: # Relative path of region description file
../hideandseek/hideandseek.regions

Sensors: # List of sensor propositions and their state (enabled = 1, disabled = 0)


======== SPECIFICATION ========

RegionMapping: # Mapping between region names and their decomposed counterparts
Classroom1 = p12
Classroom2 = p11
Office = p7
Closet = p10
Gym = p8
others = p1, p13, p14, p15, p16, p17, p18, p19, p20, p21, p22, p23, p24, p25
Parking = p6

Spec: # Specification in structured English
go to Classroom1
go to Parking

