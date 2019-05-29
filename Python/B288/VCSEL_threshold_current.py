# -*- coding:utf-8 -*-
#!/usr/bin/env python
# Files: Optical_sense_self_test_threshold_current_evt2_v2.py
#--------------------------------------------------
# FOR:Optical sense self test at FCT , it will connect to MLB via serial
# Input Args:
#   Threshold = -1 , Do the calibration on OA1_OFFSET_TRIM
#   Threshold = 0
#   Threshold = 1 will only return threshold current data
#   commandtype = 1 will use SCPSENSTAT for data, commandtype=2 will use SCPSEN for data
#   verbose = 1 will print details
#--------------------------------------------------
# BY:Haseeb, Vincent
#--------------------------------------------------
# Date: 2016-07-21
#--------------------------------------------------
# Version 3:
#   When threshould = 2, Run 7 point current sweep and averaging 100 points
#
# Version 4:
#   Added write to NVV to set target current back to 3.3mV
# Version 5:
#   Added Offset calibration, use threshold = -1 to run.
# Version 6:
#   Changed closestDistance and target distance to 50, limits changed to 10
# Version 7:
#   Changed target OFF value to 30, target distance to < 3
# Version 8:
#   Changed to binary search, target OFF value was 75
# Version 9:
#   Changed target OFF value to 30
# Version 10:
#   Changed target distance = +/-5, end criterion - added || distance < 3
# Version 11:
#   Updated optical trim section to show failiure message and for test script to capture all data points and log to PDCA
# Version 13:
#   Updated threshold current to three points: 3.0mA, 4.0mA and 5.0mA
# Verision 15:
#   Updated delay time for 20Hz
# Version 16:
#   Updated sampling from 100 to 75 for VRsense Cal
#   Removed CMEAS and CERR check and 100 samples for test time saving
# Version 17:
#   Updated time out time for OS Pre_Trim
#   [Post_Concha_off,Post_Tragus_off]=Sen_Sample(sensor=[0,2],Sample_count=25,timeout=1.0)
# Version 18:
#   Updated time out time for OS Pre_Trim
#   [Post_Concha_off,Post_Tragus_off]=Sen_Sample(sensor=[0,2],Sample_count=25,timeout=5.0)
# Version 20:
#   Updated threshold current points from[3.0, 4.0, 5.0] to [2.5, 3.25, 4.0]mA

import glob
import re
import os
import sys
import serial
import argparse
import wave
import cStringIO
import time
import binascii
import logging
import math
import numpy
import intrigueFT

SerDev = None

def Regular_expression(patternString,Response):

    pattern = re.compile(patternString, re.I|re.M|re.S)
    match = pattern.search(Response)

    if (match):
        return (True, match)
    else:
        return (False, Response)

def parseargs():

    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("-p",'--serialport',
                        help = "Serial port device for communication with the DUT.")
    parser.add_argument('-v',"--verbose",type = int,
                        help = "0 - Only show some UART message    1 - Show all UART message")
    parser.add_argument('-t',"--threshold",type = int,choices=range(-1,3),
                        help = "Print Threshold Current Data")
    parser.add_argument('-ct',"--commandtype",type = int,
                        help = "commandtype")

    args = parser.parse_args()
    return args

def open_port():
    """ Setup the serial port
    """
    global SerDev
    print "SerialPort=%s"%SerialPort
    SerDev = serial.Serial(SerialPort, 115200, timeout=0.1)

def Send_CMD(patternString="",cmd="",timeout=0.1):
    # print "CMD Sent: ", cmd
    SerDev.flushOutput()
    SerDev.flushInput()

    SerDev.write(cmd)
    Response =""
    time.sleep(0.1)
    startTime = time.time()

    if SerDev.inWaiting ==0:
        print "\nError: Record start command failed."
        sys.exit()
    while ((time.time() - startTime) < timeout):
        tempStr = SerDev.read(64)            # 64 chosen arbitrarily
        Response += tempStr
        match = re.search(patternString,Response)
        if (match):
            return Response
    print "Time out receving correct string"
    return Response

