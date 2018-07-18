import sys
from MFC import MFC
import serial
from guizero import App, TextBox,  Box, PushButton, Text, Window, MenuBar, warn, yesno, ListBox
import  ChkUsrInputX
import binascii

Experiment_in_Progress = False
file_name = ""
count= 0
flow = MFC()
flow.Initilize()
CR =b'\r'
s = serial.Serial('/dev/ttyUSB0')              ## Open Serial port
s.write(flow.Stream_Write('Echo'))


def get_flow_Rate():
	s.write(flow.flow_Read_Cmd)               ## Writes Read flow command 
	a = s.read_until(CR)			## Reads valuw back until cr
	a_hex =  binascii.hexlify(a)    ## turns in to byte  b''  hex
	a_hex_str = str(a_hex)
	str_hex =  a_hex_str[2:-7]
	un_hex = binascii.unhexlify(str_hex)
	un_hex_str = str(un_hex)
#	print("String unhex", un_hex_str)
	if un_hex_str[2] == 'F':
		value = un_hex_str[6:-1]
		flow_Value = float(value)
		flow.set_flow_Rate(flow_Value)
		return flow_Value
	else:
		get_flow_Rate()
		return 0



## Log Functions
def enable_Log():	# Opens Logging Window
	logWin.show()
	logWin.enable()



## Gui Functions

def ask_to_close():     # Propmts User before Program Exits
	if yesno("Exit", "Do you want to quit?"):
		gui.destroy()
	else:
		return

## Eperiment Functions

          # Begin Experiment Configuration   Starts with choosing Gas

def close_Exp_Conf():
	transfer_mol_Window.disable()
	transfer_mol_Window.hide()
	gui.show()

def select_gas():
	gui.hide()
	gasBox.enable()
	gasBox.show()
	moleBox.disable()
	moleBox.hide()
	transfer_mol_Window.show()
	transfer_mol_Window.enable()

def set_gas():
	flow.set_Gas(gas_list.value)      # Sets class instance gas


def select_moles():
	set_gas()

	gasBox.disable()
	gasBox.hide()

	flowBox.disable()
	flowBox.hide()

	gas_text.value = flow.gas_Type
	moleBox.enable()
	moleBox.show()


def set_moles():
	if ChkUsrInputX.chkUsrNumMole(enter_moles_textbox.value):
		flow.set_Moles(enter_moles_textbox.value)
		flow.moles_to_ccm()
		select_flow()
	else:
		warn("Oops", "Not a Valid Number")


		select_moles()
		print("hide moles")
def select_flow():
	confirmBox.disable()
	confirmBox.hide()
	moleBox.disable()
	moleBox.hide()
	ccm_gas_text.value =flow.volume
	flowBox.enable()
	flowBox.show()

def set_Exp_Flow():
	if ChkUsrInputX.chkUsrNumSetPoint(flow_rate_textbox.value):
		print('Flow accepted is ',flow_rate_textbox.value)
		flow.set_Exp_flow_Rate(flow_rate_textbox.value)

	else:
		warn("Oops", "Not a Valid Number")
		select_flow()

def set_Flow():
	Cmd =flow.SetPoint_Write(flow.Exp_flow_Rate)
	s.write(Cmd)
	print("setting flow at", flow.Exp_flow_Rate)
def set_units():
	flow.set_Units(exp_units_list.value)

def confirm_Experiment():
	set_Exp_Flow()
	set_units()
	flowBox.disable()
	flowBox.hide()
	InitBox.disable()
	InitBox.hide()


	confirm_moles_text.value = flow.moles
	confirm_flow_rate_text.value = flow.Exp_flow_Rate


	confirm_time_est_text.value = flow.time_Estimated_str

	confirmBox.enable()
	confirmBox.show()

def prime_Valve():
	confirmBox.disable()
	confirmBox.hide()
	set_Flow()
	primeBox = Box(transfer_mol_Window)
	InitBox.enable()
	InitBox.show()
	primeBox.after(5000,Initilize_Valve)
def Initilize_Valve():
	print("Initialize Valve")
	waitBox = Box(transfer_mol_Window)
	waitBox.after(1000,wait_for_Flow)

def wait_for_Flow():
	global count
	prime = get_flow_Rate()

	if int(prime*100)<=1:
		count = count +1
		print(count)
		Initilize_Valve()
		return
	elif int(prime*100)>= 1:
		RUN_Experiment()
		return

def RUN_Experiment():
	
	global  Experiment_in_Progress

	Experiment_in_Progress = True

	InitBox.disable()
	InitBox.hide()
	close_Exp_Conf()
	print("Running")



	progress_Win.enable()
	progress_Win.show()

	abort_exp_button.enable()
	abort_exp_button.show()

	flow.create_filename()
	updateBox =Box(progressBox)
	updateBox.repeat(1000,Update_Progress)



def Write_Log():
	if Experiment_in_Progress== True:
		flow.write_file()
		print("Write_File")
	else:
		return

