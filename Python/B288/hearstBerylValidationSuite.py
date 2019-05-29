#Author: Calvin Ryan <calvin_ryan@apple.com>
#Apple Inc. Audio Products Team


import serial
import serial.tools.list_ports
import uart
import time
import sys
import serial
import beryl_resetcode as rst
import Beryl as brl
import os
import gpio
import hw

def wiggle_pin_with_resetcode(handle):
    uart = serial.Serial('/dev/cu.usbmodem1421', 1200)

    beryl = handle

    beryl.configure_resetcode_decoder(EN_RSTCD = 0x1, RSTCD_SOURCE_SEL = 0x1)

    beryl.configure_io_mfio_conf(MFIO_num = 3, FUNC = 'RSTCD', IOCELL_CFG = 'INPUT', SUPPLY = 'VDD_1V8') #configure that RSTCD input
    beryl.configure_io_mfio_conf(MFIO_num = 2, FUNC = 'VCHG_DET', IOCELL_CFG = 'PUSH_PULL', SUPPLY = 'VDD_1V8')


    beryl.configure_io_mfio_conf(MFIO_num = 7, FUNC = 'GP_RSTCD', IOCELL_CFG = 'PUSH_PULL', SUPPLY = 'VDD_1V8') #configure that GP_RSTCD OUTPUT
    beryl.configure_io_mfio_conf(MFIO_num = 10, FUNC = 'COMMS_EN/DOCK_CONN', IOCELL_CFG = 'PUSH_PULL', SUPPLY = 'VDD_1V8')
    beryl.configure_io_mfio_conf(MFIO_num = 11, FUNC = 'SWD', IOCELL_CFG = 'PUSH_PULL', SUPPLY = 'VDD_1V8')
    beryl.configure_io_mfio_conf(MFIO_num = 12, FUNC = 'HOSTDFU', IOCELL_CFG = 'PUSH_PULL', SUPPLY = 'VDD_1V8')

    print beryl.read_resetcode()

    raw_input("Paused. Hit enter to continue.")

    reset = rst.resetcode_uart(0x30)
    uart.write(str(chr(reset[2])))
    uart.write(str(chr(reset[3])))

    time.sleep(.6)
    print beryl.read_resetcode()

    for i in range(33, 48):

        print i

        reset = rst.resetcode_uart(i)
        uart.write(str(chr(reset[2])))
        uart.write(str(chr(reset[3])))

        time.sleep(.6)
        print beryl.read_resetcode()

        reset = rst.resetcode_uart(0x20)
        uart.write(str(chr(reset[2])))
        uart.write(str(chr(reset[3])))

        time.sleep(.6)
        print beryl.read_resetcode()

def test_por_reset(handle):
    uart = serial.Serial('/dev/cu.usbmodem1421', 1200)

    beryl = handle

    beryl.configure_resetcode_decoder(EN_RSTCD = 0x1, RSTCD_SOURCE_SEL = 0x1)

    beryl.configure_io_mfio_conf(MFIO_num = 3, FUNC = 'RSTCD', IOCELL_CFG = 'INPUT', SUPPLY = 'VDD_1V8') #configure that RSTCD input
    beryl.configure_io_mfio_conf(MFIO_num = 2, FUNC = 'VCHG_DET', IOCELL_CFG = 'PUSH_PULL', SUPPLY = 'VDD_1V8')

    raw_input("Paused. Hit enter to continue.")

    print beryl.read_resetcode()

    reset = rst.resetcode_uart(0xA01)
    uart.write(str(chr(reset[2])))
    uart.write(str(chr(reset[3])))

    print beryl.read_resetcode()