# This function shall be updated (Will be RAM Variables)
def Command_Response(patternString,CMD,timeout=0.1):
    Response=Send_CMD(patternString,CMD,timeout=timeout)
    ok,match=Regular_expression(patternString,Response)
    if not ok:
        print "Incorrect response from CMD %s"%CMD
        print "Reponse : %s"%Response
        sys.exit()
    else:
        print "Sent %s"%CMD
        return match


def Sen_Sample(sensor=[1,2,3,4],Sample_count=5,timeout=0.2):
#Using SCPSENSTAT with limited data dump
    cmd= "[SCPSEN-"
    Last_sample_response ="<%d,"%(Sample_count-1)
    cmd_response = '<\d+,'
    for x in range (0,len(sensor)):
        if x == len(sensor)-1:
            cmd_response += '(\d+)>'
            Last_sample_response+='(\d+)>'
            cmd+="%d-%d]"%(sensor[x],Sample_count)
        else:
            cmd+="%d,"%(sensor[x])
            cmd_response += '(\d+),'
            Last_sample_response+= '(\d+),'

    Response=Send_CMD(Last_sample_response,cmd,timeout)
    pattern=re.compile(cmd_response,re.I|re.M)

    if verbose==1:
        print Response

    Result=pattern.findall(Response)

    if verbose==1:
        print "Capture %d samples"%len(Result)
    Return_value=[]
    # print Result

    for x in range(0,len(sensor)):
        Return_value.append(0.0)

    if len(Result)==Sample_count:
        for x in range(0,Sample_count):
            for y in range(0,len(sensor)):
                Return_value[y]+=float(int(Result[x][y]))
    else:
        print "Did not capture %d samples"%(Sample_count)
        print "Quitting the process"
        sys.exit()

    for y in range(0,len(sensor)):
        # print y
        Return_value[y]= Return_value[y]/float(Sample_count)
    # print Return_value
    return Return_value


def Sample_100(no=5,sample=1,comtype=1,timeout=10):
#Using SCPSENSTAT with limited data dump
    if comtype==1:
        cmd = '[SCPSENSTAT-0,1,2,3,12,13-%s]' % no
        SerDev.write(cmd)
        time.sleep(timeout)

        for i in range(0, 3):
            CmdRead = SerDev.readline()
        if verbose==1:
            print CmdRead
        Mean = []
        #  try:
        #    for i in range(0, 4):
        ScpRead = SerDev.readline()
        if verbose==1:
            print ScpRead
        # ScpGet = re.findall("\d+",ScpRead)
        ScpGet = map(float, re.findall('[\d\.]+', ScpRead))
        #print 'ScpGet=',ScpGet
        #print 'ScpGet_first',ScpGet[0]
        Mean = ScpGet
        mean_concha_off=  Mean[0]
        mean_tragus_off=  Mean[2]
        mean_concha_on=  Mean[1]
        mean_tragus_on=  Mean[3]
        mean_concha_rsense=  Mean[4]
        mean_tragus_rsense=  Mean[5]
#Using SCPSEN with raw data dump
    if comtype==2:
        #print '[SCPSEN-0,1,2,3,6,7,8,9,12,13-'+str(no)+']'
        Sensor_array=Sen_Sample(sensor=[0,1,2,3,12,13],Sample_count=no,timeout=5)

        # pattern=re.compile('<\d+,(\d+),(\d+),(\d+),(\d+),(\d+),(\d+)>',re.I|re.M)
        # if verbose==1:
        #     print Response
        # Result=pattern.findall(Response)
        # if verbose==1:
        #     print "Capture %d samples"%len(Result)
        total_concha_off = 0.0
        total_concha_on = 0.0
        total_tragus_off = 0.0
        total_tragus_on = 0.0
