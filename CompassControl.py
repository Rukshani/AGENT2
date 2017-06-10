import RPi.GPIO as IO
import time
import sys
import Tkinter as tk
import os
import smbus
import math
import thread
import interrupt
from Client_modified_4 import CompassBearing
from encoderTicks import WheelEncoder

IO.setwarnings(False)
IO.setmode (IO.BOARD)

IO.setup(31,IO.OUT)
IO.setup(33,IO.OUT)
IO.setup(35,IO.OUT)
IO.setup(37,IO.OUT)
IO.setup(38,IO.OUT)
IO.setup(40,IO.OUT)

left    = IO.PWM(38,100)
right   = IO.PWM(40,100)

left.start(0)
right.start(0)

DONE = ""
RANGE = 5

coveredLocationList = []
coveredKeypointsList = []
tickDirection = []
CRITICAL_ULTRASONIC = 50
currentLocation = []
updatedAssignedArea = []
personDetected = 0
remainingTicks = 0

encoder11 = WheelEncoder(11, 20, 3.3)
encoder12 = WheelEncoder(12, 20, 3.3)

class Compass:
   bus = smbus.SMBus(1)
   address = 0x1e
   def __init__(self, address):
	 self.address = address

   def read_byte(self, adr):
	 return self.bus.read_byte_data(self.address, adr)

   def read_word(self, adr):
	 high = self.bus.read_byte_data(self.address, adr)
	 low = self.bus.read_byte_data(self.address, adr+1)
	 val = (high << 8) + low
	 return val

   def read_word_2c(self, adr):
	 val = self.read_word(adr)
	 if (val >= 0x8000):
		 return -((65535 - val) + 1)
	 else:
		 return val

   def write_byte(self, adr, value):
	 self.bus.write_byte_data(self.address, adr, value)

   def getOrientation(self):
	 self.write_byte(0, 0b01110000) # Set to 8 samples @ 15Hz
	 self.write_byte(1, 0b00100000) # 1.3 gain LSb / Gauss 1090 (default)
	 self.write_byte(2, 0b00000000) # Continuous sampling
#    time.sleep(3)
	 scale = 0.92
	 
	 x_offset = 51
	 y_offset = -126
	 #~ x_offset = 46
	 #~ y_offset = -117
	 x_out = (self.read_word_2c(3) - x_offset) * scale
	 y_out = (self.read_word_2c(7) - y_offset) * scale
	 z_out = (self.read_word_2c(5)) * scale
	 bearing  = math.atan2(y_out, x_out)
	 if (bearing < 0):
	   bearing += 2 * math.pi
	 return math.degrees(bearing)

def ultrasonicDistance(targetTicks):
	from random import randint
	numberUS = (randint(0, 100))
	time.sleep(0.1)
	print "RandomUS: ", numberUS
	time.sleep(0.1)
	while True:
		##        response = serialPort.readline()
		response = 10
		status = False
		# print response
		if numberUS == 105 or numberUS == 225 or numberUS == 135 or numberUS == 255 or numberUS == 325:
			# if response < float(CRITICAL_ULTRASONIC):
			status = True  # found obstacle
		else:
			status = False
			# ------------------ encoder tick counter start ----------------
			
			global remainingTicks
			global avgTick
			remainingTicks = 0
			avgTick	= 0 
			while (True):
				#~ print "avgTick:", (encoder11.getTicks() + encoder12.getTicks()) / 2
				avgTick = (encoder11.getTicks() + encoder12.getTicks()) / 2
				if avgTick < 200:
					# ------------------ forward motion start----------------
					IO.output(31,IO.HIGH)
					IO.output(33,IO.LOW)
					IO.output(35,IO.LOW)
					IO.output(37,IO.HIGH)
					
					right.ChangeDutyCycle(30)
					left.ChangeDutyCycle(30)
					time.sleep(1)
					left.ChangeDutyCycle(0)
					right.ChangeDutyCycle(0)
					
					print "Forward"
					# ------------------ forward motion end----------------
					avgDist = (encoder11.getCurrentDistance() + encoder12.getCurrentDistance())/2
					#~ print "Distance: ", avgDist, "cm"
					#~ print "Ticks: ", avgTick
					time.sleep(0.01)
				else:
					break
			#~ print "Distance: ", avgDist, "cm"
			#~ print "Ticks: ", avgTick
			#~ print "avgTick:", (encoder11.getTicks() + encoder12.getTicks()) / 2
			remainingTicks=targetTicks-avgTick
			
		if status == True:
			print "Obstacle Detected"
			time.sleep(0.3)
			interrupt.currentEvent = interrupt.Interrupt.ULTRASONIC_NOTIFICATION
			thread.interrupt_main()
			break
		else:
			if interrupt.currentEvent == interrupt.Interrupt.ULTRASONIC_NOTIFICATION:
				break
