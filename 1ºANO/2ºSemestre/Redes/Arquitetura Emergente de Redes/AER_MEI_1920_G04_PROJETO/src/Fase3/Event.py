
class Event:

    NUMBER_TYPES = 3

    # Events
    INTEREST = 1
    STORE = 2
    RESPONSE = 3
    
    
    TRASH = 0

    def __init__(self,type,data):
        if type > 0 and type < (Event.NUMBER_TYPES+1):
            self.type = type
            self.data = data