#total_concha_temp= 0.0
#total_tragus_temp = 0.0
        total_concha_rsense = 0.0 # Rsense
        total_tragus_rsense = 0.0 # Rsense
        mean_concha_off = Sensor_array[0]
        mean_concha_on = Sensor_array[1]
        mean_tragus_off = Sensor_array[2]
        mean_tragus_on = Sensor_array[3]
        mean_concha_rsense = Sensor_array[4]
        mean_tragus_rsense = Sensor_array[5]

    if sample==1:
        difference= abs(mean_tragus_rsense- mean_concha_rsense)
        print "difference=",difference
        print "difference=",(difference/(mean_concha_rsense+mean_tragus_rsense)/2)*100,"%"
        return mean_concha_rsense , mean_tragus_rsense
    elif sample==2:
        print "mean_concha=",mean_concha_rsense
        print "mean_tragus=",mean_tragus_rsense
        difference= abs(mean_tragus_rsense- mean_concha_rsense)
        print "difference=",difference
        print "difference=",(difference/(mean_concha_rsense+mean_tragus_rsense)/2)*100,"%"
        return ((mean_concha_rsense + mean_tragus_rsense) / float(2))
    else:
        return mean_concha_off, mean_concha_on, mean_tragus_off, mean_tragus_on,mean_concha_rsense,mean_tragus_rsense


def calib_fast_charge(T0,D1,D2):
    # reduce settling time for time-constant measurement
    m=Command_Response('<scpsp-11-.*:pass>','[SCPSP-11-150]')
    print m.group(0)
    m=Command_Response('<scpsp-10-.*:pass>','[SCPSP-10-%d]'%T0)
    print m.group(0)
    m=Command_Response('<scpsp-9-.*:pass>','[SCPSP-9-%d]'%D1)
    print m.group(0)
    y_c_off, y_c_on, y_t_off, y_t_on,C11,C12 = Sample_100(no=75,sample=3, comtype=commandtype)
    Command_Response('<scpsp-9-.*:pass>','[SCPSP-9-%d]'%D2)
    y_c_off, y_c_on, y_t_off, y_t_on,C21,C22 = Sample_100(no=75,sample=3,comtype=commandtype)
    print ""
    print ""
    print "C11 = %f, C12 = %f" %(C11,C12)
    print "C21 = %f, C22 = %f" %(C21,C22)
    # change back
    DC1 = (C12-C11)
    DC2 = (C22-C21)

    print "D1=%d"%D1
    print "D2=%d"%D2
    print "T0=%d"%T0
    print "DC1=(C12-C11) = %f"%DC1
    print "DC2=(C22-C21) = %f"%DC2
    # print "(DC1*D2-DC2*D1)=%f"%((DC1*D2-DC2*D1))
    # print "(DC1-DC2)=%f"%(DC1-DC2)
    print

    D0 = ((DC1*D2-DC2*D1)/(DC1-DC2))
    print "D0 = ((DC1*D2)-(DC2*D1)/(DC1-DC2))=%f"%D0
    # print "D0 = abs(D0)= %f"%abs(D0)
    Command_Response('<scpsp-11-300:pass>','[SCPSP-11-300]')
    Command_Response('<scpsp-9-%d:pass>'%(round(D0)),'[SCPSP-9-%d]'%(round(D0)))
    C0=Sample_100(no=75,sample=2,comtype=commandtype)
    #y0 = (y12*y21 - y11*y22) / (y12+y21-y11-y22)
    return C11,C12,C21,C22,C0,D0

def lin_interp(x1,x2,y1,y2,x0):
    y0 = (y2-y1)*(x0-x1)/(x2-x1)+y1
    return y0

