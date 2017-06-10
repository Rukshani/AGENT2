import thread
from serial import Serial
from ws4py.client.threadedclient import WebSocketClient
import time
import re
import socket
import json
import sys
from time import sleep
from time import gmtime, strftime
import datetime
import interrupt

CRITICAL_BATTERY_LEVEL = 3.6
BROADCAST_NETWORK = '192.168.8.255'
WEBSOCKET_SERVER_ENDPOINT = "ws://localhost:8080/Coordinator/coordinator"

AGENT_IP = ""
COORDINATOR = ""

AREA_MAP = []
INTITAL_PLACE = []
PERSON_DETAILS = []

incomeMsg = ""
assignedArea = []
socket


#~ F_DEGREE = 14 37
    #~ B_DEGREE = 256 261
    #~ R_DEGREE = 98 124
    #~ L_DEGREE = 320 329
class CompassBearing:
    F_DEGREE = 37
    B_DEGREE = 261
    R_DEGREE = 124
    L_DEGREE = 329


class Priority:
    LOW = 0
    NORMAL = 1
    HIGH = 2

##-------------------- List of Intrrupts ---------------------------##
class Message:
    READY_TO_WORK = 0
    KEY_PLACE_AREAS = 1
    LIST_OF_OTHER_AGENTS = 2
    LOCATION_MAP = 3
    ASSIGNED_AREA = 4
    PERSONS_DETAILS = 5
    SUSPICIOUS_PERSON = 6
    CURRENT_BATTERY_VOLTAGE = 7
    CRITICAL_BATTERY_LEVEL = 8
    PERSON_DETECTED = 9
    CURRENT_LOCATION = 10
    AGENT_COMMUNICATION_STOPPED = 11
    BATTERY_STATUS  = 12;
    LOCATION_STATUS = 13;

##-------------------- Battery Monitoring Service ---------------------------##

def monitorBatteries(ws):
	serialPort = Serial("/dev/ttyAMA0", 9600, timeout=2)		
	if (serialPort.isOpen() == False):
		
		serialPort.open()
    
        outStr = ''
        inStr = ''
    
        serialPort.flushInput()
        serialPort.flushOutput()

	while True:
		response = serialPort.readline()
	
		status = False

		msg = formatTheMessageAndSend(response, Message. BATTERY_STATUS, AGENT_IP, COORDINATOR,
										  Priority.NORMAL);
		ws.send(msg)
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
    

	serialPort.close()

##-------------------- End of Battery Monitoring Service---------------------------##


##-------------------- Register to the Service via Coordinator---------------------##
def registerToService():
    addr = (BROADCAST_NETWORK, 33333)  # broadcast address explicitly

    UDPSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Create socket
    UDPSock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    print "Starting the registering process"

    data1 = "register"
    # Almost infinite loop... ;)
    while True:
        if UDPSock.sendto(data1, addr):
            print "Sending message '%s'..." % data1
            try:
                UDPSock.settimeout(5)
                
                data, addr = UDPSock.recvfrom(1024)
                UDPSock.close()
                print "Server IP is %s" % (data)
                data1 = []
                data1.append(data)

                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                s.connect((data, 80))
                s.getsockname()[0]
                
                data1.append(s.getsockname()[0])
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
        global incomeMsg
        incomeMsg = str(m)
        interrupt.currentEvent = interrupt.Interrupt.INCOMING_MESSAGE
        thread.interrupt_main()


##-------------------- Draw obstacles ---------------------------------------------##

def drawObstacles(rectangle):
    global AREA_MAP
    # for x in range(0, len(AREA_MAP)):
    #    print AREA_MAP[x]
    for y in range(int(rectangle[1]), int(rectangle[1]) + int(rectangle[3]) + 1):
        for x in range(int(rectangle[0]), int(rectangle[0]) + int(rectangle[2]) + 1):
            if x == rectangle[0] or x == rectangle[0] + rectangle[2] or y == rectangle[1] or y == rectangle[1] + \
                    rectangle[3]:
                AREA_MAP[y][x] = 1


##    for x in range(0, len(AREA_MAP)):
##        print AREA_MAP[x]
## 



