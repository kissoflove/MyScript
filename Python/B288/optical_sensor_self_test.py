#Version PROTO1_V2
#!/usr/bin/env python
#
# Version 2:
#   Added PD_VF_BIAS measurement
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
    parser.add_argument("-p","--serialport", help = "Serial port device for communication with the DUT.")
    parser.add_argument("-n","--Iter", help = "iterative process",
                                type = int,
                                default = 2)

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

def minus(data1,data2):
    data_diff = float(data1) - float(data2)
    return data_diff

def main():
    startTime = time.time()
    global SerialPort

    input_args = parse_args()

    # get the serial port name
    SerialPort = input_args.serialport
    # open the serial port
    # open_port()
    Iter = input_args.Iter

    intrigue = intrigueFT.Intrigue(spPort = SerialPort)
    # Iter #| C(off) | C(on) | T(off) | T(on) | C(tp) | T(tp) | RS(c) | RS(t) | CDS_C | CDS_T

    TIA_VREF    = 0
    PD1_Vr      = 1
    PD_VF_LOW   = 2
    TIA1_DARK   = 3
    TIA1_LIGHT  = 4
    VSINK1_ON   = 5
    VSINK1_OFF  = 6
    PD2_Vr      = 7
    TIA2_DARK   = 9
    TIA2_LIGHT  = 10
    VSINK2_ON   = 11
    VSINK2_OFF  = 12

    TIA_VREF_ADC_GAIN = 0.3
    VSINK_ADC_GAIN = 0.3

    cumResults = intrigue.intrigue_ied(suppress_print = True, num_samples = Iter, raw_result = True)
    tempResultsConcha = intrigue.intrigue_temp(suppress_print = True, photodiode = 1, num_samples = Iter)
    tempResultsTragus = intrigue.intrigue_temp(suppress_print = True, photodiode = 2, num_samples = Iter)

    # Concha cal
    print "TIA_VREF============================================!"
    print 'TIA_VREF_MIN                      = %f' % (numpy.min(cumResults[:, TIA_VREF])/4096.0*1.5/TIA_VREF_ADC_GAIN)
    print 'TIA_VREF_MAX                      = %f' % (numpy.max(cumResults[:, TIA_VREF])/4096.0*1.5/TIA_VREF_ADC_GAIN)
    print 'TIA_VREF_MEAN                     = %f' % (numpy.mean(cumResults[:, TIA_VREF])/4096.0*1.5/TIA_VREF_ADC_GAIN)
    print 'TIA_VREF_RANGE                    = %f' % ((numpy.max(cumResults[:, TIA_VREF]) - numpy.min(cumResults[:, TIA_VREF]))/4096.0*1.5/TIA_VREF_ADC_GAIN)
    print 'TIA_VREF_STDDEV                   = %f' % (numpy.std(cumResults[:, TIA_VREF])/4096.0*1.5/TIA_VREF_ADC_GAIN)
    print "Concha============================================!"
    print '----------OFF----------'
    print 'CONCHA_DARK_PRE-RAW_4.7mm_MIN     = %f' % numpy.min(cumResults[:, TIA1_DARK])
    print 'CONCHA_DARK_PRE-RAW_4.7mm_MAX     = %f' % numpy.max(cumResults[:, TIA1_DARK])
    print 'CONCHA_DARK_PRE-RAW_4.7mm_MEAN    = %f' % numpy.mean(cumResults[:, TIA1_DARK])
#print 'CONCHA_DARK_4.7mm_VARIANCE =%f' %Variance[0]
    print 'CONCHA_DARK_PRE-RAW_4.7mm_RANGE   = %f' % (numpy.max(cumResults[:, TIA1_DARK]) - numpy.min(cumResults[:, TIA1_DARK]))
    print 'CONCHA_DARK_PRE-RAW_4.7mm_STDDEV  = %f' % numpy.std(cumResults[:, TIA1_DARK])
    print 'CONCHA_VSINK_OFF_MIN              = %f' % (numpy.min(cumResults[:, VSINK1_OFF])/4096.0*1.5/VSINK_ADC_GAIN)
    print 'CONCHA_VSINK_OFF_MAX              = %f' % (numpy.max(cumResults[:, VSINK1_OFF])/4096.0*1.5/VSINK_ADC_GAIN)
    print 'CONCHA_VSINK_OFF_MEAN             = %f' % (numpy.mean(cumResults[:, VSINK1_OFF])/4096.0*1.5/VSINK_ADC_GAIN)
