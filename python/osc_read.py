import argparse
import time
import pandas as pd

from pythonosc import dispatcher
from pythonosc import osc_server

PORT_NUMBER = 8000
IP_DEFAULT = "127.0.0.1"

global start
start = time.process_time()
temp_start = time.process_time()

metrics = ["/fac/eyeAct/lookL", "/fac/eyeAct/lookR", "/fac/eyeAct/blink", "/fac/eyeAct/winkL", "/fac/eyeAct/winkR",
           "/fac/uAct/neutral", "/fac/uAct/frown", "/fac/uAct/surprise", "/fac/lAct/neutral", "/fac/lAct/clench",
           "/fac/lAct/laugh", "/fac/lAct/smile", "/fac/lAct/smirkLeft", "/fac/lAct/smirkRight", "/com/neutral",
           "/com/push", "/com/pull", "/com/left", "/com/right", "/com/lift", "/com/drop", "/com/rotateLeft",
           "/com/rotateRight", "/com/rotateClockwise", "/com/rotateCounterClockwise", "/com/rotateForwards",
           "/com/rotateReverse", "/com/disappear", "/met/foc", "/met/int", "/met/rel", "/met/str", "/met/exc",
           "/met/eng", "/met/cognitiveStress", "/met/visualAttention", "/met/auditoryAttention"]
num = len(metrics)
lookup = {val:idx for idx, val in enumerate(metrics)}
data = {}  # time: [metric values (ordered)]
with open('data.csv', 'a') as f:
   f.write('time,{}\n'.format(','.join(metrics)))


def filter_handler(address, *args):
    global start,temp_start
    #print(f"{address}: {args}")
    curr = time.process_time() - start
    #print(curr)
    # add time + metric value to data
    if curr not in data:
        data[curr] = [0 for i in range(num)]
    val = args
    while not isinstance(val, int) and not isinstance(val, float):
        val = val[0]
    data[curr][lookup[address]] = val

   # recording done, export data to csv
    if time.process_time()-temp_start > 0.05:
        # columns: time, metrics
        df = pd.DataFrame.from_dict(data, orient='index', columns=metrics)
        with open('data.csv', 'a') as f:
            f.write(f'{curr},')
            f.write(','.join([str(x) for x in list(df.iloc[-1])]))
            f.write('\n')
        print('written')
        temp_start = time.process_time()
        #print('done')
        #exit()
def shrek_get_sleep():
    global start
    start = time.process_time()
def get_data(address, dispatcher):
   dispatcher.map(address, filter_handler)
   

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip",
                        default=IP_DEFAULT, help="The ip to listen on")
    parser.add_argument("--port",
                        type=int, default=PORT_NUMBER, help="The port to listen on")
    args = parser.parse_args()

    dispatcher = dispatcher.Dispatcher()

    # === Facial Expressions Eye
    dispatcher.map("/fac/eyeAct/lookL", filter_handler)
    dispatcher.map("/fac/eyeAct/lookR", filter_handler)
    dispatcher.map("/fac/eyeAct/blink", filter_handler)
    dispatcher.map("/fac/eyeAct/winkL", filter_handler)
    dispatcher.map("/fac/eyeAct/winkR", filter_handler)

    # === Facial Expressions Upperface
    dispatcher.map("/fac/uAct/neutral", filter_handler, time.process_time() - start)  # WORK IN PROGRESS
    dispatcher.map("/fac/uAct/frown", filter_handler)
    dispatcher.map("/fac/uAct/surprise", filter_handler)

    # === Facial Expressions Lowerface
    dispatcher.map("/fac/lAct/neutral", filter_handler, time.process_time() - start)
    dispatcher.map("/fac/lAct/clench", filter_handler)
    dispatcher.map("/fac/lAct/laugh", filter_handler)
    dispatcher.map("/fac/lAct/smile", filter_handler)
    dispatcher.map("/fac/lAct/smirkLeft", filter_handler)
    dispatcher.map("/fac/lAct/smirkRight", filter_handler)

    # === Mental Commands
    dispatcher.map("/com/neutral", filter_handler)
    dispatcher.map("/com/push", filter_handler)
    dispatcher.map("/com/pull", filter_handler)
    dispatcher.map("/com/left", filter_handler)
    dispatcher.map("/com/right", filter_handler)
    dispatcher.map("/com/lift", filter_handler)
    dispatcher.map("/com/drop", filter_handler)
    dispatcher.map("/com/rotateLeft", filter_handler)
    dispatcher.map("/com/rotateRight", filter_handler)
    dispatcher.map("/com/rotateClockwise", filter_handler)
    dispatcher.map("/com/rotateCounterClockwise", filter_handler)
    dispatcher.map("/com/rotateForwards", filter_handler)
    dispatcher.map("/com/rotateReverse", filter_handler)
    dispatcher.map("/com/disappear", filter_handler)

    # === Performance Metrics
    dispatcher.map("/met/foc", filter_handler)
    dispatcher.map("/met/int", filter_handler)
    dispatcher.map("/met/rel", filter_handler)
    dispatcher.map("/met/str", filter_handler)
    dispatcher.map("/met/exc", filter_handler)
    dispatcher.map("/met/eng", filter_handler)
    dispatcher.map("/met/cognitiveStress", filter_handler)
    dispatcher.map("/met/visualAttention", filter_handler)
    dispatcher.map("/met/auditoryAttention", filter_handler)

    server = osc_server.ThreadingOSCUDPServer(
        (args.ip, args.port), dispatcher)
    print("Serving on {}".format(server.server_address))
    server.serve_forever()