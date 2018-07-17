from MFC import MFC
import serial



flow = MFC()
s = serial.Serial("/dev/ttyUSB0")
val = input("Enter SetPoint  ")
s.write(flow.SetPoint_Write(val))

s.close()
