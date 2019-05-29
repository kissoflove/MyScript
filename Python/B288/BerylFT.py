#Manan Patel, Calvin Ryan, Apple July 10, 2017
#For questions email <coyote@apple.com>


#################### BERYL DEFINITIONS #######################

BERYL_SPMI_ADDRESS = 0x0F
BERYL_ADDRESS = 0x3C
MUX_ADDRESS = 0x70

import sys
import os
import __builtin__
import signal
from array import array
import time
import datetime
# from bs4 import BeautifulSoup
# import spmi
# from aardvark_py import *
import argparse
# import hw
import serial
import glob
import string

h = None

class Beryl(object):

    channel = None
    verbose = False
    standalone = False
    update = False


    def __init__(self, channel = None, port = None):
        global h
        global i2cHandle
        global exemptRegList
        global serialHandle
        global berylVersion

        berylVersion = "A0"

        if channel == "UART1":
            self.channel = channel
            serialPort = port
            baudRate = 115200
            serialHandle = serial.Serial(serialPort, baudRate, timeout = 6)
            serialHandle.flush()
        # s.write("beryl read 0x1B042\n")
        # returnString = s.readline()
        # returnString = s.readline()




        # port = 0

        # i2cHandle = None

        # i2cHandle = aa_open(port)
        # if (i2cHandle > 0):
        #     i2c_exist = True
        # else:
        #     print "Unable to open Aardvark device on port %d" % port
        #     print "Error code = %d" % i2cHandle
        #     print "Could not create I2C handle."
        #     i2c_exist = False


        # # Ensure that the I2C selfubsystem is enabled
        # aa_configure(i2cHandle,  AA_CONFIG_SPI_I2C)
        # # Enable the Aardvark adapter's power supply.
        # aa_target_power(i2cHandle, AA_TARGET_POWER_BOTH)
        # # Set the bitrate
        # bitrate = aa_i2c_bitrate(i2cHandle, 100)

        ######### Create an SPMI handle

        # spmi_exist = False
        # spmi_exist = True

        # if force_chan != "i2c":
        #     try:
        #         hwHandle = h
        #         spmi.spmi_init(hwh = hwHandle)
        #     except SystemExit:
        #         print "Could not create SPMI handle."
        #         spmi_exist = False
        #     try:
        #         hwHandle = h
        #         spmi.spmi_init(hwh = hwHandle)
        #     except SystemExit:
        #         print "Could not create SPMI handle."
        #         spmi_exist = False

        # print
        # if i2c_exist == True:
        #     print "I2C Handle created."

        # if spmi_exist == True:
        #     print "SPMI Handle created."

        # if (force_chan == 'spmi') & spmi_exist:
        #     self.channel = 'spmi'
        #     print "Using spmi handle"
        # elif (force_chan == 'spmi') & (not spmi_exist):
        #     print "Cannot force spmi - no handle available."
        #     sys.exit()
        # elif (force_chan == 'i2c') & i2c_exist:
        #     self.channel = 'i2c'
        #     print "Using i2c handle"
        # elif (force_chan == 'i2c') & (not i2c_exist):
        #     print "Cannot force i2c - no handle available."
        #     sys.exit()

        self.regDict = self.init_reg_dict_from_text()
        # self.set_verbosity()
        self.regs = {}

        #Define comm channel, prefer spmi
        # if spmi_exist & i2c_exist:
        #     Beryl.channel = 'spmi'
        # elif spmi_exist & (not i2c_exist):
        #     Beryl.channel = 'spmi'
        # elif (not spmi_exist) & i2c_exist:
        #     Beryl.channel = 'i2c'
        # else:
        #     print "No comm channels available. Exiting..."
        #     sys.exit()

    def write_reg(self, reg, data_out, addr_len = 16):
        # if self.channel == 'i2c':

        #     if (reg == None or data_out == None):
        #         raise ValueError('Check function inputs')

        #     reg_MSB = (reg & 0xFF00) >> 8
        #     reg_LSB = (reg & 0x00FF)
        #     llen = len(data_out)

        #     payload = array_u08(llen + 2)
        #     payload[0] = reg_MSB
        #     payload[1] = reg_LSB

        #     for i in range (0,llen):
        #         payload[i+2] = data_out[i]

        #     if self.standalone == False:
        #         aa_i2c_write(i2cHandle, MUX_ADDRESS, AA_I2C_NO_FLAGS, array('B', [0x01]))

        #     aa_i2c_write(i2cHandle, BERYL_ADDRESS, AA_I2C_NO_FLAGS, payload)

        #     key = self.regDict.keys()[self.regDict.values().index(reg)]


        #     # These registers have bits that return to POR value immediately after being written
        #     exemptRegList = [
        #         "ISINK_ISINK1_PWM_TRIGGER",
        #         "ISINK_ISINK2_PWM_TRIGGER",
        #         "ISINK_ISINK3_PWM_TRIGGER",
        #         "GPADC_SCH_1_TRIG",
        #         "GPADC_SCH1_COMP",
        #         "GPADC_SCH_2_TRIG",
        #         "GPADC_SCH2_COMP"
        #         ]

        #     if self.read_reg(reg = reg, length = 1) != data_out[0]:
        #         if key not in exemptRegList:
        #             print "write failed, register : %s" %key

        #     else:
        #         key = self.regDict.keys()[self.regDict.values().index(reg)]
        #         self.regs[key] = array('B', [data_out[0]])

        # elif self.channel == 'spmi':
        #     if addr_len == 16:
        #         #Beryl datasheet Section20.1 - A full 16 bit address can be specified only using SPMI ERRL or ERWL commands."
        #         spmi.erwl(slave = BERYL_SPMI_ADDRESS, addr = reg, data = data_out)

        #     elif addr_len == 8:
        #         spmi.erw(slave = BERYL_SPMI_ADDRESS, addr = reg, data = data_out)

        #     elif addr_len == 5:
        #         spmi.rw(slave = BERYL_SPMI_ADDRESS, addr = reg, data = data_out)

        if self.channel == "UART1":
            for data in data_out:
                # serialHandle.flush()
                serialHandle.flushOutput()
                serialHandle.flushInput()
                cmd = "beryl write %s %s\n" % (reg, data)
                print datetime.datetime.now().strftime("\n%Y-%m-%d %H:%M:%S.%f"),'  ',cmd ,
                serialHandle.write("beryl write %s %s\n" % (reg, data))
                returnString = serialHandle.read_until(']')
                print datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"),' ',returnString ,
                # print "Line 1 WRITE: %s" % returnString
                # First line is just an echo of the sent command, discard and read another line
                #returnString = serialHandle.readline()
                # print "Line 2 WRITE: %s" % returnString
                #print datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"),' ', returnString


        else:
            print "No channels available."

    # Removed write_spmi_zero()

    def read_reg(self, reg, length = 1, ret_addr = False, addr_len = 16):
        # # if self.channel == 'i2c':

        #     if (reg == None or length == None):
        #         raise ValueError('Check function inputs')

        #     reg_MSB = (reg & 0xFF00) >> 8
        #     reg_LSB = (reg & 0x00FF)
        #     payload = array_u08(2)
        #     payload[0] = reg_MSB
        #     payload[1] = reg_LSB
        #     data = array_u08(length)

        #     if self.standalone == False:
        #         aa_i2c_write(i2cHandle, MUX_ADDRESS, AA_I2C_NO_FLAGS, array('B', [0x01]))

        #     #send write and register address
        #     aa_i2c_write(i2cHandle, BERYL_ADDRESS, AA_I2C_NO_FLAGS, payload)
        #     #send read command
        #     (count, data_in) = aa_i2c_read(i2cHandle, BERYL_ADDRESS, AA_I2C_NO_FLAGS, 1)

        #     key = self.regDict.keys()[self.regDict.values().index(reg)]
        #     self.regs[key] = data_in

        #     if ret_addr == True:
        #         return [hex(reg), data_in[0]]
        #     else:
        #         return data_in[0]

        # elif self.channel == 'spmi':
        # #Beryl datasheet Section20.1 - "A full 16 bit address can be specified only using SPMI ERRL or ERWL commands."
        #     if addr_len == 16:
        #         if ret_addr == True:
        #             ret = spmi.errl(slave = BERYL_SPMI_ADDRESS, addr = reg)
        #             if self.verbose:
        #                 print [hex(reg), hex(int(ret[1][0]))]
        #             return [reg, ret[1][0]]

        #         else:
        #             ret = spmi.errl(slave = BERYL_SPMI_ADDRESS, addr = reg)
        #             if self.verbose:
        #                 print hex(int(ret[1][0]))
        #             return ret[1][0] #just the value

        #     ### SAM
        #     elif addr_len == 8:
        #         if ret_addr == True:
        #             ret = spmi.err(slave = BERYL_SPMI_ADDRESS, addr = reg)
        #             if self.verbose:
        #                 print [hex(reg), hex(int(ret[1][0]))]
        #             return [reg, ret[1][0]]

        #         else:
        #             ret = spmi.err(slave = BERYL_SPMI_ADDRESS, addr = reg)
        #             if self.verbose:
        #                 print hex(int(ret[1][0])) #just the value
        #             return ret[1][0] #just the value

        #     ### SAM
        #     elif addr_len == 5:
        #         if ret_addr == True:
        #             ret = spmi.rr(slave = BERYL_SPMI_ADDRESS, addr = reg)
        #             if self.verbose:
        #                 print [hex(reg), hex(int(ret[1]))]
        #             return [reg, ret[1]]

        #         else:
        #             ret = spmi.rr(slave = BERYL_SPMI_ADDRESS, addr = reg)
        #             if self.verbose:
        #                 print hex(int(ret[1])) #just the value
        #             return ret[1] #just the value

        if self.channel == "UART1":
            # serialHandle.flush()
            serialHandle.flushOutput()
            serialHandle.flushInput()
            cmd = "beryl read %s\n" % hex(reg)
            print datetime.datetime.now().strftime("\n%Y-%m-%d %H:%M:%S.%f"),'  ', cmd ,
            serialHandle.write("beryl read %s\n" % hex(reg))
            returnString = serialHandle.read_until(']')
            print datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"), ' ', returnString ,
            # print "Line 1: %s" % returnString
            # First line is just an echo of the sent command, discard and read another line
            # returnString = serialHandle.readline()
            # print datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"),' ', returnString
            # print "Line 2: %s" % returnString

            if "error" in returnString or "]" not in returnString:
                print returnString
            else:
                tmpStr = returnString.split('beryl:ok')[1]
                tmpStr = tmpStr.replace(']','')
                tmpStr = tmpStr.replace('\n','')
                tmpStr = tmpStr.replace('\r','')
                tmpStr = tmpStr.strip()
                return int(tmpStr,16)
                #return int(returnString.split()[2], 16)
        else:
            print "No channels available."

    def dump_reg(self, startReg, stopReg):
        if self.channel == "UART1":
            # serialHandle.flush()
            serialHandle.flushOutput()
            serialHandle.flushInput()
            cmd = "beryl dump %s %s\n" % (hex(startReg), hex(stopReg))
            print datetime.datetime.now().strftime("\n%Y-%m-%d %H:%M:%S.%f"),'  ',cmd ,
            serialHandle.write("beryl dump %s %s\n" % (hex(startReg), hex(stopReg)))
            returnString = serialHandle.read_until(']')
            print datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"),'  ', returnString,

            if ']' not in returnString:
                print returnString
                raise RuntimeError('Unit Response invalid !')

            # returnString = serialHandle.readline()
            # if "error" in returnString:
                # print returnString
            returnList = []
            # First line is just an echo of the sent command, discard and read another line
            # for i in range (stopReg - startReg + 1):
            #     returnList.append(int(serialHandle.readline().split()[2], 16))
            #
            # returnString = serialHandle.readline()
            # if "error" in returnString:
            #     print returnString
            # else:
            #     return returnList

            arr = returnString.split('\n')
            for sub in arr:
                if '=' in sub:
                    returnList.append(int(sub.split('=')[1].strip(), 16))

            if 'error' in returnString:
                print '\n', returnString
                return returnString
            else:
                print '\n', returnList
                return returnList
        else:
            print "No channels available."


            # Removed set_verbosity()

    # Dependency: Beautiful Soup
    # TODO: consider removing dependency
    # def init_reg_dict_from_html(self):
    #     with open('BERYL_A0_regmap_customer_v4_2_0.html') as fp:
    #         soup = BeautifulSoup(fp, "html.parser")

    #     for script in soup(["script", "style"]):
    #         script.extract()

    #     text = soup.get_text()
    #     text = text.splitlines()

    #     startFound = False
    #     endFound = False

    #     regDict = {}
    #     index = 0
    #     while (startFound is False):
    #         for each in text:
    #             index = index + 1
    #             #print each
    #             if each == 'VIRTUAL ADDRESSES':
    #                 print 'beginning found!'
    #                 startFound = True
    #                 index = index + 1
    #                 break

    #     while(endFound is False):
    #         for i in range(index, len(text)):
    #             if text[i] == 'VIRTUAL ADDRESSES':
    #                 endFound = True
    #                 print 'beginning found!'
    #                 break

    #             #print each
    #             temp = text[i].split('0x')
    #             #print temp
    #             if len(temp) == 2:
    #                 temp[0] = str((temp[0].split('('))[0])
    #                 temp[1] = int('0x' + str(temp[1]), 0)
    #                 regDict['%s' % temp[0]] = temp[1]


        #file = open('BerylRegs.txt', 'w')
        #for key,val in self.regDict.items():
        #   s = '{} = {} \n'.format(key,hex(val))
        #   file.write(s)

        # return regDict

    def close_port(self):
        serialHandle.flush()
        serialHandle.close()

    # Dependency: BerylRegs.txt
    def init_reg_dict_from_text(self):
        file = open('BerylRegs.txt', 'r')
        dic = {}
        for line in file:
            line = line.split(' = ')
            name = line[0]
            address = int(line[1].strip(' \n'), 0)
            dic['%s' %name] = address

        return dic

    def update_reg_values(self, regDict):

        regValues = {}

        for each in regDict:
            regValues[each] = self.read_reg(reg = regDict[each], length = 1)

        self.regs = regValues

    def force_power_mode(self, FORCE_STATE):

            modes = {
                    'ACT0' : 0x00,
                    'ACT1' : 0x01,
                    'ACT2' : 0x02,
                    'ACT3' : 0x03,
                    'HOSTOFF' : 0x04,
                    'SYSOFF' : 0x05,
                    'SHIP' : 0x06
                    }

            reg = 'VSYS_POWER_STATE_FORCE'

            data = [modes[FORCE_STATE] | 0x80]
            self.write_reg(self.regDict[reg], data)

    def set_32k_ref(self, SRC = 'INTERNAL'):
        sources = {
            'INTERNAL': 0x02,
            'HOST'    : 0x01,
            'AUTO'    : 0x00
        }

        reg = 'VMAX_CTRL'
        data = [sources[SRC] | 0x08]   # The 0x08 sets the test mode bit
        self.write_reg(self.regDict[reg], data)

    def toggle_supply(self, MODE, ON = True, SUPPLY = None, ALL_SUPPLIES = False):
        """ For more information see registers 0x1300 - 0x130B in Beryl regmap. """

        supplies = {
                  'BUCK0' : 0,
                  'BUCK1' : 1,
                  'BUCK2' : 2,
                  'BUCK3' : 3,
                  'LDO0' : 4,
                  'LDO1' : 5,
                  'LDO2' : 6,
                  'LDO3' : 7
                  }

        reg = self.regDict['PWRONOFF_%s_CONF_A' %MODE]

        if ALL_SUPPLIES == True:
            if ON == True:
                toSend = [1]
            elif ON == False:
                toSend = [0]
            self.write_reg(reg, toSend)

        else:
            data = 1 << supplies[SUPPLY]
            if ON == True:
                toSend = [self.read_reg(reg = reg) | data]
            elif ON == False:
                toSend = [self.read_reg(reg = reg) & ~(data)]

            self.write_reg(reg, toSend)


    def set_slew_rate(self, value):
        if self.read_reg(reg = self.regDict['DFTCTL_TEST_EN'], length = 1) != 0:
            self.write_reg(reg = self.regDict['SPMISLV_CONF_PAD_PP_STR'], data_out = value)
        else:
            print '\nNeed to enable Test mode to modify slew rate, try calling test_mode_enable().'

    def test_mode_enable(self):
        print "******** Begin test mode check."
        if self.read_reg(reg = self.regDict['DFTCTL_TEST_EN'], length = 1) == 0:

            self.write_reg(reg = self.regDict['DFTCTL_KEY1'], data_out = [0x44])
            self.write_reg(reg = self.regDict['DFTCTL_KEY2'], data_out = [0x61])
            self.write_reg(reg = self.regDict['DFTCTL_KEY3'], data_out = [0x76])
            self.write_reg(reg = self.regDict['DFTCTL_KEY4'], data_out = [0x65])
            self.write_reg(reg = self.regDict['VMAX_CTRL'],   data_out = [0x8])

            #print "ignore write fail"
            print '******** Test mode enabled.'

        else:
            print '******** Test mode already enabled.'

    def test_mode_disable(self):

        if self.read_reg(reg = self.regDict['DFTCTL_TEST_EN'], length = 1) != 0:
            self.write_reg(reg = self.regDict['DFTCTL_TEST_EN'], data_out = [0])

            print "test mode disabled"
        else:
            print 'test mode already disabled'

    def trigger_isink(self, isink_num):
        regName = 'ISINK_ISINK%s_PWM_TRIGGER' %isink_num
        self.write_reg(reg = self.regDict[regName], data_out = [0x1])

    def set_isink_current(self, isink_num, current, iset_num = 0):
        """
        See registers 0x1B05, 0x1B06, 0x1B12, 0x1B13 in the beryl regmap
        current value is in uA
        """

        data = (current - 50)/50
        reg = 'ISINK_ISINK{}_ISET{}'.format(isink_num, iset_num)
        self.write_reg(reg = self.regDict[reg], data_out = [data])

    def enable_isink(self, isink_num, PWM_MODE = 'CC', FAST_EN = 0x0, TRIG_SEL = 'SW'):
        pwm_modes = {
                    'CC' : 0x00,
                    'Pulse' : 0x01,
                    'PWM' : 0x02,
                    'Blink' : 0x03,
                    'Ramp' : 0x04,
                }

        hw_trigs =  {
                    'GPADC' : 0x00,
                    'MFIO' : 0x01,
                    'SW' : 0x02,
                    'SPMI' : 0x03,
                    }

        data =  int(FAST_EN) << 6 | pwm_modes[PWM_MODE] << 3 | hw_trigs[TRIG_SEL] << 1 | 0x01

        #print data
        regName = 'ISINK_ISINK%s_CONTROL' %isink_num
        self.write_reg(reg = self.regDict[regName], data_out = [data])

    def disable_isink(self, isink_num):
        regName = 'ISINK_ISINK%s_CONTROL' %isink_num
        self.write_reg(reg = self.regDict[regName], data_out = [0])

    def enable_isink_global(self, FAST_EN = 0x0):
        regName = 'ISINK_SYS_CONTROL'
        data = 0x02 | int(FAST_EN)
        self.write_reg(reg = self.regDict[regName], data_out = [data])

    def disable_isink_global(self, FAST_EN = 0x0):
        regName = 'ISINK_SYS_CONTROL'
        self.write_reg(reg = self.regDict[regName], data_out = [0x0])

    def config_isink_pwm(self, isink_num, PWM_CYC = 0, PWM0 = 0, PWM1 = 0): #period and on-time in uS
        """
        See registers 0x1B07 - 0x1BC and 0x1B14 - 0x1B19 in beryl regmap
        period and on-time given in uS
        """

        p_data = (PWM_CYC - 32)/32
        p_MSB = ((p_data & 0xFF00) >> 8)
        p_LSB = p_data & 0x00FF

        o_data0 = PWM0/32
        o_MSB0 = ((o_data0 & 0xFF00) >> 8)
        o_LSB0 = o_data0 & 0x00FF

        o_data1 = PWM1/32
        o_MSB1 = ((o_data1 & 0xFF00) >> 8)
        o_LSB1 = o_data1 & 0x00FF

        #there is better way to do the following lol
        if (p_MSB < 0):
            p_MSB = 0

        if (o_MSB0 < 0):
            o_MSB0 = 0

        if (o_MSB1 < 0):
            o_MSB1 = 0

        pHI_regName = 'ISINK_ISINK%s_PWM_CYC_HI' %isink_num
        pLO_regName = 'ISINK_ISINK%s_PWM_CYC_LO' %isink_num

        oHI0_regName = 'ISINK_ISINK%s_PWM0_HI' %isink_num
        oLO0_regName = 'ISINK_ISINK%s_PWM0_LO' %isink_num

        oHI1_regName = 'ISINK_ISINK%s_PWM1_HI' %isink_num
        oLO1_regName = 'ISINK_ISINK%s_PWM1_LO' %isink_num

        self.write_reg(reg = self.regDict[pHI_regName], data_out = [p_MSB])
        self.write_reg(reg = self.regDict[pLO_regName], data_out = [p_LSB])

        self.write_reg(reg = self.regDict[oHI0_regName], data_out = [o_MSB0])
        self.write_reg(reg = self.regDict[oLO0_regName], data_out = [o_LSB0])

        self.write_reg(reg = self.regDict[oHI1_regName], data_out = [o_MSB1])
        self.write_reg(reg = self.regDict[oLO1_regName], data_out = [o_LSB1])

    def pulse_isink(self, current=3300, width=10000, cycle=1, num_samples=10): #width in uS, cycle in secs
        #VCSEL_EN = 11
        #self.beryl.configure_io_mfio_conf(FUNC = 'GPIO',MFIO_num = VCSEL_EN, IOCELL_CFG =  'PUSH_PULL', SUPPLY = 'VDD_1V8')
        #self.beryl.configure_io_mfio_conf(FUNC = 'ISINK3_PWM',MFIO_num = 8, IOCELL_CFG =  'PUSH_PULL', SUPPLY = 'VDD_1V8')
        self.beryl.disable_isink_global(FAST_EN = 0x0)
        self.beryl.enable_isink_global(FAST_EN = 0x0)
        self.beryl.enable_isink(isink_num = 1, PWM_MODE = 'Pulse', FAST_EN = 0x0, TRIG_SEL = 'SW')
        self.beryl.enable_isink(isink_num = 2, PWM_MODE = 'Pulse', FAST_EN = 0x0, TRIG_SEL = 'SW')
        #self.beryl.enable_isink(isink_num = 3, PWM_MODE = 'Pulse', FAST_EN = 0x0, TRIG_SEL = 'SW')
        self.beryl.config_isink_pwm(isink_num = 1, PWM_CYC = 0, PWM0 =  width)
        self.beryl.config_isink_pwm(isink_num = 2, PWM_CYC = 0, PWM0 =  width)
        #self.beryl.config_isink_pwm(isink_num = 3, PWM_CYC = 0, PWM0 =  width)
        self.beryl.set_isink_current(isink_num = 1, current = current)
        self.beryl.set_isink_current(isink_num = 2, current = current)
        #self.beryl.set_isink_current(isink_num = 3, current = current)
        j=0
        while j < num_samples:
            #self.beryl.configure_io_gpio_conf(GPIO_num = VCSEL_EN, IO_CONFIG = 0x0, DEB = '0ms', WAKE_LVL = 1)
            #self.beryl.configure_io_gpio_conf(GPIO_num = VCSEL_EN, IO_CONFIG = 0x1, DEB = '0ms', WAKE_LVL = 1)
            self.beryl.trigger_isink(isink_num = 1)
            #self.beryl.trigger_isink(isink_num = 3)
            time.sleep(cycle)
            if num_samples != 0:
                j += 1
        j=0
        while j < num_samples:
            #self.beryl.configure_io_gpio_conf(GPIO_num = VCSEL_EN, IO_CONFIG = 0x0, DEB = '0ms', WAKE_LVL = 1)
            #self.beryl.configure_io_gpio_conf(GPIO_num = VCSEL_EN, IO_CONFIG = 0x1, DEB = '0ms', WAKE_LVL = 1)
            self.beryl.trigger_isink(isink_num = 2)
            #self.beryl.trigger_isink(isink_num = 3)
            time.sleep(cycle)
            if num_samples != 0:
                j += 1
        return


    def configure_io_mfio_conf(self, MFIO_num, FUNC = 'GPIO', IOCELL_CFG = 'PD_OD_PMOS', IN_MONITOR = 0x0, POLARITY = 0x0, SUPPLY = 'VDD_MAIN', SENS = 'POS_EDGE'):

        func_modes = {
                    'GPIO' : 0x00,
                    'RESET_IN/BUTTON' : 0x01,
                    'SINKTRIG1' : 0x02,
                    'SINKTRIG2' : 0x03,
                    'SINKTRIG3' : 0x04,
                    'RSTCD' : 0x05,
                    'CCTRIG' : 0x06,
                    'ADCTRIG1' : 0x07,
                    'ADCTRIG2' : 0x08,
                    'PWR_TRANS' : 0x09,
                    'ACTIVEHOLD' : 0x0A,
                    'TBUCK0' : 0x0B,
                    'TBUCK1' : 0x0C,
                    'TBUCK2' : 0x0D,
                    'TBUCK_STRB' : 0x0E,
                    'ISINK3_PWM' : 0x0F,
                    'VCHG_DET' : 0x10,
                    'VCHG_DEC' : 0x11,
                    'ACT_DIODE' : 0x12,
                    'ADCSEQ1' : 0x13,
                    'ADCSEQ2' : 0x14,
                    'ADCSEQ3' : 0x15,
                    'ADCSEQ4' : 0x16,
                    'PCLK_32K' : 0x17,
                    'RTC_32K' : 0x18,
                    'RTC_1HZ' : 0x19,
                    'HOSTDFU' : 0x1A,
                    'COMMS_EN/DOCK_CONN' : 0x1B,
                    'SWD' : 0x1C,
                    'GP_RSTCD' : 0x1D,
                    'PSEQ' : 0x1E,
                    'NIRQ' : 0x1F
                }

        io_modes = {
                    'INPUT' : 0x00,
                    'PU_OD_NMOS' : 0x01,
                    'PD_OD_PMOS' : 0x02,
                    'OD_PMOS' : 0x03,
                    'OD_NMOS' : 0x04,
                    'PUSH_PULL' : 0x05
                }

        supply_modes = {
                    'VDDIOA' : 0x00,
                    'VDD_1V8' : 0x01,
                    'VDDIOB' : 0x02,
                    'VDD_MAIN' : 0x03
                }

        sens_modes = {
                    'HI_LEV' : 0x00,
                    'LO_LEV' : 0x01,
                    'POS_EDGE' : 0x02,
                    'NEG_EDGE' : 0x03,
                    'ANY_EDGE' : 0x04
                }

        data = func_modes[FUNC]  << 3 | io_modes[IOCELL_CFG]
        regName = 'IO_MFIO%s_CONF1' %MFIO_num
        self.write_reg(reg = self.regDict[regName], data_out = [data])

        data = IN_MONITOR << 6 | POLARITY << 5 | supply_modes[SUPPLY] << 3 | sens_modes[SENS]
        regName = 'IO_MFIO%s_CONF2' %MFIO_num
        self.write_reg(reg = self.regDict[regName], data_out = [data])

    def configure_io_gpio_conf(self, GPIO_num, SPMI_TRANS_DLY_EN = 0x0, RTC_CNT_TRANS_DLY_EN = 0x0, IO_CONFIG = 0x0, DEB = '10ms', WAKE_LVL = 0x0):
        #register 0x191A

        debounce_modes = {
                    '0ms' : 0x00,
                    '5ms' : 0x01,
                    '10ms' : 0x02,
                    '50ms' : 0x03,
                    '250ms' : 0x04,
                    '500ms' : 0x05,
                    '750ms' : 0x06,
                    '1000ms' : 0x07
                }

        data = RTC_CNT_TRANS_DLY_EN << 6 | SPMI_TRANS_DLY_EN << 5 | IO_CONFIG << 4 | debounce_modes[DEB] << 1 | WAKE_LVL
        regName = 'IO_GPIO%s_CONF1' %GPIO_num
        self.write_reg(reg = self.regDict[regName], data_out = [data])

    # Removed configure_buttons()

    def configure_reset_in(self, RIN3_T_DEB = 0x1, RIN2_T_DEB = 0x1, RIN1_T_DEB = 0x1, RIN3_DIS = 0x0, RIN2_DIS = 0x0, RIN1_DIS = 0x0):
        data = RIN3_T_DEB << 5 | RIN2_T_DEB << 4 | RIN1_T_DEB << 3 | RIN3_DIS << 2 | RIN2_DIS << 1 | RIN1_DIS
        regName = 'IO_CONF_C'
        self.write_reg(reg = self.regDict[regName], data_out = [data])

    # Removed configure_2_finger_reset()

    def configure_adc_triggers(self, ADC_TRIG2_CFG = 'SCAN2', ADC_TRIG1_CFG = 'SCAN1'):
        adc_agent_modes = {
                    'SCAN1' : 0x00,
                    'SCAN2' : 0x01,
                    'MAN1' : 0x02,
                    'MAN2' : 0x03
                }

        regName = 'IO_CONF'

        current = self.read_reg(reg = self.regDict[regName], length = 1)
        keepMask = current & 0xC3

        data = adc_agent_modes[ADC_TRIG2_CFG] << 4 | adc_agent_modes[ADC_TRIG1_CFG] << 2 | keepMask
        self.write_reg(reg = self.regDict[regName], data_out = [data])

    # Double check this function.........
    def configure_io_rtc_count_thr(self, RTC_COUNT_THR = 0xFFFFFFFF):

        update_reg_values(self, self.regDict)

        regName = 'IO_RTC_COUNT_THR_A'
        if self.regs[regName] != (RTC_COUNT_THR & 0x000000FF): #Don't think this is necassary??
            data = (RTC_COUNT_THR & 0x000000FF)
            self.write_reg(reg = self.regDict[regName], data_out = [data])

        regName = 'IO_RTC_COUNT_THR_B'
        if self.regs[regName] != ((RTC_COUNT_THR & 0x0000FF00) >> 2) :
            data = ((RTC_COUNT_THR & 0x0000FF00) >> 2)
            self.write_reg(reg = self.regDict[regName], data_out = [data])

        regName = 'IO_RTC_COUNT_THR_C'
        if self.regs[regName] != ((RTC_COUNT_THR & 0x00FF0000) >> 4) :
            data = ((RTC_COUNT_THR & 0x00FF0000) >> 4)
            self.write_reg(reg = self.regDict[regName], data_out = [data])

        regName = 'IO_RTC_COUNT_THR_D'
        if self.regs[regName] != ((RTC_COUNT_THR & 0xFF000000) >> 6) :
            data = ((RTC_COUNT_THR & 0xFF000000) >> 6)
            self.write_reg(reg = self.regDict[regName], data_out = [data])

    def configure_irq_masks(self, IRQ_BTN3_DBL = 0x0, IRQ_BTN2_DBL = 0x0, IRQ_BTN1_DBL = 0x0, IRQ_BUTTON_1 = 0x0, IRQ_BUTTON_2 = 0x0, IRQ_BUTTON_3 = 0x0,
        IRQ_GPIO8 = 0x0, IRQ_GPIO7 = 0x0, IRQ_GPIO6 = 0x0, IRQ_GPIO5 = 0x0, IRQ_GPIO4 = 0x0, IRQ_GPIO3 = 0x0, IRQ_GPIO2 = 0x0, IRQ_GPIO1 = 0x0, IRQ_GPIO13 = 0x0,
        IRQ_GPIO12 = 0x0, IRQ_GPIO11 = 0x0, IRQ_GPIO10 = 0x0, IRQ_GPIO9 = 0x0):

        regName = 'IO_IRQ_MASK_A'
        data = IRQ_BTN3_DBL << 6 | IRQ_BTN2_DBL << 5 | IRQ_BTN1_DBL << 4 | IRQ_BUTTON_3 << 2 | IRQ_BUTTON_2 << 1 | IRQ_BUTTON_1
        self.write_reg(reg = self.regDict[regName], data_out = [data])

        regName = 'IO_IRQ_MASK_B'
        data = IRQ_GPIO8 << 7 | IRQ_GPIO7 << 6 | IRQ_GPIO6 << 5 | IRQ_GPIO5 << 4 | IRQ_GPIO4 << 3 | IRQ_GPIO3 << 2 | IRQ_GPIO2 << 1 | IRQ_GPIO1
        self.write_reg(reg = self.regDict[regName], data_out = [data])

        regName = 'IO_IRQ_MASK_C'
        data = IRQ_GPIO13 << 4 | IRQ_GPIO12 << 3 | IRQ_GPIO11 << 2 | IRQ_GPIO10 << 1 | IRQ_GPIO9
        self.write_reg(reg = self.regDict[regName], data_out = [data])

    def configure_resetcode_decoder(self, RSTCD_SOURCE_SEL = 0x0, CLR_ON_CHG_REM = 0x0, EN_RSTCD = 0x0, BAUD_RATE = '1200 baud', CLR_HOST_DFU = 0x0):

        baud_modes = {
                    '1200 baud' : 0x00,
                    '300 baud' : 0x01,
                    '100 baud' : 0x02,
                    '25 baud' : 0x03
                }

        regName = 'SYSCTL_RESETCODE_CONF'
        data = RSTCD_SOURCE_SEL << 4 | CLR_ON_CHG_REM << 3 | EN_RSTCD << 2 | baud_modes[BAUD_RATE]
        self.write_reg(reg = self.regDict[regName], data_out = [data])

        regName = 'SYSCTL_RESETCODE_CONF2'
        data = CLR_HOST_DFU
        self.write_reg(reg = self.regDict[regName], data_out = [data])

    def read_resetcode(self):
        regName = 'SYSCTL_RESETCODE'
        return self.read_reg(reg = self.regDict[regName], length = 1)

    # TODO consider integrating dict into BerylFT instead of reading a CSV
    def build_adc_channel_dict(self, csv = 'ADCChannelList.csv'):

        file = open(csv, 'r')
        lines = file.readlines()
        file.close

        ADCDict = {}

        for i, nextline in enumerate(lines):
            linewords = nextline.split(',')
            if linewords:
                if i != 0:
                    ADCDict[int(linewords[0])] = [linewords[2], linewords[3][:-2], linewords[4], linewords[6], linewords[5], linewords[8]]

        return ADCDict
        #for i, j in enumerate(sorted(ADCDict)):
        #   print j, ADCDict[j]

    def build_slot_channel_dict(self, channelList):

        slotChannelDict = {}

        for slots in range(16):
            slotChannelDict[slots] = 254 #disable slots by default

        if len(channelList) <= 16:
            for i, j in enumerate(channelList):
                slotChannelDict[i] = j
        else:
            print "Too many channels to measure"

        return slotChannelDict

    def configure_adc_scan_agent_slots(self, agent_num, slotChannels):
        """
        slotChannels should be a dictionary with keys = slot number and value = ADC channel to measure. dictionary must be complete from slot 0 to 15. write chan 254 to skip the slot!!!
        For more info see registers 0x400F - 0x405A and 0x40CE - 0x40DC
        """

        if agent_num != 1 & agent_num != 2:
            print "agent number out of range"
            sys.exit()

        if agent_num == 1:
            for i, j in enumerate(slotChannels):
                regName = 'GPADC_SCH_1_SLOT%s' %i
                self.write_reg(reg = self.regDict[regName], data_out = [slotChannels[j]])

        else:
            for i, j in enumerate(slotChannels):
                regName = 'GPADC_SCH_2_SLOT%s' %i
                self.write_reg(reg = self.regDict[regName], data_out = [slotChannels[j]])

    def set_adc_slot_properties(self, agent_num, slot_num, DEFAULT_MFIO_KEEP = 0x1, DEFAULT_MFIO_SEL = 0x0, DEFAULT_ISINK_SEL = 0x0, DEFAULT_ISINK_KEEP = 0x01, DEFAULT_DAC = 0, DEFAULT_SETTLE = 0x3F, DEFAULT_PREAMP = 0x0):
        prop0_reg = 'GPADC_SCH_%s_SLOT%s_PROP0' %(agent_num, slot_num)
        prop1_reg = 'GPADC_SCH_%s_SLOT%s_PROP1' %(agent_num, slot_num)
        prop2_reg = 'GPADC_SCH_%s_SLOT%s_PROP2' %(agent_num, slot_num)

        prop0_data = DEFAULT_MFIO_KEEP << 7 | DEFAULT_MFIO_SEL << 3 | DEFAULT_ISINK_SEL
        prop1_data = DEFAULT_ISINK_KEEP << 4 | DEFAULT_DAC
        prop2_data = DEFAULT_SETTLE << 2 | DEFAULT_PREAMP

        if agent_num == 2:
            self.test_mode_enable()

        self.write_reg(reg = self.regDict[prop0_reg], data_out = [prop0_data])
        self.write_reg(reg = self.regDict[prop1_reg], data_out = [prop1_data])
        self.write_reg(reg = self.regDict[prop2_reg], data_out = [prop2_data])

    def configure_adc_scan_agent(self, agent_num, slotChannels = None, T_SCH_DLY = 0x0, T_SCH_ALT = 0x0, AUTO_ACCUMULATORS_EN = 0x0,
        ACQ_CFG = 0x0, TRIG_MODE = 0x0):
        """ For more info see registers 0x4008, 0x4009, 0x40C6, and 0x40C7 """

        if agent_num != 1 & agent_num != 2:
            print "agent number out of range"
            sys.exit()

        regName = 'GPADC_SCH_%s_CGF_1' %agent_num
        data = T_SCH_DLY << 5 | T_SCH_ALT << 4 | AUTO_ACCUMULATORS_EN << 2 | ACQ_CFG
        self.write_reg(reg = self.regDict[regName], data_out = [data])

        regName = 'GPADC_SCH_%s_TRIG' %agent_num
        data = TRIG_MODE
        self.write_reg(reg = self.regDict[regName], data_out = [data])

    def start_adc_conversion(self, agent_type, agent_num, channel = None):
        """ For more info see register 0x4000 and 0x4004 in beryl regmap """

        if ''.join([agent_type, str(agent_num)]) == 'MAN1':
            if channel <= 182:
                self.write_reg(reg = self.regDict['GPADC_MAN_CTRL1'], data_out = [channel])
            else:
                print "channel out of range"

        elif ''.join([agent_type, str(agent_num)]) == 'MAN2':
            if channel <= 182:
                self.write_reg(reg = self.regDict['GPADC_MAN_CTRL2'], data_out = [channel])
            else:
                print "channel out of range"

        elif ''.join([agent_type, str(agent_num)]) == 'SCAN1':
            self.configure_adc_scan_agent(agent_num = 1, ACQ_CFG = 0x2, TRIG_MODE = 0x1)

        elif ''.join([agent_type, str(agent_num)]) == 'SCAN2':
            self.configure_adc_scan_agent(agent_num = 2, ACQ_CFG = 0x2, TRIG_MODE = 0x1)

        else:
            print "invalid ADC agent"

    def scan_adc_read(self, agent_num, adc_dict_in, slotChannels, suppress_print = False, returnedChannels = range(16), raw_result = False):
        """
        slotChannels is a dictionary.
        For more info see registers 0x4060 - 0x407F and 0x40DE - 0x40FD in beryl regmap
        """
        results = {}

        #make sure result is valid and conversion isn't pending
        if returnedChannels != range(16):
            for i, slot_num in enumerate(slotChannels):
                if i in returnedChannels:
                    if slotChannels[slot_num] != 254:
                        regLSB = 'GPADC_SCH_%s_SLOT%s_RES_LSB' %(agent_num, slot_num)
                        regMSB = 'GPADC_SCH_%s_SLOT%s_RES_MSB' %(agent_num, slot_num)

                        lsbdata = self.read_reg(reg = self.regDict[regLSB], length = 1)
                        invalid = lsbdata & 0x80
                        invalidRegStr = "Register: %s; Value: %s" % (regLSB, hex(lsbdata))

                        if invalid == 0:
                            #check for overFloGama,WizardofAllThingsSolder
                            overflow = lsbdata & 0x40

                            if overflow == 0:
                                resultLSB = self.read_reg(reg = self.regDict[regLSB], length = 1) & 0x0F
                                resultMSB = self.read_reg(reg = self.regDict[regMSB], length = 1)
                                # print "read %s from register %s" % (hex(self.read_reg(reg = self.regDict[regLSB], length = 1)), hex(self.regDict[regLSB]))
                                # print "read %s from register %s" % (hex(self.read_reg(reg = self.regDict[regMSB], length = 1)), hex(self.regDict[regMSB]))


                                rawResult = (resultMSB << 4) | resultLSB

                                # Check if the channel is susceptible to the ADC inversion issue, and correct it if applicable
                                # Check chip version
                                # if self.read_reg(reg=0x0000) == 0x00:
                                if berylVersion == "A0":
                                    # Check if channel is 5V single-ended
                                    if adc_dict_in[slotChannels[slot_num]][4] == "5":
                                        # Check if channel is differential
                                        if "Differential" not in adc_dict_in[slotChannels[slot_num]][5]:
                                            rawResult = 4095 - rawResult
                                    # ILDOx is affected too:
                                    elif "ILDO" in adc_ict_in[slotChannels[slot_num]][0]:
                                        rawResult = 4095 - rawResult
                                    # ICHG is also affected:
                                    elif "ICHG" in adc_dict_in[slotChannels[slot_num]][0]:
                                        rawResult = 4095 - rawResult

                                result = rawResult * float(adc_dict_in[slotChannels[slot_num]][1]) * 1E-3 + float(adc_dict_in[slotChannels[slot_num]][2])
                                results[slot_num] = result

                                if not suppress_print:
                                    print "Result for " + str(adc_dict_in[slotChannels[slot_num]][0]) + " is " + "{:02.2f}".format(result) + str(adc_dict_in[slotChannels[slot_num]][3])

                            else:
                                overflowInfo = (self.read_reg(reg = self.regDict[regLSB], length = 1)) | 0x30
                                if overflowInfo == 0:
                                    print 'Overflow is positive - result larger than 12 bit.'
                                elif overflowInfo == 1:
                                    print 'Overflow is positive - result larger than 13 bit.'
                                elif overflowInfo == 2:
                                    print 'Overflow is negative - result larger than 12 bit.'
                                elif overflowInfo == 3:
                                    print 'Overflow is negative - result larger than 12 bit.'

                        else:
                            print "result is invalid!!!"
                            print invalidRegStr
                        # print self.read_reg(reg = 0x4080)

        else:

            startReg = 'GPADC_SCH_%s_SLOT%s_RES_LSB' %(agent_num, 0)
            stopReg  = 'GPADC_SCH_%s_SLOT%s_RES_MSB' %(agent_num, 15)
            dumpData = self.dump_reg(self.regDict[startReg], self.regDict[stopReg])

            for i, slot_num in enumerate(slotChannels):
                if slotChannels[slot_num] != 254:
                    # regLSB = 'GPADC_SCH_%s_SLOT%s_RES_LSB' %(agent_num, slot_num)
                    # regMSB = 'GPADC_SCH_%s_SLOT%s_RES_MSB' %(agent_num, slot_num)

                    lsbdata = dumpData[2*slot_num]
                    invalid = lsbdata & 0x80
                    invalidRegStr = "Register Slot: %d; Value: %s" % (slot_num, hex(lsbdata))

                    if invalid == 0:
                        #check for overFloGama,WizardofAllThingsSolder
                        overflow = lsbdata & 0x40

                        if overflow == 0:
                            # resultLSB = self.read_reg(reg = self.regDict[regLSB], length = 1) & 0x0F
                            # resultMSB = self.read_reg(reg = self.regDict[regMSB], length = 1)
                            resultLSB = dumpData[2*slot_num] & 0x0F
                            resultMSB = dumpData[2*slot_num + 1]
                            # print "read %s from register %s" % (hex(self.read_reg(reg = self.regDict[regLSB], length = 1)), hex(self.regDict[regLSB]))
                            # print "read %s from register %s" % (hex(self.read_reg(reg = self.regDict[regMSB], length = 1)), hex(self.regDict[regMSB]))


                            rawResult = (resultMSB << 4) | resultLSB

                            # Check if the channel is susceptible to the ADC inversion issue, and correct it if applicable
                            # Check chip version
                            # if self.read_reg(reg=0x0000) == 0x00:
                            if berylVersion == "A0":
                                # Check if channel is 5V single-ended
                                if adc_dict_in[slotChannels[slot_num]][4] == "5":
                                    # Check if channel is differential
                                    if "Differential" not in adc_dict_in[slotChannels[slot_num]][5]:
                                        rawResult = 4095 - rawResult
                                # ILDOx is affected too:
                                elif "ILDO" in adc_ict_in[slotChannels[slot_num]][0]:
                                    rawResult = 4095 - rawResult
                                # ICHG is also affected:
                                elif "ICHG" in adc_dict_in[slotChannels[slot_num]][0]:
                                    rawResult = 4095 - rawResult

                            result = rawResult * float(adc_dict_in[slotChannels[slot_num]][1]) * 1E-3 + float(adc_dict_in[slotChannels[slot_num]][2])
                            if raw_result == True:
                                results[slot_num] = rawResult
                            else:
                                results[slot_num] = result

                            if not suppress_print:
                                print "Result for " + str(adc_dict_in[slotChannels[slot_num]][0]) + " is " + "{:02.2f}".format(result) + str(adc_dict_in[slotChannels[slot_num]][3])

                        else:
                            overflowInfo = (self.read_reg(reg = self.regDict[regLSB], length = 1)) | 0x30
                            if overflowInfo == 0:
                                print 'Overflow is positive - result larger than 12 bit.'
                            elif overflowInfo == 1:
                                print 'Overflow is positive - result larger than 13 bit.'
                            elif overflowInfo == 2:
                                print 'Overflow is negative - result larger than 12 bit.'
                            elif overflowInfo == 3:
                                print 'Overflow is negative - result larger than 12 bit.'

                    else:
                        print "result is invalid!!!"
                        print invalidRegStr
                    # print self.read_reg(reg = 0x4080)



        self.write_reg(reg = self.regDict['GPADC_SCH%s_COMP' % agent_num], data_out = [0x01])
        return results


    def man_adc_read(self, agent_num, dict_in, channel, suppress_print = False, raw_result = False):
        """ For more info see registers 0x4001, 0x4002, 0x4005, 0x4006 in beryl regmap """

        #make sure result is valid and conversion isn't pending
        regLSB = 'GPADC_MAN%s_RES_LSB' %agent_num
        regMSB = 'GPADC_MAN%s_RES_MSB' %agent_num
        regLSBresult = self.read_reg(reg = self.regDict[regLSB], length = 1)
        invalid = regLSBresult & 0x80

        if invalid == 0:
            #check for overFloGama,WizardofAllThingsSolder
            overflow = regLSBresult & 0x40

            if overflow == 0:
                resultLSB = regLSBresult & 0x0F
                resultMSB = self.read_reg(reg = self.regDict[regMSB], length = 1)
                # print "MSB: %s" % hex(resultMSB)
                # print "LSB: %s" % hex(resultLSB)

                rawResult = (resultMSB << 4) | resultLSB

                # Check if the channel is susceptible to the ADC inversion issue, and correct it if applicable
                # Check chip version
                # if self.read_reg(reg=0x0000) == 0x00:
                if berylVersion == "A0":
                    # Check if channel is 5V single-ended
                    if dict_in[channel][4] == "5":
                        # Check if channel is differential
                        if "Differential" not in dict_in[channel][5]:
                            rawResult = 4095 - rawResult
                    # ILDOx is affected too:
                    elif "ILDO" in dict_in[channel][0]:
                        rawResult = 4095 - rawResult
                    # ICHG is also affected:
                    elif "ICHG" in dict_in[channel][0]:
                        rawResult = 4095 - rawResult

                if raw_result == False:
                    result = rawResult * float(dict_in[channel][1]) * 1E-3 + float(dict_in[channel][2])
                else:
                    result = rawResult

                if not suppress_print:
                    print "Result for " + str(dict_in[channel][0]) + " is " + "{:02.2f}".format(result) + str(dict_in[channel][3])
                return result

            else:
                overflowInfo = (self.read_reg(reg = self.regDict[regLSB], length = 1)) | 0x30
                if overflowInfo == 0:
                    print 'Overflow is positive - result larger than 12 bit.'
                elif overflowInfo == 1:
                    print 'Overflow is positive - result larger than 13 bit.'
                elif overflowInfo == 2:
                    print 'Overflow is negative - result larger than 12 bit.'
                elif overflowInfo == 3:
                    print 'Overflow is negative - result larger than 12 bit.'

        else:
            print "result is invalid!!!"

    def configure_ccadc(self, TRIGGER_TYPE = 0x1, HOSTOFF_GLOBAL_EN = 0x0, ACCUM_EN = 0x1, IN_FIFO_EN = 0x1, GLOBAL_EN = 0x0,
        INVERT_HOST_CLK_EN = 0x0, CLEAR_ACCUM_CNTR = 0x0, CLEAR_SAMPLE_CNTR = 0x0, PREAMP_GAIN = 0x0):
        """ For more info see registers 0x4800, 0x4801, and 0x4804 - 0x4807 """

        regName = 'CCADC_ENABLE_CCADC'
        data = TRIGGER_TYPE << 7 | HOSTOFF_GLOBAL_EN << 3 | ACCUM_EN << 2 | IN_FIFO_EN << 1 | GLOBAL_EN
        self.write_reg(reg = self.regDict[regName], data_out = [data])

        regName = 'CCADC_CCADC_CONFIG'
        data = INVERT_HOST_CLK_EN << 2 | CLEAR_ACCUM_CNTR << 1 | CLEAR_SAMPLE_CNTR
        self.write_reg(reg = self.regDict[regName], data_out = [data])

        regName = 'CCADC_PREAMP_GAIN'
        data = PREAMP_GAIN
        self.write_reg(reg = self.regDict[regName], data_out = [data])

    def read_ccadc(self):
        regName = 'CCADC_CHARGE_ACCUM_0'
        result0 = self.read_reg(reg = self.regDict[regName], length = 1)

        regName = 'CCADC_CHARGE_ACCUM_1'
        result1 = self.read_reg(reg = self.regDict[regName], length = 1)

        regName = 'CCADC_CHARGE_ACCUM_2'
        result2 = self.read_reg(reg = self.regDict[regName], length = 1)

        regName = 'CCADC_CHARGE_ACCUM_3'
        result3 = self.read_reg(reg = self.regDict[regName], length = 1)

        rawResult = (result3 << 24) | (result2 << 16) | (result1 << 8) | result0

        shunt = .2 #based on Prosperity Daughtercard
        A0 = 455.11 #Based on Beryl datasheet Table 41

        result = rawResult/(A0 * shunt * 3600)

        print "SoC = " + "{:02.2f}".format(result) +  "mAh"
        return result

    def read_event(self, all = True, event_name = None):

        self.test_mode_enable()

        eventRegList = [
            'MFSM_EVENT_POWER_STATE',
            'MFSM_EVENT_ERROR',
            'SYSCTL_EVENT',
            'SYSCTL_EVENT_BUCK',
            'VMAX_EVENT',
            'IO_EVENT_A',
            'IO_EVENT_B',
            'IO_EVENT_C',
            'CHGCTL_EVENT1',
            'PWR_LDO_EVENT1',
            'GPADC_EVENT_EOC',
            'GPADC_EVENT_ERROR',
            'GPADC_EVENT_SCAN1_ERROR',
            'GPADC_EVENT_SCAN2_ERROR',
            'GPADC_EVENT_SLOT_ERROR',
            'GPADC_EVENT_TDEV0',
            'GPADC_EVENT_TDEV1',
            'GPADC_EVENT_TDIE0',
            'GPADC_EVENT_TDIE1',
            'GPADC_EVENT_FIFO1',
            'GPADC_EVENT_FIFO2',
            'GPADC_EVENT_FIFO_WARNING',
            'CCADC_EVENT',

            'OTP_EVENT'
        ]

        if all == True:
            for i, j in enumerate(eventRegList):
                print j + ": "+ str(self.read_reg(reg = self.regDict[j], length = 1))

        else:
            if event_name in eventRegList:
                print event_name + ": "+ str(self.read_reg(reg = self.regDict[event_name], length = 1))
            else:
                print "Event name invalid."

    def write_event(self, value, all = True, event_name = None):

        self.test_mode_enable()

        eventRegList = [
            'MFSM_EVENT_POWER_STATE',
            'MFSM_EVENT_ERROR',
            'SYSCTL_EVENT',
            'SYSCTL_EVENT_BUCK',
            'VMAX_EVENT',
            'IO_EVENT_A',
            'IO_EVENT_B',
            'IO_EVENT_C',
            'CHGCTL_EVENT1',
            'PWR_LDO_EVENT1',
            'GPADC_EVENT_EOC',
            'GPADC_EVENT_ERROR',
            'GPADC_EVENT_SCAN1_ERROR',
            'GPADC_EVENT_SCAN2_ERROR',
            'GPADC_EVENT_SLOT_ERROR',
            'GPADC_EVENT_TDEV0',
            'GPADC_EVENT_TDEV1',
            'GPADC_EVENT_TDIE0',
            'GPADC_EVENT_TDIE1',
            'GPADC_EVENT_FIFO1',
            'GPADC_EVENT_FIFO2',
            'GPADC_EVENT_FIFO_WARNING',
            'CCADC_EVENT',
            'SPMISLV_EVENT_A',
            'SPMISLV_EVENT_B',
            'OTP_EVENT'
        ]

        if all == True:
            for i, j in enumerate(eventRegList):
                self.write_reg(reg = self.regDict[j], data_out = [value])
                #print j + ": "+ str(self.read_reg(reg = self.regDict[j], length = 1))
            print "All events written to {}".format(str(value))

        else:
            if event_name in eventRegList:
                self.write_reg(reg = self.regDict[event_name], data_out = [value])
                print event_name + ": "+ str(self.read_reg(reg = self.regDict[event_name], length = 1))
            else:
                print "Event name invalid."

        self.test_mode_disable()

    def configure_tdev(self, settle_time, current):
        regName = 'GPADC_FSM_TRIM2'
        val_time = (settle_time)/8
        curr = ((current -25) / 25)
        data = val_time << 3 | curr
        self.write_reg(reg = self.regDict[regName], data_out = [data])

    def enable_tdev(self, data):
        # data = 1 << (num-1)
        regName = 'GPADC_TDEV_CTRL1'
        self.write_reg(reg = self.regDict[regName], data_out = [data])

    def set_tdev_to_amux(self, amux, source = False):
        regName = 'GPADC_FSM_TRIM12'

        data = (1 << amux)
        if source == True:
            toSend = self.regs[regName] & ~(data)

        elif source == False:
            toSend = self.regs[regName] | (data)

        self.write_reg(reg = self.regDict[regName], data_out = [toSend])


if __name__ == "__main__":
    print
