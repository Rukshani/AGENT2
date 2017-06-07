

##-------------------- List of Intrrupts ---------------------------##

class Interrupt:
    NO_EVENT = 0
    INCOMING_MESSAGE = 1
    CRITICAL_BATTERY_LEVEL_REACHED = 2
    REGISTER_TO_SERVICE = 3
    VIDEO_PROCESSOR_NOTIFICATION = 4


currentEvent = ""
