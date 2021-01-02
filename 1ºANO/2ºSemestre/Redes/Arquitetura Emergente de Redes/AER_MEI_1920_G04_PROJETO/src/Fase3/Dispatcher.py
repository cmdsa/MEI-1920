import socket
import struct
import pickle

from threading import Thread,Condition
from Event import Event

class Dispatcher:

    MULTICAST_IP = "ff02::abcd:1"
    PORT = 9999
    DATA_SIZE = 1024

    def __init__(self,routing_manager):

        # Data strutuctures
        self.event_queue = []
        self.routing_manager = routing_manager

        # Conditions
        self.event_condition = Condition()

        # Class Properties and Utilities
        self.socket = socket.socket(socket.AF_INET6,socket.SOCK_DGRAM) # UDP socket

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
            print(unpickled_data.data)
            if unpickled_data.data["hostname"] == socket.gethostname():
                continue
            self.event_condition.acquire()
            self.event_queue.append(unpickled_data)
            self.event_condition.notify()
            self.event_condition.release()

        sock.close()
    
    def processing(self):

        processing_functions = [self.routing_manager.process_interest,None,self.routing_manager.process_response]

        while True:
            self.event_condition.acquire()
            while len(self.event_queue) <= 0:
                self.event_condition.wait()
                
            
            event = self.event_queue.pop(0)
            self.event_condition.release()
            if event.data["hostname"] == socket.gethostname():
                response = event
            else:
                print("PROCESSING")
                print(event.type)
                print(event.data)
                process = processing_functions[event.type - 1]
                response = process(event.data,1)
               
            
            
            
            if response != None:
                print("MULTICASTING")
                print(response.data)
               
                self.socket.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_MULTICAST_LOOP, True)
                self.socket.sendto(pickle.dumps(response),(Dispatcher.MULTICAST_IP,Dispatcher.PORT))
                self.socket.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_MULTICAST_LOOP, False)
                
    def run(self):
        
        process_thread = Thread(target=self.processing)
        listener_thread = Thread(target=self.listener_UDP)

        process_thread.start()
        listener_thread.start()