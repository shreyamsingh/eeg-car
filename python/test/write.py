import serial

# open serial port
# to find arduino port, go to tools > port
# capitalization doesn't matter
ser = serial.Serial(port='COM3', baudrate=9600, timeout=.1)

# write message
ser.write(b'S')

# close serial port
ser.close()