#print 'CONCHA_DARK_4.7mm_VARIANCE =%f' %Variance[0]
    print 'CONCHA_VSINK_OFF_RANGE            = %f' % ((numpy.max(cumResults[:, VSINK1_OFF]) - numpy.min(cumResults[:, VSINK1_OFF]))/4096.0*1.5/VSINK_ADC_GAIN)
    print 'CONCHA_VSINK_OFF_STDDEV           = %f' % (numpy.std(cumResults[:, VSINK1_OFF])/4096.0*1.5/VSINK_ADC_GAIN)
    print '----------ON----------'
    print 'CONCHA_LIGHT_PRE-RAW_4.7mm_MIN    = %f' % numpy.min(cumResults[:, TIA1_LIGHT])
    print 'CONCHA_LIGHT_PRE-RAW_4.7mm_MAX    = %f' % numpy.max(cumResults[:, TIA1_LIGHT])
    print 'CONCHA_LIGHT_PRE-RAW_4.7mm_MEAN   = %f' % numpy.mean(cumResults[:, TIA1_LIGHT])
#print 'CONCHA_LIGHT_4.7mm_VARIANCE =%f' %Variance[0]
    print 'CONCHA_LIGHT_PRE-RAW_4.7mm_RANGE  = %f' % (numpy.max(cumResults[:, TIA1_LIGHT]) - numpy.min(cumResults[:, TIA1_LIGHT]))
    print 'CONCHA_LIGHT_PRE-RAW_4.7mm_STDDEV = %f' % numpy.std(cumResults[:, TIA1_LIGHT])
    print 'CONCHA_VSINK_ON_MIN               = %f' % (numpy.min(cumResults[:, VSINK1_ON])/4096.0*1.5/VSINK_ADC_GAIN)
    print 'CONCHA_VSINK_ON_MAX               = %f' % (numpy.max(cumResults[:, VSINK1_ON])/4096.0*1.5/VSINK_ADC_GAIN)
    print 'CONCHA_VSINK_ON_MEAN              = %f' % (numpy.mean(cumResults[:, VSINK1_ON])/4096.0*1.5/VSINK_ADC_GAIN)
#print 'CONCHA_DARK_4.7mm_VARIANCE =%f' %Variance[0]
    print 'CONCHA_VSINK_ON_RANGE             = %f' % ((numpy.max(cumResults[:, VSINK1_ON]) - numpy.min(cumResults[:, VSINK1_ON]))/4096.0*1.5/VSINK_ADC_GAIN)
    print 'CONCHA_VSINK_ON_STDDEV            = %f' % (numpy.std(cumResults[:, VSINK1_ON])/4096.0*1.5/VSINK_ADC_GAIN)
    print '----------ON-OFF----------'
    print 'CONCHA_LD_PRE-RAW_4.7mm_MEAN      = %f' % (numpy.mean(cumResults[:, TIA1_LIGHT]) - numpy.mean(cumResults[:, TIA1_DARK]))
    print 'CONCHA_VCSEL_VF_MEAN              = %f' % ((numpy.mean(cumResults[:, VSINK1_OFF]) - numpy.mean(cumResults[:, VSINK1_ON]))/4096.0*1.5/VSINK_ADC_GAIN)
    print '----------OTHER----------'
    print 'CONCHA_PD_VR_MIN                  = %f' % (numpy.min(cumResults[:, PD1_Vr])/4096.0*1.5/VSINK_ADC_GAIN)
    print 'CONCHA_PD_VR_MAX                  = %f' % (numpy.max(cumResults[:, PD1_Vr])/4096.0*1.5/VSINK_ADC_GAIN)
    print 'CONCHA_PD_VR_MEAN                 = %f' % (numpy.mean(cumResults[:, PD1_Vr])/4096.0*1.5/VSINK_ADC_GAIN)