def calc_measured_current(adcReading):
    '''
        Calculates the current (in mA) based on a voltage measured across
        the Rsense resistor
        '''
    # Make sure inputs are floats
    #Vdd = float(Vdd)
    #pwmDutyCycle = float(pwmDutyCycle)
    Vrsense = (float(adcReading)/4095) * 2.4
    #Vref = pwmDutyCycle * Vdd
    iVcsel = Vrsense/100
    return (iVcsel * 1000.0)

# Main code section
def main():
    # print "Hello code"
    global SerialPort
    global verbose
    global threshold
    global commandtype

    input_args = parseargs()
    # get the serial port
    SerialPort = input_args.serialport
    verbose = input_args.verbose
    threshold = input_args.threshold
    commandtype = input_args.commandtype
    intrigue = intrigueFT.Intrigue(spPort = SerialPort)
    numSamples = 3 # Number of readings to take from each sensor for threshold current
    vcselCurrents = [3.0, 4.0, 5.0] # VCSEL currents that will be used for testing in mA
    conchaReadings = []
    tragusReadings = []
    conchaCurrents = []
    tragusCurrents = []

    LSB = 2.4/4096
    T0_1 = 50
    T0_2 = 100
    D1_1 = 15
    D2_1 = 65
    D1_2 = 50
    D2_2 = 100
    C_TGT = 563

    open_port()
    time.sleep(0.1)

    # if threshold==-1:
           #      closestDistanceTrim = ''
           #      Command_Response('[\w\W]+<scpinit:pass>','[SCPINIT]',timeout=0.5)
           #      Response=Command_Response('<scpgp-15:(.*)>','[SCPGP-15]')
           #      print Response.group(0)
           #      defaultTrim= int(Response.group(1))
           #      [Pre_Concha_off,Pre_Tragus_off]=Sen_Sample(sensor=[0,2],Sample_count=25,timeout=5.0)

           #      searchRange = range(31, 0, -1) # 31,30,….1
           #      searchRange += (range(32, 64))
           #      TARGET_OFF_VALUE=30


           #      print "Default Trim:", defaultTrim
           #      print "Target OFF:", TARGET_OFF_VALUE
           #      closestDistance = 500

           #      while True:
           #              currTrim = searchRange[int(len(searchRange)/2)]
           #              print ("Offset Trim: " + str(currTrim))
           #              Command_Response('<scpsp-15-%d:pass>'%currTrim,'[SCPSP-15-%d]'%currTrim)
           #              [Concha_off,Tragus_off]=Sen_Sample(sensor=[0,2],Sample_count=5,timeout=5.0)
           #              averageDark = (Concha_off+Tragus_off)/2
           #              if averageDark > TARGET_OFF_VALUE:
        			# searchRange = searchRange[:int(len(searchRange)/2)]
           #              else:
           #                      searchRange = searchRange[int(len(searchRange)/2):]
           #              distance = abs(averageDark - TARGET_OFF_VALUE)
           #              if distance < closestDistance:
           #                      closestDistance = distance
           #                      closestDistanceTrim = currTrim
           #              if len(searchRange) <= 1 or closestDistance < 3:
           #                      print "Closest (" + str(closestDistance) +  ") Trim:", closestDistanceTrim
           #                      break

           #      if closestDistance < 5:
           #          Result=Command_Response('<pass>','[SCPNVWR-OA1_OFFSET_TRIM-%d]'%closestDistanceTrim)
           #          print Result.group(0)
           #          Result=Command_Response('%d'%closestDistanceTrim,'[SCPNVRD-OA1_OFFSET_TRIM]')
           #          print Result.group(0)

           #          Command_Response('[\w\W]+<scpinit:pass>','[SCPINIT]',timeout=0.5)
           #          [Post_Concha_off,Post_Tragus_off]=Sen_Sample(sensor=[0,2],Sample_count=25,timeout=5.0)

           #          print "==========="
           #          print "Calibration complete"
           #          print "Pre cal trim = %d"%defaultTrim
           #          print "Pre_Concha_off=%f"%Pre_Concha_off
           #          print "Pre_Tragus_off=%f"%Pre_Tragus_off
           #          print "Post cal trim =%d"%closestDistanceTrim
           #          print "Post_Concha_off=%f"%Post_Concha_off
           #          print "Post_Tragus_off=%f"%Post_Tragus_off

           #      else:
           #          Result=Command_Response('<pass>','[SCPNVWR-OA1_OFFSET_TRIM-%d]'%closestDistanceTrim)
           #          print Result.group(0)
           #          Result=Command_Response('%d'%closestDistanceTrim,'[SCPNVRD-OA1_OFFSET_TRIM]')
           #          print Result.group(0)

           #          Command_Response('[\w\W]+<scpinit:pass>','[SCPINIT]',timeout=0.5)
           #          [Post_Concha_off,Post_Tragus_off]=Sen_Sample(sensor=[0,2],Sample_count=25,timeout=5.0)

           #          print "==========="
           #          print "Calibration failed"
           #          print "Pre cal trim = %d"%defaultTrim
           #          print "Pre_Concha_off=%f"%Pre_Concha_off
           #          print "Pre_Tragus_off=%f"%Pre_Tragus_off
           #          print "Post cal trim =%d"%closestDistanceTrim
           #          print "Post_Concha_off=%f"%Post_Concha_off
           #          print "Post_Tragus_off=%f"%Post_Tragus_off


    # if threshold==0:

        # C11_1,C12_1,C21_1,C22_1,C0_1,D0_1 = calib_fast_charge(T0_1,D1_1,D2_1)
        # C11_2,C12_2,C21_2,C22_2,C0_2,D0_2 = calib_fast_charge(T0_2,D1_2,D2_2)

        # # print("(C0_1 D0_1 T0_1) = (%d %d %d)" %(round(C0_1), round(D0_1), round(T0_1)))

        # # print("(C0_2 D0_2 T0_2) = (%d %d %d)" %(round(C0_2), round(D0_2), round(T0_2)))

        # m=Command_Response('<pass>','[SCPNVWR-RSENSE_CURR_CAL0-%d-%d-%d]'%(round(D0_1),T0_1,round(C0_1)))
        # print m.group(0)
        # m=Command_Response('<%d,%d,%d>'%(round(D0_1),T0_1,round(C0_1)),'[SCPNVRD-RSENSE_CURR_CAL0]')
        # print m.group(0)
        # m=Command_Response('<pass>','[SCPNVWR-RSENSE_CURR_CAL1-%d-%d-%d]'%(round(D0_2),T0_2,round(C0_2)))
        # print m.group(0)
        # m=Command_Response('<%d,%d,%d>'%(round(D0_2),T0_2,round(C0_2)),'[SCPNVRD-RSENSE_CURR_CAL1]')
        # print m.group(0)
        # m=Command_Response('<pass>','[SCPNVWR-TARG_CURR-%d]'%(C_TGT))
        # print m.group(0)
        # m=Command_Response('<%d>'%C_TGT,'[SCPNVRD-TARG_CURR]')
        # print m.group(0)
        # m=Command_Response('[\w\W]+<scpinit:pass>','[SCPINIT]',timeout=0.2)
        # print m.group(0)

        #C_MEAS = Sample_100(no=100,sample=2,comtype=commandtype)
        #C_ERR = (C_MEAS-float(C_TGT))/float(C_TGT)

        # print "\n\n"
        # print "X2A – FCT Optical Sense Self Test completed"
        # print "*******************"
        # print "D0_1=%f"%D0_1
        # print "C0_1=%f"%C0_1
        # print "D0_2=%f"%D0_2
        # print "C0_2=%f"%C0_2
        # print "C11_1=%f"%C11_1
        # print "C12_1=%f"%C12_1
        # print "C21_1=%f"%C21_1
        # print "C22_1=%f"%C22_1
        # print "C11_2=%f"%C11_2
        # print "C12_2=%f"%C12_2
        # print "C21_2=%f"%C21_2
        # print "C22_2=%f"%C22_2
        # #print "C_MEAS=%f"%C_MEAS
        # #print "C_ERR=%f"%C_ERR

    if threshold==1:
        vcselCurrents = [2.5, 3.25, 4.0]
        numSamples = 10
    #print "Long Current Sweep for threshold"

    # Threshold Current
    if threshold>=1:
        # Threshold Current Section
        for current in vcselCurrents:

            # C_TGT = round(((((current/1000)*100)/2.4)*4095))

            # #print "threshold current=%d"%C_TGT

            # m=Command_Response('<pass>','[SCPNVWR-TARG_CURR-%d]'%(C_TGT))
            # print m.group(0)

            # m=Command_Response('<%d>'%C_TGT,'[SCPNVRD-TARG_CURR]')

            # print m.group(0)


            # m=Command_Response('[\w\W]+<scpinit:pass>','[SCPINIT]',timeout=0.5)
            # print m.group(0)
            # time.sleep(2)

            # y_c_off, y_c_on, y_t_off, y_t_on,rsense_c,rsense_t = Sample_100(numSamples,sample=3,comtype=commandtype)

            avgResults = intrigue.intrigue_i_threshold(suppress_print = True, num_samples = numSamples, vcsel_current = int(current*1000))
            y_c_on  = avgResults["TIA1_LIGHT"]
            y_c_off = avgResults["TIA1_DARK"]
            y_t_on  = avgResults["TIA2_LIGHT"]
            y_t_off = avgResults["TIA2_DARK"]

            conchaReadings.append(y_c_on - y_c_off)
            tragusReadings.append(y_t_on - y_t_off)
            # conchaCurrent = calc_measured_current(rsense_c)
            # tragusCurrent = calc_measured_current(rsense_t)
            conchaCurrent = current
            tragusCurrent = current
            conchaCurrents.append(conchaCurrent)
            tragusCurrents.append(tragusCurrent)

        # Calculate Concha Values
        m_c, b_c = numpy.polyfit(conchaCurrents, conchaReadings, 1) # y = mx + b
        conchaGain = m_c
        conchaThresholdCurrent = -1 * b_c/m_c
        conchaRsq = numpy.corrcoef(conchaCurrents, conchaReadings)[0, 1]**2
        # Calculate Tragus Values
        m_t, b_t = numpy.polyfit(tragusCurrents, tragusReadings, 1) # y = mx + b
        tragusGain = m_t
        tragusThresholdCurrent = -1 * b_t/m_t
        tragusRsq = numpy.corrcoef(tragusCurrents, tragusReadings)[0, 1]**2
        # Print results
        for i in range(len(vcselCurrents)):
            print "(Concha Current %d, Concha y %d): (%f, %f)" % (i, i, conchaCurrents[i], conchaReadings[i])
        for i in range(len(vcselCurrents)):
            print "(Tragus Current %d, Tragus y %d): (%f, %f)" % (i, i, tragusCurrents[i], tragusReadings[i])
        print "Concha Threshold Current: %fmA" % conchaThresholdCurrent
        print "Tragus Threshold Current: %fmA" % tragusThresholdCurrent
        print "Concha gain: %f" % conchaGain
        print "Tragus gain: %f" % tragusGain
        print "Concha Rsqared: %f" % conchaRsq
        print "Tragus Rsquared: %f" % tragusRsq

        # C_TGT = 563
        # m=Command_Response('<pass>','[SCPNVWR-TARG_CURR-%d]'%(C_TGT))
        # print m.group(0)
        # m=Command_Response('<%d>'%C_TGT,'[SCPNVRD-TARG_CURR]')
        # print m.group(0)
        # m=Command_Response('[\w\W]+<scpinit:pass>','[SCPINIT]',timeout=0.5)
        # print m.group(0)
        return
if __name__ == '__main__':
    print 'Version: PROTO1_V01'
    main()
