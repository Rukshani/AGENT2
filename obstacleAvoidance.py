import time
import RPi.GPIO as IO
import time

IO.setwarnings(False)
IO.setmode(IO.BOARD)

IO.setup(31, IO.OUT)
IO.setup(33, IO.OUT)
IO.setup(35, IO.OUT)
IO.setup(37, IO.OUT)
IO.setup(38, IO.OUT)
IO.setup(40, IO.OUT)

left = IO.PWM(38, 100)
right = IO.PWM(40, 100)

left.start(0)
right.start(0)

TRIG = 16
ECHO = 18

time.sleep(5)


def stop():
    print "stop"
    IO.output(31, IO.LOW)
    IO.output(33, IO.LOW)
    IO.output(35, IO.LOW)
    IO.output(37, IO.LOW)


def forward():
    IO.output(31, IO.HIGH)
    IO.output(33, IO.LOW)
    IO.output(35, IO.LOW)
    IO.output(37, IO.HIGH)

    left.ChangeDutyCycle(60)
    right.ChangeDutyCycle(60)
    time.sleep(1)
    left.ChangeDutyCycle(0)
    right.ChangeDutyCycle(0)
    print ("Forward")


def backward():
    IO.output(31, IO.LOW)
    IO.output(33, IO.HIGH)
    IO.output(35, IO.HIGH)
    IO.output(37, IO.LOW)

    left.ChangeDutyCycle(60)
    right.ChangeDutyCycle(60)
    time.sleep(1)
    left.ChangeDutyCycle(0)
    right.ChangeDutyCycle(0)
    print "Backward"


def left():
    IO.output(31, IO.LOW)
    IO.output(33, IO.HIGH)
    IO.output(35, IO.LOW)
    IO.output(37, IO.HIGH)

    left.ChangeDutyCycle(60)
    right.ChangeDutyCycle(60)
    time.sleep(1)
    left.ChangeDutyCycle(0)
    right.ChangeDutyCycle(0)
    print ("Left")


def right():
    IO.output(31, IO.HIGH)
    IO.output(33, IO.LOW)
    IO.output(35, IO.HIGH)
    IO.output(37, IO.LOW)

    left.ChangeDutyCycle(60)
    right.ChangeDutyCycle(60)
    time.sleep(1)
    left.ChangeDutyCycle(0)
    right.ChangeDutyCycle(0)
    print ("Right")


stop()


def measureDistance():
    IO.output(TRIG, True)
    time.sleep(0.00001)
    IO.output(TRIG, False)
    while IO.input(ECHO) == 0:
        pulse_start = time.time()
    while IO.input(ECHO) == 1:
        pulse_end = time.time()
    duration = pulse_end - pulse_start
    distance = duration * 17150
    distance = round(distance, 2)
    print "Distance	", distance, "cm"
    return distance

print ("Distance measurement in progress")

IO.setup(TRIG, IO.OUT)
IO.setup(ECHO, IO.IN)

IO.output(TRIG, False)
print("Waiting to settle the sensor")
time.sleep(2)

while True:
    distance = measureDistance()
    if distance < 10:
        right()