##-------------------- Agent Main Process ------------------------------------------##   
def agentMainProcess(currentEvent, group):
    if (currentEvent != interrupt.Interrupt.NO_EVENT):
        a = datetime.datetime.now()
        if (currentEvent == interrupt.Interrupt.REGISTER_TO_SERVICE):
            ws = group.get(COORDINATOR, None);
            msg = formatTheMessageAndSend(Message.READY_TO_WORK, Message.READY_TO_WORK, AGENT_IP, COORDINATOR,
                                          Priority.NORMAL);
            ws.send(msg)
        elif (currentEvent == interrupt.Interrupt.INCOMING_MESSAGE):

            j = json.loads(incomeMsg)
            tag = j['Header'][0]['Tag'][0]
            if (int(tag) == int(Message.LIST_OF_OTHER_AGENTS)):
                agentList = j['Body'][0]['Message'][0]
                print agentList

                ##########################################################################################Create Agent Network#############################
                ws = group.get(COORDINATOR, None);
                msg = formatTheMessageAndSend(Message.LOCATION_MAP, Message.LOCATION_MAP, AGENT_IP, COORDINATOR,
                                              Priority.NORMAL);
                ws.send(msg)
            elif (int(tag) == int(Message.LOCATION_MAP)):
                # map = j['Body'][0]['Message'][0]
                # print map
                #                map = '{"height":10,"width":15,"data":[[5,5,8,3],[2,2,7,6]]}'
                # map = '{"height":6,"width":12,"data1":[[1,2,2,2],[4,4,0,1],[2,6,4,1]],"data2":[[0,7],[0,10],[3,11],[5,10],[5,8],[5,5],[3,5]],"data3":[0,5]}'
                map = '{"height":6,"width":12,"data1":[[2,1,2,2],[4,4,0,1],[6,2,4,2]],' \
                      '"data2":[[0,7],[0,10],[3,11],[5,10],[5,8],[5,5],[3,5]],"data3":[0,5]}'
                      
                
                j = json.loads(map)
                global AREA_MAP
                height = int(j['height'])
                width = int(j['width'])
                for x in range(0, height):
                    row = []
                    for y in range(0, width):
                        row.append(0)
                    AREA_MAP.append(row)

                for x in range(0, len(AREA_MAP)):
                  print AREA_MAP[x]

                for x in range(0, len(j['data1'])):
                    drawObstacles(j['data1'][x])

                global INTITAL_PLACE
                INTITAL_PLACE = j['data3']

                print "Map is ready"
                b = datetime.datetime.now()
                print(b - a)

                ws = group.get(COORDINATOR, None);
                msg = formatTheMessageAndSend(Message.ASSIGNED_AREA, Message.ASSIGNED_AREA, AGENT_IP, COORDINATOR,
                                              Priority.NORMAL);
                ws.send(msg)


            elif (int(tag) == int(Message.ASSIGNED_AREA)):
                global assignedArea
                # assignedArea = j['Body'][0]['Message'][0]
                #---------------------for testinnnnnnnnnnnnnnnnnnnnnnnnnnnng
                #~ [3,11],[5,10],[5,8],[5,5],[3,5]]
                assignedArea = [INTITAL_PLACE,[0,7],[0,10],[3,11],[5,10],[5,8],[5,5],[3,5]]
                print "Area assigned"
                print assignedArea

                from KeyPointCoverage import mainKeyPointCoverage as mainKeyPointCoverage
                mainKeyPointCoverage(AREA_MAP,assignedArea, INTITAL_PLACE)

            ############################## initializing completed ##################################################################
            elif (int(tag) == int(Message.PERSONS_DETAILS)):
                global PERSON_DETAILS
                PERSON_DETAILS = j['Body'][0]['Message'][0]
                print PERSON_DETAILS
##                global socket
##                socket = getSocket()
##                sendMsgToVideoProcessor("upper:#342342,lower:#345678")
                print "client request recieved"
                # assignedArea = [INTITAL_PLACE, [0,7],[0,10],[3,11],[5,10],[5,8],[5,5],[3,5]]
                # print "Area assigned"
                # print assignedArea
                #
                # from KeyPointCoverage import mainKeyPointCoverage as mainKeyPointCoverage
                # mainKeyPointCoverage(AREA_MAP,assignedArea, INTITAL_PLACE)

            elif (int(tag) == int(Message.PERSON_DETECTED)):
