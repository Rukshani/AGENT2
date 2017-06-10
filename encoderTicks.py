import RPi.GPIO as GPIO
import time
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

GPIO.setup(31, GPIO.OUT)
GPIO.setup(33, GPIO.OUT)
GPIO.setup(35, GPIO.OUT)
GPIO.setup(37, GPIO.OUT)
GPIO.setup(38, GPIO.OUT)
GPIO.setup(40, GPIO.OUT)

left = GPIO.PWM(38, 100)
right = GPIO.PWM(40, 100)

left.start(0)
right.start(0)

leftTick = 0
rightTick = 0


#~ def forward():
	#~ print "working forward........................................."
	#~ GPIO.output(31, GPIO.HIGH)
	#~ GPIO.output(33, GPIO.LOW)
	#~ GPIO.output(35, GPIO.LOW)
	#~ GPIO.output(37, GPIO.HIGH)
#~ 
	#~ right.ChangeDutyCycle(30)
	#~ left.ChangeDutyCycle(30)
	#~ time.sleep(1)
	#~ left.ChangeDutyCycle(0)
	#~ right.ChangeDutyCycle(0)
 

class WheelEncoder:
    inputPin = 0
    ticks = 0
    accTicks = 0
    ticksPerTurn = 0
    radius = 0.0
    distPerTick = 0.0
    PI = 3.1415

    def __init__(self, inputPin, ticksPerTurn, radius):
        self.inputPin = inputPin
        self.ticksPerTurn = ticksPerTurn
        self.radius = radius

        self.setDistPerTick(self.ticksPerTurn, self.radius)

        GPIO.setup(self.inputPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(self.inputPin, GPIO.FALLING, callback=self.my_callback)

    def getTicks(self):
        return self.ticks

    def resetTicks(self):
        self.ticks = 0

    def getTicksPerTurn(self):
        return self.ticksPerTurn

    def setTicksPerTurn(self, ticks):
        self.ticksPerTurn = ticks

    def getRadius(self):
        return self.radius

    def setRadius(self, rad):
        self.radius = rad

    def setDistPerTick(self, ticksPerTurn, radius):
        self.distPerTick = (2 * self.PI * radius) / ticksPerTurn

    def getCurrentDistance(self):
        return self.ticks * self.distPerTick

    def getTotalDistance(self):
        return self.accTicks * self.distPerTick

    def my_callback(self, channel):
        self.ticks += 1
        self.accTicks += 1

    def getTicksPerDistance(self, dist):
        return (dist / self.distPerTick)
        
#~ encoder11 = WheelEncoder(11, 20, 3.3)
#~ encoder12 = WheelEncoder(12, 20, 3.3) 
 #~ 
#~ while (True):
	#~ print "avgTick:", (encoder11.getTicks() + encoder12.getTicks()) / 2
	#~ avgTick = (encoder11.getTicks() + encoder12.getTicks()) / 2
	#~ if avgTick < 200:
		#~ forward()
		#~ avgDist = (encoder11.getCurrentDistance() + encoder12.getCurrentDistance())/2
		#~ print "Distance: ", avgDist, "cm"
		#~ print "Ticks: ", avgTick
		#~ time.sleep(0.01)
	#~ else:
		#~ break
 
