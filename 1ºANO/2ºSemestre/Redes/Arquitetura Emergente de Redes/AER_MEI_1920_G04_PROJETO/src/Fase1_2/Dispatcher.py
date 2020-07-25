
import socket
import pickle
import struct

import Routing_Manager
from threading import Condition,Thread
from Event import Event

class Dispatcher:

    MULTICAST_IP = "ff02::abcd:1"
    PORT = 9999
    DATA_SIZE = 1024

    def __init__(self,name,Routing_Manager,net_layer_queue,net_layer_condition):
        
    # Data structures
        self.event_queue = [] # list of events waiting to be processed or redirected to the place where it should be processed
                              # For example, a new Hello_Init should send the broacast message to all, a Hello_Response should be
                              # redirected to the Routing_Manager

        self.pending_client_request = [] # GET/PUT of the Client waiting for a Route_Request to terminate to be send (finding the destination host next jump)
        
        # Client side
        self.net_layer_queue = net_layer_queue

    # Locks/Conditions
        self.event_condition = Condition()  #  Condition  for the event queue
        self.net_layer_condition = net_layer_condition 
    
    # Manager of the Routing Table and responsible for processing the events Hello,Route
        self.Routing_Manager = Routing_Manager
        self.Routing_Manager.set_Event_Queue(self.event_queue,self.event_condition)
        
    # Class Properties and Utilities
        self.socket = socket.socket(socket.AF_INET6,socket.SOCK_DGRAM) # UDP socket
        self.name = name

    # Waits for packets, unpacks them and adds them do the Event Queue
    def listener_UDP(self):
        sock = self.socket

        # Allows address to be reused
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(("",Dispatcher.PORT))

        # Allow messages from this socket to loop back for development
        sock.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_MULTICAST_LOOP, True)

        # Construct message for joining multicast group
        mreq = struct.pack("16s15s".encode('utf-8'), socket.inet_pton(socket.AF_INET6, "ff02::abcd:1"), (chr(0) * 16).encode('utf-8'))
        sock.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_JOIN_GROUP, mreq)

        while True:
            data,adrr = sock.recvfrom(Dispatcher.DATA_SIZE)
            unpickled_data = pickle.loads(data)
            
            if Event.PUT_INFO == unpickled_data.type or Event.GET_INFO == unpickled_data.type or Event.REPLY_INFO == unpickled_data.type or not ((unpickled_data.data["ip"]) == self.Routing_Manager.ip):
                
                self.event_condition.acquire()
                self.event_queue.append(unpickled_data)
                self.event_condition.notify()
                self.event_condition.release()
        sock.close()

    def process_Events(self):
        while True:
            self.event_condition.acquire()
            while len(self.event_queue) <= 0:
                self.event_condition.wait()
            event = self.event_queue.pop(0)
            self.event_condition.release()
            data = event.data
            
            process_functions = [self.routing_process,self.routing_process,self.routing_process,self.routing_process,self.client_process,self.client_process,self.client_process,self.route_success_process,self.route_failed_process]

            process_function = process_functions[event.type-1]
            process_function(event)
                
            

    def routing_process(self,event : Event):
        data = event.data

        if data["ip"] is self.Routing_Manager.ip:
            if event.type == Event.HELLO_INIT  or  event.type == Event.ROUTE_REQUEST:
                self.socket.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_MULTICAST_LOOP, True)
                self.socket.sendto(pickle.dumps(event),(Dispatcher.MULTICAST_IP,Dispatcher.PORT))
                self.socket.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_MULTICAST_LOOP, False)
            elif event.type == Event.ROUTE_REPLY:
            # Send the reply to next in the reverse path
                dest = event.data["table"][event.data["position"]+1]["name"]
                try:
                    next_hop = self.Routing_Manager.get_Route(dest)
                    self.socket.sendto(pickle.dumps(event),(next_hop,Dispatcher.PORT))    
                except ValueError as vs:
                    # if the reverse route cannot continue
                    print("Reverse path not found")
                    pass  
        elif event.type >= Event.HELLO_INIT and event.type <= Event.ROUTE_REPLY:
            if event.type == Event.HELLO_INIT:     
                event.type = Event.HELLO_RESPONSE

            self.Routing_Manager.add_event_processing(event)

    def client_process(self,event : Event):
        data = event.data
       
        if data["destination"] == self.name:
           
            self.net_layer_condition.acquire()
            self.net_layer_queue.append(event)
            self.net_layer_condition.notify()
            self.net_layer_condition.release()
        else:
            try:
                next_hop = self.Routing_Manager.get_Route(data["destination"])
                self.socket.sendto(pickle.dumps(event),(next_hop,Dispatcher.PORT))
            except Exception as vss:
                # Start a route request to find the destination
                self.pending_client_request.append(event)
                if (not self.Routing_Manager.is_request_pending(data["destination"])) and (self.Routing_Manager.is_request_available(data["destination"])):

                    route_event = self.Routing_Manager.create_route_request(data["destination"])
                    self.Routing_Manager.add_pending_request(data["destination"])
                    self.socket.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_MULTICAST_LOOP, True)
                    self.socket.sendto(pickle.dumps(route_event),(Dispatcher.MULTICAST_IP,Dispatcher.PORT))
                    self.socket.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_MULTICAST_LOOP, False)
    
    def route_failed_process(self,event : Event):
        self.remove_pending_client(event.data)
    
    def route_success_process(self,event : Event):
        data = event.data
        try:
            next_hop = self.Routing_Manager.get_Route(data["destination"])
            
        except Exception as es:
            next_hop = None
        i = 0
        while i < len(self.pending_client_request):
            elem = self.pending_client_request[i]
            if next_hop != None and elem.data["destination"] == data["destination"]:
                self.pending_client_request.pop(i)
                self.socket.sendto(pickle.dumps(elem),(next_hop,Dispatcher.PORT))
        
            elif elem.data["destination"] == data["destination"]:
                self.pending_client_request.pop(i)

    def remove_pending_client(self,data):
        i = 0
        while i < len(self.pending_client_request):
            elem = self.pending_client_request[i]
            if elem.data["destination"] == data["destination"]:
                self.pending_client_request.pop(i)

    def run(self):
         # Routing Manager
        self.Routing_Manager.run()
        
        # Dispatcher
        process_Thread = Thread(target=self.process_Events)
        listener_Thread = Thread(target=self.listener_UDP)
        
        # starting Dispatcher Threads
        process_Thread.start()
        listener_Thread.start()
