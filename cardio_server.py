
from rsa import encrypt
from cryptography_tools import Cryptography_tools
from pacemaker import Pacemaker
from base64 import encode
import sys
import errno
import socket
import threading
import json as js
import chardet

#debug boolean disabled by default 
debug = False


class Cardio_server():

    def __init__(self):
        #tcp_socket settings
        self._tcp_ip = "127.0.0.1"
        self._buff_size = 8196
        self._tcp_port = 8080
        self._tcp_sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.crypto_tools = Cryptography_tools() 
        self.connections = []  
        
        #if debug enabled run basic interface 
        if(debug == True):
            self.basic_menu
    
   
    #debug menu     
    def basic_menu(self):
        
        print("Command List \n 1: exit\n 2: run server")
        while True:
            command = input("enter command:  ")
            if command == '1':
                if self.server_running is False:
                #self._tcp_sock.shutdown()
                    print("run server must be ran befoe shutting down ")

                else:
                    self._tcp_sock.close()
                    sys.exit(0)
            if command == '2':
                self.create_server()
                
        
        
    def create_server(self):
        #creates server 
        #if port in use, attempts to bind alternative port 
        try:
            self._tcp_sock.bind((self._tcp_ip,self._tcp_port))
            
        except socket.error as e:
            # if error is address in use self._tcp_port equals alternative port 
            if e.errno == errno.EADDRINUSE:
                    print(("Port %s in use, using alternative port"%(str(self._tcp_port))))
                    self._tcp_port = 10080
                    print("using port: ",self._tcp_port)
                    self._tcp_sock.bind((self._tcp_ip,self._tcp_port))
                    
        #server running boolean, limits connections to 1 client 
        self.server_running = True
        self._tcp_sock.listen(1)
        print('Server running')
        
        #runs client listener on its own thread 
        listener_thread = threading.Thread(target=self.client_listener)
        listener_thread.daemon = True
        listener_thread.start()
        print("listener started")
        
        
    #handles client connections
    def client_handler(self,c,a):
        #listens for data from client if no data client disconnected
        while True:
            data = c.recv(self._buff_size)
          
            if not data:
                print('Pacemaker: ',c," is disconnected")
                break

            #converts from bytes back to json
            data = js.loads(str(data,"utf-8"))
            data = data['data']
            
            #loops through data if header equal inital coonection from client get pacemaker ID 
            for x in data:    
            #if header is id print id and save to list 
                if (x['header'] == 'pacemaker_identity'):
                    print("pacemaker id is ",x['pacemaker_id'])
                    #TODO add save to list 
                
                #this is the gui will recieve the update from the client
                if(x['header'] == "update"):
                        mode = x["mode"]
                        battery = x["battery"]
                        pace = x["pace"]
                        encrypt_status = x["encryption"]

                        self.update_gui(mode,battery,pace,encrypt_status)

            print(data)
    #returns vars for gui to update
    def update_gui(self,mode,battery,pace,encrypt_status):
        return mode,battery,pace,encrypt_status

    def decode_message(self,data):
        
        pass
        #decrypt
        return data
        
            
    def client_listener(self):
        
        while True:
            
            c,a = self._tcp_sock.accept()
            print("client",c," connected")
            self.connections.append(c)

            client_thread = threading.Thread(target=self.client_handler,args=(c,a))
            client_thread.daemon = True
            client_thread.start()
           
            
    def send_msg(self,data):
          for connection in self.connections:
            
            msg = str(data,encoding='utf-8')
            connection.send(bytes(msg,encoding='utf-8'))
           
    
   

            
    def set_encrypt_on_off(self,encrypt):


        if encrypt == False:
            
        
            data = {"data":[
                    {"header":"command", "command_name": "set_encryption",
                        "value":False}
                    ]
                }
            
        if encrypt == True:
            data = {"data":[
                    {"header":"command", "command_name": "set_encryption",
                        "value":True}
                    ]
                }




        data  = js.dumps(data)
        data = self.crypto_tools.encrypt(data)

        self.send_msg(data) 

        

       
            
            
