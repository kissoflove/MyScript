import BerylFT
import sys
import time
import argparse

if __name__ == '__main__':
    print 'Version: PROTO1_V2'
    parser = argparse.ArgumentParser(description='Beryl measurement functions Coulomb Counter current/charge.')
    parser.add_argument('-p', '--serialport', help='Beryl serial port name.', type=str, default=False,required=True)
    args = parser.parse_args()

    b = BerylFT.Beryl(channel = "UART1", port = args.serialport)
    b.configure_ccadc(GLOBAL_EN = 0x1)

    start_cum 	= b.read_ccadc()
    startTime = time.time()
    end_cum 	= b.read_ccadc()
    eTime = time.time() - startTime
    print "Average Current (mA): %f" % ((end_cum - start_cum)*3600/eTime)
