import serial
import serial.tools.list_ports
# import uart
import time
import sys
import serial
# import beryl_resetcode as rst
import BerylFT as brl
import os
import numpy
import yc.misc as misc
import argparse

capture=1
filepath = '/vault/results/'

class Intrigue(object):
    def __init__(self, spPort, hwh = None):
        global output
        #initialize beryl
        self.beryl = brl.Beryl(channel = 'UART1',port = spPort)
        output=misc.output

    def close_port(self):
        self.beryl.close_port()

    def laserSafetyTest_enable(self,isinknum):
        # Measures how long VCSEL1 stays on if ISINK and VCSEL_LDO_EN are both stuck "on"
        # VCSEL1 is considered "on" if V_do of ISINK is > 50mV

        VCSEL_EN = 11
        adc_dict = self.beryl.build_adc_channel_dict()
        self.beryl.test_mode_enable()


        # while True:
        self.beryl.enable_isink_global(FAST_EN=0x0)
        # self.beryl.enable_isink(isink_num = 2, PWM_MODE = 'CC', FAST_EN = 0x0, TRIG_SEL = 'SW')
        self.beryl.enable_isink(isink_num=isinknum, PWM_MODE='CC', FAST_EN=0x0, TRIG_SEL='SW')
        self.beryl.configure_io_mfio_conf(MFIO_num=VCSEL_EN, IOCELL_CFG='PUSH_PULL', SUPPLY='VDD_1V8')
        self.beryl.configure_io_gpio_conf(GPIO_num=VCSEL_EN, IO_CONFIG=0x1, DEB='0ms', WAKE_LVL=0)
        time.sleep(0.2)
        self.beryl.configure_io_gpio_conf(GPIO_num=VCSEL_EN, IO_CONFIG=0x1, DEB='0ms', WAKE_LVL=1)
        # startTime = time.time()
        self.beryl.trigger_isink(isinknum)
        # V_do = 1
        # while V_do > 0.05:
        #     self.beryl.start_adc_conversion('MAN', 1, 40)
        #     V_do = self.beryl.man_adc_read(1, adc_dict, 40, suppress_print = True)
        #     print V_do
        #     elapsedTime = time.time() - startTime

        # self.beryl.disable_isink(isinknum)
        # self.beryl.configure_io_gpio_conf(GPIO_num=VCSEL_EN, IO_CONFIG=0x1, DEB='0ms', WAKE_LVL=0)
        # time.sleep(0.1)
        # print elapsedTime
        # return elapsedTime

    def laserSafetyTest_disable(self,isinknum):
        # Measures how long VCSEL1 stays on if ISINK and VCSEL_LDO_EN are both stuck "on"
        # VCSEL1 is considered "on" if V_do of ISINK is > 50mV

        VCSEL_EN = 11
        # adc_dict = self.beryl.build_adc_channel_dict()
        # self.beryl.test_mode_enable()
        #
        #
        #
        # # while True:
        # self.beryl.enable_isink_global(FAST_EN=0x0)
        # # self.beryl.enable_isink(isink_num = 2, PWM_MODE = 'CC', FAST_EN = 0x0, TRIG_SEL = 'SW')
        # self.beryl.enable_isink(isink_num=isinknum, PWM_MODE='CC', FAST_EN=0x0, TRIG_SEL='SW')
        # self.beryl.configure_io_mfio_conf(MFIO_num=VCSEL_EN, IOCELL_CFG='PUSH_PULL', SUPPLY='VDD_1V8')
        # self.beryl.configure_io_gpio_conf(GPIO_num=VCSEL_EN, IO_CONFIG=0x1, DEB='0ms', WAKE_LVL=1)
        # # startTime = time.time()
        # self.beryl.trigger_isink(isinknum)
        # V_do = 1
        # while V_do > 0.05:
        #     self.beryl.start_adc_conversion('MAN', 1, 40)
        #     V_do = self.beryl.man_adc_read(1, adc_dict, 40, suppress_print = True)
        #     print V_do
        #     elapsedTime = time.time() - startTime

        self.beryl.disable_isink(isinknum)
        self.beryl.configure_io_gpio_conf(GPIO_num=VCSEL_EN, IO_CONFIG=0x1, DEB='0ms', WAKE_LVL=0)
        self.beryl.test_mode_disable()
        # time.sleep(0.1)
        # print elapsedTime
        # return elapsedTime

    def pulse_isink(self, sink_num, current=3300, width=10000, cycle=1, num_samples=10):  # width in uS, cycle in secs
        # VCSEL_EN = 11
        # self.beryl.configure_io_mfio_conf(FUNC = 'GPIO',MFIO_num = VCSEL_EN, IOCELL_CFG =  'PUSH_PULL', SUPPLY = 'VDD_1V8')
        # self.beryl.configure_io_mfio_conf(FUNC = 'ISINK3_PWM',MFIO_num = 8, IOCELL_CFG =  'PUSH_PULL', SUPPLY = 'VDD_1V8')
        self.beryl.test_mode_enable()
        self.beryl.disable_isink_global(FAST_EN=0x0)
        self.beryl.enable_isink_global(FAST_EN=0x0)
        self.beryl.enable_isink(isink_num=sink_num, PWM_MODE='Pulse', FAST_EN=0x0, TRIG_SEL='SW')
        # self.beryl.enable_isink(isink_num=sink_num, PWM_MODE='Pulse', FAST_EN=0x0, TRIG_SEL='SW')
        # self.beryl.enable_isink(isink_num = 3, PWM_MODE = 'Pulse', FAST_EN = 0x0, TRIG_SEL = 'SW')
        self.beryl.config_isink_pwm(isink_num=sink_num, PWM_CYC=0, PWM0=width)
        # self.beryl.config_isink_pwm(isink_num=2, PWM_CYC=0, PWM0=width)
        # self.beryl.config_isink_pwm(isink_num = 3, PWM_CYC = 0, PWM0 =  width)
        self.beryl.set_isink_current(isink_num=sink_num, current=current)
        # self.beryl.set_isink_current(isink_num=2, current=current)
        # self.beryl.set_isink_current(isink_num = 3, current = current)

        self.beryl.trigger_isink(isink_num=sink_num)

        # j = 0
        # while j < num_samples:
            # self.beryl.configure_io_gpio_conf(GPIO_num = VCSEL_EN, IO_CONFIG = 0x0, DEB = '0ms', WAKE_LVL = 1)
            # self.beryl.configure_io_gpio_conf(GPIO_num = VCSEL_EN, IO_CONFIG = 0x1, DEB = '0ms', WAKE_LVL = 1)
            # self.beryl.trigger_isink(isink_num=sink_num)
            # self.beryl.trigger_isink(isink_num = 3)
            # time.sleep(cycle)
            # if num_samples != 0:
            #     j += 1
        # j = 0
        # while j < num_samples:
        #     # self.beryl.configure_io_gpio_conf(GPIO_num = VCSEL_EN, IO_CONFIG = 0x0, DEB = '0ms', WAKE_LVL = 1)
        #     # self.beryl.configure_io_gpio_conf(GPIO_num = VCSEL_EN, IO_CONFIG = 0x1, DEB = '0ms', WAKE_LVL = 1)
        #     self.beryl.trigger_isink(isink_num=2)
        #     # self.beryl.trigger_isink(isink_num = 3)
        #     time.sleep(cycle)
        #     if num_samples != 0:
        #         j += 1
        self.beryl.test_mode_disable()
        return

    def TIA_Test(self):

        """
        HOW TO USE:

        1) Shunt MFIO12 to 1V8 to enable TIAs indefinetly
        2) Make sure TIA EN jumpers are stuffed
        3) run script and probe correct TIA!

        """
        self.beryl.test_mode_enable()
        self.beryl.toggle_supply(SUPPLY = 'LDO2', MODE = 'ACT0', ON = True)
        # Set power mode target to ACT0
        self.beryl.write_reg(0x1401, [0x00])
        #beryl.toggle_supply(SUPPLY = 'LDO2', MODE = 'ACT0', ON = True)
        self.beryl.disable_isink_global(FAST_EN = 0x0)
        self.beryl.enable_isink_global(FAST_EN = 0x0)

        self.beryl.disable_isink(isink_num = 1)
        self.beryl.enable_isink(isink_num = 1, PWM_MODE = 'CC', FAST_EN = 0x0, TRIG_SEL = 'SW')
        self.beryl.set_isink_current(isink_num = 1, current = 3300)
        #self.beryl.config_ISINK_PWM(isink_num = 3, period  = 25000, on_time = 400) #1Hz

        #self.beryl.configure_io_mfio_conf(MFIO_NUM = 1, FUNC = 'ISINK3_PWM', IOCELL_CFG =  "PUSH_PULL", SUPPLY = 'VDD_1V8')
        self.beryl.configure_io_mfio_conf(MFIO_NUM = 11, FUNC = 'RTC_1HZ', IOCELL_CFG =  "PUSH_PULL", SUPPLY = 'VDD_1V8')
        self.beryl.triggerISINK(isink_num = 1)

    def intrigue_ied(self, loop = True, suppress_print = False, num_samples = 10, raw_result = False):
        #beryl = brl.Beryl(update = False, standalone = False, spmi_in = True, verbose_in = False)

        #set isinks to be GPADC triggered and pulse mode
        self.beryl.test_mode_enable()
        #turn on 1V75 rail
        self.beryl.toggle_supply(SUPPLY = 'LDO2', MODE = 'ACT0', ON = True)
        # Set power mode target to ACT0
        self.beryl.write_reg(0x1401, [0x00])

        #this makes sure currentsinks function correctly, probably don't need
        self.beryl.disable_isink_global(FAST_EN = 0x0)
        self.beryl.enable_isink_global(FAST_EN = 0x0)

        # self.beryl.disable_isink(isink_num = 2)
        # self.beryl.disable_isink(isink_num = 1)

        #set to desired current
        self.beryl.set_isink_current(isink_num = 2, current = 3300)
        self.beryl.set_isink_current(isink_num = 1, current = 3300)

        #set iSink trigger as GPADC
        self.beryl.enable_isink(isink_num = 2, PWM_MODE = 'CC', FAST_EN = 0x0, TRIG_SEL = 'GPADC')
        self.beryl.enable_isink(isink_num = 1, PWM_MODE = 'CC', FAST_EN = 0x0, TRIG_SEL = 'GPADC')

        #beryl.enable_isink(isink_num = 2, PWM_MODE = 'Pulse', FAST_EN = 0x0, TRIG_SEL = 'GPADC')

        #beryl.config_ISINK_PWM(isink_num = 1, period = 500, on_time =  25000)
        #beryl.config_ISINK_PWM(isink_num = 2, period = 500, on_time =  25000)

        #beryl.set_isink_current(isink_num = 2, current = 3300)

        measurement = [
            "TIA_VREF",   # 0
            "PD1_Vr",     # 1
            "PD_VF_LOW",  # 2
            "TIA1_DARK",  # 3
            "TIA1_LIGHT", # 4
            "VSINK1_ON",  # 5
            "VSINK1_OFF", # 6
            "PD2_Vr",     # 7
            "ignore",     # 8
            "TIA2_DARK",  # 9
            "TIA2_LIGHT", # 10
            "VSINK2_ON",  # 11
            "VSINK2_OFF", # 12
            "PD1_TEMP",   # 13
            "PD2_TEMP",   # 14
            "PD_VF_HIGH"  # 15
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
        # self.beryl.configure_io_gpio_conf(GPIO_num = TIA_EN, IO_CONFIG = 0x1, DEB = '0ms', WAKE_LVL = 0)

        self.beryl.configure_io_mfio_conf(MFIO_num = VCSEL_EN, FUNC = 'ADCSEQ1', IOCELL_CFG =  'PUSH_PULL', POLARITY = 0x0, SUPPLY = 'VDD_1V8')
        # self.beryl.configure_io_mfio_conf(MFIO_num = TIA_EN, FUNC = 'ADCSEQ2', IOCELL_CFG =  'PUSH_PULL', POLARITY = 0x0, SUPPLY = 'VDD_1V8')
        # self.beryl.configure_io_mfio_conf(MFIO_num = TIA_EN, FUNC = 'ADCSEQ2', IOCELL_CFG =  'PUSH_PULL', POLARITY = 0x0, SUPPLY = 'VDD_1V8')
        #for IED, we are setting this pin low always, you can choose to make this ADCSEQ3 and just never trigger it
        self.beryl.configure_io_mfio_conf(MFIO_num = PD_VF_BIAS, FUNC = 'ADCSEQ3', IOCELL_CFG =  'PUSH_PULL', POLARITY = 0x0, SUPPLY = 'VDDIOA')
        # self.beryl.configure_io_mfio_conf(MFIO_num = PD_VF_BIAS,  IOCELL_CFG =  'PUSH_PULL', SUPPLY = 'VDDIOA')
        # self.beryl.configure_io_gpio_conf(GPIO_num = PD_VF_BIAS, IO_CONFIG = 0x1, DEB = '0ms', WAKE_LVL = 0)


        # self.beryl.configure_tdev(settle_time = 240, current = 200)
        # self.beryl.enable_tdev(data = 0x03)
        # # self.beryl.set_tdev_to_amux(amux = 6, source = False)
        # self.beryl.write_reg(reg = 0x4171, data_out = [0xC0])
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
            91,
            91,
            91])

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
        self.beryl.set_adc_slot_properties(agent_num = 1, slot_num = 12, DEFAULT_MFIO_KEEP = 1, DEFAULT_MFIO_SEL = 0, DEFAULT_ISINK_SEL = 0x00, DEFAULT_ISINK_KEEP = 0x00, DEFAULT_DAC = 0, DEFAULT_SETTLE = 0x19, DEFAULT_PREAMP = 0x00)
        # de-assert TIA_EN, PD_VF_BIAS, LDO_EN (THIS IS DONE IN THE PREVIOUS SECTION TO MAKE SURE ITS DESSARTED DURING THIS MEASUREMENT), measure PD0
        self.beryl.set_adc_slot_properties(agent_num = 1, slot_num = 13, DEFAULT_MFIO_KEEP = 1, DEFAULT_MFIO_SEL = 0, DEFAULT_ISINK_SEL = 0x00, DEFAULT_ISINK_KEEP = 0X00, DEFAULT_DAC = 0, DEFAULT_SETTLE = 0x19, DEFAULT_PREAMP = 0x00)
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
                results = (self.beryl.scan_adc_read(agent_num = 1, adc_dict_in = ADCDictionary, slotChannels = SCAN1SlotDict, suppress_print = True, raw_result = raw_result))
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

        return cumResults

            # time.sleep(0.01)

    def intrigue_autosequence(self, suppress_print = False, startstop = "start"):
        if startstop == "start":
            #set isinks to be GPADC triggered and pulse mode
            self.beryl.test_mode_enable()
            #turn on 1V75 rail
            self.beryl.toggle_supply(SUPPLY = 'LDO2', MODE = 'ACT0', ON = True)
            # Set power mode target to ACT0
            self.beryl.write_reg(0x1401, [0x00])

            #this makes sure currentsinks function correctly, probably don't need
            self.beryl.disable_isink_global(FAST_EN = 0x0)
            self.beryl.enable_isink_global(FAST_EN = 0x0)

            # self.beryl.disable_isink(isink_num = 2)
            # self.beryl.disable_isink(isink_num = 1)

            #set to desired current
            self.beryl.set_isink_current(isink_num = 2, current = 3300)
            self.beryl.set_isink_current(isink_num = 1, current = 3300)

            #set iSink trigger as GPADC
            self.beryl.enable_isink(isink_num = 2, PWM_MODE = 'CC', FAST_EN = 0x0, TRIG_SEL = 'GPADC')
            self.beryl.enable_isink(isink_num = 1, PWM_MODE = 'CC', FAST_EN = 0x0, TRIG_SEL = 'GPADC')

            #beryl.enable_isink(isink_num = 2, PWM_MODE = 'Pulse', FAST_EN = 0x0, TRIG_SEL = 'GPADC')

            #beryl.config_ISINK_PWM(isink_num = 1, period = 500, on_time =  25000)
            #beryl.config_ISINK_PWM(isink_num = 2, period = 500, on_time =  25000)

            #beryl.set_isink_current(isink_num = 2, current = 3300)

            measurement = [
                "TIA_VREF",   # 0
                "PD1_Vr",     # 1
                "PD_VF_LOW",  # 2
                "TIA1_DARK",  # 3
                "TIA1_LIGHT", # 4
                "VSINK1_ON",  # 5
                "VSINK1_OFF", # 6
                "PD2_Vr",     # 7
                "ignore",     # 8
                "TIA2_DARK",  # 9
                "TIA2_LIGHT", # 10
                "VSINK2_ON",  # 11
                "VSINK2_OFF", # 12
                "PD1_TEMP",   # 13
                "PD2_TEMP",   # 14
                "PD_VF_HIGH"  # 15
            ]

            #set MFIOs to be GPADC triggered
            VCSEL_EN = 11
            TIA_EN = 12
            PD_VF_BIAS = 13

            # Upon initial startup, the PD AC coupling cap needs to bias.
            # Enable the TIAs for an extended period of time to do this.
            self.beryl.configure_io_mfio_conf(MFIO_num = TIA_EN, IOCELL_CFG = 'PUSH_PULL', SUPPLY = 'VDD_1V8')
            self.beryl.configure_io_gpio_conf(GPIO_num = TIA_EN, IO_CONFIG = 0x1, DEB = '0ms', WAKE_LVL = 1)
            # time.sleep(1)
            # self.beryl.configure_io_gpio_conf(GPIO_num = TIA_EN, IO_CONFIG = 0x1, DEB = '0ms', WAKE_LVL = 0)

            self.beryl.configure_io_mfio_conf(MFIO_num = VCSEL_EN, FUNC = 'ADCSEQ1', IOCELL_CFG =  'PUSH_PULL', POLARITY = 0x0, SUPPLY = 'VDD_1V8')
            # self.beryl.configure_io_mfio_conf(MFIO_num = TIA_EN, FUNC = 'ADCSEQ2', IOCELL_CFG =  'PUSH_PULL', POLARITY = 0x0, SUPPLY = 'VDD_1V8')
            # self.beryl.configure_io_mfio_conf(MFIO_num = TIA_EN, FUNC = 'ADCSEQ2', IOCELL_CFG =  'PUSH_PULL', POLARITY = 0x0, SUPPLY = 'VDD_1V8')
            #for IED, we are setting this pin low always, you can choose to make this ADCSEQ3 and just never trigger it
            self.beryl.configure_io_mfio_conf(MFIO_num = PD_VF_BIAS, FUNC = 'ADCSEQ3', IOCELL_CFG =  'PUSH_PULL', POLARITY = 0x0, SUPPLY = 'VDDIOA')
            # self.beryl.configure_io_mfio_conf(MFIO_num = PD_VF_BIAS,  IOCELL_CFG =  'PUSH_PULL', SUPPLY = 'VDDIOA')
            # self.beryl.configure_io_gpio_conf(GPIO_num = PD_VF_BIAS, IO_CONFIG = 0x1, DEB = '0ms', WAKE_LVL = 0)


            # self.beryl.configure_tdev(settle_time = 240, current = 200)
            # self.beryl.enable_tdev(data = 0x03)
            # # self.beryl.set_tdev_to_amux(amux = 6, source = False)
            # self.beryl.write_reg(reg = 0x4171, data_out = [0xC0])
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
                91,
                91,
                91])

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
            self.beryl.set_adc_slot_properties(agent_num = 1, slot_num = 12, DEFAULT_MFIO_KEEP = 1, DEFAULT_MFIO_SEL = 0, DEFAULT_ISINK_SEL = 0x00, DEFAULT_ISINK_KEEP = 0x00, DEFAULT_DAC = 0, DEFAULT_SETTLE = 0x19, DEFAULT_PREAMP = 0x00)
            # de-assert TIA_EN, PD_VF_BIAS, LDO_EN (THIS IS DONE IN THE PREVIOUS SECTION TO MAKE SURE ITS DESSARTED DURING THIS MEASUREMENT), measure PD0
            self.beryl.set_adc_slot_properties(agent_num = 1, slot_num = 13, DEFAULT_MFIO_KEEP = 1, DEFAULT_MFIO_SEL = 0, DEFAULT_ISINK_SEL = 0x00, DEFAULT_ISINK_KEEP = 0X00, DEFAULT_DAC = 0, DEFAULT_SETTLE = 0x19, DEFAULT_PREAMP = 0x00)
            #measure PD1
            self.beryl.set_adc_slot_properties(agent_num = 1, slot_num = 14, DEFAULT_MFIO_KEEP = 1, DEFAULT_MFIO_SEL = 0, DEFAULT_ISINK_SEL = 0x00, DEFAULT_ISINK_KEEP = 0X00, DEFAULT_DAC = 0, DEFAULT_SETTLE = 0x19, DEFAULT_PREAMP = 0x00)
            #assert PD_BIASN, measure PD_BIASN
            self.beryl.set_adc_slot_properties(agent_num = 1, slot_num = 15, DEFAULT_MFIO_KEEP = 0, DEFAULT_MFIO_SEL = 4, DEFAULT_ISINK_SEL = 0x00, DEFAULT_ISINK_KEEP = 0X00, DEFAULT_DAC = 0, DEFAULT_SETTLE = 0x19, DEFAULT_PREAMP = 0x00)

        # First, disable the scan agent
        self.beryl.configure_adc_scan_agent(1, T_SCH_DLY = 0x0, T_SCH_ALT = 0x0, ACQ_CFG = 0x0, TRIG_MODE = 0x0)
        # Then, set the scan agent to automatically repeat every 25 ms
        if startstop == "start":
            self.beryl.configure_adc_scan_agent(1, T_SCH_DLY = 0x6, T_SCH_ALT = 0x1, ACQ_CFG = 0x3, TRIG_MODE = 0x1)

        #after setting the slot properties, do infinite scans
        # firstMeasurement = False

        # # if num_samples == 0, then take measurements forever
        # if num_samples == 0:
        #     j = -1
        #     cumResults = numpy.zeros((1, 16))

        # else:
        #     j = 0
        #     cumResults = numpy.zeros((num_samples, 16))
        # while j < num_samples:
        #     results = {}
        #     self.beryl.start_adc_conversion(agent_type = 'SCAN', agent_num = 1, channel = 1)
        #     time.sleep(0.01)

        #     if firstMeasurement:
        #         firstMeasurement = False
        #     else:
        #         results = (self.beryl.scan_adc_read(agent_num = 1, adc_dict_in = ADCDictionary, slotChannels = SCAN1SlotDict, suppress_print = True, raw_result = raw_result))
        #         if not suppress_print:
        #             print "Sample %d" % j
        #             for i in range (16):
        #                 print "%s - %s: %s : %f " % (str(i).ljust(2), ADCDictionary[SCAN1SlotDict[i]][0].rjust(20), measurement[i].ljust(11) , results[i])
        #             print "\n"

        #         for i in range(16):
        #             cumResults[max(j, 0), i] = results[i]



        #     if num_samples != 0:
        #         j += 1

        # if not suppress_print:
        #     print "AVERAGES:"
        #     for i in range (16):
        #         print "%s - %s: %s : %f " % (str(i).ljust(2), ADCDictionary[SCAN1SlotDict[i]][0].rjust(20), measurement[i].ljust(11) , numpy.mean(cumResults[:, i]))
        #     print "\n"

        # results = {}
        # for i in range(16):
        #     results[measurement[i]] = numpy.mean(cumResults[:, i])

        # return cumResults

            # time.sleep(0.01)


    def intrigue_i_threshold(self, loop = True, suppress_print = False, num_samples = 10, vcsel_current = 3300):
        #beryl = brl.Beryl(update = False, standalone = False, spmi_in = True, verbose_in = False)

        #set isinks to be GPADC triggered and pulse mode
        self.beryl.test_mode_enable()
        #turn on 1V75 rail
        self.beryl.toggle_supply(SUPPLY = 'LDO2', MODE = 'ACT0', ON = True)
        # Set power mode target to ACT0
        self.beryl.write_reg(0x1401, [0x00])
        self.beryl.set_isink_current(isink_num = 1, current = vcsel_current)
        self.beryl.set_isink_current(isink_num = 2, current = vcsel_current)

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
        # self.beryl.configure_io_gpio_conf(GPIO_num = TIA_EN, IO_CONFIG = 0x1, DEB = '0ms', WAKE_LVL = 0)

        self.beryl.configure_io_mfio_conf(MFIO_num = VCSEL_EN, FUNC = 'ADCSEQ1', IOCELL_CFG =  'PUSH_PULL', POLARITY = 0x0, SUPPLY = 'VDD_1V8')
        # self.beryl.configure_io_mfio_conf(MFIO_num = TIA_EN, FUNC = 'ADCSEQ2', IOCELL_CFG =  'PUSH_PULL', POLARITY = 0x0, SUPPLY = 'VDD_1V8')
        # self.beryl.configure_io_mfio_conf(MFIO_num = TIA_EN, FUNC = 'ADCSEQ2', IOCELL_CFG =  'PUSH_PULL', POLARITY = 0x0, SUPPLY = 'VDD_1V8')
        #for IED, we are setting this pin low always, you can choose to make this ADCSEQ3 and just never trigger it
        self.beryl.configure_io_mfio_conf(MFIO_num = PD_VF_BIAS, FUNC = 'ADCSEQ3', IOCELL_CFG =  'PUSH_PULL', POLARITY = 0x0, SUPPLY = 'VDDIOA')
        # self.beryl.configure_io_mfio_conf(MFIO_num = PD_VF_BIAS,  IOCELL_CFG =  'PUSH_PULL', SUPPLY = 'VDDIOA')
        # self.beryl.configure_io_gpio_conf(GPIO_num = PD_VF_BIAS, IO_CONFIG = 0x1, DEB = '0ms', WAKE_LVL = 0)


        # self.beryl.configure_tdev(settle_time = 240, current = 200)
        # self.beryl.enable_tdev(data = 0x03)
        # # self.beryl.set_tdev_to_amux(amux = 6, source = False)
        # self.beryl.write_reg(reg = 0x4171, data_out = [0xC0])
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
            91,
            91,
            91])

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
        self.beryl.set_adc_slot_properties(agent_num = 1, slot_num = 12, DEFAULT_MFIO_KEEP = 1, DEFAULT_MFIO_SEL = 0, DEFAULT_ISINK_SEL = 0x00, DEFAULT_ISINK_KEEP = 0x00, DEFAULT_DAC = 0, DEFAULT_SETTLE = 0x19, DEFAULT_PREAMP = 0x00)
        # de-assert TIA_EN, PD_VF_BIAS, LDO_EN (THIS IS DONE IN THE PREVIOUS SECTION TO MAKE SURE ITS DESSARTED DURING THIS MEASUREMENT), measure PD0
        self.beryl.set_adc_slot_properties(agent_num = 1, slot_num = 13, DEFAULT_MFIO_KEEP = 1, DEFAULT_MFIO_SEL = 0, DEFAULT_ISINK_SEL = 0x00, DEFAULT_ISINK_KEEP = 0X00, DEFAULT_DAC = 0, DEFAULT_SETTLE = 0x19, DEFAULT_PREAMP = 0x00)
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
                returnedChannels = [3, 4, 9, 10]
                results = (self.beryl.scan_adc_read(agent_num = 1, adc_dict_in = ADCDictionary, slotChannels = SCAN1SlotDict, suppress_print = True, returnedChannels = returnedChannels))
                if not suppress_print:
                    print "Sample %d" % j
                    for i in range(16):
                        print "%s - %s: %s : %f " % (str(i).ljust(2), ADCDictionary[SCAN1SlotDict[i]][0].rjust(20), measurement[i].ljust(11) , results[i])
                    print "\n"

                for i in returnedChannels:
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

            # time.sleep(0.01)

    def GPADC_man(self, channel = 3, num_samples = 10, average_samples = 50):
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
            self.beryl.start_adc_conversion(agent_type = 'MAN', agent_num = 1, channel = chan)
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

    def turn_off_everything(self):
        self.beryl.write_reg(reg = 0x48C2, data_out = [0x1])
        return

    def intrigue_temp(self, suppress_print = False, photodiode = 1, num_samples = 10, raw_result = False):

        """Implementation of Temp Compensation

        TODO: TDEV current sink does not currently work
        TODO: I faced an issue with backpowering from PD_VF_BIAS TO LDO2, James says this can be fixed by setting a certian OVP OTP bit

        """
        PD_VF_BIAS = 13
        self.beryl.test_mode_enable()
        self.beryl.toggle_supply(SUPPLY = 'LDO2', MODE = 'ACT0', ON = True)
        # Set power mode target to ACT0
        self.beryl.write_reg(0x1401, [0x00])
        time.sleep(0.5)

        # #specific channels for TEMP SENSING ARCH
        # self.beryl.enableTDEV(1)
        # self.beryl.setTDEVtoAMUX(amux = 6, source = False)
        # SCAN1SlotDict = self.beryl.build_slot_channel_dict(channelList = [96, 96, 66])

        ADCDictionary = self.beryl.build_adc_channel_dict(csv = 'ADCChannelList.csv')

        # self.beryl.configure_io_mfio_conf(MFIO_NUM = PD_VF_BIAS, FUNC = 'ADCSEQ1', IOCELL_CFG =  'PUSH_PULL', POLARITY = 0x0, SUPPLY = 'VDD_MAIN')
        self.beryl.configure_io_mfio_conf(MFIO_num = PD_VF_BIAS,  IOCELL_CFG =  'PUSH_PULL', SUPPLY = 'VDDIOA')
        self.beryl.configure_io_gpio_conf(GPIO_num = PD_VF_BIAS, IO_CONFIG = 0x1, DEB = '0ms', WAKE_LVL = 1)
        self.beryl.configure_tdev(settle_time = 240, current = 100)
        self.beryl.enable_tdev(data = 1)
        # self.beryl.set_tdev_to_amux(amux = 6, source = False)
        self.beryl.write_reg(reg = 0x4171, data_out = [0xC0])
        PD_Vf = []
        for i in range(num_samples):
            self.beryl.start_adc_conversion('MAN', 1, 65 + photodiode)
            PD_K = self.beryl.man_adc_read(1, ADCDictionary, 65 + photodiode, suppress_print = True)
            self.beryl.start_adc_conversion('MAN', 1, 90)
            PD_A= self.beryl.man_adc_read(1, ADCDictionary, 90, suppress_print = True)
            PD_Vf.append(PD_A - PD_K)
            if suppress_print == False:
                print "PD%d Vf: %.3f" % (photodiode, PD_Vf[i])
        if suppress_print == False:
            print "PD%d average Vf: %.3f" % (photodiode, numpy.mean(PD_Vf))
        return PD_Vf

        # self.beryl.configure_adc_scan_agent_slots(agent_num = 1, slotChannels = SCAN1SlotDict)


        # self.beryl.set_adc_slot_properties(agent_num = 1, slot_num = 0, DEFAULT_MFIO_KEEP =  1, DEFAULT_MFIO_SEL = 1, DEFAULT_ISINK_SEL = 0x00, DEFAULT_ISINK_KEEP = 0X00, DEFAULT_DAC = 0, DEFAULT_SETTLE = 0x19, DEFAULT_PREAMP = 0x00)

        # self.beryl.set_adc_slot_properties(agent_num = 1, slot_num = 1, DEFAULT_MFIO_KEEP =  1, DEFAULT_MFIO_SEL = 0, DEFAULT_ISINK_SEL = 0x00, DEFAULT_ISINK_KEEP = 0X00, DEFAULT_DAC = 0, DEFAULT_SETTLE = 0x19, DEFAULT_PREAMP = 0x00)

        # self.beryl.set_adc_slot_properties(agent_num = 1, slot_num = 2, DEFAULT_MFIO_KEEP =  1, DEFAULT_MFIO_SEL = 0, DEFAULT_ISINK_SEL = 0x00, DEFAULT_ISINK_KEEP = 0X00, DEFAULT_DAC = 0, DEFAULT_SETTLE = 0x19, DEFAULT_PREAMP = 0x00)


        # self.beryl.start_adc_conversion(agent = 'SCAN1', channel = 1)
        #     #time.sleep(.5)
        # self.beryl.scan_adc_read(agent_num = 1, adc_dict_in = ADCDictionary, slotChannels = SCAN1SlotDict)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Intrigue Test")
    parser.add_argument('-p', '--port', help='Serial port name.', type=str, default=False, required=True)
    parser.add_argument('-enablesafety','--enablesafety',help='Intrigue Enable Safety Test.', type=bool, default=False, required=False)
    parser.add_argument('-disablesafety', '--disablesafety', help='Intrigue Disable Safety Test.', type=bool, default=False,required=False)
    parser.add_argument('-pulse', '--pulseisink', help='Intrigue Pulse iSink.', type=bool, default=False, required=False)
    parser.add_argument('-n', '--isinknum', help='Intrigue Pulse iSink Num.', type=int, default=False, required=False)
    parser.add_argument('-tia', '--tiatest', help='Intrigue TIA Test.', type=bool, default=False, required=False)
    parser.add_argument('-ied', '--ied', help='Intrigue IED.', type=bool, default=False, required=False)
    parser.add_argument('-gpadc', '--gpadcman', help='Intrigue GPADC Man.', type=bool, default=False, required=False)
    parser.add_argument('-temp', '--temp', help='Intrigue Temp.', type=bool, default=False, required=False)
    args = parser.parse_args()

    print args

    i = Intrigue(args.port)
    # i.turn_off_everything()

    if args.enablesafety:
        print '\n ******************* Enable Safety Test *******************'
        i.laserSafetyTest_enable(args.isinknum)

    if args.disablesafety:
        print '\n ******************* Disable Safety Test *******************'
        i.laserSafetyTest_disable(args.isinknum)

    if args.pulseisink:
        print '\n ******************* Pulse iSink Test *******************'
        i.pulse_isink(args.isinknum)

    if args.tiatest:
        print '\n ******************* TIA Test *******************'
        i.TIA_Test()

    if args.ied:
        print '\n ******************* IED Test *******************'
        i.intrigue_ied()

    if args.gpadcman:
        print '\n ******************* GPADC Man *******************'
        i.GPADC_man()

    if args.temp:
        print '\n ******************* Temp *******************'
        i.intrigue_temp()

    # i.pulse_isink()
    #i.TIA_Test()
    # i.intrigue_ied()
    # i.GPADC_man()
    #i.intrigue_temp()

    i.close_port()
