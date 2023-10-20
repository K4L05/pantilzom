# Proj pantilzom
# The Prototype
# Version 1.0
# With a bunch of stuff

# Author:   	Kalos Robinson-Frani
# Email:    	st20218@howick.school.nz
# Start Date:	16/10/2023 @ 10:19 (During 12BUS)
# Finish Date:	19/10/2023 @ 10:37 (During 12DGT)

import serial
from inputs import get_gamepad
import math
import threading
from time import sleep

comPort = 'COM9'
camAddr = 1

xActive = 0
aActive = 0
LsActive = 0
trigActive = 0
bumperActive = 0

powerState = 1
backLightState = 0


dz = 0.2 # Deadzone
trigDz = 0.1


def title():
	titleart = """
					  _   _ _                    
					 | | (_) |                   
	_ __   __ _ _ __ | |_ _| |_______  _ __ ___  
	| '_ \ / _` | '_ \| __| | |_  / _ \| '_ ` _ \ 
	| |_) | (_| | | | | |_| | |/ / (_) | | | | | |
	| .__/ \__,_|_| |_|\__|_|_/___\___/|_| |_| |_|
	| |                                           
	|_|                                
		   A VISCA Pan Tilt Zoom Controller
			Created by Kalos - Version 1.0      
					 Go get 'em     
	"""

	print(titleart)

# Camera Power
def on():
	print('[CAM] CAMERA ON')
	data =  bytearray.fromhex(f'8{camAddr} 01 04 00 02 FF')
	ser.write(data)

def off():
	print('[CAM] CAMERA OFF')
	data =  bytearray.fromhex(f'8{camAddr} 01 04 00 03 FF')
	ser.write(data)

# Camera Zoom
def zoom_stop():
	print('[ZOOM] Stop')
	data =  bytearray.fromhex(f'8{camAddr} 01 04 07 00 FF')
	ser.write(data)

def zoom_in():
	print('[ZOOM] IN')
	data =  bytearray.fromhex(f'8{camAddr} 01 04 07 02 FF') # Zoom in = telephoto
	ser.write(data)

def zoom_out():
	print('[ZOOM] OUT')
	data =  bytearray.fromhex(f'8{camAddr} 01 04 07 03 FF') # Zoom out = wide
	ser.write(data)

# Variable Camera Zoom (is it for zoom speed?)
def zoom_in_v(arg): #argument is expecting int in range (0-7)
	print(f'[ZOOM] IN ({arg})')
	data =  bytearray.fromhex(f'8{camAddr} 01 04 07 2{str(arg)} FF')
	ser.write(data)

def zoom_out_v(arg): #argument is expecting int in range (0-7)
	print(f'[ZOOM] OUT ({arg})')
	data =  bytearray.fromhex(f'8{camAddr} 01 04 07 3{arg} FF')
	ser.write(data)

def zoom_direct(arg): #argument is expecting int in range (0-4000) #4000 might be able to go higher?
	# Not sure if I did this correctly?
	arg = str(arg)
	print(f'[ZOOM] DIRECT {arg}')
	if len(arg) == 1:
		arg = f'000{arg}'

	if len(arg) == 2:
		arg = f'00{arg}'
	
	if len(arg) == 3:
		arg = f'0{arg}'
	data =  bytearray.fromhex(f'8{camAddr} 01 04 47 0{arg[0]} 0{arg[1]} 0{arg[2]} 0{arg[3]} FF')
	ser.write(data)


# Camera Focus
def focus_stop():
	print('[FOCUS] STOP')
	data =  bytearray.fromhex(f'8{camAddr} 01 04 08 00 FF')
	ser.write(data)

def focus_far():
	print('[FOCUS] FAR')
	data =  bytearray.fromhex(f'8{camAddr} 01 04 08 02 FF')
	ser.write(data)

def focus_near():
	print('[FOCUS] NEAR')
	data =  bytearray.fromhex(f'8{camAddr} 01 04 08 03 FF')
	ser.write(data)

def focus_direct(arg):
	# Not sure what argument is expected here?
	arg = str(arg)
	print('[FOCUS] DIRECT')
	data =  bytearray.fromhex(f'8{camAddr} 01 04 48 0{arg[0]} 0{arg[1]} 0{arg[2]} 0{arg[3]} FF')
	ser.write(data)

