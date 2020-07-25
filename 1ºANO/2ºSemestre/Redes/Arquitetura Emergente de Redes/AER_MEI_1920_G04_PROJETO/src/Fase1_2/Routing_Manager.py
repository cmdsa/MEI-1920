from threading import Lock,Thread,Condition
import time
import socket
import pprint
import sys
import copy
from random import randint
from Event import Event

class Routing_Manager:

    def __init__(self,name, hello_interval,dead_interval,ip,debug=False,garbage_collection_number=100,route_request_wait=200,unavaliable_time=8,split_size = 1024,delete_entry=3,ttl=5,debug_time=3):
        # Configuration
        self.dead_interval = dead_interval # Time it has to pass, to be marked as dead
        self.hello_interval = hello_interval # Time between Hello_init being added to the queue event
        self.shutdown = False # Bool to shutdown
        self.garbage_collection_number = garbage_collection_number # Number of update to the routing table needed to check if there is garbage(dead) entry that should be deleted
        self.delete_entry = delete_entry # Number of times it has to be marked as dead to actually deleted, this is done so near hosts can also mark as dead the entry and not resend it
        self.split_size = split_size # The maximum size of the table sent in a Hello packet
        self.debug = debug # Bool that determines if is in debug mode
        self.debug_time = debug_time # Time between each print
        # Route_Request/Reply configurations
        self.ttl = ttl # Time-to-Live, number of jumps before this packet is discarded
        self.route_request_wait = route_request_wait # Time to wait before the route request is discarded
        self.unavaliable_time = unavaliable_time # Time that the node is unavaliable after a failed Route_Request
        
        # Data strucutures 
        self.routing_table = dict()
        self.routing_condition = Condition()
        self.processing_queue = []
        self.processing_condition = Condition()
        self.pending_request = []
        self.unavaliable_request = []
        self.pending_condition = Condition()
        
        
        # Class Properties
        self.name = name
        self.sequence_number = randint(0,2**32)
        self.ip = ip
        

    def set_Event_Queue(self,event_queue,lock_condition : Condition):
        self.event_queue = event_queue
        self.event_condition = lock_condition

    # DEAD ENTRIES FUNCTIONS

    def collect_gargabe(self):
        # dead nodes cleaning
        key_list = list(self.routing_table.keys())
        for key in key_list:
            self.dead_mark(key)    
        # Unavialable destination cleaning     
        time_actual = time.time()
        i = 0
        while i < len(self.unavaliable_request):
            if (time_actual - self.unavaliable_request[i]["time"]) >= 0:
                self.unavaliable_request.pop(i)
            else:
                i+=1
                   

    def dead_mark(self,key):
        is_dead = False
        if "dead" in self.routing_table[key]:
                self.routing_table[key]["dead"] += 1
                is_dead = True
                if self.routing_table[key]["dead"] > self.delete_entry:
                    del self.routing_table[key]
        elif (time.time() - self.routing_table[key]["time"]) > self.dead_interval:
                self.routing_table[key]["dead"] = 0 
                is_dead = True
        return is_dead
    
    def is_request_available(self,destination):
        avaliable = True
        self.pending_condition.acquire()
        for entry in self.unavaliable_request:
            if entry["destination"] == destination:
                avaliable = False
                break
        self.pending_condition.release()

        return avaliable
    # TABLE FUNCTIONS

    def update_routing_table(self,event):
        data = event.data
        # Add the node that responded
        response_node = data["name"]
        if not (response_node in self.routing_table):
            self.routing_table[response_node] = {"ip": data["ip"],"jump": response_node,"sequence_number": data["sequence_number"],"radius": 1,"time": time.time()}
        else:
            original_entry = self.routing_table[response_node]    
            if (original_entry["sequence_number"] < data["sequence_number"]):
                self.routing_table[response_node] = {"ip": data["ip"],"jump": response_node,"sequence_number": data["sequence_number"],"radius": 1,"time": time.time()}


        # Check table received in response
        response_table = data["table"]
        for key in response_table:
            response_entry = response_table[key]
            self.remove_pending_request(key)
            # Update the next jump parameter to the host that sent this routing table and update the time of contact
            response_entry["time"] = time.time()
            response_entry["radius"] = 2 # The nodes at radius one only send back their routing table for nodes with radius 1 for them so 2 radius to this node
            response_entry["ip"] = data["ip"]
            if key == self.name:
                continue
            if not key in self.routing_table:    
                self.routing_table[key] = response_entry
            else:
                original_entry = self.routing_table[key]
                if original_entry["sequence_number"] < response_entry["sequence_number"]:
                    self.routing_table[key] = response_entry
        

    def update_routing_table_reply(self,event):
        data = event.data
        # Add the node that responded
        
        response_node = data["name"]
        if not (response_node in self.routing_table):
            self.routing_table[response_node] = {"ip": data["ip"],"jump": response_node,"sequence_number": data["sequence_number"],"radius": 1,"time": time.time()}
        else:
            original_entry = self.routing_table[response_node]    
            if (original_entry["sequence_number"] < data["sequence_number"]):
                self.routing_table[response_node] = {"ip": data["ip"],"jump": response_node,"sequence_number": data["sequence_number"],"radius": 1,"time": time.time()}
        
        position =  data["position"]
        radius = position
        if data["destination"] != self.name:
            if not (data["destination"] in self.routing_table):
                self.routing_table[data["destination"]] = {"ip": data["ip"],"jump": response_node,"sequence_number": data["destination_sequence"],"radius": data["destination_radius"] + radius,"time": time.time()}
            else:
                original_entry = self.routing_table[response_node]    
                if (original_entry["sequence_number"] < data["destination_sequence"]):
                    self.routing_table[data["destination"]] = {"ip": data["ip"],"jump": response_node,"sequence_number": data["destination_sequence"],"radius": data["destination_radius"] + radius,"time": time.time()}
        
        table_copy = copy.deepcopy(data["table"])

        for entry in table_copy:
            
            if radius <= 0:
                # Update with the host next to this in the list?
                break

            if self.name != entry["name"]:
                entry["time"] = time.time()
                entry["radius"] = radius
                entry["jump"] = response_node
                entry["ip"] = data["ip"]
                if not entry["name"] in self.routing_table:    
                    self.routing_table[entry["name"]] = entry
                    
                else:
                    original_entry = self.routing_table[entry["name"]]
                    if original_entry["sequence_number"] < entry["sequence_number"]:
                        self.routing_table[entry["name"]] = entry
                    elif original_entry["sequence_number"] == entry["sequence_number"] and original_entry["radius"] > radius:
                        self.routing_table[entry["name"]] = entry
                del entry["name"]

            radius-=1
    
    
    def split_routing_table(self):
        list_of_tables = []
        
        new_table = dict()
        total_size = 0
        if not self.routing_table:
            return [{}]

        for key in self.routing_table:
            entry = self.routing_table[key]
            
            if not ("dead" in entry) and entry["radius"] == 1:
                entry_size = sys.getsizeof(entry)
                
                total_size += entry_size
                if total_size > self.split_size:
                    total_size = entry_size
                    list_of_tables.append(new_table)
                    new_table = dict()
                new_table[key] = {"ip":entry["ip"],"sequence_number": entry["sequence_number"]}
        list_of_tables.append(new_table)        
        return list_of_tables
    
    # EVENTS FUNCTIONS

    def add_event_processing(self,event):
        self.processing_condition.acquire()
        self.processing_queue.append(event)
        self.processing_condition.notify()
        self.processing_condition.release()

        
    def add_hello_event(self):
        splitted_table = self.split_routing_table()
        for sub_table in splitted_table:
            hello_data = {"name": self.name,"ip": self.ip,"sequence_number":self.sequence_number,"table":sub_table}
            hello_event = Event(Event.HELLO_INIT,hello_data)
            self.event_queue.append(hello_event)
        # Increase the number of times I have given information about myself
        self.sequence_number += 1 

    def process_hello_response(self,event):
        self.routing_condition.acquire()
        self.update_routing_table(event)
        self.routing_condition.release()

    def create_route_request(self,destination,ttl=None,table=None):
        # Lock with routing_condition?
        if ttl is None:
            ttl = self.ttl
        if table is None:
            table = []
        
        table.append({"name": self.name,"sequence_number": self.sequence_number})
        route_data = {"name": self.name,"ip": self.ip,"sequence_number":self.sequence_number,"destination": destination,"TTL": ttl,"table" : table}
        self.sequence_number += 1
        route_event = Event(Event.ROUTE_REQUEST,route_data)
        return route_event
    
    def create_route_reply(self,route_event : Event,position=0):
        
        data = route_event.data

        route_reply_data = {"name": self.name,"destination_radius": data["destination_radius"],"destination": data["destination"],"destination_sequence": data["destination_sequence"],"ip":self.ip,"sequence_number":self.sequence_number,"position": position,"table": data["table"]}
        route_reply = Event(Event.ROUTE_REPLY,route_reply_data)
        self.sequence_number += 1
        return route_reply
    
    def create_route_sucess(self,destination):
        data = {"destination": destination}
        route_sucess = Event(Event.ROUTE_SUCESS,data)
        return route_sucess

    def create_route_fail(self,destination):
        data = {"destination": destination}
        route_fail = Event(Event.ROUTE_FAILED,data)
        return route_fail

    def process_route_request(self,event):
        data = event.data
        
        if self.cycle_detection(event):
            return

        self.routing_condition.acquire()
        if data["destination"] == self.name:
            event_reply = self.create_route_reply(event)
            self.remove_pending_request(data["destination"])
            
        else :
            try:    
                entry = self.get_Route(data["destination"],isEntry=True)
                data["destination_sequence"] = entry["sequence_number"]
                data["destination_radius"] = entry["radius"]
                
                data["table"].append({"name":self.name,"sequence_number": self.sequence_number})
                data["table"].reverse()
                event_reply = self.create_route_reply(event)
                
            except ValueError as ve:
                # The host does not know the destination
                event_reply = self.create_route_request(data["destination"],data["TTL"]-1,data["table"])
                

        self.event_condition.acquire()
        self.event_queue.append(event_reply)
        self.event_condition.notify()
        self.event_condition.release()
        self.routing_condition.release()
              
    def cycle_detection(self,event : Event):
        table = event.data["table"]
        isHere = False
        for entry in table:
            if entry["name"] == self.name:
                isHere = True
                break
        return isHere

    def is_request_pending(self,destination):
        pending = False
        self.pending_condition.acquire()
        
        for entry in self.pending_request:
            if destination == entry["destination"]:
                pending = True
                break

        self.pending_condition.release()
        return pending

    def add_pending_request(self,destination):
        self.pending_condition.acquire()
        self.pending_request.append({"destination":destination,"time":time.time() + self.route_request_wait})
        self.pending_condition.notify()
        self.pending_condition.release()
    
    def remove_pending_request(self,destination):
        self.pending_condition.acquire()
        
        i=0
        for entry in self.pending_request:
            if entry["destination"] == destination:
                break
            i+=1
        if i < len(self.pending_request):
            self.pending_request.pop(i)
        self.pending_condition.release()

    def process_route_reply(self,event):
        data = event.data
        data["position"] += 1
        self.routing_condition.acquire()
        if data["position"] == (len(data["table"])-1):
            # Notify that it has reached
            event_sucess = self.create_route_sucess(data["destination"])
            self.pending_condition.acquire()
            
            i = 0
            while i < len(self.pending_request):
                elem =  self.pending_request[i]
                if elem["destination"] == data["destination"]:
                    self.pending_request.pop(i)
                else:
                    i+=1
            
            self.event_condition.acquire()
            self.event_queue.append(event_sucess)
            self.event_condition.notify()
            self.event_condition.release()
            
            self.pending_condition.release()

            
        else:
            # Pass it to another host
            event_reply = self.create_route_reply(event,data["position"])
            self.event_condition.acquire()
            self.event_queue.append(event_reply)
            self.event_condition.notify()
            self.event_condition.release()

        self.update_routing_table_reply(event)
        self.routing_condition.release()

    # GET FUNCTIONS

    def get_Route(self,destination_name,isEntry=False):
        self.routing_condition.acquire()
        if not destination_name in self.routing_table:
            self.routing_condition.release()
            raise ValueError("Entry for this destination does not exist")
        is_dead = self.dead_mark(destination_name)
        if is_dead:
            self.routing_condition.release()
            raise ValueError("Route entry, probably dead")
        table_entry = self.routing_table[destination_name]
        entry = {"ip": table_entry["ip"], "sequence_number": table_entry["sequence_number"],"radius" : table_entry["radius"]}
        self.routing_condition.release()
        if isEntry:
            return entry
        return entry["ip"]

    # MAIN THREADS FUNCTIONS

    def hello_protocol(self):
       
        while not self.shutdown:
            
            time.sleep(self.hello_interval)
            
            self.routing_condition.acquire()
            self.event_condition.acquire()

            self.add_hello_event() 
            self.event_condition.notify()

            self.event_condition.release()
            self.routing_condition.release()
            
        

    def processing(self):
        garbage_index = 0
        event_processing = [self.process_hello_response,self.process_route_request,self.process_route_reply]

        while not self.shutdown:
            self.processing_condition.acquire()
            while len(self.processing_queue) <= 0:
                self.processing_condition.wait()
            event = self.processing_queue.pop(0)
            self.processing_condition.release()
            if Event.HELLO_RESPONSE <= event.type and Event.ROUTE_REPLY >= event.type:
                f = event_processing[event.type-2]
                # if it of the kind that updates the routing table
                garbage_index+=1
                if garbage_index == self.garbage_collection_number:
                    self.routing_condition.acquire()
                    self.pending_condition.acquire()
                    self.collect_gargabe()
                    self.pending_condition.release()
                    self.routing_condition.release()
                    garbage_index = 0 
                f(event)

    def route_request_timer(self):
        while not self.shutdown:
            self.pending_condition.acquire()
            while True:
                if (len(self.pending_request)) > 0:
                    delta_time = self.pending_request[0]["time"] - time.time()
                    if  delta_time <= 0 :
                        break
                    else:
                        self.pending_condition.wait(timeout=delta_time)
                else:
                    self.pending_condition.wait()
            self.unavaliable_request.append({"destination":self.pending_request[0]["destination"],"time": time.time() + self.unavaliable_time})
            event_pending = self.pending_request.pop(0)
            self.event_condition.acquire()
            self.pending_condition.release()
            event_fail = self.create_route_fail(event_pending["destination"])
            self.event_queue.append(event_fail)
            self.event_condition.notify()
            self.event_condition.release()

    # Prints in time to time the content of the Routing Table, Pending Route_Request List
    def debug_prints(self):
        while not self.shutdown:
            time.sleep(self.debug_time)
            self.routing_condition.acquire()

            print(self.name)
            print("\n")

            print("---------- Routing Table --------\n")
            pprint.pprint(self.routing_table)
            print("---------------------------------\n\n")
            self.routing_condition.release()
        
            self.pending_condition.acquire()
            
            print("---------- Pending Request ------\n")
            pprint.pprint(self.pending_request)
            print("---------------------------------\n\n")

            print("---------- Unavailable ----------\n")
            print(self.unavaliable_request)
            print("---------------------------------\n\n")

            self.pending_condition.release()  
    # MAIN FUNCTION

    def run(self):
        # Initialize Threads that keep running the HELLO_REQUEST protocol, updating the routing table and processing the Events incoming
        hello_thread = Thread(target=self.hello_protocol)
        processing_thread = Thread(target=self.processing)
        route_timer_thread = Thread(target=self.route_request_timer)
    
        hello_thread.start()
        processing_thread.start()
        route_timer_thread.start()

        if self.debug:
            debugging_thread = Thread(target=self.debug_prints)
            debugging_thread.start()