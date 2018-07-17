import crcmod.predefined
import binascii
import time
import datetime
import math

crc_func = crcmod.predefined.mkCrcFun('crc-ccitt-false')
T = float(298) # Kelvin
density_air     = float(0.001275)

density_oxygen  =float( 0.001429) # grams per cm ^3
density_hydrogen = float(0.0000899)

density_nitrogen = float(0.001251)

molarmass_oxygen = float(15.999) # grams per mol
molarmass_air = float(28.96)
molarmass_nitrogen =float(28.014)
molarmass_hydrogen = float(2.016)
R =  float(0.0821)   # atm*L/mol*K








def str2_dec_array(str):
	bin_str = binascii.a2b_qp(str)  ##  Converts command string to bytes  b'' for crc calculation

	hex_str = str.encode("utf-8").hex()   ##  Converts command string to hexadecimal string

	hex_crc_temp = hex(crc_func(bin_str))  ## Generates 2 Bytes for CRC in 0x#### format 
	hex_crc = hex_crc_temp[2:]		## Removes hex identifier 0x from  CRC

	hex_crc_full = hex_str+hex_crc+"0d"     ## Consolidates into hex string the Command string amending CRC and Carrige return ## 'CR' == 13 == 0d
	dec_array = []				## Initialize Empty Array

	dec_array = [int(hex_crc_full[i:i+2],16) for i in range(0,len(hex_crc_full),2)] ## Every two hex chars are converted to decimal and added to array 

	return dec_array


def format_Value(Value):                      ##  Ensures the Value sent is in the format 0.000  #.###
	formatted_Value = format(Value, '.3f')
	return formatted_Value


class MFC:

	gas_Type = ""
	molarmass = 0
	moles = 0
	density = 0
	Exp_flow_Rate =  0.000
	flow_Rate = 0.00
	flow_Rate_str = ""
	low_Flow = 0.100
	volume = 0
	volume_Transfered = 0
	volume_Remaining =0
	volume_Remaining_str = ""
	instantaneous_volume_Transfered = 0
	mass = 20;
	mass_Transfered = 13
	mass_Remaining = 0

	units_Type = ""

	
	time_Estimated = 0
	time_Estimated_str = ""
	time_Passed = 0
	time_Passed_str = ""
	time_Interval = 0
	time_Remaining = 0
	time_Remaining_str = ""
	temp_epoch_time = 0

	default_path = "/home/Dlab/MFC/Logs/temp_Logs/"
	default_type = ".txt"
	path_filename = ""

	Experiment_Start_Time = 0
	temp_epoch_Time = 0


	##  Varibles used to store read Commmnads   MAy be Faster then Calculating CRC each time flow is read for log 
	flow_Read_Cmd = []


	def Initilize(self):
		self.flow_Read_Cmd =  self.Flow_Read()

	def Volume_Remaining(self):
		self.volume_Remaining =   self.volume - self.volume_Transfered
		self.volume_Remaining_str = format_Value(self.volume_Remaining)
		return self.volume_Remaining

	def Volume_Transfered(self):
		volume_Temp = self.volume_Transfered + self.instantaneous_volume_Transfered
		self.volume_Transfered = volume_Temp
		print("Vol transfered", self.volume_Transfered)
	def Instantaneous_Volume_Transfered(self):
		if self.units_Type == "scc/m":
			self.instantaneous_volume_Transfered = (float(self.flow_Rate)/60) * float(self.time_Interval)
			print("instan vol transfered", self.instantaneous_volume_Transfered)

	def Mass_Remaining(self  ):
		self.mass_Remaining = self.mass - self.mass_Transfered
		return self.mass_Remaining

