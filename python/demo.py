import time, msvcrt
import serial

# open serial port
# to find arduino port, go to tools > port
# capitalization doesn't matter
ser = serial.Serial(port='COM3', baudrate=9600, timeout=.1)

# write message
while (key:=msvcrt.getwch()):
    if key == "x": break
    ser.write(bytes(key, 'utf-8'))
    time.sleep(0.01)

# close serial port
ser.close()