def test_isink_pwm(handle):

    beryl = handle

    beryl.configure_io_mfio_conf(MFIO_num = 2, FUNC = 'ISINK3_PWM', IOCELL_CFG = "PUSH_PULL", SUPPLY = 'VDD_1V8')
    
    beryl.test_mode_enable()
    
    beryl.disable_isink_global()
    
    beryl.enable_isink_global()
    
    beryl.disable_isink(isink_num = 3)
    
    beryl.enable_isink(isink_num = 3, PWM_MODE = 'PWM', TRIG_SEL = 'SW')
    
    beryl.set_isink_current(isink_num = 3, current = 12000)
    

    beryl.config_isink_pwm(isink_num = 3, PWM_CYC = 1000000, PWM0 = 500000) #1Hz
    
    beryl.trigger_isink(isink_num = 3)

    raw_input("1Hz sent. Hit enter to continue.")
    beryl.config_isink_pwm(isink_num = 3, PWM_CYC = 500000, PWM0 = 250000) #2Hz
    raw_input("2Hz sent. Hit enter to continue.")
    beryl.config_isink_pwm(isink_num = 3, PWM_CYC = 200000, PWM0 = 100000) #5Hz
    raw_input("5Hz sent. Hit enter to continue.")
    beryl.config_isink_pwm(isink_num = 3, PWM_CYC = 100000, PWM0 = 50000) #10Hz
    raw_input("10Hz sent. Hit enter to continue.")
    beryl.config_isink_pwm(isink_num = 3, PWM_CYC = 50000, PWM0 = 25000) #20Hz
    raw_input("20Hz sent. Hit enter to continue.")
    beryl.config_isink_pwm(isink_num = 3, PWM_CYC = 20000, PWM0 = 10000) #50Hz
    raw_input("50Hz sent. Hit enter to continue.")
    beryl.config_isink_pwm(isink_num = 3, PWM_CYC = 10000, PWM0 = 5000) #100Hz
    raw_input("100Hz sent. Hit enter to continue.")
    beryl.config_isink_pwm(isink_num = 3, PWM_CYC = 1024, PWM0 = 512) #977Hz
    raw_input("1kHz sent. Hit enter to continue.")
    beryl.config_isink_pwm(isink_num = 3, PWM_CYC = 96 , PWM0 = 48) #10417Hz
    raw_input("10kHz sent. Hit enter to continue.")
    beryl.config_isink_pwm(isink_num = 3, PWM_CYC = 64, PWM0 = 32) #15625Hz
    print "16kHz sent"


def test_spmi_zero_write_gpio_hi_lo(handle):

    beryl = handle

    beryl.configure_io_mfio_conf(MFIO_num = 1, FUNC = 'GPIO', IOCELL_CFG = 'PUSH_PULL', SUPPLY = 'VDD_1V8')
    beryl.configure_io_gpio_conf(GPIO_num = 1, SPMI_TRANS_DLY_EN = 1, IO_CONFIG = 1, DEB = '0ms', WAKE_LVL = 1)
    beryl.configure_io_mfio_conf(MFIO_num = 2, FUNC = 'RTC_1HZ', IOCELL_CFG = 'PUSH_PULL', SUPPLY = 'VDD_1V8')

    raw_input("Press enter to set MFIO high over SPMI...")
    beryl.write_spmi_zero(data_out = 0x40)

    beryl.configure_io_gpio_conf(GPIO_num = 1, SPMI_TRANS_DLY_EN = 1, IO_CONFIG = 1, DEB = '0ms', WAKE_LVL = 0)

    beryl.configure_io_gpio_conf(GPIO_num = 1, SPMI_TRANS_DLY_EN = 1, IO_CONFIG = 1, DEB = '0ms', WAKE_LVL = 0)

    raw_input("Press enter to set MFIO low over SPMI...")
    beryl.write_spmi_zero(data_out = 0x40)

def test_lpclk_from_host(handle):

    beryl = handle

    beryl.configure_io_mfio_conf(MFIO_num = 1, FUNC = 'RTC_32K', IOCELL_CFG = 'PUSH_PULL', SUPPLY = 'VDD_1V8')
    beryl.set_32k_ref(SRC = 'HOST')

