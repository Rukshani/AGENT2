# import RPi.GPIO as IO
import time
import sys
import Tkinter as tk
import os
import thread

# IO.setwarnings(False)
# IO.setmode(IO.BOARD)
#
# IO.setup(31,IO.OUT)
# IO.setup(33,IO.OUT)
# IO.setup(35,IO.OUT)
# IO.setup(37,IO.OUT)
# IO.setup(38,IO.OUT)
# IO.setup(40,IO.OUT)
#
# left    = IO.PWM(38,100)
# right   = IO.PWM(40,100)

# left.start(0)
# right.start(0)

coveredLocationList = []
coveredKeypointsList = []
four_directions = ['^', '>', 'v', '<']

def forward():
    # IO.output(31,IO.HIGH)
    # IO.output(33,IO.LOW)
    # IO.output(35,IO.LOW)
    # IO.output(37,IO.HIGH)
    #
    # left.ChangeDutyCycle(60)
    # right.ChangeDutyCycle(60)
    # time.sleep(1)
    # left.ChangeDutyCycle(0)
    # right.ChangeDutyCycle(0)
    print ("Forward")


def right():
    # IO.output(31,IO.HIGH)
    # IO.output(33,IO.LOW)
    # IO.output(35,IO.HIGH)
    # IO.output(37,IO.LOW)
    #
    # left.ChangeDutyCycle(60)
    # right.ChangeDutyCycle(60)
    # time.sleep(1)
    # left.ChangeDutyCycle(0)
    # right.ChangeDutyCycle(0)
    print ("Right")


def left():
    # IO.output(31,IO.LOW)
    # IO.output(33,IO.HIGH)
    # IO.output(35,IO.LOW)
    # IO.output(37,IO.HIGH)
    #
    # left.ChangeDutyCycle(60)
    # right.ChangeDutyCycle(60)
    # time.sleep(1)
    # left.ChangeDutyCycle(0)
    # right.ChangeDutyCycle(0)
    print ("Left")


def backward():
    print "Backward"


def stop():
    # left.ChangeDutyCycle(0)
    # right.ChangeDutyCycle(0)
    print "Stop"


def serverNavigation_IP():
    global msgSuspicious
    from random import randint
    while True:
        number = (randint(0, 100))
        time.sleep(0.1)
        msgSuspicious = False
        # print "Random:", number
        if number == 10 or number == 2:
            print "Stop"
            msgSuspicious = True
            break
        else:
            msgSuspicious = False


def goToStart(currentLocation, initialLocationPoint):
    print "------------Reaching Start-----------"
    from KeyPointsNavigation import searchDetails as searchDetails
    searchDetails(currentLocation, initialLocationPoint)


# ------------------ localization of robot from one key point to other--------------------------- #
def key_input(path, f_degree, b_degree, r_degree, l_degree, initialLocation, currentLocationList, AREA_MAP, assignedArea):
    # msgSuspicious = False
    global currentLocation
    currentLocation = []

    # thread.start_new_thread(serverNavigation_IP, ())
    # serverNavigation_IP()
    # print "msgSuspicious", msgSuspicious

    global initialLocationPoint
    initialLocationPoint = initialLocation
    # print "Initial Location", initialLocationPoint

    msgSuspicious = True

    key_press_index = 0
    for key_press in path:
        from random import randint
        number = (randint(0, 100))
        numberUS = (randint(0, 100))
        print "Random: ", number
        time.sleep(0.1)

        currentLocation = currentLocationList[key_press_index]
        print "Current location: ", currentLocation
        coveredLocationList.append(currentLocation)
        # print "Covered Locations List: ", coveredLocationList

        if numberUS == 102 or numberUS == 222 or numberUS == 132:  # ---------------checking Ultrasonic sensor
            print "UUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUU"
            print "Key_press: ", key_press
            indexFourDirections = four_directions.index(key_press)
            print "indexFourDirections:", indexFourDirections
            # for x in range(len(AREA_MAP)):
            #     print AREA_MAP[x]

            print "Covered Locations List: ", coveredLocationList

            print "assignedArea1",assignedArea
            for keypoint in assignedArea:
                if keypoint in coveredLocationList:
                    coveredKeypointsList.append(keypoint)
                    assignedArea.remove(keypoint)
            print "coveredKeypointsList: ", coveredKeypointsList

            # -----remove covered key points from assignedArea and add current location as a key point
            print "assignedArea2",assignedArea
            assignedArea.insert(0,currentLocation)

            print "New assignedArea: ",assignedArea


            thread.interrupt_main()

        if number == 20 or number == 60 or number == 52 or number == 48 or number == 12:
            print "Stop"
            msgSuspicious = True
            print "Suspicious image received.Sending image and current location to Coordinator"
            # --------------- send current location + image in here
            thread.start_new_thread(goToStart, (currentLocation, initialLocationPoint))
            time.sleep(2)  # ----------------------------check here
            # global currentEvent
            # currentEvent =
            thread.interrupt_main()
            break
        else:
            msgSuspicious = False

        # -----------------------pyCharm-----------------
        if not msgSuspicious:
            if key_press == "^":
                forward()
            elif key_press == ">":
                right()
            elif key_press == "<":
                left()
            elif key_press == "v":
                backward()

        key_press_index += 1