#print 'CONCHA_DARK_4.7mm_VARIANCE =%f' %Variance[0]
    print 'CONCHA_PD_VR_RANGE                = %f' % ((numpy.max(cumResults[:, PD1_Vr]) - numpy.min(cumResults[:, PD1_Vr]))/4096.0*1.5/VSINK_ADC_GAIN)
    print 'CONCHA_PD_VR_STDDEV               = %f' % (numpy.std(cumResults[:, PD1_Vr])/4096.0*1.5/VSINK_ADC_GAIN)
    print 'CONCHA_TEMP_PD_VF_MIN             = %f' % (numpy.min(tempResultsConcha))
    print 'CONCHA_TEMP_PD_VF_MAX             = %f' % (numpy.max(tempResultsConcha))
    print 'CONCHA_TEMP_PD_VF_MEAN            = %f' % (numpy.mean(tempResultsConcha))
#print 'CONCHA_DARK_4.7mm_VARIANCE =%f' %Variance[0]
    print 'CONCHA_TEMP_PD_VF_RANGE           = %f' % ((numpy.max(tempResultsConcha) - numpy.min(tempResultsConcha)))
    print 'CONCHA_TEMP_PD_VF_STDDEV          = %f' % (numpy.std(tempResultsConcha))

    # Tragus cal
    print "TRAGUS============================================!"
    print '----------OFF----------'
    print 'TRAGUS_DARK_PRE-RAW_4.7mm_MIN     = %f' % numpy.min(cumResults[:, TIA2_DARK])
    print 'TRAGUS_DARK_PRE-RAW_4.7mm_MAX     = %f' % numpy.max(cumResults[:, TIA2_DARK])
    print 'TRAGUS_DARK_PRE-RAW_4.7mm_MEAN    = %f' % numpy.mean(cumResults[:, TIA2_DARK])
#print 'TRAGUS_DARK_4.7mm_VARIANCE =%f' %Variance[0]
    print 'TRAGUS_DARK_PRE-RAW_4.7mm_RANGE   = %f' % (numpy.max(cumResults[:, TIA2_DARK]) - numpy.min(cumResults[:, TIA2_DARK]))
    print 'TRAGUS_DARK_PRE-RAW_4.7mm_STDDEV  = %f' % numpy.std(cumResults[:, TIA2_DARK])
    print 'TRAGUS_VSINK_OFF_MIN              = %f' % (numpy.min(cumResults[:, VSINK2_OFF])/4096.0*1.5/VSINK_ADC_GAIN)
    print 'TRAGUS_VSINK_OFF_MAX              = %f' % (numpy.max(cumResults[:, VSINK2_OFF])/4096.0*1.5/VSINK_ADC_GAIN)
    print 'TRAGUS_VSINK_OFF_MEAN             = %f' % (numpy.mean(cumResults[:, VSINK2_OFF])/4096.0*1.5/VSINK_ADC_GAIN)
#print 'TRAGUS_DARK_4.7mm_VARIANCE =%f' %Variance[0]
    print 'TRAGUS_VSINK_OFF_RANGE            = %f' % ((numpy.max(cumResults[:, VSINK2_OFF]) - numpy.min(cumResults[:, VSINK2_OFF]))/4096.0*1.5/VSINK_ADC_GAIN)
    print 'TRAGUS_VSINK_OFF_STDDEV           = %f' % (numpy.std(cumResults[:, VSINK2_OFF])/4096.0*1.5/VSINK_ADC_GAIN)
    print '----------ON----------'
    print 'TRAGUS_LIGHT_PRE-RAW_4.7mm_MIN    = %f' % numpy.min(cumResults[:, TIA2_LIGHT])
    print 'TRAGUS_LIGHT_PRE-RAW_4.7mm_MAX    = %f' % numpy.max(cumResults[:, TIA2_LIGHT])
    print 'TRAGUS_LIGHT_PRE-RAW_4.7mm_MEAN   = %f' % numpy.mean(cumResults[:, TIA2_LIGHT])