def test_gpadc(handle):

    beryl = handle

    SCANSlotDict = beryl.build_slot_channel_dict(channelList = [1, 10, 11])
    ADCDictionary = beryl.build_adc_channel_dict(csv = 'ADCChannelList.csv')

    raw_input("Press enter for manual agent read...")
    chan = 1 #VCHG in
    agent = 1 #will test man1 agent and/or scan1 agent
    beryl.start_adc_conversion(agent_type = 'MAN', agent_num = agent, channel = chan)
    beryl.man_adc_read(agent_num = agent, dict_in = ADCDictionary, channel = chan)

    raw_input("Press enter for scan agent read...")
    beryl.configure_adc_scan_agent_slots(agent_num = agent, slotChannels = SCANSlotDict)
    beryl.start_adc_conversion(agent_type = 'SCAN', agent_num = agent)
    beryl.scan_adc_read(agent_num = agent, adc_dict_in = ADCDictionary, slotChannels = SCANSlotDict)

def measure_ccadc_spmi_trig(handle):

    beryl = handle

    beryl.configure_io_mfio_conf(MFIO_num = 1, FUNC = 'CCTRIG', IOCELL_CFG = 'INPUT', SUPPLY = 'VDD_1V8')
    beryl.configure_io_mfio_conf(MFIO_num = 2, FUNC = 'GPIO', IOCELL_CFG = 'PUSH_PULL', SUPPLY = 'VDD_1V8')
    beryl.configure_io_gpio_conf(GPIO_num = 2, IO_CONFIG = 1, DEB = '0ms', WAKE_LVL = 0)
    beryl.configure_ccadc(GLOBAL_EN = 0x1, HOSTOFF_GLOBAL_EN = 0x1)

    #raw_input("Press enter for SPMI/MFIO CCADC trigger...")

    time.sleep(.2)

    beryl.configure_io_gpio_conf(GPIO_num = 2, IO_CONFIG = 1, DEB = '0ms', WAKE_LVL = 1)

    val = beryl.read_ccadc()[0]

    beryl.configure_io_gpio_conf(GPIO_num = 2, IO_CONFIG = 1, DEB = '0ms', WAKE_LVL = 1)

    return val

def measure_ccadc(handle):

    beryl = handle

    vals = beryl.read_ccadc()

    return vals