##                sendMsgToVideoProcessor("stop")
                print "Person detected"
                from CompassControl import personDetectedNotify
                personDetectedNotify(Message.PERSON_DETECTED)

        elif (currentEvent == interrupt.Interrupt.VIDEO_PROCESSOR_NOTIFICATION):
            print "VIDEO_PROCESSOR_NOTIFICATION"
            from CompassControl import currentLocation
            currentLocationofAgent = currentLocation

        elif (currentEvent == interrupt.Interrupt.ULTRASONIC_NOTIFICATION):
            print "ULTRASONIC_NOTIFICATIONNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNN"
            from CompassControl import ultrasonicDistance
            from CompassControl import remainingTicks
            if remainingTicks >20 :
                ultrasonicDistance(remainingTicks)

            from KeyPointCoverage import mainKeyPointCoverage as mainKeyPointCoverage
            # assignedArea = [[3,11],[5,10],[5,8],[5,5],[3,5]]
            from CompassControl import updatedAssignedArea
            from CompassControl import currentLocation
            print "currentLocation from client_modified: ",currentLocation
            updatedAssignedArea.insert(0,currentLocation)
            print "remainKeypoints: ",updatedAssignedArea
            if (len(updatedAssignedArea)>2):
                mainKeyPointCoverage(AREA_MAP, updatedAssignedArea, INTITAL_PLACE)
            elif (len(updatedAssignedArea)==2):
                from CompassControl import goToStart as goToStart
                goToStart(currentLocation, INTITAL_PLACE)
            else:
                print "Completion"

        elif (currentEvent == interrupt.Interrupt.GOTO_START):
            from CompassControl import goToStart as goToStart
            from CompassControl import currentLocation
            goToStart(currentLocation, INTITAL_PLACE)
            print "Key Point Coverage Completion"

        elif (currentEvent == interrupt.Interrupt.COMPLETION_NOTIFICATION):
            print "Key Point Coverage Completion"


                

def getSocket():
    HOST = 'localhost'   # The remote host
    PORT = 50001              # The same port as used by the server
    s = None
    for res in socket.getaddrinfo(HOST, PORT, socket.AF_UNSPEC, socket.SOCK_STREAM):
        af, socktype, proto, canonname, sa = res
        try:
            s = socket.socket(af, socktype, proto)
        except socket.error as msg:
            s = None
            continue
        try:
            s.connect(sa)
        except socket.error as msg:
            s.close()
            s = None
            continue
        if socket is None:
            print 'could not open socket'
            sys.exit(1)
        else:
            return s


def sendMsgToVideoProcessor(msg): 
    socket.sendall(msg)
    data = socket.recv(1024)
    print 'Received', repr(data)



##-------------------- Message Format ------------------------------------------##
def formatTheMessageAndSend(msg, tag, sender, receiver, priority):
    message = {'Header':
        {
            'Sender': sender,
            'Reciever': receiver,
            'TimeStamp': strftime("%Y-%m-%d %H:%M:%S", gmtime()),
            'Tag': tag,
            'Priority': priority,
            'CoomunicatorGroup': "",
        },
        'Body':
            {
                'Message': msg
            }
    }

    msgPacket = json.dumps(message)
    return msgPacket


##-------------------- End of WebSocket Connection ---------------------------------##



def main():
    try:
        
        interrupt.currentEvent = interrupt.Interrupt.NO_EVENT
        CommunicatorGroup = {}        

        ######### Register to the Service #############
        serverIp = registerToService()
        global COORDINATOR
        COORDINATOR = serverIp[0]
        global AGENT_IP
        AGENT_IP = serverIp[1]
        newEndPoint = "ws://" + COORDINATOR + ":" + WEBSOCKET_SERVER_ENDPOINT.split(":")[2]

        ######### Create Web Socket Connection ########

        ws = DummyClient(newEndPoint)
        ws.connect()
        
        ######### Start Battery Monitoring Thread #####
        thread.start_new_thread(monitorBatteries, (ws,))

        CommunicatorGroup[COORDINATOR] = ws
        interrupt.currentEvent = interrupt.Interrupt.REGISTER_TO_SERVICE

        ######### Start the main process of Agent #######
        while True:
            try:
                agentMainProcess(interrupt.currentEvent, CommunicatorGroup);
                interrupt.currentEvent = interrupt.Interrupt.NO_EVENT
                ws.run_forever()
            except KeyboardInterrupt:
                print('interrupted')

    except KeyboardInterrupt:
        print "Exception"
        ws.close()

    print "App closed"


if __name__ == "__main__":
    main()
