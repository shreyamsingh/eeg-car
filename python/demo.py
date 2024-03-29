import time, msvcrt
import serial

# open serial port
ser = serial.Serial(port='COM3', baudrate=9600, timeout=.1)

# write message
while (key:=msvcrt.getwch()):
    if key == "x": break
    ser.write(bytes(key, 'utf-8'))
    print(key)
    time.sleep(0.01)

# close serial port
ser.close()
