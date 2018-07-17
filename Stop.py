import MFC
import serial

s = serial.Serial('/dev/ttyUSB0')
flow = MFC()
s.write(flow.Stream_Write('On'))
s.write(flow.SetPoint_Write('0.000'))
s.close()
