import BerylFT
import sys
import time 

b = BerylFT.Beryl(channel = "UART1", port = sys.argv[1])
b.configure_ccadc(GLOBAL_EN = 0x1)

start_cum 	= b.read_ccadc()
startTime = time.time()
end_cum 	= b.read_ccadc()
eTime = time.time() - startTime

print "Average Current: %f mA " % ((end_cum - start_cum)*3600/eTime)
