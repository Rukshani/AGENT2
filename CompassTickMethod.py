import smbus
import thread
import time
import math
import RPi.GPIO as IO
import time
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

    scale = 0.92

    x_offset = 46
    y_offset = -117

    x_out = (self.read_word_2c(3) - x_offset) * scale
    y_out = (self.read_word_2c(7) - y_offset) * scale
    z_out = (self.read_word_2c(5)) * scale

    bearing  = math.atan2(y_out, x_out)
    if (bearing < 0):
      bearing += 2 * math.pi

    return math.degrees(bearing)

##    for i in range(0,500):
##      x_out = self.read_word_2c(3)
##      y_out = self.read_word_2c(7)
##      z_out = self.read_word_2c(5)
##
##      bearing  = math.atan2(y_out, x_out)
##      if (bearing < 0):
##        bearing += 2 * math.pi
##
##      print x_out, y_out, (x_out * scale), (y_out * scale)
##      time.sleep(1)

def watcher():
  compass = Compass(0x1e)
  currentDir = compass.getOrientation()
  print currentDir
  nextDir = currentDir - 90
  while(nextDir < currentDir):
    currentDir = compass.getOrientation()
    print currentDir
  thread.interrupt_main()



def forward():
  IO.output(31,IO.HIGH)
  IO.output(33,IO.LOW)
  IO.output(35,IO.LOW)
  IO.output(37,IO.HIGH)
  right.ChangeDutyCycle(60)
  left.ChangeDutyCycle(60)

def stop():
  left.ChangeDutyCycle(0)
  right.ChangeDutyCycle(0)

def leftSide():
  print "MAKE LEFT TURN"
  IO.output(31,IO.LOW)
  IO.output(33,IO.HIGH)
  IO.output(35,IO.LOW)
  IO.output(37,IO.HIGH)
  left.ChangeDutyCycle(40)
  right.ChangeDutyCycle(40)
  time.sleep(0.1)
  stop()
  time.sleep(0.5)


try:
  count = 0
  compass = Compass(0x1e)
  currentDir = compass.getOrientation()
  print currentDir
  for x in range(0,26):
    leftSide()
    count += 1
    print count

  time.sleep(2)
  currentDir = compass.getOrientation()
  print currentDir
##    currentDir = compass.getOrientation()
##    if(nextDir > currentDir):
##      break


except KeyboardInterrupt:
  stop()
  print "stop"

