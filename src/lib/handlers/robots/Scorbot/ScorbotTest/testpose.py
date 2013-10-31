import time
import serial 


ser = serial.Serial('/dev/tty.usbserial-A1001aew')
ser.flush()

ser.write('here pose\r')
ser.write('listpv pose\r')

line = ser.readline()
line2 = ser.readline()
line3 = ser.readline()
line4 = ser.readline()

print line, line2, line3, line4 


ser.close()