def focus_auto():
	print('[FOCUS] AUTO')
	data =  bytearray.fromhex(f'8{camAddr} 01 04 18 01 FF')
	ser.write(data)

# Camera Zoom Focus (whatever that means)
def zoomFocus_direct(arg1, arg2):
	print('[ZOOM & FOCUS] DIRECT')
	arg1 = str(arg1) # Arg1: Zoom Position (0-4000)
	arg2 = str(arg2) # Arg2: Focus Position (?)
	

	if len(arg1) == 1:
		arg1 = f'000{arg1}'

	if len(arg1) == 2:
		arg1 = f'00{arg1}'
	
	if len(arg1) == 3:
		arg1 = f'0{arg1}'


	data =  bytearray.fromhex(f'8{camAddr} 01 04 47 0{arg1[0]} 0{arg1[1]} 0{arg1[2]} 0{arg1[3]} 0{arg2[0]} 0{arg2[1]} 0{arg2[2]} 0{arg2[3]} FF')
	ser.write(data)

def pan_up(arg1 = 10, arg2 = 10):
	print('[PAN] UP')
	# Arguments must be 2 digits
	arg1 = str(arg1) # (VV) Pan Speed (range of 01-18)
	arg2 = str(arg2) # (WW) Tilt Speed (range of 01-14)

	data =  bytearray.fromhex(f'8{camAddr} 01 06 01 {arg1} {arg2} 03 01 FF')
	ser.write(data)

def pan_down(arg1 = 10, arg2 = 10):
	print('[PAN] DOWN')
	# Arguments must be 2 digits
	arg1 = str(arg1) # (VV) Pan Speed (range of 01-18)
	arg2 = str(arg2) # (WW) Tilt Speed (range of 01-14)

	data =  bytearray.fromhex(f'8{camAddr} 01 06 01 {arg1} {arg2} 03 02 FF')
	ser.write(data)

def pan_left(arg1 = 10, arg2 = 10):
	print('[PAN] LEFT')
	# Arguments must be 2 digits
	arg1 = str(arg1) # (VV) Pan Speed (range of 01-18)
	arg2 = str(arg2) # (WW) Tilt Speed (range of 01-14)

	data =  bytearray.fromhex(f'8{camAddr} 01 06 01 {arg1} {arg2} 01 03 FF')
	ser.write(data)

def pan_right(arg1 = 10, arg2 = 10):
	print('[PAN] RIGHT')
	# Arguments must be 2 digits
	arg1 = str(arg1) # (VV) Pan Speed (range of 01-18)
	arg2 = str(arg2) # (WW) Tilt Speed (range of 01-14)

	data =  bytearray.fromhex(f'8{camAddr} 01 06 01 {arg1} {arg2} 02 03 FF')
	ser.write(data)

def pan_stop(arg1 = 10, arg2 = 10):
	print('[PAN] STOP')
	# Arguments must be 2 digits
	arg1 = str(arg1) # (VV) Pan Speed (range of 01-18)
	arg2 = str(arg2) # (WW) Tilt Speed (range of 01-14)

	data =  bytearray.fromhex(f'8{camAddr} 01 06 01 {arg1} {arg2} 03 03 FF')
	ser.write(data)

def pan_upleft(arg1 = 10, arg2 = 10):
	print('[PAN] UP-LEFT')

	arg1 = str(arg1) # (VV) Pan Speed (range of 01-18)
	arg2 = str(arg2) # (WW) Tilt Speed (range of 01-14)
	data =  bytearray.fromhex(f'8{camAddr} 01 06 01 {arg1} {arg2} 01 01 FF')
	ser.write(data)

def pan_upright(arg1 = 10, arg2 = 10):
	print('[PAN] UP-RIGHT')

	arg1 = str(arg1) # (VV) Pan Speed (range of 01-18)
	arg2 = str(arg2) # (WW) Tilt Speed (range of 01-14)
	data =  bytearray.fromhex(f'8{camAddr} 01 06 01 {arg1} {arg2} 02 01 FF')
	ser.write(data)