def test_ccadc(handle):
    beryl = handle

    filename = 'CCADC' + str(time.time()) + '.csv' 
    doc3 = open(filename, 'w')

    beryl.test_mode_enable()

    beryl.write_reg(reg = 0x1800, data_out = [0x1]) #USE EXTERNAL CLOCK SOURCE!

    ###### From Xtal ######
    beryl.write_reg(reg = 0x284C, data_out = [0x6F]) #Sets battery target voltage
    beryl.write_reg(reg = 0x2847, data_out = [0x1]) #Sets the VBAT_GOOD_THR to 2.9V
    
    #Sets the charge current to 3C
    beryl.write_reg(reg = 0x2848, data_out = [0x18])
    beryl.write_reg(reg = 0x2849, data_out = [0x18])
    
    #Sets the pre-charge current to 0.1C
    beryl.write_reg(reg = 0x2846, data_out = [0x1])
    beryl.write_reg(reg = 0x2847, data_out = [0x1])
    

    #################

    beryl.write_reg(reg = 0x1808, data_out = [0x0])
    beryl.write_reg(reg = 0x1809, data_out = [0xA]) #set UVLO thresh to 2.5V (minimum)

    beryl.write_reg(reg = 0x4166, data_out = [0x7E])#adcram space as fifo2
    beryl.write_reg(reg = 0x415B, data_out = [0x01])#enable ccadc measurement schedular

    beryl.write_reg(reg = 0x48C0, data_out = [0x0]) #clear CCADC_EVENT

    raws = []
    fifos = []
    counts = []
    nows = []

    sample_cnt = 0
    now = 0

    start = time.time()

    beryl.write_reg(reg = 0x41C9, data_out = [0x07]) #clear and enable FIFO2

    raws.append(beryl.read_ccadc_accum()) #record the starting accumulator value

    while (now < 600): #Run for 10 minutes
        beryl.configure_ccadc(TRIGGER_TYPE = 0x1, GLOBAL_EN = 0x1, IN_FIFO_EN = 0X1, HOSTOFF_GLOBAL_EN = 0x1, ACCUM_EN = 0x1, PREAMP_GAIN = 0x2) #Get 256 more FIFO samples
        for sample_cnt in range(256):
            counts.append(sample_cnt) #put the current fifo count in a list
            sample_cnt = beryl.read_reg(reg = 0x41CA) #update the current sample account in the fifo 
            print sample_cnt
            fifos.append(beryl.read_reg(reg = 0x41CC)) #put the fifo value in a list
            now = time.time() - start #update the time
            print now
            nows.append(now)#put the current time in a list

    beryl.write_reg(reg = 0x4800, data_out = [0x00]) #disable the ccadc

    raws.append(beryl.read_ccadc_accum()) #record the ending accumulator value

    #store the absolute time, fifo counts, and corresponding fifo values in the doct 
    doc3.write('time' + ',' + 'fifo count' + ',' + 'fifo value'+ '\n')
    for i in range(len(fifos)):
        doc3.write(str(nows[i]) + ',' + str(counts[i])+ ',' + str(fifos[i]) + '\n')
    
    doc3.write('\n\n')
    
    #store the starting and ending raw accumulator value in the spreadsheet.
    for i in range(len(raws)):
        doc3.write(str(raws[i]) + '\n')
        
    doc3.close()

def test_adamstown_en(handle):
    beryl = handle

    beryl.configure_io_mfio_conf(MFIO_num = 10, FUNC = 'GPIO', IOCELL_CFG = 'PUSH_PULL', SUPPLY = 'VDD_1V8')
    beryl.configure_io_gpio_conf(GPIO_num = 10, SPMI_TRANS_DLY_EN = 1, IO_CONFIG = 1, DEB = '0ms', WAKE_LVL = 1)
    beryl.configure_io_mfio_conf(MFIO_num = 2, FUNC = 'RTC_1HZ', IOCELL_CFG = 'PUSH_PULL', SUPPLY = 'VDD_1V8') #heartbeat for funsies

    raw_input("Press enter to set MFIO10 high over SPMI...")
    beryl.write_spmi_zero(data_out = 0x48)

    beryl.configure_io_gpio_conf(GPIO_num = 10, SPMI_TRANS_DLY_EN = 1, IO_CONFIG = 1, DEB = '0ms', WAKE_LVL = 0)

    raw_input("Press enter to set MFIO10 low over SPMI...")
    beryl.write_spmi_zero(data_out = 0x48)

