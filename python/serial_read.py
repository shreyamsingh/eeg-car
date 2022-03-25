import serial, time
import pandas as pd

# open serial port
ser = serial.Serial(port='COM3', baudrate=9600, timeout=.1)

commands = {'f', 'b', 'l', 'r', 's'}
start = time.process_time()
last_dir = 's'

while True:
    # read csv
    df = pd.read_csv('serial.csv')
    # get last command
    msg = df.loc[len(df)-1].at['msg']
    # write message to serial port
    write_before = time.process_time()
    if msg in commands and not msg == last_dir:
        ser.write(bytes(msg, 'utf-8'))
        last_dir = msg
    # print('write serial: ', str(time.process_time() - write_before))
    time.sleep(0.01)