def pan_downleft(arg1 = 10, arg2 = 10):
	print('[PAN] DOWN-LEFT')

	arg1 = str(arg1) # (VV) Pan Speed (range of 01-18)
	arg2 = str(arg2) # (WW) Tilt Speed (range of 01-14)
	data =  bytearray.fromhex(f'8{camAddr} 01 06 01 {arg1} {arg2} 01 02 FF')
	ser.write(data)
	
def pan_downright(arg1 = 10, arg2 = 10):
	print('[PAN] DOWN-RIGHT')

	arg1 = str(arg1) # (VV) Pan Speed (range of 01-18)
	arg2 = str(arg2) # (WW) Tilt Speed (range of 01-14)
	data =  bytearray.fromhex(f'8{camAddr} 01 06 01 {arg1} {arg2} 02 02 FF')
	ser.write(data)

class XboxController(object):
	MAX_TRIG_VAL = math.pow(2, 8)
	MAX_JOY_VAL = math.pow(2, 15)

	def __init__(self):

		self.LeftJoystickY = 0
		self.LeftJoystickX = 0
		self.RightJoystickY = 0
		self.RightJoystickX = 0
		self.LeftTrigger = 0
		self.RightTrigger = 0
		self.LeftBumper = 0
		self.RightBumper = 0
		self.A = 0
		self.X = 0
		self.Y = 0
		self.B = 0
		self.LeftThumb = 0
		self.RightThumb = 0
		self.Back = 0
		self.Start = 0
		self.LeftDPad = 0
		self.RightDPad = 0
		self.UpDPad = 0
		self.DownDPad = 0

		self._monitor_thread = threading.Thread(target=self._monitor_controller, args=())
		self._monitor_thread.daemon = True
		self._monitor_thread.start()


	def read(self): # return the buttons/triggers that you care about in this methode
		x = self.LeftJoystickX
		y = self.LeftJoystickY
		lStick = self.LeftThumb

		LBumper = self.LeftBumper
		RBumper = self.RightBumper

		LTrigger = self.LeftTrigger
		RTrigger = self.RightTrigger
		pwr = self.Start
		backlight = self.Back

		# Powerbutton is mapped to the wrong button.
		global powerState # Put this into its own function later
		if pwr:
			if powerState:
				off()
				powerState = 0
			elif not powerState:
				on()
				powerState = 1

		# Next do backlight
		
		if -dz < x < dz and -dz < y < dz:
			pantiltHandler("stop")
		elif x > dz and y > dz:
			pantiltHandler("upright",xspeed=x,yspeed=y)
		elif x < -dz and y > dz:
			pantiltHandler("upleft",xspeed=x,yspeed=y)
		elif x > dz and y < -dz:
			pantiltHandler("downright",xspeed=x,yspeed=y)
		elif x < -dz and y < -dz:
			pantiltHandler("downleft",xspeed=x,yspeed=y)
		elif x > dz and -dz < y < dz:
			pantiltHandler("right", xspeed=x)
		elif x < -dz and -dz < y < dz:
			pantiltHandler("left", xspeed=x)
		elif y > dz and -dz < x < dz:
			pantiltHandler("up", yspeed=y)
		elif y < -dz and -dz < x < dz:
			pantiltHandler("down", yspeed=y)
		if lStick == 1:
			pan_stop()
		
		if LBumper and RBumper:
			focusHandler('auto')
		
		if LBumper and not RBumper:
			focusHandler('near')
		
		if RBumper and not LBumper:
			focusHandler('far')
		
		if not RBumper and not LBumper:
			focusHandler('stop')

		if LTrigger > trigDz and RTrigger < trigDz:
			zoomHandler('out',LTrigger)
		if RTrigger > trigDz and LTrigger < trigDz:
			zoomHandler('in',RTrigger)
		if LTrigger < trigDz and RTrigger < trigDz:
			zoomHandler('stop')


	def _monitor_controller(self):
		while True:
			events = get_gamepad()
			for event in events:
				if event.code == 'ABS_Y':
					self.LeftJoystickY = event.state / XboxController.MAX_JOY_VAL # normalize between -1 and 1
				elif event.code == 'ABS_X':
					self.LeftJoystickX = event.state / XboxController.MAX_JOY_VAL # normalize between -1 and 1
				elif event.code == 'ABS_RY':
					self.RightJoystickY = event.state / XboxController.MAX_JOY_VAL # normalize between -1 and 1
				elif event.code == 'ABS_RX':
					self.RightJoystickX = event.state / XboxController.MAX_JOY_VAL # normalize between -1 and 1
				elif event.code == 'ABS_Z':
					self.LeftTrigger = event.state / XboxController.MAX_TRIG_VAL # normalize between 0 and 1
				elif event.code == 'ABS_RZ':
					self.RightTrigger = event.state / XboxController.MAX_TRIG_VAL # normalize between 0 and 1
				elif event.code == 'BTN_TL':
					self.LeftBumper = event.state
				elif event.code == 'BTN_TR':
					self.RightBumper = event.state
				elif event.code == 'BTN_SOUTH':
					self.A = event.state
				elif event.code == 'BTN_NORTH':
					self.Y = event.state #previously switched with X
				elif event.code == 'BTN_WEST':
					self.X = event.state #previously switched with Y
				elif event.code == 'BTN_EAST':
					self.B = event.state
				elif event.code == 'BTN_THUMBL':
					self.LeftThumb = event.state
				elif event.code == 'BTN_THUMBR':
					self.RightThumb = event.state
				elif event.code == 'BTN_SELECT':
					self.Back = event.state
				elif event.code == 'BTN_START':
					self.Start = event.state
				elif event.code == 'BTN_TRIGGER_HAPPY1':
					self.LeftDPad = event.state
				elif event.code == 'BTN_TRIGGER_HAPPY2':
					self.RightDPad = event.state
				elif event.code == 'BTN_TRIGGER_HAPPY3':
					self.UpDPad = event.state
				elif event.code == 'BTN_TRIGGER_HAPPY4':
					self.DownDPad = event.state


