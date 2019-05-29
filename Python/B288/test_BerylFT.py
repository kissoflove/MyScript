import BerylFT
import time

b = BerylFT.Beryl(channel = "UART1", port = '/dev/cu.usbserial-14112C')
adc_dict = b.build_adc_channel_dict()

adcChannel = 12
for i in range(30):
	b.start_adc_conversion('MAN', 1, adcChannel)
	print "***RESULT*** %f" % b.man_adc_read(1, adc_dict, adcChannel, suppress_print = True)

# print b.read_reg(reg = 0x1b02)
# b.write_reg(reg = 0x1200, data_out = 0x00)
# print b.read_reg(reg = 0x1b02)
# print b.read_reg(reg = 0x1b02)
# b.write_reg(reg = 0x1200, data_out = 0x00)
# print b.read_reg(reg = 0x1b02)