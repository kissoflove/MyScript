# Beryl Power Self Test
# (c) 2017 Apple Inc.
# Author: Jason Brinsfield
# Description: reports voltages of all Beryl power rails for FCT
#
# Revision History:
# v1 - 10/4/17 : initial release

import BerylFT
import sys,string
import numpy
import argparse


def Main(port,channellist):
    serialPort = port
    numSamples = 1

    b = BerylFT.Beryl(channel="UART1", port=serialPort)
    adc_dict = b.build_adc_channel_dict()
    # channelList = [1, 3, 5, 10, 11, 12, 13, 20, 21, 22, 23]
    channelList = channellist

    # Measure rails after power-up
    for channel in channelList:
        val = []
        for i in range(numSamples):
            b.start_adc_conversion('MAN', 1, channel)
            val.append(b.man_adc_read(1, adc_dict, channel, suppress_print=True))

        print '\nRaw data:', val
        print "%s_MIN: %f ;" % (adc_dict[channel][0], numpy.min(val))
        print "%s_MEAN: %f ;" % (adc_dict[channel][0], numpy.mean(val))
        print "%s_MAX: %f ;" % (adc_dict[channel][0], numpy.max(val))
        print "%s_RANGE: %f ;" % (adc_dict[channel][0], numpy.max(val) - numpy.min(val))

    # Disable turn on LDO 2 and 3 except LDO 2 and 3 channel
    if set([22]).issubset(set(channellist)) or set([23]).issubset(set(channellist)):
        # Turn on LDOs 2 and 3
        print "Enable LDO2 and LDO3"
        b.toggle_supply(SUPPLY='LDO2', MODE='ACT0', ON=True)
        b.toggle_supply(SUPPLY='LDO3', MODE='ACT0', ON=True)
        channelList = [22, 23]

        # Measure LDOs 2 and 3 after turning them on
        for channel in channelList:
            val = []
            for i in range(numSamples):
                b.start_adc_conversion('MAN', 1, channel)
                val.append(b.man_adc_read(1, adc_dict, channel, suppress_print=True))

            print "\nRaw data:", val
            print "%s_ON_MIN: %f ;" % (adc_dict[channel][0], numpy.min(val))
            print "%s_ON_MEAN: %f ;" % (adc_dict[channel][0], numpy.mean(val))
            print "%s_ON_MAX: %f ;" % (adc_dict[channel][0], numpy.max(val))
            print "%s_ON_RANGE: %f ;" % (adc_dict[channel][0], numpy.max(val) - numpy.min(val))

        print "Disable LDO2 and LDO3"
        b.toggle_supply(SUPPLY='LDO2', MODE='ACT0', ON=False)
        b.toggle_supply(SUPPLY='LDO3', MODE='ACT0', ON=False)

    b.close_port()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Beryl measurement functions arguments.')
    parser.add_argument('-p', '--port', help='Beryl serial port name.', type=str, default=False,required=True)
    parser.add_argument('-c', '--channellist', help='Channel List, hexdecimal value with bracket. example: -c [01,02,5F].', type=str, default=False, required=True)

    args = parser.parse_args()
    tmp = args.channellist
    tmp = string.replace(tmp,'[','')
    tmp = string.replace(tmp, ']', '')

    channellist = [string.atoi(cl,16) for cl in tmp.split(',')]

    Main(args.port,channellist)