def test_button(handle):

    beryl = handle

    beryl.test_mode_enable()

    beryl.force_power_mode(FORCE_STATE = 'ACT0')

    beryl.set_32k_ref(SRC = 'AUTO')
    
    beryl.configure_io_mfio_conf(MFIO_num = 8, FUNC = 'RESET_IN/BUTTON', IOCELL_CFG = 'PU_OD_NMOS', SUPPLY = 'VDD_1V8', SENS = 'ANY_EDGE', POLARITY = 1)
    beryl.configure_io_mfio_conf(MFIO_num = 9, FUNC = 'RESET_IN/BUTTON', IOCELL_CFG = 'PU_OD_NMOS', SUPPLY = 'VDD_1V8', SENS = 'ANY_EDGE', POLARITY = 1)
    beryl.configure_io_mfio_conf(MFIO_num = 13, FUNC = 'RESET_IN/BUTTON', IOCELL_CFG = 'PU_OD_NMOS', SUPPLY = 'VDD_1V8', SENS = 'ANY_EDGE', POLARITY = 1)


    beryl.configure_irq_masks(IRQ_BTN3_DBL = 0x1, IRQ_BTN2_DBL = 0x1, IRQ_BTN1_DBL = 0x1, IRQ_BUTTON_1 = 0x0, IRQ_BUTTON_2 = 0x0, IRQ_BUTTON_3 = 0x0,
        IRQ_GPIO8 = 0x1, IRQ_GPIO7 = 0x1, IRQ_GPIO6 = 0x1, IRQ_GPIO5 = 0x1, IRQ_GPIO4 = 0x1, IRQ_GPIO3 = 0x1, IRQ_GPIO2 = 0x1, IRQ_GPIO1 = 0x1, IRQ_GPIO13 = 0x1,
        IRQ_GPIO12 = 0x1, IRQ_GPIO11 = 0x1, IRQ_GPIO10 = 0x1, IRQ_GPIO9 = 0x1)

    
    beryl.write_reg(reg = 0x6000, data_out = 0x1f) #IRQ handler active
    beryl.write_reg(reg = 0x6030, data_out = 0x46) #read-to-clear mode, repeats command 3 times in case of nack
    beryl.write_reg(reg = 0x6031, data_out = 0x00) #disable arbitration clock timeout
    beryl.write_reg(reg = 0x602F, data_out = 0x07) #bypass HW enable
    beryl.write_reg(reg = 0x6035, data_out = 0x0F) #keep SCLK on
    beryl.write_reg(reg = 0x6020, data_out = 0x11) #enable slave id
    beryl.write_reg(reg = 0x6100, data_out = 0x0D) #enable IRQ handler
    beryl.write_reg(reg = 0x122C, data_out = 0xFD) #disable all IRQH handlers except for io handler
    beryl.write_reg(reg = 0x122D, data_out = 0xFF) #disable all other IRQH handlers
    beryl.write_reg(reg = 0x1220, data_out = 0x00) #clear mode to read/write to clear
    beryl.write_reg(reg = 0x1461, data_out = 0x00) #RCS time out disable


    beryl.read_event(all = True)
    raw_input("Press enter to read all events again...")

    beryl.read_event(all = True)
    raw_input("Press enter to read all events again...")

    beryl.read_event(all = True)
    raw_input("Press enter to read all events again...")

    beryl.read_event(all = True)
    raw_input("Press enter to read all events again...")

    beryl.read_event(all = True)
    raw_input("Press enter to read all events again...")

    