#print 'TRAGUS_LIGHT_4.7mm_VARIANCE =%f' %Variance[0]
    print 'TRAGUS_LIGHT_PRE-RAW_4.7mm_RANGE  = %f' % (numpy.max(cumResults[:, TIA2_LIGHT]) - numpy.min(cumResults[:, TIA2_LIGHT]))
    print 'TRAGUS_LIGHT_PRE-RAW_4.7mm_STDDEV = %f' % numpy.std(cumResults[:, TIA2_LIGHT])
    print 'TRAGUS_VSINK_ON_MIN               = %f' % (numpy.min(cumResults[:, VSINK2_ON])/4096.0*1.5/VSINK_ADC_GAIN)
    print 'TRAGUS_VSINK_ON_MAX               = %f' % (numpy.max(cumResults[:, VSINK2_ON])/4096.0*1.5/VSINK_ADC_GAIN)
    print 'TRAGUS_VSINK_ON_MEAN              = %f' % (numpy.mean(cumResults[:, VSINK2_ON])/4096.0*1.5/VSINK_ADC_GAIN)
#print 'TRAGUS_DARK_4.7mm_VARIANCE =%f' %Variance[0]
    print 'TRAGUS_VSINK_ON_RANGE             = %f' % ((numpy.max(cumResults[:, VSINK2_ON]) - numpy.min(cumResults[:, VSINK2_ON]))/4096.0*1.5/VSINK_ADC_GAIN)
    print 'TRAGUS_VSINK_ON_STDDEV            = %f' % (numpy.std(cumResults[:, VSINK2_ON])/4096.0*1.5/VSINK_ADC_GAIN)
    print '----------ON-OFF----------'
    print 'TRAGUS_LD_PRE-RAW_4.7mm_MEAN      = %f' % (numpy.mean(cumResults[:, TIA2_LIGHT]) - numpy.mean(cumResults[:, TIA2_DARK]))
    print 'TRAGUS_VCSEL_VF_MEAN              = %f' % ((numpy.mean(cumResults[:, VSINK2_OFF]) - numpy.mean(cumResults[:, VSINK2_ON]))/4096.0*1.5/VSINK_ADC_GAIN)
    print '----------OTHER----------'
    print 'TRAGUS_PD_VR_MIN                  = %f' % (numpy.min(cumResults[:, PD2_Vr])/4096.0*1.5/VSINK_ADC_GAIN)
    print 'TRAGUS_PD_VR_MAX                  = %f' % (numpy.max(cumResults[:, PD2_Vr])/4096.0*1.5/VSINK_ADC_GAIN)
    print 'TRAGUS_PD_VR_MEAN                 = %f' % (numpy.mean(cumResults[:, PD2_Vr])/4096.0*1.5/VSINK_ADC_GAIN)
#print 'TRAGUS_DARK_4.7mm_VARIANCE =%f' %Variance[0]
    print 'TRAGUS_PD_VR_RANGE                = %f' % ((numpy.max(cumResults[:, PD2_Vr]) - numpy.min(cumResults[:, PD2_Vr]))/4096.0*1.5/VSINK_ADC_GAIN)
    print 'TRAGUS_PD_VR_STDDEV               = %f' % (numpy.std(cumResults[:, PD2_Vr])/4096.0*1.5/VSINK_ADC_GAIN)
    print 'TRAGUS_TEMP_PD_VF_MIN             = %f' % (numpy.min(tempResultsTragus))
    print 'TRAGUS_TEMP_PD_VF_MAX             = %f' % (numpy.max(tempResultsTragus))
    print 'TRAGUS_TEMP_PD_VF_MEAN            = %f' % (numpy.mean(tempResultsTragus))
#print 'TRAGUS_DARK_4.7mm_VARIANCE =%f' %Variance[0]
    print 'TRAGUS_TEMP_PD_VF_RANGE           = %f' % ((numpy.max(tempResultsTragus) - numpy.min(tempResultsTragus)))
    print 'TRAGUS_TEMP_PD_VF_STDDEV          = %f' % (numpy.std(tempResultsTragus))

    print '\n\n'
    print '---------METADATA-------'
    print 'OS_TEST_CYCLE_TIME                = %f' % (time.time() - startTime)





if __name__ == '__main__':
    parse_args()
    print 'Version: PROTO1_V2'
    main()
