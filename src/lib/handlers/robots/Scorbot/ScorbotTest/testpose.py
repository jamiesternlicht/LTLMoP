import time
import serial 
import re


ser = serial.Serial('/dev/tty.usbserial-A1001aew', timeout=.2)

ser.flush()
ser.write('here pose\r')
ser.write('listpv pose\r')

gotPose = False
while not gotPose:
#for i in range(10):
    line = ser.readline()[1:]
    if line == "":
        continue

    if line[0][0] == "X":
        gotPose = True




blah = map(int, re.findall(r'-?\d+', line))
pose = blah[:3]


print pose

ser.close()