def test_sam(handle):

    beryl = handle

    beryl.test_mode_enable()

    raw_input("Press enter to check 5 bit SAM...")

    #check default pointer1 address
    print '2x 16 bit read to check default pointer1 address:'
    beryl.read_reg(reg = 0x6202, length = 1, ret_addr = True)
    beryl.read_reg(reg = 0x6203, length = 1, ret_addr = True)
    #check default pointer2 address
    print '2x 16 bit read to check default pointer1 address:'
    beryl.read_reg(reg = 0x6204, length = 1, ret_addr = True)
    beryl.read_reg(reg = 0x6205, length = 1, ret_addr = True)
    #check default pointer3 address
    print '2x 16 bit read to check default pointer1 address:'
    beryl.read_reg(reg = 0x6206, length = 1, ret_addr = True)
    beryl.read_reg(reg = 0x6207, length = 1, ret_addr = True)
    print 

    #RW set pointer1 top 0x1900
    print "5 bit write... "
    beryl.write_reg(reg = 0b00011, data_out = 0x19, addr_len = 5)
    print "5 bit write... "
    beryl.write_reg(reg = 0b00010, data_out = 0x00, addr_len = 5)
    #RW set pointer2 top 0x1400
    print "5 bit write... "
    beryl.write_reg(reg = 0b00101, data_out = 0x14, addr_len = 5)
    print "5 bit write... "
    beryl.write_reg(reg = 0b00100, data_out = 0x00, addr_len = 5)
    #RW set pointer3 top 0x2000
    print "5 bit write... "
    beryl.write_reg(reg = 0b00111, data_out = 0x20, addr_len = 5)
    print "5 bit write... "
    beryl.write_reg(reg = 0b00110, data_out = 0x00, addr_len = 5)
    print


    #verify pointer1 address was set by SAM write
    print '2x 16 bit read to check written pointer1 address:'
    beryl.read_reg(reg = 0x6202, length = 1, ret_addr = True)
    beryl.read_reg(reg = 0x6203, length = 1, ret_addr = True)
    #verify pointer2 address was set by SAM write
    print '2x 16 bit read to check written pointer2 address:'
    beryl.read_reg(reg = 0x6204, length = 1, ret_addr = True)
    beryl.read_reg(reg = 0x6205, length = 1, ret_addr = True)
    #verify pointer3 address was set by SAM write
    print '2x 16 bit read to check written pointer3 address:'
    beryl.read_reg(reg = 0x6206, length = 1, ret_addr = True)
    beryl.read_reg(reg = 0x6207, length = 1, ret_addr = True)
    print

    for i in range(0,7):
        #RR
        print "5 bit read: "
        addr5 = 0b01000 + i 
        beryl.read_reg(reg = addr5, length = 1, addr_len = 5, ret_addr = True) #pointer1[15:3], reg[2:0]
        print "16 bit read: "
        addr16 = 0x1900 + i 
        beryl.read_reg(reg = addr16, length = 1, ret_addr = True)
        print
        
    for i in range(0,7):
        #RR
        print "5 bit read: "
        addr5 = 0b10000 + i 
        beryl.read_reg(reg = addr5, length = 1, addr_len = 5, ret_addr = True) #pointer1[15:3], reg[2:0]
        print "16 bit read: "
        addr16 = 0x1400 + i 
        beryl.read_reg(reg = addr16, length = 1, ret_addr = True)
        print

    for i in range(0,7):
        #RR
        print "5 bit read: "
        addr5 = 0b11000 + i 
        beryl.read_reg(reg = addr5, length = 1, addr_len = 5, ret_addr = True) #pointer1[15:3], reg[2:0]
        print "16 bit read: "
        addr16 = 0x2000 + i 
        beryl.read_reg(reg = addr16, length = 1, ret_addr = True)
        print


    print "testing 5 bit writes"

    beryl.read_reg(reg = 0b01000, addr_len = 5, ret_addr = True)
    print "5 bit write - pointer 1 to 0x01..."
    beryl.write_reg(reg = 0b01000, data_out = 0x01, addr_len = 5)
    beryl.read_reg(reg = 0b01000, addr_len = 5, ret_addr = True)

    beryl.read_reg(reg = 0b10000, addr_len = 5, ret_addr = True)
    print "5 bit write - pointer 2 to 0x01..."
    beryl.write_reg(reg = 0b10000, data_out = 0x01, addr_len = 5)
    beryl.read_reg(reg = 0b10000, addr_len = 5, ret_addr = True)

    beryl.read_reg(reg = 0b11000, addr_len = 5, ret_addr = True)
    print"5 bit write - pointer 3 to 0x01..."
    beryl.write_reg(reg = 0b11000, data_out = 0x01, addr_len = 5)
    beryl.read_reg(reg = 0b11000, addr_len = 5, ret_addr = True)


    raw_input("Press enter to check 8 bit SAM...")

    #check default pointer addresses
    print '16 bit read to check default EXT_READ address:'
    print beryl.read_reg(reg = 0x6200, length = 1, ret_addr = True)
    print '16 bit read to check default EXT_WRITE address:'
    print beryl.read_reg(reg = 0x6201, length = 1, ret_addr = True)
    print 

    #RW set pointers to 0x1900
    print "5 bit write... "
    beryl.write_reg(reg = 0b00000, data_out = 0x19, addr_len = 5)
    print "5 bit write... "
    beryl.write_reg(reg = 0b00001, data_out = 0x19, addr_len = 5)
    print

    #check written pointer addresses
    print '16 bit read to check default EXT_READ address:'
    print beryl.read_reg(reg = 0x6200, length = 1, ret_addr = True)
    print '16 bit read to check default EXT_WRITE address:'
    print beryl.read_reg(reg = 0x6201, length = 1, ret_addr = True)
    print 

    for i in range(0,255):
        #ERR
        print "8 bit read: "
        addr8 = i
        print beryl.read_reg(reg = addr8, length = 1, addr_len = 8, ret_addr = True)
        print "16 bit read: "
        addr16 = 0x1900 + i
        print beryl.read_reg(reg = addr16, length = 1, ret_addr = True)
        print

    print "Check 8 bit write functionality..."

    print "8 bit read: "
    print beryl.read_reg(reg = 0x00, length = 1, addr_len = 8, ret_addr = True)

    raw_input("trigger now")

    print "8 bit write... "
    beryl.write_reg(reg = 0x00, data_out = 0x5, addr_len = 8)

    raw_input("wait")

    print "8 bit read: "
    print beryl.read_reg(reg = 0x00, length = 1, addr_len = 8, ret_addr = True)



