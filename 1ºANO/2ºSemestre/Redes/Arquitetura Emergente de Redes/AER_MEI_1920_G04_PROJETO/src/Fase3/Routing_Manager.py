import pickle
import time
from threading import Thread,Condition
from Dispatcher import Dispatcher
import random
import pprint
from Event import Event
import socket
import copy

class Routing_Manager:

    APP_FACE = 0
    MULTI_FACE = 1

    def __init__(self,client,client_queue,client_condition,freshness_period,debug_time=5):
        self.pit = dict()
        self.content_store = dict()
        self.forward_IB = dict()
        
        self.dispatcher = Dispatcher(self)
        
        self.client = client
        self.client_queue = client_queue
        self.client_condition = client_condition

        self.routing_condition = Condition()
        self.sequence_number = random.randint(1,10000)
        self.debug_time = debug_time
        self.freshness_period = freshness_period

    def getSequenceNumber(self):
        self.routing_condition.acquire()
        sequence_number = self.sequence_number
        self.sequence_number += 1
        self.routing_condition.release()
        return sequence_number

    def process_interest(self,data,face):

        self.routing_condition.acquire()
        if self.inContentStore(data):
            print("IN CONTENT STORE")
            self.routing_condition.release()
            return self.getContent(data,face)
        
        elif data["name"] in self.pit:
            print("IN PIT")
            self.add_pit_entry(data["name"],data,face)
            
        
        elif self.inFIB(data):
            print("FORWARDING")
            
            self.create_pit_entry(data["name"],data,face)
            self.routing_condition.release()
            return self.forward_interest(data,face)
        self.routing_condition.release()
        
        return None

    def process_store(self,data):

        result = dict()
        result["time"] = time.time()
        result["name"] = data["name"]
        result["freshness_period"] = -1 # Means that is always fresh because this is the source
        result["content"] = data["content"]
        result["sequence_number"] = data["sequence_number"]

        self.routing_condition.acquire()
        self.content_store[data["name"]] = result
        print("SAVED IN CONTENT STORE")
        self.routing_condition.release()

    def add_pit_entry(self,name,data,face):
        pit = self.pit

        if data["hop_limit"] == 0:
            return
        
        data["hop_limit"] -= 1
        data["time"] = time.time()

        list_faces = pit[name]

        for entry in list_faces:
            nonce = entry["data"]["nonce"]
            if nonce == data["nonce"]:
                return

        list_faces.append({"data":data,"face":face})
        # ...
        pit[name] = list_faces

    def create_pit_entry(self,name,data,face):
        pit = self.pit
        list_faces = []

        if data["hop_limit"] == 0:
            return
        
        data["hop_limit"] -= 1
        data["time"] = time.time()

        entry = {"data": data,"face":face}
        list_faces.append(entry)
        pit[name] = list_faces

    def delete_pit_entry(self,data):
        list_faces = self.pit[data["name"]]
        del self.pit[data["name"]]
        return list_faces

    def inContentStore(self,data):
        value = False
        if data["name"] in self.content_store:
            value = True
            result = self.content_store[data["name"]]
            if "fresh" in data and data["fresh"] == "True":
                if result["freshness_period"] == -1:
                    value = True
                else:
                    value = time.time() < (result["time"] + result["freshness_period"])

        return value

    def getContent(self,data,face):
        o_data = data
        data = self.content_store[data["name"]]
        new_data = copy.deepcopy(data)
        new_data["hostname"] = socket.gethostname()
        new_data["freshness_period"] = self.freshness_period
        event = None
        
        if Routing_Manager.APP_FACE == face:
            self.client_condition.acquire()
            self.client_queue.append(Event(Event.RESPONSE,new_data))
            self.client_condition.notify()
            self.client_condition.release()
        elif Routing_Manager.MULTI_FACE == face:
            event = Event(Event.RESPONSE,new_data)

        return event

    def inFIB(self,name):
        return True
 
    def process_response(self,data,face):
        
        if data["name"] in self.pit:
            print("RESPONSE ARRIVED")
            print(data)
            entries = self.delete_pit_entry(data)
            self.cache_Data(data)
            return self.forward_response(entries,face,data)
    
    def cache_Data(self,data):
        if not data["name"] in self.content_store or ( data["name"] in self.content_store and self.content_store[data["name"]]["sequence_number"] < data["sequence_number"]):
            result = dict()
            result["time"] = time.time()
            result["freshness_period"] =  data["freshness_period"]
            result["name"] = data["name"]
            result["hostname"] = data["hostname"]
            result["content"] = data["content"]
            result["sequence_number"] = data["sequence_number"]

            self.content_store[data["name"]] = result
            print("CACHED DATA")

    def forward_response(self,entries,face,data_R):
        event = None
        print(entries)
        for entry in entries:
            face = entry["face"]
            data = entry["data"]
            if face == Routing_Manager.APP_FACE:
                r_event = Event(Event.RESPONSE,data_R)
                self.client_condition.acquire()
                self.client_queue.append(r_event)
                self.client_condition.notify()
                self.client_condition.release()         
            elif face == Routing_Manager.MULTI_FACE:
                data["hostname"] = socket.gethostname()
                event = Event(Event.RESPONSE,data_R)

        return event    

    def forward_interest(self,data,face):
        if Routing_Manager.APP_FACE == face:
            print("thing")
            self.dispatcher.event_condition.acquire()
            self.dispatcher.event_queue.append(Event(Event.INTEREST,data))
            self.dispatcher.event_condition.notify()
            self.dispatcher.event_condition.release()
            return None
        elif Routing_Manager.MULTI_FACE == face:
            print("correct")
            data["hostname"] = socket.gethostname()
            return Event(Event.INTEREST,data)

    def clean_pit(self):
        while True:
            time.sleep(30)
            self.routing_condition.acquire()
            keys = []
            pit = self.pit
            items = pit.items()
            for tup in items:
                (key,l) = tup
                j = 0
                while j < len(l):
                    entry = l[j]["data"]
                    if entry["time"] + entry["lifetime"] < time.time():
                        l.pop(j)
                    else:
                        j=+1
                
                if len(l) <= 0:
                    keys.append(key)
            
            for i in keys:
                del pit[i]

            self.routing_condition.release()

    def clean_cs(self):
        while True:
            time.sleep(30)
            self.routing_condition.acquire()
            keys = []
            pit = self.content_store
            items = pit.items()
            for tup in items:
                (key,l) = tup
                if l["time"] + l["freshness_period"] * 5 < time.time() and l["freshness_period"] != -1:
                    keys.append(key)
            
            for i in keys:
                del pit[i]

            self.routing_condition.release()

    def debug_print(self):
        while True:
            time.sleep(self.debug_time)
            self.routing_condition.acquire()
            print(socket.gethostname())

            print("---------- Content Store --------\n")
            pprint.pprint(self.content_store)
            print("---------------------------------\n\n")
            
        

            
            print("---------- PIT ------\n")
            pprint.pprint(self.pit)
            print("---------------------------------\n\n")

            print("---------- FIB ----------\n")
            print(self.forward_IB)
            print("---------------------------------\n\n")
            self.routing_condition.release()

    def run(self):

        cleaning_thread = Thread(target=self.clean_pit)
        cleaning_cs_thread = Thread(target=self.clean_cs)
        debug_thread = Thread(target=self.debug_print)

        cleaning_cs_thread.start()
        cleaning_thread.start()
        debug_thread.start()
        self.dispatcher.run()
        

        


