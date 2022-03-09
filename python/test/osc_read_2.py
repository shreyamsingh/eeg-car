import argparse
import time
import pandas as pd

from pythonosc import dispatcher
from pythonosc import osc_server
import serial

PORT_NUMBER = 8000
IP_DEFAULT = "127.0.0.1"

# open serial port
# to find arduino port, go to tools > port
ser = serial.Serial(port='COM3', baudrate=9600, timeout=.1)

start = time.process_time()
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


def write(address):
    if address in {"/fac/uAct/frown", "/com/push"}:
        ser.write(b'f')  # forward
    elif address in {"/fac/lAct/clench", "/com/drop"}:
        ser.write(b'b')  # backward
    elif address in {"/fac/eyeAct/lookL", "/com/left"}:
        ser.write(b'l')  # left
    elif address in {"/fac/eyeAct/lookR", "/com/right"}:
        ser.write(b'r')  # right
    elif address in {"/fac/uAct/surprise", "/com/pull"}:
        ser.write(b's')  # stop


def filter_handler(address, *args):
    curr = time.process_time() - start
    print(f"{time}:{address}:{args}")

    # add time + metric value to data
    if curr not in data:
        data[curr] = [0 for i in range(num)]
    val = args
    while not isinstance(val, int) and not isinstance(val, float):
        val = val[0]
    data[curr][lookup[address]] = val

    # threshold classification algorithm
    threshold = 0.6
    if val > threshold:
        write(address, curr)

    # write data to csv - columns: time, metrics
    df = pd.DataFrame.from_dict(data, orient='index', columns=metrics)
    df.to_csv('data/push_112421_04.csv')


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip",
                        default=IP_DEFAULT, help="The ip to listen on")
    parser.add_argument("--port",
                        type=int, default=PORT_NUMBER, help="The port to listen on")
    args = parser.parse_args()

    dispatcher = dispatcher.Dispatcher()

    for m in metrics:
        # print strength + write to csv for each signal
        dispatcher.map(m, filter_handler)

    server = osc_server.ThreadingOSCUDPServer(
        (args.ip, args.port), dispatcher)
    print("Serving on {}".format(server.server_address))
    server.serve_forever()