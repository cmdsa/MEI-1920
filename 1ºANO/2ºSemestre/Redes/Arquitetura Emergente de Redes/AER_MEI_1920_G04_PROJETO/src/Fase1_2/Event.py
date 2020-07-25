
class Event:

    NUMBER_TYPES = 9

    # Events
    HELLO_INIT = 1 # The Event who inits the process of discovery in a radius of 2
    HELLO_RESPONSE = 2 # The response of Hello_Init, just for distinguish purposes
    ROUTE_REQUEST = 3 # The Request for a flooding to find a specific host
    ROUTE_REPLY = 4 # Reply of a sucessful Route_Request
    GET_INFO = 5 # Get of information by the Client
    PUT_INFO = 6 # Put of information by the Client
    REPLY_INFO = 7 # Reply of a Get of information by the Client
    ROUTE_SUCESS = 8 # Internal Event to inform that the Route Request that it "requested" has succeeded
    ROUTE_FAILED = 9 # Internal Event to inform that the Route Request that it "requested" has failed 
    
    TRASH = 0

    def __init__(self,type,data):
        if type > 0 and type < (Event.NUMBER_TYPES+1):
            self.type = type
            self.data = data