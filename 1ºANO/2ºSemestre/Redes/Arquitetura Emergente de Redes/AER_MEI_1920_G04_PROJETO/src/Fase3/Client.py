from Routing_Manager import Routing_Manager
from Event import Event
import socket
from threading import Thread,Condition
import os
import random

class Client:

    PORT = 9999
    DATA_SIZE = 1024

    def __init__(self,hop_limit=3,lifetime=30):

        
        
        
        self.tcp_socket = socket.socket(socket.AF_INET6,socket.SOCK_STREAM)
        self.connection = None
        self.hostname = socket.gethostname()

        self.event_queue = []
        self.event_condition = Condition()

        self.hop_limit = hop_limit
        self.lifetime = lifetime
        self.freshness_period = int(lifetime/2)

        self.routing_Manager = Routing_Manager(self,self.event_queue,self.event_condition,self.freshness_period)

    def processing(self):
        while True:
            self.event_condition.acquire()
            while len(self.event_queue) <= 0:
                self.event_condition.wait()
                
            event = self.event_queue.pop(0)
            self.event_condition.release()

            functions = [self.process_interest,self.process_store,self.process_response]
            f = functions[event.type-1]
            f(event.data)
    
    def process_interest(self,data):
        self.routing_Manager.process_interest(data,Routing_Manager.APP_FACE)

    def process_store(self,data):
        self.routing_Manager.process_store(data)
    
    def process_response(self,data):
        print("RESPONSE 2.0")
        print(data)
        if "name" in data and "content" in data:
            self.connection.send(data["name"].encode("utf-8"))
            self.connection.send("\n".encode("utf-8"))
            self.connection.send(data["content"].encode("utf-8"))
            
        else:
            self.connection.send("Mal-formed response".encode("utf-8"))
            self.connection.send("\n".encode("utf-8"))

    def listener_TCP(self):
        tcp_sock = self.tcp_socket
        tcp_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        tcp_sock.bind(("localhost",Client.PORT))
        tcp_sock.listen(1)

        conn,adrr = tcp_sock.accept()
        self.connection = conn
        while True:
            data,adrr = conn.recvfrom(Client.DATA_SIZE)    
            decoded = data.decode("utf-8")
            
            
            if decoded.strip() == "exit" :
                break

            parsed_data = self.parse(decoded)
            if not parsed_data is None:
                self.add_event(parsed_data)
                
        
        conn.close()
        tcp_sock.close()

    def parse(self,data):
        splitted_data = data.split()
        event = None
        event_data = dict()

        if len(splitted_data) >= 2 and splitted_data[0] == "GET":
            event_data["name"] = splitted_data[1] 
            event_data["hostname"] = self.hostname
            event_data["nonce"] = os.urandom(4)
            event_data["lifetime"] = self.lifetime
            event_data["hop_limit"] = self.hop_limit
            if len(splitted_data) >= 3:
                event_data["fresh"] = splitted_data[2]
            else:
                event_data["fresh"] = "False"
                event = Event(Event.INTEREST,event_data)

        elif len(splitted_data) >= 3 and splitted_data[0] == "STORE":
            event_data["name"] = self.hostname + "/" + splitted_data[1]
            event_data["content"] = splitted_data[2]
            event_data["sequence_number"] = self.routing_Manager.getSequenceNumber()
            event = Event(Event.STORE,event_data)

        return event

    def add_event(self,event):
        self.event_condition.acquire()
        self.event_queue.append(event)
        self.event_condition.notify()
        self.event_condition.release()

    def run(self):

        processing_Thread = Thread(target=self.processing)

        processing_Thread.start()
        self.routing_Manager.run()
        self.listener_TCP()

client = Client()
client.run()