#	def Mass_Transfered(self, )


	def set_Exp_flow_Rate(self,Value):
		self.Exp_flow_Rate = format_Value(float(Value)) 


	def set_flow_Rate(self,Value):
		self.flow_Rate =format_Value(float(Value))

	def SetPoint_Read(self):
		str_Cmd ='?Setf'
		dec_array = str2_dec_array(str_Cmd)
		return dec_array

	def SetPoint_Write(self,Value):
		str_Cmd = '!Setf'+  format_Value(float(Value))  #Creates str from Cmd and Val 
		dec_array = str2_dec_array(str_Cmd) #str+crc+cr array 
		print (dec_array)
		return dec_array

	def Flow_Read(self):
		str_Cmd = '?Flow'
		dec_array = str2_dec_array(str_Cmd)
		return dec_array

	def Units_Read(self):
		str_Cmd = '?Unti'
		dec_array = str2_dec_array(str_Cmd)
		return dec_array

	def Units_Write(self,Value):
		str_Cmd = '!Unti'+ Value
		dec_array = str2_dec_array(str_Cmd)
		return dec_array

	def ValveState_Read(self):
		str_Cmd = '?Vlvi'
		dec_array = str2_dec_array(str_Cmd)
		return dec_array

	def ValveState_Write(self,Value):
		str_Cmd = '!Vlvi'+ Value
		dec_array = str2_dec_array(str_Cmd)
		return dec_array

	def Stream_Read(self):
		str_Cmd = '?Strm'
		dec_array = str2_dec_array(str_Cmd)
		return dec_array

	def Stream_Write(self, Value):
		str_Cmd = '!Strm'+ Value
		dec_array = str2_dec_array(str_Cmd)
		return dec_array
	def Sync_Read(self):
		str_Cmd = '?Sync'
		dec_array = str2_dec_array(str_Cmd)
		return dec_array



	def set_Gas(self, Gas):


		if  Gas =="Oxygen":
			self.gas_Type = Gas
			self.density = density_oxygen
			self.molarmass = molarmass_oxygen
			print(self.gas_Type)
			print(self.density)
		elif Gas == "Nitrogen":
			self.gas_Type = Gas
			self.density = density_nitrogen
			self.molarmass = molarmass_nitrogen
		elif Gas == "Hydrogen":
			self.gas_Type = Gas
			self.density = density_hydrogen
			self.molarmass = molarmass_hydrogen
		elif Gas == "Air": 
			self.gas_Type = Gas
			self.density = density_air
			self.molarmass = molarmass_air



	def set_Units(self, Units):
		if Units == "scc/m":
			self.units_Type = Units
			time_Estimated = float(self.volume) / (float(self.Exp_flow_Rate)/ 60)
			self.time_Estimated_str = self.time_decode(time_Estimated)
			print("set units")
			print(self.time_Estimated_str)
		if Units == "scc/s":
			self.units_Type = Units
		if Units == "g/m":
			self.units_Type = Units












	def set_Moles(self,Moles):
		self.moles = Moles


	def moles_to_ccm(self):
		print("moles to ccm")
		uMoles = float(self.moles)*(0.000001)
		grams = float(uMoles) * self.molarmass
		cubic_centimeters = grams / self.density
		self.volume = cubic_centimeters
		print(self.volume)
	#	return cubic_centimeters




	def time_of_flow(self,vol, units):

		if units == "scc/m":
			sec_total =vol/60
			if sec_total >= 60:
				mins = sec_total/60
				return mins
		else:
			sec = sec_total 
			return sec

#	def get_Pressure(Volume, Moles):
#        	pressure =( Moles * R * T)/ Volume
#        	return pressure






			## Tracking and Logging Functions ##

	def create_filename(self):
		now = datetime.datetime.now()
		now_str =str(now)
		self.path_filename = self.default_path + now_str + self.default_type
		f = open(self.path_filename,"a")
		f.write("Epoch_Time\tFlow_Rate\n ")
		self.Experiment_Start_Time = time.time()
		return self.path_filename

	def write_file(self):
		epoch_time = time.time()
	##	self.flow_Rate = self.flow_Read()   ## needs to be decoded
		epoch_time_str = str(epoch_time)
		flow_Rate_str = str(self.flow_Rate)
		f = open(self.path_filename, "a")
		f.write(epoch_time_str)
		f.write("\t")
		f.write(flow_Rate_str)
		f.write("\n")
		f.close()
		self.time_Interval = (epoch_time - self.Experiment_Start_Time)  - self.temp_epoch_time
		print("time int ", self.time_Interval)
		self.temp_epoch_time = (epoch_time- self.Experiment_Start_Time)
		self.Instantaneous_Volume_Transfered()
		self.time_Passed = epoch_time - self.Experiment_Start_Time
		self.Volume_Transfered()
		## add the time decoder here to create string time h m s
		self.time_Passed_str = self.time_decode(self.time_Passed)
		self.Volume_Remaining()
		if float(self.flow_Rate) <= 0.0001:
			flow_Rate_Temp = 0.000001
		else:
			flow_Rate_Temp = float(self.flow_Rate)

		self.time_Remaining =float( self.volume_Remaining) / (flow_Rate_Temp/60)
		self.time_Remaining_str = self.time_decode(self.time_Remaining)


	def time_decode(self,Sec):
		timespan = math.ceil(float(Sec))
		mins = math.floor(timespan/60)
		sec = timespan - (mins * 60)
		mins_str = str(mins)
		sec_str = str(sec)
		str_time =  mins_str+ " mins : " + sec_str + " secs"
		return str_time