class Motion:
	def forward(self):
		#~ print "working forward........................................."
	    #~ thread.start_new(ultrasonicDistance, (200,))
		IO.output(31,IO.HIGH)
		IO.output(33,IO.LOW)
		IO.output(35,IO.LOW)
		IO.output(37,IO.HIGH)
		
		left.ChangeDutyCycle(60)
		right.ChangeDutyCycle(60)
		time.sleep(1)
		left.ChangeDutyCycle(0)
		right.ChangeDutyCycle(0)
		time.sleep(1)
		print "Forward"
	def right(self,duration):
		#~ print "working right........................................."
		IO.output(31,IO.HIGH)
		IO.output(33,IO.LOW)
		IO.output(35,IO.HIGH)
		IO.output(37,IO.LOW)
		
		left.ChangeDutyCycle(45)
		right.ChangeDutyCycle(45)
		time.sleep(0.5)
		left.ChangeDutyCycle(0)
		right.ChangeDutyCycle(0)
		time.sleep(0.5)
		#~ print "Right"
	def left(self,duration):
		#~ print "working left........................................."
		IO.output(31,IO.LOW)
		IO.output(31,IO.LOW)
		IO.output(33,IO.HIGH)
		IO.output(35,IO.LOW)
		IO.output(37,IO.HIGH)
		
		left.ChangeDutyCycle(45)
		right.ChangeDutyCycle(45)
		time.sleep(0.5)
		left.ChangeDutyCycle(0)
		right.ChangeDutyCycle(0)
		time.sleep(0.5)
		#~ print "Left"
		
	def tempStop(self):
		#~ print "working tempStop........................................."
		IO.output(31,IO.LOW)
		IO.output(33,IO.LOW)
		IO.output(35,IO.LOW)
		IO.output(37,IO.LOW)
		left.ChangeDutyCycle(0)
		right.ChangeDutyCycle(0)
		time.sleep(1)
		left.ChangeDutyCycle(0)
		right.ChangeDutyCycle(0)
		#~ print "tempStop"

def calDir(target, current, compassRange=RANGE):
	motion = Motion()
	delta = 0 
	direction = ""
	if(current > target):
		if((current - target) > 180 ):
			delta = (360-current)+(target)
			direction = "right"
		else:
			delta = (current - target)
			direction = "left"
	else:
		if((target - current) > 180 ):
			delta = (360-target)+(current)
			direction = "left"
		else:
			delta = (target - current)
			direction = "right"
	print("Target=%f Current=%f Delta=%f" % (target, current, delta))
	if(delta <= compassRange):
		return DONE
	else:
		duration = (delta+6.4)/68
		if(direction == "left"):
			motion.left(duration)
		else:
			motion.right(duration)
		return "no"
		

	#~ target = target % 360
	#~ current = current % 360
	#~ delta = (target - current) % 360
	#~ print("Target=%f Current=%f Delta=%f" % (target, current, delta))
	#~ if delta <= compassRange:
		#~ status = DONE
	#~ else:
		#~ if delta > 180:
			#~ status = motion.left()
		#~ else:
			#~ status = motion.right()
	#~ return status
	


