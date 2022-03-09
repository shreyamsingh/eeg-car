import serial, time
import pandas as pd

# open serial port
ser = serial.Serial(port='COM3', baudrate=9600, timeout=.1)

while True:
    # read csv
    df = pd.read_csv('serial.csv')
    # get last command
    msg = df.loc[len(df)-1].at['msg']
    # write message to serial port
    ser.write(msg.encode())
    time.sleep(0.01)