def pantiltHandler(position, xspeed = 1, yspeed = 1):
	input_range = [dz, 1] # Adjust stick deadzones here
	xOutput_range = [1, 16]
	yOutput_range = [1, 14]
	global LsActive

	xspeed = abs(xspeed)
	yspeed = abs(yspeed)
	
	if position == 'up':
		output_range = yOutput_range
		speedTranslated = str(round(((yspeed - input_range[0]) / (input_range[1] - input_range[0])) * (output_range[1] - output_range[0]) + output_range[0]))
		if len(speedTranslated) == 1:
			speedTranslated = f"0{speedTranslated}"
		pan_up(arg2=speedTranslated)
		LsActive = 1
		
	
	if position == 'down':
		output_range = yOutput_range

		yspeed = abs(yspeed)
		speedTranslated = str(round(((yspeed - input_range[0]) / (input_range[1] - input_range[0])) * (output_range[1] - output_range[0]) + output_range[0]))
		if len(speedTranslated) == 1:
			speedTranslated = f"0{speedTranslated}"
		pan_down(arg2=speedTranslated)
		LsActive = 1
		
	
	if position == 'left':
		output_range = xOutput_range
		xspeed = abs(xspeed)
		speedTranslated = str(round(((xspeed - input_range[0]) / (input_range[1] - input_range[0])) * (output_range[1] - output_range[0]) + output_range[0]))
		if len(speedTranslated) == 1:
			speedTranslated = f"0{speedTranslated}"
		pan_left(arg1=speedTranslated)
		LsActive = 1
	
	if position == 'right':
		output_range = xOutput_range

		speedTranslated = str(round(((xspeed - input_range[0]) / (input_range[1] - input_range[0])) * (output_range[1] - output_range[0]) + output_range[0]))
		if len(speedTranslated) == 1:
			speedTranslated = f"0{speedTranslated}"
		pan_right(arg1=speedTranslated)
		LsActive = 1
	
	if position == 'upright':
		xSpeedTranslated = str(round(((xspeed - input_range[0]) / (input_range[1] - input_range[0])) * (xOutput_range[1] - xOutput_range[0]) + xOutput_range[0]))
		ySpeedTranslated = str(round(((yspeed - input_range[0]) / (input_range[1] - input_range[0])) * (yOutput_range[1] - yOutput_range[0]) + yOutput_range[0]))

		if len(xSpeedTranslated) == 1:
			xSpeedTranslated = f"0{xSpeedTranslated}"
		
		if len(ySpeedTranslated) == 1:
			ySpeedTranslated = f"0{ySpeedTranslated}"


		pan_upright(xSpeedTranslated, ySpeedTranslated)

		LsActive = 1

	if position == 'upleft':
		xspeed = abs(xspeed)
		xSpeedTranslated = str(round(((xspeed - input_range[0]) / (input_range[1] - input_range[0])) * (xOutput_range[1] - xOutput_range[0]) + xOutput_range[0]))
		ySpeedTranslated = str(round(((yspeed - input_range[0]) / (input_range[1] - input_range[0])) * (yOutput_range[1] - yOutput_range[0]) + yOutput_range[0]))

		if len(xSpeedTranslated) == 1:
			xSpeedTranslated = f"0{xSpeedTranslated}"
		
		if len(ySpeedTranslated) == 1:
			ySpeedTranslated = f"0{ySpeedTranslated}"


		pan_upleft(xSpeedTranslated, ySpeedTranslated)
		LsActive = 1
	
	if position == 'downright':
		yspeed = abs(yspeed)

		xSpeedTranslated = str(round(((xspeed - input_range[0]) / (input_range[1] - input_range[0])) * (xOutput_range[1] - xOutput_range[0]) + xOutput_range[0]))
		ySpeedTranslated = str(round(((yspeed - input_range[0]) / (input_range[1] - input_range[0])) * (yOutput_range[1] - yOutput_range[0]) + yOutput_range[0]))

		if len(xSpeedTranslated) == 1:
			xSpeedTranslated = f"0{xSpeedTranslated}"
		
		if len(ySpeedTranslated) == 1:
			ySpeedTranslated = f"0{ySpeedTranslated}"


		pan_downright(xSpeedTranslated, ySpeedTranslated)
		LsActive = 1
	
	if position == 'downleft':
		xspeed = abs(xspeed)
		yspeed = abs(yspeed)
		xSpeedTranslated = str(round(((xspeed - input_range[0]) / (input_range[1] - input_range[0])) * (xOutput_range[1] - xOutput_range[0]) + xOutput_range[0]))
		ySpeedTranslated = str(round(((yspeed - input_range[0]) / (input_range[1] - input_range[0])) * (yOutput_range[1] - yOutput_range[0]) + yOutput_range[0]))

		if len(xSpeedTranslated) == 1:
			xSpeedTranslated = f"0{xSpeedTranslated}"
		
		if len(ySpeedTranslated) == 1:
			ySpeedTranslated = f"0{ySpeedTranslated}"


		pan_downleft(xSpeedTranslated, ySpeedTranslated)
		LsActive = 1

	if position == 'stop':
		if LsActive:
			LsActive = 0
			pan_stop()

