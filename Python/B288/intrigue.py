import serial
import serial.tools.list_ports
import uart
import time
import sys
import serial
import beryl_resetcode as rst
import Beryl as brl
import os
import numpy
import yc.misc as misc

capture=1
filepath = 'yc/results/'

class Intrigue(object):
    def __init__(self, hwh = None):
        global output
        #initialize beryl
        self.beryl = brl.Beryl(force_chan = 'spmi',hwh = hwh)
        output=misc.output
    
    def laserSafetyTest(self):
        # Measures how long VCSEL1 stays on if ISINK and VCSEL_LDO_EN are both stuck "on"
        # VCSEL1 is considered "on" if V_do of ISINK is > 50mV

        VCSEL_EN = 11
        adc_dict = self.beryl.build_adc_channel_dict()

        while True:
            self.beryl.enable_isink_global(FAST_EN = 0x0)
            self.beryl.enable_isink(isink_num = 2, PWM_MODE = 'CC', FAST_EN = 0x0, TRIG_SEL = 'SW')
            self.beryl.enable_isink(isink_num = 1, PWM_MODE = 'CC', FAST_EN = 0x0, TRIG_SEL = 'SW')
            self.beryl.configure_io_mfio_conf(MFIO_num = VCSEL_EN, IOCELL_CFG =  'PUSH_PULL', SUPPLY = 'VDD_1V8')
            self.beryl.configure_io_gpio_conf(GPIO_num = VCSEL_EN, IO_CONFIG = 0x1, DEB = '0ms', WAKE_LVL = 1)
            startTime = time.time()
            self.beryl.trigger_isink(isink_num = 1)
            V_do = 1
            while V_do > 0.05:
                self.beryl.start_adc_conversion('MAN', 1, 40)
                V_do = self.beryl.man_adc_read(1, adc_dict, 40, suppress_print = True)
                elapsedTime = time.time() - startTime

            self.beryl.disable_isink(isink_num = 1)
            self.beryl.configure_io_gpio_conf(GPIO_num = VCSEL_EN, IO_CONFIG = 0x1, DEB = '0ms', WAKE_LVL = 0)
            time.sleep(0.1)
            return elapsedTime


    def TIA_Test(self):

        """ 
        HOW TO USE:

        1) Shunt MFIO12 to 1V8 to enable TIAs indefinetly
        2) Make sure TIA EN jumpers are stuffed
        3) run script and probe correct TIA!

        """
        self.beryl.test_mode_enable()
        self.beryl.toggle_supply(SUPPLY = 'LDO2', MODE = 'ACT0', ON = True)
        #beryl.toggle_supply(SUPPLY = 'LDO2', MODE = 'ACT0', ON = True)
        self.beryl.disable_isink_global(FAST_EN = 0x0)
        self.beryl.enable_isink_global(FAST_EN = 0x0)

        self.beryl.disable_isink(isink_num = 1)
        self.beryl.enable_isink(isink_num = 1, PWM_MODE = 'CC', FAST_EN = 0x0, TRIG_SEL = 'SW')
        self.beryl.set_isink_current(isink_num = 1, current = 3300)
        #self.beryl.config_ISINK_PWM(isink_num = 3, period  = 25000, on_time = 400) #1Hz

        #self.beryl.configure_io_mfio_conf(MFIO_NUM = 1, FUNC = 'ISINK3_PWM', IOCELL_CFG =  "PUSH_PULL", SUPPLY = 'VDD_1V8')
        self.beryl.configure_io_mfio_conf(MFIO_NUM = 11, FUNC = 'RTC_1HZ', IOCELL_CFG =  "PUSH_PULL", SUPPLY = 'VDD_1V8')
        self.beryl.trigger_isink(isink_num = 1)

    def intrigue_ied(self, loop = True, suppress_print = False, num_samples = 0):
        #beryl = brl.Beryl(update = False, standalone = False, spmi_in = True, verbose_in = False)

        #set isinks to be GPADC triggered and pulse mode
        # self.beryl.test_mode_enable()
        #turn on 1V75 rail
        self.beryl.toggle_supply(SUPPLY = 'LDO2', MODE = 'ACT0', ON = True)

        #this makes sure currentsinks function correctly, probably don't need
        self.beryl.disable_isink_global(FAST_EN = 0x0)
        self.beryl.enable_isink_global(FAST_EN = 0x0)

        # self.beryl.disable_isink(isink_num = 2)
        # self.beryl.disable_isink(isink_num = 1)

        #set to desired current
        # self.beryl.set_isink_current(isink_num = 2, current = 3300)
        # self.beryl.set_isink_current(isink_num = 1, current = 3300)

        #set iSink trigger as GPADC
        self.beryl.enable_isink(isink_num = 2, PWM_MODE = 'CC', FAST_EN = 0x0, TRIG_SEL = 'GPADC')
        self.beryl.enable_isink(isink_num = 1, PWM_MODE = 'CC', FAST_EN = 0x0, TRIG_SEL = 'GPADC')

        #beryl.enable_isink(isink_num = 2, PWM_MODE = 'Pulse', FAST_EN = 0x0, TRIG_SEL = 'GPADC')

        #beryl.config_ISINK_PWM(isink_num = 1, period = 500, on_time =  25000)
        #beryl.config_ISINK_PWM(isink_num = 2, period = 500, on_time =  25000)

        #beryl.set_isink_current(isink_num = 2, current = 3300)

        measurement = [
            "TIA_VREF",
            "PD1_Vr",
            "PD_VF_LOW",
            "TIA1_DARK",
            "TIA1_LIGHT",
            "VSINK1_ON",
            "VSINK1_OFF",
            "PD2_Vr",
            "ignore",
            "TIA2_DARK",
            "TIA2_LIGHT",
            "VSINK2_ON",
            "VSINK2_OFF",
            "PD1_TEMP",
            "PD2_TEMP",
            "PD_VF_HIGH"
        ]
        
        #set MFIOs to be GPADC triggered
        VCSEL_EN = 11
        TIA_EN = 12
        PD_VF_BIAS = 13

        # Upon initial startup, the PD AC coupling cap needs to bias.
        # Enable the TIAs for an extended period of time to do this.  
        self.beryl.configure_io_mfio_conf(MFIO_num = TIA_EN, IOCELL_CFG = 'PUSH_PULL', SUPPLY = 'VDD_1V8')
        self.beryl.configure_io_gpio_conf(GPIO_num = TIA_EN, IO_CONFIG = 0x1, DEB = '0ms', WAKE_LVL = 1)
        time.sleep(1)
        self.beryl.configure_io_gpio_conf(GPIO_num = TIA_EN, IO_CONFIG = 0x1, DEB = '0ms', WAKE_LVL = 0)

        self.beryl.configure_io_mfio_conf(MFIO_num = VCSEL_EN, FUNC = 'ADCSEQ1', IOCELL_CFG =  'PUSH_PULL', POLARITY = 0x0, SUPPLY = 'VDD_1V8')
        self.beryl.configure_io_mfio_conf(MFIO_num = TIA_EN, FUNC = 'ADCSEQ2', IOCELL_CFG =  'PUSH_PULL', POLARITY = 0x0, SUPPLY = 'VDD_1V8')
        #for IED, we are setting this pin low always, you can choose to make this ADCSEQ3 and just never trigger it
        self.beryl.configure_io_mfio_conf(MFIO_num = PD_VF_BIAS, FUNC = 'ADCSEQ3', IOCELL_CFG =  'PUSH_PULL', POLARITY = 0x0, SUPPLY = 'VDDIOA')
        # self.beryl.configure_io_mfio_conf(MFIO_num = PD_VF_BIAS,  IOCELL_CFG =  'PUSH_PULL', SUPPLY = 'VDDIOA')
        # self.beryl.configure_io_gpio_conf(GPIO_num = PD_VF_BIAS, IO_CONFIG = 0x1, DEB = '0ms', WAKE_LVL = 0)


        self.beryl.configure_tdev(settle_time = 240, current = 200)
        self.beryl.enable_tdev(data = 0x03)
        # self.beryl.set_tdev_to_amux(amux = 6, source = False)
        self.beryl.write_reg(reg = 0x4171, data_out = [0xC0])
        #specific channels for OPTICAL SENSING ARCH, this might need re-confirmation
        SCAN1SlotDict = self.beryl.build_slot_channel_dict(channelList = [
            91, 
            159, 
            90, 
            175, 
            175,
            40, 
            40, 
            160, 
            155, 
            176, 
            176, 
            41, 
            41, 
            66, 
            67, 
            90])

        ADCDictionary = self.beryl.build_adc_channel_dict(csv = 'ADCChannelList.csv')
        self.beryl.configure_adc_scan_agent_slots(agent_num = 1, slotChannels = SCAN1SlotDict)

        #config each slot ()
        # first assert LDO_EN, TIA_EN, PD_VF_BIAS


        # TODO: Change to 1.5V scale

        self.beryl.set_adc_slot_properties(agent_num = 1, slot_num = 0, DEFAULT_MFIO_KEEP =  1, DEFAULT_MFIO_SEL = 3, DEFAULT_ISINK_SEL = 0x00, DEFAULT_ISINK_KEEP = 0X00, DEFAULT_DAC = 0, DEFAULT_SETTLE = 0x19, DEFAULT_PREAMP = 0x00)
        # measurement only, PD0-PD_N
        self.beryl.set_adc_slot_properties(agent_num = 1, slot_num = 1, DEFAULT_MFIO_KEEP =  1, DEFAULT_MFIO_SEL = 0, DEFAULT_ISINK_SEL = 0x00, DEFAULT_ISINK_KEEP = 0X00, DEFAULT_DAC = 0, DEFAULT_SETTLE = 0x19, DEFAULT_PREAMP = 0x00)
        # measurement only, PD_P - PD_N
        self.beryl.set_adc_slot_properties(agent_num = 1, slot_num = 2, DEFAULT_MFIO_KEEP =  1, DEFAULT_MFIO_SEL = 0, DEFAULT_ISINK_SEL = 0x00, DEFAULT_ISINK_KEEP = 0X00, DEFAULT_DAC = 0, DEFAULT_SETTLE = 0x19, DEFAULT_PREAMP = 0x00)
        # measurement only, TIA_OUT0 - TIA_VREF
        self.beryl.set_adc_slot_properties(agent_num = 1, slot_num = 3, DEFAULT_MFIO_KEEP =  1, DEFAULT_MFIO_SEL = 0, DEFAULT_ISINK_SEL = 0x00, DEFAULT_ISINK_KEEP = 0X00, DEFAULT_DAC = 0, DEFAULT_SETTLE = 0x19, DEFAULT_PREAMP = 0x00)
        # enable current sink 0, measure TIA0, leave current sink on
        self.beryl.set_adc_slot_properties(agent_num = 1, slot_num = 4, DEFAULT_MFIO_KEEP =  1, DEFAULT_MFIO_SEL = 0, DEFAULT_ISINK_SEL = 0x01, DEFAULT_ISINK_KEEP = 0X01, DEFAULT_DAC = 0, DEFAULT_SETTLE = 0x19, DEFAULT_PREAMP = 0x00)
        # measurement only, V_ISINK0
        self.beryl.set_adc_slot_properties(agent_num = 1, slot_num = 5, DEFAULT_MFIO_KEEP =  1, DEFAULT_MFIO_SEL = 0, DEFAULT_ISINK_SEL = 0x00, DEFAULT_ISINK_KEEP = 0X01, DEFAULT_DAC = 0, DEFAULT_SETTLE = 0x19, DEFAULT_PREAMP = 0x00)
        # measure PD_P, turn off ISINK0
        self.beryl.set_adc_slot_properties(agent_num = 1, slot_num = 6, DEFAULT_MFIO_KEEP =  1, DEFAULT_MFIO_SEL = 0, DEFAULT_ISINK_SEL = 0x00, DEFAULT_ISINK_KEEP = 0x00, DEFAULT_DAC = 0, DEFAULT_SETTLE = 0x19, DEFAULT_PREAMP = 0x00)
        # measurement only, PD1 - PD_N
        self.beryl.set_adc_slot_properties(agent_num = 1, slot_num = 7, DEFAULT_MFIO_KEEP =  1, DEFAULT_MFIO_SEL = 0, DEFAULT_ISINK_SEL = 0x00, DEFAULT_ISINK_KEEP = 0X00, DEFAULT_DAC = 0, DEFAULT_SETTLE = 0x19, DEFAULT_PREAMP = 0x00)
        # measurement only, PD_P - PD_N
        self.beryl.set_adc_slot_properties(agent_num = 1, slot_num = 8, DEFAULT_MFIO_KEEP =  1, DEFAULT_MFIO_SEL = 0, DEFAULT_ISINK_SEL = 0x00, DEFAULT_ISINK_KEEP = 0X00, DEFAULT_DAC = 0, DEFAULT_SETTLE = 0x19, DEFAULT_PREAMP = 0x00)
        # measurement only, TIA_OUT1 - TIA_VREF
        self.beryl.set_adc_slot_properties(agent_num = 1, slot_num = 9, DEFAULT_MFIO_KEEP =  1, DEFAULT_MFIO_SEL = 0, DEFAULT_ISINK_SEL = 0x00, DEFAULT_ISINK_KEEP = 0X00, DEFAULT_DAC = 0, DEFAULT_SETTLE = 0x19, DEFAULT_PREAMP = 0x00)
        # enable current sink 1, measure TIA_OUT1
        self.beryl.set_adc_slot_properties(agent_num = 1, slot_num = 10, DEFAULT_MFIO_KEEP = 1, DEFAULT_MFIO_SEL = 0, DEFAULT_ISINK_SEL = 0x02, DEFAULT_ISINK_KEEP = 0X01, DEFAULT_DAC = 0, DEFAULT_SETTLE = 0x19, DEFAULT_PREAMP = 0x00)
        # measurement only, V_ISINK1
        self.beryl.set_adc_slot_properties(agent_num = 1, slot_num = 11, DEFAULT_MFIO_KEEP = 1, DEFAULT_MFIO_SEL = 0, DEFAULT_ISINK_SEL = 0x00, DEFAULT_ISINK_KEEP = 0X01, DEFAULT_DAC = 0, DEFAULT_SETTLE = 0x19, DEFAULT_PREAMP = 0x00)
        # measure PD_P, turn off ISINK1
        self.beryl.set_adc_slot_properties(agent_num = 1, slot_num = 12, DEFAULT_MFIO_KEEP = 0, DEFAULT_MFIO_SEL = 0, DEFAULT_ISINK_SEL = 0x00, DEFAULT_ISINK_KEEP = 0x00, DEFAULT_DAC = 0, DEFAULT_SETTLE = 0x19, DEFAULT_PREAMP = 0x00)
        # de-assert TIA_EN, PD_VF_BIAS, LDO_EN (THIS IS DONE IN THE PREVIOUS SECTION TO MAKE SURE ITS DESSARTED DURING THIS MEASUREMENT), measure PD0
        self.beryl.set_adc_slot_properties(agent_num = 1, slot_num = 13, DEFAULT_MFIO_KEEP = 1, DEFAULT_MFIO_SEL = 4, DEFAULT_ISINK_SEL = 0x00, DEFAULT_ISINK_KEEP = 0X00, DEFAULT_DAC = 0, DEFAULT_SETTLE = 0x19, DEFAULT_PREAMP = 0x00)
        #measure PD1
        self.beryl.set_adc_slot_properties(agent_num = 1, slot_num = 14, DEFAULT_MFIO_KEEP = 1, DEFAULT_MFIO_SEL = 0, DEFAULT_ISINK_SEL = 0x00, DEFAULT_ISINK_KEEP = 0X00, DEFAULT_DAC = 0, DEFAULT_SETTLE = 0x19, DEFAULT_PREAMP = 0x00)
        #assert PD_BIASN, measure PD_BIASN
        self.beryl.set_adc_slot_properties(agent_num = 1, slot_num = 15, DEFAULT_MFIO_KEEP = 0, DEFAULT_MFIO_SEL = 4, DEFAULT_ISINK_SEL = 0x00, DEFAULT_ISINK_KEEP = 0X00, DEFAULT_DAC = 0, DEFAULT_SETTLE = 0x19, DEFAULT_PREAMP = 0x00)

        #after setting the slot properties, do infinite scans
        firstMeasurement = False

        # if num_samples == 0, then take measurements forever
        if num_samples == 0:
            j = -1
            cumResults = numpy.zeros((1, 16))

        else:
            j = 0
            cumResults = numpy.zeros((num_samples, 16))
        while j < num_samples:
            results = {}
            self.beryl.start_adc_conversion(agent_type = 'SCAN', agent_num = 1, channel = 1)
            time.sleep(0.01)

            if firstMeasurement:
                firstMeasurement = False
            else:
                results = (self.beryl.scan_adc_read(agent_num = 1, adc_dict_in = ADCDictionary, slotChannels = SCAN1SlotDict, suppress_print = True))
                if not suppress_print:
                    print "Sample %d" % j
                    for i in range (16):
                        print "%s - %s: %s : %f " % (str(i).ljust(2), ADCDictionary[SCAN1SlotDict[i]][0].rjust(20), measurement[i].ljust(11) , results[i])
                    print "\n"
                
                for i in range(16):
                    cumResults[max(j, 0), i] = results[i]



            if num_samples != 0:
                j += 1

        if not suppress_print:
            print "AVERAGES:"
            for i in range (16):
                print "%s - %s: %s : %f " % (str(i).ljust(2), ADCDictionary[SCAN1SlotDict[i]][0].rjust(20), measurement[i].ljust(11) , numpy.mean(cumResults[:, i]))
            print "\n"

        results = {}
        for i in range(16):
            results[measurement[i]] = numpy.mean(cumResults[:, i])
        
        return results


    def GPADC_man(self, channel = 5, num_samples = 50, average_samples = 1):
        f = output('adc_man.csv',False,True,filepath)
        """ THIS IS AN EXAMPLE OF HOW TO DO A MANUAL SCAN"""
        chan = channel
        PD_VF_BIAS = 13
        #self.beryl.configure_adc_scan_agent_slots(agent_num = 1, slotChannels = SCAN1SlotDict)
        #self.beryl.configure_io_mfio_conf(MFIO_num= PD_VF_BIAS, FUNC = 'RTC_1HZ', IOCELL_CFG =  'PUSH_PULL', POLARITY = 0x0, SUPPLY = 'VDD_MAIN')

        ADCDictionary = self.beryl.build_adc_channel_dict(csv = 'ADCChannelList.csv')

        if num_samples == 0:
            j = -1
        else:
            j = 0

        while j < num_samples:
            #self.beryl.start_adc_conversion(agent_type = 'MAN', agent_num = 1, channel = chan)
            temp = []
            for i in range(average_samples):
                self.beryl.start_adc_conversion('MAN', 1, chan)
                temp.append(self.beryl.man_adc_read(1, ADCDictionary, chan, suppress_print = True))
            temp_avg = numpy.mean(temp)
            print "Data: %.3f" % temp_avg
            if(capture):
                f.csv_write([temp_avg])
            time.sleep(0.05)
            if num_samples != 0:
                j += 1
        f.close()

    def intrigue_direct_channels(self, loop = True, suppress_print = False, num_samples = 0):
        measurement = [
            "VBUCK0",
            "VBUCK1",
            "VLDO1",
            "VCHG",
            "VBUCK0",
            "VBUCK1",
            "VLDO1",
            "VCHG",
            "VBUCK0",
            "VBUCK1",
            "VLDO1",
            "VCHG",
            "VBUCK0",
            "VBUCK1",
            "VLDO1",
            "VCHG"
        ]
        

        SCAN1SlotDict = self.beryl.build_slot_channel_dict(channelList = [
            10, 
            11, 
            21, 
            1, 
            10,
            11, 
            21, 
            1, 
            10, 
            11, 
            21, 
            1, 
            10, 
            11, 
            21, 
            1])

        ADCDictionary = self.beryl.build_adc_channel_dict(csv = 'ADCChannelList.csv')
        self.beryl.configure_adc_scan_agent_slots(agent_num = 1, slotChannels = SCAN1SlotDict)

        self.beryl.set_adc_slot_properties(agent_num = 1, slot_num = 0, DEFAULT_MFIO_KEEP =  1, DEFAULT_MFIO_SEL = 0, DEFAULT_ISINK_SEL = 0x00, DEFAULT_ISINK_KEEP = 0X00, DEFAULT_DAC = 0, DEFAULT_SETTLE = 0x19, DEFAULT_PREAMP = 0x00)
        self.beryl.set_adc_slot_properties(agent_num = 1, slot_num = 1, DEFAULT_MFIO_KEEP =  1, DEFAULT_MFIO_SEL = 0, DEFAULT_ISINK_SEL = 0x00, DEFAULT_ISINK_KEEP = 0X00, DEFAULT_DAC = 0, DEFAULT_SETTLE = 0x19, DEFAULT_PREAMP = 0x00)
        self.beryl.set_adc_slot_properties(agent_num = 1, slot_num = 2, DEFAULT_MFIO_KEEP =  1, DEFAULT_MFIO_SEL = 0, DEFAULT_ISINK_SEL = 0x00, DEFAULT_ISINK_KEEP = 0X00, DEFAULT_DAC = 0, DEFAULT_SETTLE = 0x19, DEFAULT_PREAMP = 0x00)
        self.beryl.set_adc_slot_properties(agent_num = 1, slot_num = 3, DEFAULT_MFIO_KEEP =  1, DEFAULT_MFIO_SEL = 0, DEFAULT_ISINK_SEL = 0x00, DEFAULT_ISINK_KEEP = 0X00, DEFAULT_DAC = 0, DEFAULT_SETTLE = 0x19, DEFAULT_PREAMP = 0x00)
        self.beryl.set_adc_slot_properties(agent_num = 1, slot_num = 4, DEFAULT_MFIO_KEEP =  1, DEFAULT_MFIO_SEL = 0, DEFAULT_ISINK_SEL = 0x00, DEFAULT_ISINK_KEEP = 0X00, DEFAULT_DAC = 0, DEFAULT_SETTLE = 0x19, DEFAULT_PREAMP = 0x00)
        self.beryl.set_adc_slot_properties(agent_num = 1, slot_num = 5, DEFAULT_MFIO_KEEP =  1, DEFAULT_MFIO_SEL = 0, DEFAULT_ISINK_SEL = 0x00, DEFAULT_ISINK_KEEP = 0X00, DEFAULT_DAC = 0, DEFAULT_SETTLE = 0x19, DEFAULT_PREAMP = 0x00)
        self.beryl.set_adc_slot_properties(agent_num = 1, slot_num = 6, DEFAULT_MFIO_KEEP =  1, DEFAULT_MFIO_SEL = 0, DEFAULT_ISINK_SEL = 0x00, DEFAULT_ISINK_KEEP = 0x00, DEFAULT_DAC = 0, DEFAULT_SETTLE = 0x19, DEFAULT_PREAMP = 0x00)
        self.beryl.set_adc_slot_properties(agent_num = 1, slot_num = 7, DEFAULT_MFIO_KEEP =  1, DEFAULT_MFIO_SEL = 0, DEFAULT_ISINK_SEL = 0x00, DEFAULT_ISINK_KEEP = 0X00, DEFAULT_DAC = 0, DEFAULT_SETTLE = 0x19, DEFAULT_PREAMP = 0x00)
        self.beryl.set_adc_slot_properties(agent_num = 1, slot_num = 8, DEFAULT_MFIO_KEEP =  1, DEFAULT_MFIO_SEL = 0, DEFAULT_ISINK_SEL = 0x00, DEFAULT_ISINK_KEEP = 0X00, DEFAULT_DAC = 0, DEFAULT_SETTLE = 0x19, DEFAULT_PREAMP = 0x00)
        self.beryl.set_adc_slot_properties(agent_num = 1, slot_num = 9, DEFAULT_MFIO_KEEP =  1, DEFAULT_MFIO_SEL = 0, DEFAULT_ISINK_SEL = 0x00, DEFAULT_ISINK_KEEP = 0X00, DEFAULT_DAC = 0, DEFAULT_SETTLE = 0x19, DEFAULT_PREAMP = 0x00)
        self.beryl.set_adc_slot_properties(agent_num = 1, slot_num = 10, DEFAULT_MFIO_KEEP = 1, DEFAULT_MFIO_SEL = 0, DEFAULT_ISINK_SEL = 0x00, DEFAULT_ISINK_KEEP = 0X00, DEFAULT_DAC = 0, DEFAULT_SETTLE = 0x19, DEFAULT_PREAMP = 0x00)
        self.beryl.set_adc_slot_properties(agent_num = 1, slot_num = 11, DEFAULT_MFIO_KEEP = 1, DEFAULT_MFIO_SEL = 0, DEFAULT_ISINK_SEL = 0x00, DEFAULT_ISINK_KEEP = 0X00, DEFAULT_DAC = 0, DEFAULT_SETTLE = 0x19, DEFAULT_PREAMP = 0x00)
        self.beryl.set_adc_slot_properties(agent_num = 1, slot_num = 12, DEFAULT_MFIO_KEEP = 1, DEFAULT_MFIO_SEL = 0, DEFAULT_ISINK_SEL = 0x00, DEFAULT_ISINK_KEEP = 0x00, DEFAULT_DAC = 0, DEFAULT_SETTLE = 0x19, DEFAULT_PREAMP = 0x00)
        self.beryl.set_adc_slot_properties(agent_num = 1, slot_num = 13, DEFAULT_MFIO_KEEP = 1, DEFAULT_MFIO_SEL = 0, DEFAULT_ISINK_SEL = 0x00, DEFAULT_ISINK_KEEP = 0X00, DEFAULT_DAC = 0, DEFAULT_SETTLE = 0x19, DEFAULT_PREAMP = 0x00)
        self.beryl.set_adc_slot_properties(agent_num = 1, slot_num = 14, DEFAULT_MFIO_KEEP = 1, DEFAULT_MFIO_SEL = 0, DEFAULT_ISINK_SEL = 0x00, DEFAULT_ISINK_KEEP = 0X00, DEFAULT_DAC = 0, DEFAULT_SETTLE = 0x19, DEFAULT_PREAMP = 0x00)
        self.beryl.set_adc_slot_properties(agent_num = 1, slot_num = 15, DEFAULT_MFIO_KEEP = 1, DEFAULT_MFIO_SEL = 0, DEFAULT_ISINK_SEL = 0x00, DEFAULT_ISINK_KEEP = 0X00, DEFAULT_DAC = 0, DEFAULT_SETTLE = 0x19, DEFAULT_PREAMP = 0x00)

        #after setting the slot properties, do infinite scans
        firstMeasurement = False

        # if num_samples == 0, then take measurements forever
        if num_samples == 0:
            j = -1
            cumResults = numpy.zeros((1, 16))

        else:
            j = 0
            cumResults = numpy.zeros((num_samples, 16))
        while j < num_samples:
            results = {}
            self.beryl.start_adc_conversion(agent_type = 'SCAN', agent_num = 1, channel = 1)
            time.sleep(0.01)

            if firstMeasurement:
                firstMeasurement = False
            else:
                results = (self.beryl.scan_adc_read(agent_num = 1, adc_dict_in = ADCDictionary, slotChannels = SCAN1SlotDict, suppress_print = True))
                if not suppress_print:
                    print "Sample %d" % j
                    for i in range (16):
                        print "%s - %s: %s : %f " % (str(i).ljust(2), ADCDictionary[SCAN1SlotDict[i]][0].rjust(20), measurement[i].ljust(11) , results[i])
                    print "\n"
                
                for i in range(16):
                    cumResults[max(j, 0), i] = results[i]



            if num_samples != 0:
                j += 1

        if not suppress_print:
            print "AVERAGES:"
            for i in range (16):
                print "%s - %s: %s : %f " % (str(i).ljust(2), ADCDictionary[SCAN1SlotDict[i]][0].rjust(20), measurement[i].ljust(11) , numpy.mean(cumResults[:, i]))
            print "\n"

        results = {}
        for i in range(16):
            results[measurement[i]] = numpy.mean(cumResults[:, i])
        
        return results


    def turn_off_everything(self):
        self.beryl.test_mode_enable()
        self.beryl.write_reg(reg = 0x48C2, data_out = [0x1])
        self.beryl.toggle_supply(SUPPLY = 'BUCK0', MODE = 'ACT0', ON = False)
        self.beryl.toggle_supply(SUPPLY = 'BUCK1', MODE = 'ACT0', ON = False)
        self.beryl.toggle_supply(SUPPLY = 'BUCK2', MODE = 'ACT0', ON = False)
        self.beryl.toggle_supply(SUPPLY = 'LDO0', MODE = 'ACT0', ON = False)
        self.beryl.toggle_supply(SUPPLY = 'LDO1', MODE = 'ACT0', ON = False)
        self.beryl.toggle_supply(SUPPLY = 'LDO2', MODE = 'ACT0', ON = False)
        self.beryl.toggle_supply(SUPPLY = 'LDO3', MODE = 'ACT0', ON = False) 
        return

    def turn_on_everything(self):
        self.beryl.test_mode_enable()
        self.beryl.write_reg(reg = 0x48C2, data_out = [0x0])
        self.beryl.toggle_supply(SUPPLY = 'BUCK0', MODE = 'ACT0', ON = True)
        self.beryl.toggle_supply(SUPPLY = 'BUCK1', MODE = 'ACT0', ON = True)
        self.beryl.toggle_supply(SUPPLY = 'BUCK2', MODE = 'ACT0', ON = True)
        self.beryl.toggle_supply(SUPPLY = 'BUCK3', MODE = 'ACT0', ON = True)
        self.beryl.toggle_supply(SUPPLY = 'LDO0', MODE = 'ACT0', ON = True)
        self.beryl.toggle_supply(SUPPLY = 'LDO1', MODE = 'ACT0', ON = True)
        self.beryl.toggle_supply(SUPPLY = 'LDO2', MODE = 'ACT0', ON = True)
        self.beryl.toggle_supply(SUPPLY = 'LDO3', MODE = 'ACT0', ON = True) 
        return
 
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

    def uvp_trigger(self):
        UV_TRIP = 4
        print('UVP trigger...')
        self.beryl.configure_io_mfio_conf(FUNC = 'GPIO',MFIO_num = UV_TRIP, IOCELL_CFG =  'PUSH_PULL', SUPPLY = 'VDD_1V8')
        self.beryl.configure_io_gpio_conf(GPIO_num = UV_TRIP, IO_CONFIG = 0x1, DEB = '0ms', WAKE_LVL = 1)       
        return

    def intrigue_temp(self):

        """Implementation of Temp Compensation
    
        TODO: TDEV current sink does not currently work
        TODO: I faced an issue with backpowering from PD_VF_BIAS TO LDO2, James says this can be fixed by setting a certian OVP OTP bit

        """
        PD_VF_BIAS = 13
        self.beryl.test_mode_enable()
        self.beryl.toggle_supply(SUPPLY = 'LDO2', MODE = 'ACT0', ON = False)
        time.sleep(0.5)

        # #specific channels for TEMP SENSING ARCH
        # self.beryl.enableTDEV(1)
        # self.beryl.setTDEVtoAMUX(amux = 6, source = False)
        # SCAN1SlotDict = self.beryl.build_slot_channel_dict(channelList = [96, 96, 66])

        ADCDictionary = self.beryl.build_adc_channel_dict(csv = 'ADCChannelList.csv')

        # self.beryl.configure_io_mfio_conf(MFIO_NUM = PD_VF_BIAS, FUNC = 'ADCSEQ1', IOCELL_CFG =  'PUSH_PULL', POLARITY = 0x0, SUPPLY = 'VDD_MAIN')
        self.beryl.configure_io_mfio_conf(MFIO_num = PD_VF_BIAS,  IOCELL_CFG =  'PUSH_PULL', SUPPLY = 'VDDIOA')
        self.beryl.configure_io_gpio_conf(GPIO_num = PD_VF_BIAS, IO_CONFIG = 0x1, DEB = '0ms', WAKE_LVL = 1)
        self.beryl.configure_tdev(settle_time = 240, current = 200)
        self.beryl.enable_tdev(data = 1)
        # self.beryl.set_tdev_to_amux(amux = 6, source = False)
        self.beryl.write_reg(reg = 0x4171, data_out = [0x40])
        while True:
            self.beryl.start_adc_conversion('MAN', 1, 66)
            temp = []
            for i in range(50):
                self.beryl.start_adc_conversion('MAN', 1, 66)
                temp.append(self.beryl.man_adc_read(1, ADCDictionary, 66, suppress_print = True))
            print "Temp: %.3f" % numpy.mean(temp)


        # self.beryl.configure_adc_scan_agent_slots(agent_num = 1, slotChannels = SCAN1SlotDict)


        # self.beryl.set_adc_slot_properties(agent_num = 1, slot_num = 0, DEFAULT_MFIO_KEEP =  1, DEFAULT_MFIO_SEL = 1, DEFAULT_ISINK_SEL = 0x00, DEFAULT_ISINK_KEEP = 0X00, DEFAULT_DAC = 0, DEFAULT_SETTLE = 0x19, DEFAULT_PREAMP = 0x00)

        # self.beryl.set_adc_slot_properties(agent_num = 1, slot_num = 1, DEFAULT_MFIO_KEEP =  1, DEFAULT_MFIO_SEL = 0, DEFAULT_ISINK_SEL = 0x00, DEFAULT_ISINK_KEEP = 0X00, DEFAULT_DAC = 0, DEFAULT_SETTLE = 0x19, DEFAULT_PREAMP = 0x00)

        # self.beryl.set_adc_slot_properties(agent_num = 1, slot_num = 2, DEFAULT_MFIO_KEEP =  1, DEFAULT_MFIO_SEL = 0, DEFAULT_ISINK_SEL = 0x00, DEFAULT_ISINK_KEEP = 0X00, DEFAULT_DAC = 0, DEFAULT_SETTLE = 0x19, DEFAULT_PREAMP = 0x00)


        # self.beryl.start_adc_conversion(agent = 'SCAN1', channel = 1)
        #     #time.sleep(.5)
        # self.beryl.scan_adc_read(agent_num = 1, adc_dict_in = ADCDictionary, slotChannels = SCAN1SlotDict)


if __name__ == "__main__":
    i = Intrigue()
    #i.turn_off_everything()
    #i.laserSafetyTest()
    #i.TIA_Test()
    #i.intrigue_ied()
    #i.pulse_isink()
    i.uvp_trigger()
    #i.turn_off_everything()
    #i.intrigue_direct_channels()
    #i.GPADC_man()
    #i.intrigue_temp()