def configure_hearst_for_rcs():
    h = hw.HW()
    h.write(addr = 0x44010040, data = 0xFFFFFFFF) #enable all RCS slaves

    h.write(addr = 0x44010000, data = 0x00004321) #enable SW queues and set priority
    h.write(addr = 0x44010004, data = 0x00000312) #enable HW queues and set priority

    #enable all hearst HW 0 interrupt bits
    h.write(addr = 0x44010a20, data = 0xFFFFFFFF)
    h.write(addr = 0x44010a24, data = 0xFFFFFFFF)
    h.write(addr = 0x44010a28, data = 0xFFFFFFFF)
    #enable all hearst HW1 interrupt bits
    h.write(addr = 0x44010b20, data = 0xFFFFFFFF)
    h.write(addr = 0x44010b24, data = 0xFFFFFFFF)
    h.write(addr = 0x44010b28, data = 0xFFFFFFFF)

    #enable all hearst SW0 interrupt bits
    h.write(addr = 0x44010420, data = 0xFFFFFFFF)
    h.write(addr = 0x44010424, data = 0xFFFFFFFF)
    h.write(addr = 0x44010428, data = 0xFFFFFFFF)
    h.write(addr = 0x4401042c, data = 0xFFFFFFFF)
    h.write(addr = 0x44010430, data = 0xFFFFFFFF)
    h.write(addr = 0x44010434, data = 0xFFFFFFFF)
    h.write(addr = 0x44010438, data = 0xFFFFFFFF)
    h.write(addr = 0x4401043c, data = 0xFFFFFFFF)
    h.write(addr = 0x44010440, data = 0xFFFFFFFF)

    #enable SW1 interrupt bits
    h.write(addr = 0x44010520, data = 0xFFFFFFFF)
    h.write(addr = 0x44010524, data = 0xFFFFFFFF)
    h.write(addr = 0x44010528, data = 0xFFFFFFFF)
    h.write(addr = 0x4401052c, data = 0xFFFFFFFF)
    h.write(addr = 0x44010530, data = 0xFFFFFFFF)
    h.write(addr = 0x44010534, data = 0xFFFFFFFF)
    h.write(addr = 0x44010538, data = 0xFFFFFFFF)
    h.write(addr = 0x4401053c, data = 0xFFFFFFFF)
    h.write(addr = 0x44010540, data = 0xFFFFFFFF)

    #enable SW2 interrupt bits
    h.write(addr = 0x44010620, data = 0xFFFFFFFF)
    h.write(addr = 0x44010624, data = 0xFFFFFFFF)
    h.write(addr = 0x44010628, data = 0xFFFFFFFF)
    h.write(addr = 0x4401062c, data = 0xFFFFFFFF)
    h.write(addr = 0x44010630, data = 0xFFFFFFFF)
    h.write(addr = 0x44010634, data = 0xFFFFFFFF)
    h.write(addr = 0x44010638, data = 0xFFFFFFFF)
    h.write(addr = 0x4401063c, data = 0xFFFFFFFF)
    h.write(addr = 0x44010640, data = 0xFFFFFFFF)    