def zoomHandler(direction, speed=3):
	global trigActive
	input_range = [trigDz, 1] # Adjust stick deadzones here
	output_range = [1, 7]
	output_value = str(round(((speed - input_range[0]) / (input_range[1] - input_range[0])) * (output_range[1] - output_range[0]) + output_range[0]))

	if direction == 'in':
		zoom_in_v(output_value)
		trigActive = 1
	if direction == 'out':
		zoom_out_v(output_value)
		trigActive = 1
	
	if trigActive:
		if direction == 'stop':
			trigActive = 0
			zoom_stop()
	
def focusHandler(direction):
	global bumperActive
	if direction == 'auto':
		focus_auto()
		

	if direction == 'near':
		focus_near()
		bumperActive = 1

	
	if direction == 'far':
		focus_far()
		bumperActive = 1
	
	if bumperActive:
		if direction == 'stop':
			focus_stop()
			bumperActive = 0
		

if __name__ == "__main__":
	title()
	try:
		ser = serial.Serial(
			port=comPort,\
			baudrate=9600,\
			parity=serial.PARITY_NONE,\
			stopbits=serial.STOPBITS_ONE,\
			bytesize=serial.EIGHTBITS,\
			timeout=0\
		)
	except serial.serialutil.SerialException:
		raise Exception("Cannot connect to COM Port")
	
	joy = XboxController()
	try:
		print("System ready \n")
		while True:
			joy.read()
			sleep(0.2)
	except KeyboardInterrupt:
		print('\n\nGoodbye')