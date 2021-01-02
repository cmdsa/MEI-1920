import socket
import Event
import Dispatcher
import pickle
import Routing_Manager
import uuid
from threading import Condition,Thread

class Net_Layer:

    DATA_SIZE = 1024
    PORT = 9999
    

    def __init__(self,cache_time,isServer : bool):
        
        # Configuration
        self.cache_time = cache_time
        self.isServer = isServer
        
        # Class properties
        
        hostname = socket.gethostname()
        self.name = hostname # uuid.uuid1()
        myip = "2001::" + hostname[len(hostname)-1] 
        self.tcp_socket = socket.socket(socket.AF_INET6,socket.SOCK_STREAM)
        self.connection = None

        # Data structures
        self.information = dict()
        self.events_queue = []
        self.events_condition = Condition()
        self.manager = Routing_Manager.Routing_Manager(self.name,1,20,myip,debug = True)
        self.dispatcher = Dispatcher.Dispatcher(self.name,self.manager,self.events_queue,self.events_condition)
        
       

    def parse(self,data):
        splited_data = data.split()
    
        if len(splited_data) >= 3:
            event_type = splited_data[0]
            destination = splited_data[1]
            zone = splited_data[2]
            data = {"destination":destination,"origin": self.name,"zone":zone}
            if event_type == 'GET':
                type = Event.Event.GET_INFO
            elif event_type == 'PUT' and len(splited_data) >= 4:
                type = Event.Event.PUT_INFO
                data["desc"] = splited_data[3]
            else:
                return None
            event = Event.Event(type,data)
            return event
        return None

    # Receives packets from the "aplication layer" 
    def listener_TCP(self):
        tcp_sock = self.tcp_socket
        tcp_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        tcp_sock.bind(("localhost",Net_Layer.PORT))
        tcp_sock.listen(1)

        conn,adrr = tcp_sock.accept()
        self.connection = conn
        while True:
            data,adrr = conn.recvfrom(Net_Layer.DATA_SIZE)    
            decoded = data.decode("utf-8")
            
            
            if decoded.strip() == "exit" :
                break

            parsed_data = self.parse(decoded)
            if not parsed_data is None:
                self.dispatcher.event_condition.acquire()
                self.dispatcher.event_queue.append(parsed_data)
                self.dispatcher.event_condition.notify()
                self.dispatcher.event_condition.release()
        
        conn.close()
        tcp_sock.close()

    def processing(self):
        while True:
            self.events_condition.acquire()
            while len(self.events_queue) <= 0:
                self.events_condition.wait()
            info_event = self.events_queue.pop(0)
            self.events_condition.release()
            if self.isServer:
                if info_event.type == Event.Event.GET_INFO:
                    
                    self.process_server_get(info_event)
                elif info_event.type == Event.Event.PUT_INFO:
                    self.process_server_put(info_event)
            else:
                if info_event.type == Event.Event.REPLY_INFO:
                    self.process_client_reply(info_event)
                elif info_event.type == Event.Event.PUT_INFO:
                    pass
                

    def process_server_get(self,info):
        data = info.data
        desc = ""
        if data["zone"] in self.information:
            desc = self.information[data["zone"]]
            
        event = Event.Event(Event.Event.REPLY_INFO,{"destination": data["origin"],"origin":data["destination"],"desc": desc,"zone":data["zone"]})

        self.dispatcher.event_condition.acquire()
        self.dispatcher.event_queue.append(event)
        self.dispatcher.event_condition.notify()
        self.dispatcher.event_condition.release()

    def process_server_put(self,info):
        data = info.data
        if  "zone" in data and "desc" in data:
            self.information[data["zone"]] = data["desc"]

    def process_client_reply(self,info):
        data = info.data
        if "zone" in data:
            self.connection.send(data["zone"].encode("utf-8") + b"\n")
        if "desc" in data:
            self.connection.send(data["desc"].encode("utf-8") + b"\n")
        else:
            self.connection.send(b"No Information about that Zone")
    
    def process_client_put(self,info):
        pass

    def run(self):
        self.dispatcher.run()
        
        processing_Thread = Thread(target=self.processing)
        processing_Thread.start()
        
        if not self.isServer:
            self.listener_TCP()