def turn_on_leds(handle):

    beryl = handle

    for i in range(1,5):
        beryl.configure_io_mfio_conf(MFIO_num = i, FUNC = 'GPIO', IOCELL_CFG = 'PUSH_PULL', SUPPLY = 'VDD_1V8')
        beryl.configure_io_gpio_conf(GPIO_num = i, IO_CONFIG = 1, DEB = '0ms', WAKE_LVL = 1)

        
def toggle_nreset_out(handle):
    beryl = handle

    beryl.test_mode_enable()
    beryl.write_reg(reg = 0x130E, data_out = [0x01])
    beryl.write_reg(reg = 0x1461, data_out = [0x1E])
    beryl.toggle_supply(MODE = 'HOSTOFF', SUPPLY = 'LDO0', ON = True)
    beryl.force_power_mode(FORCE_STATE = "HOSTOFF")
    beryl.configure_io_mfio_conf(MFIO_num = 1, FUNC = 'RTC_1HZ', IOCELL_CFG = 'PUSH_PULL', SUPPLY = 'VDD_1V8') #heartbeat for funsies

    print "Now in HOSTOFF w/ NRESET_OUT driven low."
    
    raw_input("Press enter to return to ACT0 and stop driving NRESET_OUT.")

    beryl.force_power_mode(FORCE_STATE = "ACT0")
    beryl.configure_io_mfio_conf(MFIO_num = 1, FUNC = 'GPIO', IOCELL_CFG = 'PUSH_PULL', SUPPLY = 'VDD_1V8') #heartbeat for funsies

def toggle_psoc_comms_sel(handle):
    beryl = handle

    beryl.configure_io_mfio_conf(MFIO_num = 2, FUNC = 'GPIO', IOCELL_CFG = 'PUSH_PULL', SUPPLY = 'VDD_1V8')
    beryl.configure_io_gpio_conf(GPIO_num = 2, IO_CONFIG = 1, DEB = '0ms', WAKE_LVL = 0)
    beryl.configure_io_gpio_conf(GPIO_num = 2, IO_CONFIG = 1, DEB = '0ms', WAKE_LVL = 1)
    time.sleep(.01)
    beryl.configure_io_gpio_conf(GPIO_num = 2, IO_CONFIG = 1, DEB = '0ms', WAKE_LVL = 0)
    print "psoc now in bootloader mode."


########################################################################################################################

if __name__ == "__main__":
    #configure_hearst_for_rcs() #tested spmi, no i2c available
    
    #h = hw.HW()

    beryl = brl.Beryl(force_chan = 'i2c')
    beryl.verbose = True
    #wiggle_pin_with_reset_code(handle = beryl) #need serial -> UART device to generate resetcodes!
    #test_isink_pwm(handle = beryl) #tested SPMI, tested i2c
    #test_por_reset(handle = beryl) #need serial -> UART device to generate resetcodes!
    #test_lpclk_from_host(handle = beryl) 
    #test_spmi_zero_write_gpio_hi_lo(handle = beryl) #tested spmi, no i2c available
    #test_gpadc(handle = beryl) #tested spmi, i2c
    test_ccadc(handle = beryl) #tested i2c, tested spmi
    #test_adamstown_en(handle = beryl) #tested spmi, no i2c available
    #test_button(handle = beryl)
    #test_sam(handle = beryl)
    #turn_on_leds(handle = beryl)

    #This is a sequence to program/reprogram PSOC #####
    #toggle_psoc_comms_sel(handle = beryl)
    #toggle_nreset_out(handle = beryl)

