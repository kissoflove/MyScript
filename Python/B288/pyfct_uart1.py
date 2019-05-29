#!/usr/bin/python

# Copyright Apple Inc.
# Author: Jason Brinsfield
# Description: script for testing rigid boards and MLBs in FA fixtures. Inspiration drawn from dominion.py, empire.py and qfct.py (B188)

import BerylFT
# import spim
import time
# import hw
import numpy
import intrigueFT

class bcolors:
    HEADER  = '\033[95m'
    OKBLUE  = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL    = '\033[91m'
    ENDC    = '\033[0m'
    BOLD    = '\033[1m'
    UNDERLINE = '\033[4m'

specs = {}



def read_spec_limits():
   specfile = open("pyfct_spec_limits.csv", 'r')
   speclist = specfile.readlines()

   for line in speclist[1:]:
      splitline = line.split(',')
      specs[splitline[0]] = [float(splitline[1]), float(splitline[2])]



def get_pass_fail(testItem, val, lsl, usl):
   if val < lsl:
      print (bcolors.FAIL + bcolors.BOLD + "FAIL: " + bcolors.ENDC
      + testItem.ljust(15) + ("Value: %s" % val).ljust(18)
      + ("%sLSL%s: %s" % (bcolors.FAIL, bcolors.ENDC, str(lsl))).ljust(20)
      +  "USL: %s" % str(usl))

   elif val > usl:
      print (bcolors.FAIL + bcolors.BOLD + "FAIL: " + bcolors.ENDC
      + testItem.ljust(15) + ("Value: %s" % val).ljust(18)
      + ("LSL: %s" % str(lsl)).ljust(11)
      + "%sUSL%s: %s" % (bcolors.FAIL, bcolors.ENDC, str(usl)))


   elif val <= usl and val >= lsl:
      print (bcolors.OKGREEN + bcolors.BOLD + "PASS: " + bcolors.ENDC
      + testItem.ljust(15) + ("Value: %s" % val).ljust(18)
      + ("LSL: %s" % str(lsl)).ljust(11)
      + "USL: %s" % str(usl))

   else:
      print (bcolors.FAIL + bcolors.BOLD + "FAIL: " + bcolors.ENDC
      + "Unknown Error")

def init_dut():

   return


def test_beryl(hwh = None):
   # Start by testing all the rails
   b = BerylFT.Beryl(channel = "UART1", port = '/dev/cu.usbserial-14112C')
   adc_dict = b.build_adc_channel_dict()
   channelList = [1, 3, 5, 10, 11, 12, 13, 20, 21, 22, 23]
   for channel in channelList:
      val = []
      for i in range(10):
         b.start_adc_conversion('MAN', 1, channel)
         val.append(b.man_adc_read(1, adc_dict, channel, suppress_print = True))

      avgVal = numpy.mean(val)
      lsl = specs[adc_dict[channel][0]][0]
      usl = specs[adc_dict[channel][0]][1]
      get_pass_fail(adc_dict[channel][0], avgVal, lsl, usl)

def test_adamstown():
   return

def test_mics():
   return

def test_boron2():
   return

def bma282_vdd(hwh = None, enable = 1):
   b = Beryl.Beryl(hwh = hwh)

   b.configure_io_mfio_conf(MFIO_num = 9, IOCELL_CFG = 'PUSH_PULL', SUPPLY = 'VDDIOA')
   print "Enabling BMA282 power supply"
   b.configure_io_gpio_conf(GPIO_num = 9, IO_CONFIG = 0x1, DEB = '10ms', WAKE_LVL = 0)


def test_bma282(hwh = None):
   bma = spim.Spi(hwh = hwh, core = "aon_spi", cs = 16)
   bma.clk_cfg(clkdiv = 30, clk = 1)
   bmaChipID = int(bma.rx(1)[0])

   lsl = specs["BMA282_ID"][0]
   usl = specs["BMA282_ID"][1]
   get_pass_fail("BMA282_ID", bmaChipID, lsl, usl)

   return

def test_optical_sensors(hwh = None):
   # b = Beryl.Beryl(hwh = hwh, force_chan = "i2c")
   ied = intrigue.Intrigue(hwh = hwh)
   # adc_dict = b.build_adc_channel_dict()

   # Test Laser Safety
   print "\n%sTesting Laser Safety%s" % (bcolors.BOLD + bcolors.UNDERLINE, bcolors.ENDC)
   laserOnTime = [] # measured in seconds
   for i in range(5):
      laserOnTime.append(ied.laserSafetyTest())
   laserOnTimeAvg = round(numpy.mean(laserOnTime), 3)
   lsl = specs["LSR_SFTY_T_ON"][0]
   usl = specs["LSR_SFTY_T_ON"][1]
   get_pass_fail("LSR_SFTY_T_ON", laserOnTimeAvg, lsl, usl)

   print "\n%sTesting In-Ear Detect%s" % (bcolors.BOLD + bcolors.UNDERLINE, bcolors.ENDC)
   iedMeasurements = ied.intrigue_ied(suppress_print = True, num_samples = 10)

   for measurement in iedMeasurements:
      if measurement != "ignore":
         lsl = specs[measurement][0]
         usl = specs[measurement][1]
         get_pass_fail(measurement, iedMeasurements[measurement], lsl, usl)



   # b.toggle_supply(SUPPLY = 'LDO2', MODE = 'ACT0', ON = True)
   # b.configure_io_mfio_conf(MFIO_num = 11, IOCELL_CFG = 'PUSH_PULL', SUPPLY = 'VDDIOA')
   # time.sleep(0.2)
   # for i in range(100):
   #    b.start_adc_conversion('MAN', 1, 3)
   #    time.sleep(0.05)
   #    print "ADC RESULT: %f" % b.man_adc_read(1, adc_dict, 3, suppress_print = True)
   #    time.sleep(0.05)


   # for i in range(1000):
   #    b.configure_io_gpio_conf(GPIO_num = 11, IO_CONFIG = 0x1, DEB = '0ms', WAKE_LVL = 1)
   #    b.configure_io_gpio_conf(GPIO_num = 11, IO_CONFIG = 0x1, DEB = '0ms', WAKE_LVL = 0)
   #    time.sleep(.025)

   return


   ### VCSEL1_CATHODE ###
   #   Measure when I = 0mA
   #   Measure when I = 3.3mA

   ### VCSEL2_CATHODE ###
   #   Measure when I = 0mA
   #   Measure when I = 3.3mA

   # Measure TIA_VREF

   ### PD1 ###
   #   Measure TIA out, no-VCSEL
   #   Measure TIA out, with-VCSEL
   #   Measure temperature (forward voltage)

   ### PD2 ###
   #   Measure TIA out, no-VCSEL
   #   Measure TIA out, with-VCSEL
   #   Measure temperature (forward voltage)


def test_cricket():
   return

if __name__ == "__main__":
   init_dut()
   read_spec_limits()
   # hearst = hw.HW()
   test_beryl(hwh = None)
   # test_optical_sensors(hwh = hearst)
   # test_beryl(hwh = None)
   # bma282_vdd(hwh = hearst)
   # time.sleep(0.1)
   # test_bma282(hwh = hearst)