def directionCorrection(ANGLE):
	motion = Motion()
	global tickDirection
	compass = Compass(0x1e)
	try:
		angleTarget = float(ANGLE)
		status = motion.tempStop()
		while (status != DONE):
			currentAngle = compass.getOrientation()
			status = calDir(angleTarget, currentAngle)
			time.sleep(1)
		print("Angle within range")
		motion.forward()
		tickDirection.append(currentAngle)
		time.sleep(1)
		print "------------------------------------------------------"
		print "Forward Bearing ", tickDirection
		
	except ValueError:
		pass

def goToStart(currentLocation, initialLocationPoint):
	print "------------Reaching Start-----------"
	from KeyPointsNavigation import searchDetails as searchDetails
	searchDetails(currentLocation, initialLocationPoint)

def personDetectedNotify(PERSON_DETECTED):
	global personDetected
	personDetected = PERSON_DETECTED
	stopNotify()

def stopNotify():
	print "Stop Notification checking: ", personDetected
	if personDetected == 9:
		interrupt.currentEvent = interrupt.Interrupt.GOTO_START
		thread.interrupt_main()
		
def key_input(path, initialLocation, currentLocationList, AREA_MAP, assignedArea):
	global updatedAssignedArea
	updatedAssignedArea = assignedArea
	global currentLocation
	currentLocation = []
	global initialLocationPoint
	initialLocationPoint = initialLocation
	msgSuspicious = True
	key_press_index = 0
	print "key_press_index", key_press_index
	for key_press in path:
		thread.start_new_thread(stopNotify, ())
		from random import randint
		number = (randint(0, 100))
		numberUS = (randint(0, 100))
		print "Random: ", number
		time.sleep(0.1)
		currentLocation = currentLocationList[key_press_index]

		print "Current location: ", currentLocation
		coveredLocationList.append(currentLocation)

		updatedAssignedArea.insert(len(assignedArea), initialLocation)
		print "updatedAssignedArea", updatedAssignedArea
		if (updatedAssignedArea[0] == updatedAssignedArea[1]) and len(updatedAssignedArea) == 2:
			interrupt.currentEvent = interrupt.Interrupt.COMPLETION_NOTIFICATION
			thread.interrupt_main()
		for keypoint in updatedAssignedArea:
			if keypoint in coveredLocationList:
				coveredKeypointsList.append(keypoint)
				updatedAssignedArea.remove(keypoint)
		print "coveredKeypointsList: ", coveredKeypointsList
		
		# --------------direction correction-------------------------------
		if key_press == '^':
			print "Current ^ direction"
			directionCorrection(CompassBearing.F_DEGREE)
		elif key_press == 'v':
			print "Current v direction"
			directionCorrection(CompassBearing.B_DEGREE)
		elif key_press == '<':
			print "Current < direction"
			directionCorrection(CompassBearing.L_DEGREE)
		elif key_press == '>':
			print "Current > direction"
			directionCorrection(CompassBearing.R_DEGREE)
		key_press_index += 1
		
		
# ~ path1=['^','<','v','>','^']
# ~ path1=['>','>','v','v','v','v','>','>','^','^','>','^']
# ~ path=['>','>','>','v','v','<','<','^']
#~ path = ['^', '^']
# ~ path1 = ['v','<','>','^']
# ~ path = ['>']
# ~ f_degree=140#^
# ~ b_degree=0 #V
# ~ r_degree=68 #>
# ~ l_degree=270 #<
##floor 2 small
# f_degree = 268  # ^
# b_degree = 58  # V
# r_degree = 356  # >
# l_degree = 130  # <
# key_input(path, f_degree, b_degree, r_degree, l_degree, 0, 0, 0, 0)

#~ path = ['v', 'v']
#~ key_input(path, [0,0], [], [], [])
##floor 2 small
# ~ f_degree=275 #^
# ~ b_degree=64 #V
# ~ r_degree=356 #>
# ~ l_degree=134 #<
##floor 2 large
# f_degree=204 #^
# b_degree=32 #V
# r_degree=312 #>
# l_degree=100 #<
##hostel
# ~ f_degree=17
# ~ b_degree=162
# ~ r_degree=79
# ~ l_degree=305
# ~
# ~ pathcounter=0
# ~ key_input(path1,f_degree,b_degree,r_degree,l_degree,pathcounter)

