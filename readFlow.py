from MFC import MFC
import serial
import sys
import time
import binascii
CR =b'\r'
flow = MFC()
s = serial.Serial('/dev/ttyUSB0')



for i in range(10):
	s.write(flow.Flow_Read())

	a = s.read_until(CR)
#	print("read until cr  ", a)

	a_hex =  binascii.hexlify(a)    ## turns in to byte  b''  hex
#	print("hexlify", a_hex)

	a_hex_str = str(a_hex)
#	print("str(a_hex) a_hex", a_hex_str)

	str_hex =  a_hex_str[2:-7]
#	print("Change length", str_hex)

	un_hex = binascii.unhexlify(str_hex)
#	print("unhexlify", un_hex)

	un_hex_str = str(un_hex)
#	print("String unhex", un_hex_str)

	value = un_hex_str[6:-1]
#	print("Value =", value)

	fValue = float(value)
	print("Flow is ",fValue)

	time.sleep(1)
#s.write(flow.Sync_Read())

#for i in range(26):
 #       j =s.read_until(CR)
  #      print(j)


#s.write(flow.SetPoint_Read())
#b = s.read_until(CR)
#print(b)
s.close()

