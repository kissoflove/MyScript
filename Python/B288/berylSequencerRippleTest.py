#Version PROTO1_V1
#!/usr/bin/env python
#





import os
import sys
import serial
import time
import argparse
import math
import numpy
import re
import numpy as np
import intrigueFT
SerialPort = ''
SerDev = None

def parse_args():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--serialport", help = "Serial port device for communication with the DUT.")
    parser.add_argument("--startstop", help = "\'start\' to start sequencer, \'stop\' to stop sequencer",
                                type = str,
                                default = 'start')

    args = parser.parse_args()

    return args

def open_port():
    """ Setup the serial port
        """
    global SerDev
    SerDev = serial.Serial(SerialPort, 115200, timeout=10)
    mybytes = SerDev.inWaiting()

    #time.sleep(1)
    # Clear the buffer!!!
    Buffer = SerDev.read(mybytes)

def close_port():
    """ Close the serial port
        """
    SerDev.close()

def SerWR(item):
    """ Write/Read from serial port
        """
    Ser_read = ''

    SerDev.flushOutput()
    SerDev.flushInput()

    SerDev.write(item);time.sleep(0.5)
    #time.sleep(timeOut)
    print SerDev.readlines()
#print SerDev.readline()
#Ser_read = SerDev.readlines()
#string = ''.join(Ser_read)

#print_SerRead(item,Ser_read,patternString)
#print Ser_read


def main():
    startTime = time.time()
    global SerialPort

    input_args = parse_args()

    # get the serial port name
    SerialPort = input_args.serialport
    # open the serial port
    # open_port()
    startstop = input_args.startstop

    intrigue = intrigueFT.Intrigue(spPort = SerialPort)

    intrigue.intrigue_autosequence(startstop = startstop)
    if startstop == "start":
        print "\nSequencer started - start taking measurements\n"
    else:
        print "\nSequencer stopped - move on to next test\n"




if __name__ == '__main__':
    parse_args()
    print 'Version: PROTO1_V1'
    main()
