import serial, numpy, time
import matplotlib.pyplot as plt
from math import ceil

def open_serial(port, baud=9600):
    return serial.Serial(port, baud, timeout=1)


def collect(T, dt, ser, verbose=False):
    data = {"AccX":[],"AccY":[],"AccZ":[],"RLL":[],"PCH":[],"YAW":[],"MGX":[],"MGY":[],"MGZ":[],"MGH":[],"dt":dt}

    print "Starting data collection..."
    while(T>0):
        msg = ser.readline()
        if (not '$' in msg):
            if verbose:
                print msg
            try:
                state = dict((n, float(x)) for n,x in [pair.split(":") for pair in msg.split(",")])
                for key in state.keys():
                    data[key].append(state[key])
                T -= dt
            except ValueError:
                pass

        time.sleep(dt)
    print "Data collection done"

    return data


def plot(data, key):
    plt.plot([data['dt']*i for i in range(0, len(data[key]))], data[key])
    plt.ylabel(key)
    plt.xlabel('seconds')
    plt.axis([0, data['dt']*len(data[key]), -ceil(max(data[key])), ceil(max(data[key]))])
    plt.show()
