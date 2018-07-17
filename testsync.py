from MFC import MFC
import serial
CR =b'\r'
flow = MFC()
s = serial.Serial('/dev/ttyUSB0')
a = s.read_until(CR)
print(a)
s.write(flow.Sync_Read())

for i in range(26):
	j =s.read_until(CR)
	print(j)


s.write(flow.SetPoint_Read())
b = s.read_until(CR)
print(b)
s.close()
