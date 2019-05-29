import serial
import datetime
import argparse
import numpy as np

class SerialPort():
    def __init__(self,PortName,BaudRate=115200,TimeOut=6):
        try:
            self.port = serial.Serial(PortName, baudrate=BaudRate,timeout=TimeOut)
        except:
            raise RuntimeError("Open serial port error: %s", PortName)

    def close(self):
        self.port.flush()
        self.port.close()

    def sendcmd(self, cmd):
        if self.port.is_open:
            self.port.flushInput()
            self.port.flushOutput()
            print datetime.datetime.now().strftime("\n%Y-%m-%d %H:%M:%S.%f"), '    ', cmd,
            self.port.write(cmd + '\n')
        else:
            raise RuntimeError("Cmd send error, port not open: %s", self.port.name)

    def readResponse(self,terminator=']'):
        res = self.port.read_until(terminator)
        print datetime.datetime.now().strftime("\n%Y-%m-%d %H:%M:%S.%f"), '    ', res
        if terminator in res:
            return res
        else:
            raise RuntimeError("Error: timeout %s",res)

    def send_read(self,cmd,terminator=']'):
        self.sendcmd(cmd)
        return self.readResponse(terminator)

def Accelerometer_Test(portname):
    serialport = SerialPort(portname)

    cmd = "accel stream 100000 10"
    res = serialport.send_read(cmd)

    if "Error" not in res:
        axis_x = []
        axis_y = []
        axis_z = []
        res = res.replace('\r','')
        arr = res.split('\n')

        for subarr in arr:
            if 'sample:' in subarr:
                axis_x.append(int(subarr.split('x:')[1].split('y:')[0].strip()))
                axis_y.append(int(subarr.split('y:')[1].split('z:')[0].strip()))
                axis_z.append(int(subarr.split('z:')[1].split('timestamp:')[0].strip()))
    else:
        raise RuntimeError('Error: cmd %s response invalid',cmd)

    print ""
    print 'Accel average x: %f, std x: %f' % (np.average(axis_x), np.std(axis_x))
    print 'Accel average y: %f, std y: %f' % (np.average(axis_y), np.std(axis_y))
    print 'Accel average z: %f, std y: %f' % (np.average(axis_z), np.std(axis_z))
    print 'Accel magnitude: %f' % (np.sqrt(np.square(np.average(axis_x)) + np.square(np.average(axis_y)) + np.square(np.average(axis_z))))
    print ""

    serialport.close()


if __name__ == '__main__':
    print 'Version: PROTO1_V1'
    parser = argparse.ArgumentParser(description='Accelerate Test.')
    parser.add_argument('-p', '--serialport', help='Serial port name.', type=str, default=False, required=True)
    parser.add_argument('-s', '--selftest',help='Accelerate Self Test', type=bool, default=False, required=False)

    args = parser.parse_args()

    if not args.selftest:
        Accelerometer_Test(args.serialport)