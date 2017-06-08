
##-------------------- List of Intrrupts ---------------------------##

class Interrupt:
    NO_EVENT = 0
    INCOMING_MESSAGE = 1
    CRITICAL_BATTERY_LEVEL_REACHED = 2
    REGISTER_TO_SERVICE = 3
    VIDEO_PROCESSOR_NOTIFICATION = 4
    ULTRASONIC_NOTIFICATION = 5
    GOTO_START = 6
    COMPLETION_NOTIFICATION = 7

currentEvent = ""