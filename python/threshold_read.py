import pandas as pd
import time
import serial

df = pd.read_csv('data.csv')
idx = 0
LEFT = 'LEFT'
RIGHT = 'RIGHT'
FORWARD = 'FORWARD'
STOP = 'STOP'
REVERSE = 'REVERSE'

ser = serial.Serial(port='COM3', baudrate=9600, timeout=.1)


command_to_output = {
   '/com/push': FORWARD,
   '/com/pull': STOP,
   '/com/left': LEFT,
   '/com/right': RIGHT,
   '/com/drop': REVERSE,
   '/fac/uAct/frown': FORWARD,
   '/fac/uAct/surprise': STOP,
   '/fac/eyeAct/lookL': LEFT,
   '/fac/eyeAct/lookR': RIGHT,
   '/fac/lAct/clench': STOP
}

while True:
   if not (idx % 5) and idx > 0:
      means = df.iloc[idx-5:idx].mean().drop(['time', '/fac/eyeAct/blink'])
      max_mean = means.idxmax()
      if max_mean in command_to_output:
         print(f'{max_mean}: {command_to_output[max_mean]}')
         ser.write(command_to_output[max_mean].encode())
   time.sleep(1)
   idx += 1