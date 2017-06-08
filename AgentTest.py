import thread
##from serial import Serial
from ws4py.client.threadedclient import WebSocketClient
import time
import re
import socket

CRITICAL_BATTERY_LEVEL = 3.6
CRITICAL_ULTRASONIC = 15
BROADCAST_NETWORK = '192.168.1.255'
WEBSOCKET_SERVER_ENDPOINT = "ws://localhost:8080/Coordinator/websocketserver"


##-------------------- Battery Monitoring Service ---------------------------##

def monitorBatteries():
    # serialPort = Serial("/dev/ttyAMA0", 9600, timeout=2)
    # if (serialPort.isOpen() == False):
    #     serialPort.open()
    #
    # outStr = ''
    # inStr = ''
    #
    # serialPort.flushInput()
    # serialPort.flushOutput()

    while True:
        ##        response = serialPort.readline()
        response = "3.81-----3.61"
        # response = "3.2"
        status = False
        # print response

        # if response < float(CRITICAL_BATTERY_LEVEL):
        #     print "critical"
        #     status = False
        # else:
        #     status = True
        #     print "Not critical"

        values = response.split("-----")
        for value in values:
            value = float(re.findall("\d+\.\d+", value)[0])
            if value < float(CRITICAL_BATTERY_LEVEL):
                status = True
            else:
                status = False
        if status == True:
            thread.interrupt_main()
            print "Critical Battery Level"
            break


# serialPort.close()

##-------------------- End of Battery Monitoring Service---------------------------##


##-------------------- Register to the Service via Coordinator---------------------##
def registerToService():
    addr = (BROADCAST_NETWORK, 33333)  # broadcast address explicitly

    UDPSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Create socket

    print "Starting the registering process"

    data1 = "register"
    # Almost infinite loop... ;)
    while True:
        if UDPSock.sendto(data1, addr):
            print "Sending message '%s'..." % data1
            try:
                addr1 = ('', 33334)
                UDPSock2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                UDPSock2.bind(addr1)
                UDPSock2.settimeout(10)
                data, addr1 = UDPSock2.recvfrom(1024)
                UDPSock2.close()
                print "Server IP is %s" % (data)
                data1 = data
                UDPSock.close()
                break
            except:
                print "Time out exception"

    UDPSock.close()  # Close socket
    print 'Client stopped.'
    return data1;


##-------------------- End of Register to the Service ------------------------------##



##-------------------- WebSocket Connection ----------------------------------------##

class DummyClient(WebSocketClient):
    def opened(self):
        print "Connection Established"

    def closed(self, code, reason=None):
        print "Connection Closed down", code, reason

    def received_message(self, m):
        print m


##-------------------- End of WebSocket Connection ---------------------------------##


##-------------------- Start of Ultrasonic Method---------------------------------##
def ultrasonicDistance():
    print "-----ultrasonicDistance-----"
    while True:
        ##        response = serialPort.readline()

        # //////call ULTRASONIC method here **********************************************************
        response = 20
        status = False
        # print response
        if response < float(CRITICAL_ULTRASONIC):
            status = True
        else:
            status = False
        if status == True:
            # thread.interrupt_main()


            # //////call Obstacle avoidance here **********************************************************
            # check current location
            # reconfiguration of the path
            print "Obstacle Detected"
            break


# -------------------- End of Ultrasonic Method---------------------------------##


def main():
    AREA_MAP = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
                [0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
                [0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
                [0, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
                [0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0],
                [0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0],
                [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
    INTITAL_PLACE = [0, 0]

    # AREA_MAP= [[2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    #             [0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0],
    #             [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 2, 0, 0],
    #             [0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    #             [0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 2],
    #             [0, 2, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    #             [0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0],
    #             [0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0],
    #             [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    #             [2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0]]
    # AREA_MAP = [[2, 0, 1, 0, 0, 0, 0, 0],
    #              [0, 0, 1, 0, 0, 2, 0, 1],
    #              [0, 0, 1, 0, 1, 1, 0, 0],
    #              [0, 0, 0, 2, 0, 0, 0, 2],
    #              [1, 1, 1, 0, 0, 0, 0, 1],
    #              [0, 2, 0, 0, 1, 0, 0, 1],
    #              [1, 1, 1, 0, 1, 0, 0, 0],
    #              [0, 0, 0, 0, 1, 0, 0, 0],
    #              [0, 0, 0, 0, 1, 0, 2, 0],
    #              [0, 2, 0, 0, 1, 0, 0, 0]]
    try:
        ######### Start Battery Monitoring Thread #####
        thread.start_new_thread(monitorBatteries, ())

        F_DEGREE = 3
        B_DEGREE = 3
        R_DEGREE = 3
        L_DEGREE = 3
        # assignedArea=[[],[],[],[],[],[],[],[],]
        # assignedArea=[[0, 0], [1, 7], [2, 12], [4, 14], [5, 1], [9, 0], [9, 8]]
        assignedArea = [INTITAL_PLACE, [0, 5], [0, 7], [0, 12], [2, 12], [4, 14], [8,14], [9,12]]

        ######### Getting key points path #############
        from KeyPointCoverage import mainKeyPointCoverage as mainKeyPointCoverage
        mainKeyPointCoverage(AREA_MAP, F_DEGREE, B_DEGREE, R_DEGREE, L_DEGREE, assignedArea, INTITAL_PLACE)
        ######### End of getting key points path #############

        ######### Obstacle avoidance #############
        thread.start_new_thread(ultrasonicDistance, ())
        ######### End Obstacle avoidance #############

        ######### Register to the Service #############
    ##        serverIp = registerToService()
    ##        print serverIp


    ######### Create Web Socket Connection ########
    # ws = DummyClient(WEBSOCKET_SERVER_ENDPOINT)
    # ws.connect()


    ######### Ask for other Agents in System #######
    # ws.send("Test")
    ##--------------------------------------         synchronization  error recovery methods


    except KeyboardInterrupt:
        print "Exception in Agent Test"
        # ws.close()

    print "App closed"


if __name__ == "__main__":
    main()