def Update_Progress():
	global Experiment_in_Progress
	get_flow_Rate()                    ## Turn off if no Serial
	flowrate_text.value = flow.flow_Rate
	Write_Log()

	time_remain_text.value = flow.time_Remaining_str
	volume_remain_text.value = flow.volume_Remaining_str
	if flow.volume_Remaining <= 0.001:
		STOP_Flow()
		Experiment_in_Progress = False
		progress_Win.disable()
		progress_Win.hide()
		finished_Win.enable()
		finished_Win.show()

def STOP_Flow():
	s.write(flow.SetPoint_Write("0.000"))
	print("Stop Flow")
	s.write(flow.Stream_Write('On'))
def ABORT_Experiment():

	global logbool
	STOP_Flow()    ##  Set Flow to Zero on Abort
	progress_Win.disable()
	progress_Win.hide()
#	progressBox.cancel(Update_Progress)
	progressBox.disable
	progressBox.hide()
	progress_Win.destroy()
	progressBox.destroy()
	logbool= 0
	print(logbool)
	logBox.destroy()
	STOP_Flow()
	gui.show()
gui = App(title = "Micro Trak 101 Mass Flow Controller", height = 300, width = 500)   # Creates Main Window Object

## Logger Widgets

#logWin =Window(gui, title = "Log Window", visible = 0)        #  Creates  Log Window Object
#logWin.disable()
#openLogWinButton = PushButton(gui, text ="Log Win", command =enable_Log )   # PushButton to open Log Window  for Gui Window

#closeLog_logwin_button = PushButton(logWin, text ="Close Log", command = close_Log )   # PushButton to close log for Log Window

## Eperiment Widgets
transfer_mol_Window = Window(gui, title = "Transfer Micro Mol",height=300, width = 500, visible = 0)

                    ## Choose Gas Widgests

gasBox = Box(transfer_mol_Window, visible = 0)
gas_list = ListBox(gasBox, items =["Air", "Oxygen", "Hydrogen", "Nitrogen"], selected = "Air", scrollbar = True)
select_gas_button = PushButton(gasBox, text = "Next",command = select_moles)
cancel_exp_button = PushButton(gasBox, text = "Cancel" , command = close_Exp_Conf)
		    ## Choose micro moles
moleBox = Box(transfer_mol_Window, visible = 0)
gas_text =Text(moleBox, text = "" )
enter_moles_button = PushButton(moleBox, text = "Next", command = set_moles)
enter_moles_textbox =TextBox(moleBox,text = 500)
back_moles_button  = PushButton(moleBox, text = "Back", command = select_gas)

		 ## Choose flow rate

flowBox = Box(transfer_mol_Window, visible = 0)
ccm_gas_text = Text(flowBox, text = 0 )
exp_units_list = ListBox(flowBox, items = [ "scc/s", "scc/m", "kg/m", "g/m"], selected = "scc/m", scrollbar = True  )
back_flow_button = PushButton(flowBox, text = "Back",command = select_moles )
confirm_exp_button = PushButton(flowBox, text = "Confirm", command = confirm_Experiment)
flow_rate_textbox = TextBox(flowBox, text = 0.100  )

		## Confirm Experiment ##
confirmBox = Box(transfer_mol_Window, visible = 0)
RUN_button = PushButton(confirmBox, text = "Run", command = prime_Valve)
confirm_flow_rate_text = Text(confirmBox)
confirm_back_button = PushButton(confirmBox, text = "Back", command = select_flow)
confirm_moles_text = Text(confirmBox)
confirm_time_est_text = Text(confirmBox)


		## Initilize Experiment
InitBox = Box(transfer_mol_Window, visible =0)
InitTextA = Text(InitBox, text = 'Initilizing valve.')
InitTextB = Text(InitBox, text = 'May take up to 45 sec for lowest flow')
InitCancelButton =PushButton(InitBox,text = 'Cancel', command = ABORT_Experiment)

		## Experiment Progres Window

progress_Win = Window(gui,height = 300 , width = 500, title = "Experiment Progress", visible = 0)
progressBox = Box(progress_Win)
abort_exp_button = PushButton(progressBox, text= "Abort Experiment",command = ABORT_Experiment)
time_remaining_str = Text(progressBox, text = "Estimated Time Remaining ")
time_remain_text = Text( progressBox)
volume_remaining_str = Text(progressBox, text = "Volume Remaining ")
volume_remain_text = Text(progressBox)
logBox = Box(gui, enabled = 0)
flowrate_str = Text(progressBox, text = "Flow Rate is ")
flowrate_text = Text(progressBox)

		## Finished win
finished_Win = Window(gui, title = "Operation Complete", visible = 0)




## MenuBar Widigets
File_options = [["Prepare Experiment", select_gas], ["Exit", ask_to_close] ]
DataLog_options = [ ["Open Log", enable_Log ] ]


menuBar = MenuBar(gui, ["File", "DataLog"], [File_options, DataLog_options])


gui.display()

