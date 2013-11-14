import time
import serial 
import re


ser = serial.Serial('/dev/tty.usbserial-A1001aew', timeout=.2)

ser.flush()

ser.write('move A0\r')

time.sleep(1)

ser.write('teachr oset\r')
time.sleep(.1)
ser.write('0\r')
time.sleep(.1)
ser.write('0\r')
time.sleep(.1)
ser.write('-300\r')
time.sleep(.1)
ser.write('0\r')
time.sleep(.1)
ser.write('0\r')
time.sleep(.1)

ser.write('move oset\r')

time.sleep(1)

ser.write('teachr oset\r')
time.sleep(.1)
ser.write('0\r')
time.sleep(.1)
ser.write('0\r')
time.sleep(.1)
ser.write('300\r')
time.sleep(.1)
ser.write('0\r')
time.sleep(.1)
ser.write('0\r')
time.sleep(.1)

ser.write('move oset\r')

time.sleep(1)

ser.write('move S0\r')


