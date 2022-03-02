import pandas as pd
import numpy as np
from time import sleep
import serial

df = pd.read_csv('eeg-car/melissa_push.csv')
idx = 0
LEFT = 'l'
RIGHT = 'r'
FORWARD = 'f'
STOP = 's'
REVERSE = 'b'

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
   df = pd.read_csv('data.csv')
   if not (idx % 3) and idx > 0:
      means = df.iloc[len(df)-3:len(df)].mean().drop(['time', '/fac/eyeAct/blink'])
      means = means.sort_values(ascending=False)

      n = 3
      max_mean = means.idxmax()
      dctChosen = {key: 0 for key in command_to_output.values()}
      for i in range(n):
         #print(f'the thing: {means.index[i]}')
         if ((current := means.index[i]) in command_to_output) and means.iloc[i] > 0:
            dctChosen[command_to_output[current]] += 1
      print(dctChosen)
      if max_mean in command_to_output:
         print(f'{max_mean}: {command_to_output[max_mean]}')
         ser.write(command_to_output[max_mean].encode())
   sleep(1)
   idx += 1