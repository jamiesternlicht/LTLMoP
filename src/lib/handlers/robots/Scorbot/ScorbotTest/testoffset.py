import time
import serial 
import re


ser = serial.Serial('/dev/tty.usbserial-A1001aew', timeout=.2)

ser.flush()

ser.write('move S0\r')

time.sleep(1)

blah = 300
blah1 = 300

ser.write('teachr oset\r')
time.sleep(.1)
ser.write('0\r')
time.sleep(.1)
ser.write('0\r')
time.sleep(.1)
ser.write('%d' % blah1 + '\r')
time.sleep(.1)
ser.write('0\r')
time.sleep(.1)
ser.write('0\r')
time.sleep(.1)

ser.write('move oset\r')

time.sleep(.5)

ser.write('teachr oset\r')
time.sleep(.1)
ser.write('0\r')
time.sleep(.1)
ser.write('%d' % blah + '\r')
time.sleep(.1)
ser.write('0\r')
time.sleep(.1)
ser.write('0\r')
time.sleep(.1)
ser.write('0\r')
time.sleep(.1)

ser.write('move oset\r')

time.sleep(.5)

ser.write('teachr oset\r')
time.sleep(.1)
ser.write('%d' % blah + '\r')
time.sleep(.1)
ser.write('0\r')
time.sleep(.1)
ser.write('0\r')
time.sleep(.1)
ser.write('0\r')
time.sleep(.1)
ser.write('0\r')
time.sleep(.1)

ser.write('move oset\r')

time.sleep(.5)

ser.write('move T4\r')


