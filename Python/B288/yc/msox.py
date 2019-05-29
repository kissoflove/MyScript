#!/usr/bin/env python
# Copyright (C) 2017 Apple Inc. All rights reserved.
#
# This document is the property of Apple Inc.
# It is considered confidential and proprietary.
#
# This document may not be reproduced or transmitted in any form,
# in whole or in part, without the express written permission of
# Apple Inc.
#
# Created by Yewching Chen <yewching_chen@apple.com> 
#

import sys, os
import pyvisa
from numpy import *
import time


class mso4k:
    def __init__(self, timeout=10000, reset=False):
        rm = pyvisa.ResourceManager()
        reses = rm.list_resources()

        foundscope = False
        for res in reses:
            open_res = rm.open_resource(res)
            try:
                if 'MSO-X 4' in open_res.query('*IDN?'):
                    print 'Found Keysight device:'
                    print '======================'
                    print open_res.query('*IDN?')
                    self.res = open_res
                    foundscope = True
                    break
            except(pyvisa.errors.VisaIOError):
                print 'Warning: Tried to access a non-VISA compliant resource.'
                pass

        if not foundscope:
            print '==============================================='
            print 'Error! Could not find a Keysight 4k series MSO!'
            exit()

        self.res.timeout = timeout
        self.res.clear()
        self.identity = self.idn()
        if reset:
            self.reset()
        return

    def idn(self):
        return self.query('*IDN?')

    def reset(self):
        return self.write('SYST:PRES')

    def factory_reset(self):
        retVal = self.write('*RST')
        return retVal
        
    def autoscale(self):
        self.write('AUTOSCALE')
        return

    def set_channel_scale(self, idx, scale):
        return self.write('CHAN{}:SCAL {}V'.format(idx,scale))

    def set_channel_offset(self, idx, offset):
        verticalRange = self.get_channel_range(idx)
        if abs(offset) > verticalRange/2:
            exit('ERROR: current vertical range is {}, offset must be +/- {}'.format(verticalRange,verticalRange/2))
        self.write('CHAN{}:OFFS {}'.format(idx,offset))

    def get_channel_range(self, idx):
        return float(self.write('CHAN{}:RANG?'.format(idx)))

    def enable_labels(self):
        return self.write('DISP:LAB 1')

    def disable_labels(self):
        return self.write('DISP:LAB 0')

    def set_label(self, source, label):
        return self.write('CHAN{0}:LAB "{1}"'.format(source, label))

    def set_timebase_range(self, val):
        return self.write('TIM:RANG {0}'.format(str(val)))

    def set_timebase_reference(self, val):
        if val not in ['center','left','right']:
            raise ValueError('Unrecognized timebase reference: {0}'.format(val))

        return self.write('TIM:REF {0}'.format(val[:4]))

    def set_timebase_position(self, val):
        return self.write('TIM:POS {0}'.format(val))

    def set_timebase_scale(self, val):
        return self.write('TIM:SCAL {0}'.format(val))

    def set_trigger_mode(self, source, val, slope):
        if val.lower() not in ['edge', 'glitch',' pattern', 'tv', 'delay', 'eburst', 'or', 'runt', 'shold', 'transition', 'sbus1', 'sbus2']:
            raise ValueError('Invalid trigger mode: {0}'.format(val))
        self.write('TRIG:SOURce CHANnel{0}'.format(source))
        self.write('TRIG:MODE {0}'.format(val))
        self.write('TRIG:SLOPe {0}'.format(slope))
        self.write(':TRIG:LEVel:ASETup')
        return

    def capture(self):
        self.write('*TRG')

    def acquire_points(self, points='get'):
        if points == 'get':
            return float(self.query(':WAVeform:POINts?'))
        else:
            self.write(':WAVeform:POINts '+str(points))

    def chan_scale(self, channel, scale='get'):
        if scale == 'get':
            return float(self.query(':CHANnel'+str(channel)+':SCALe?'))
        else:
            self.write(':CHANnel'+str(channel)+':SCALe '+str(scale)+'V')

    def chan_offset(self, channel, offset='get'):
        if offset == 'get':
            return float(self.query(':CHANnel'+str(channel)+':OFFSet?'))
        else:
            self.write(':CHANnel'+str(channel)+':OFFSet '+str(offset)+'V')

    def time_scale(self, scale='get'):
        if scale == 'get':
            return float(self.query(':TIMebase:SCALe?'))
        else:
            self.write(':TIMebase:SCALe '+str(scale))

    def acquire(self, channel):
        self.write(':ACQuire:TYPE NORMal')
        self.write(':ACQuire:COMPlete 100')
        self.write(':TIMebase:MODE MAIN')
        self.write(':WAVeform:POINts:MODE MAX')
        self.write(':WAVeform:SOURce CHANnel'+str(channel))
        self.write(':WAVeform:FORMat BYTE')
        
        self.write('WAV:FORM ASC')
        val = self.write('WAV:DATA?')
        data = map(float, val[10:-1].split(','))

        return data    

    def save_image(self, outputFile, imageFormat='png', imageColor='color', inksaver=False, landscape=False):
        val = self.write('DISP:DATA? {0}, {1}'.format(imageFormat, imageColor), raw = True)
        fid = open(outputFile, 'wb')
        fid.write(val[10:-1])
        fid.close()
        return True

    def measure_rise_time(self):
        resultStr = self.write('MEAS:RISEtime?')
        return float(resultStr.rstrip())

    def measure_fall_time(self):
        resultStr = self.write('MEAS:FALLtime?')
        return float(resultStr.rstrip())

    def measure_overshoot(self):
        resultStr = self.write(':MEAS:OVERshoot?')
        return float(resultStr.rstrip())

    def measure_vtop(self):
        resultStr = self.write(':MEAS:VTOP?')
        return float(resultStr.rstrip())

    def measure_vbase(self):
        resultStr = self.write(':MEAS:VBASe?')
        return float(resultStr.rstrip())

    def measure_frequency(self):
        resultStr = self.write(':MEAS:FREQuency?')
        return float(resultStr.rstrip())

    def measure_delay(self, val1, val2):
        self.write(':MEAS:DELay:DEFine {0},1,MIDDle,{1},2,MIDDle'.format(val1,val2))
        print(':MEAS:DELay:DEFine {0},0,MIDDle,{1},0,MIDDle'.format(val1,val2))
        resultStr = self.write(':MEAS:DELay?')
        return float(resultStr.rstrip())

    def measure_source(self, src):
        return self.write(':MEAS:SOURce CHANnel{0}'.format(src))

    def display_channel(self, source, val):
        return self.write(':CHANnel{0}:DISPlay {1}'.format(source,val))

    def all_channels(self, val):
        val=0
        self.write(':CHANnel1:DISPlay {0}'.format(val))
        self.write(':CHANnel2:DISPlay {0}'.format(val))
        self.write(':CHANnel3:DISPlay {0}'.format(val))
        self.write(':CHANnel4:DISPlay {0}'.format(val))
        return 

    def stop(self):
        self.write(':STOP')
        return

    def run(self):
        self.write(':RUN')
        return

    def single(self):
        return self.write('SING')

    def display_cursor(self, name, val):
        return self.write('MARK:{0}:DISP {1}'.format(name, val))

    def set_cursor_source(self, name, source):
        return self.write('MARK:{0} {1}'.format(name, source))

    def get_cursor_source(self, name):
        return self.write('MARK:{0}?'.format(name))

    def set_cursor_position(self, name, val):
        result = self.write('MARK:{0}p {1}'.format(name, val))
        time.sleep(0.5)
        return result

    def get_cursor_position(self, name):
        resultStr = self.write('MARK:{0}p?'.format(name))
        return(float(resultStr.rstrip()))

    def set_cursor_mode(self, val):
        return self.write('MARK:MODE {0}'.format(val))

    def write(self, cmd, raw=False):
        writeSucceeded = False
        while writeSucceeded == False:
            try:
                self.res.write(cmd)
                writeSucceeded = True
            except:
                self._device.clear()
                writeSucceeded = False
    
        if cmd.find('?') > 0:
            if (raw):
                response = self.res.read_raw()
            else:
                response = self.res.read()
        else:
            response = None
        return response
    
    def query(self, cmd):
        return self.res.query(cmd)


