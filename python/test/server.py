# to test connection with headset when headset is unavailable and/or not set up
from pythonosc.udp_client import SimpleUDPClient
import pandas as pd
from time import sleep

ip = "127.0.0.1"
port = 8000

client = SimpleUDPClient(ip, port)  # Create client

f = open('example_data.csv')
df = pd.read_csv(f)
for idx in df.index:
   for row in df:
      #client.send_message(row, idx)
      if row != 'time':
         client.send_message(row, float(df.loc[idx, row]))   # Send float message
   print(idx)
   print(df.loc[idx, '/fac/uAct/surprise'])
   sleep(1)