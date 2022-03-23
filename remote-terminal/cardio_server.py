
from rsa import encrypt
from cryptography_tools import Cryptography_tools
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
        self.encryption = True
        self.client_connected = False
        
        self.update_mode = ""
        self.update_battery = ""
        self.update_encrypt_status = ""
        
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
            
            if (not data):
                print('Pacemaker: ',c," is disconnected")
                break
            
            if(self.encryption):
                    #decrypt
                data = self.crypto_tools.decrypt(data)
                print("decrypted data",data)
                
            #converts from bytes back to json
            data = js.loads(str(data,encoding="utf-8"))
            data = data['data']
            
            #loops through data if header equal inital coonection from client get pacemaker ID 
            for x in data:    
            #if header is id print id and save to list 
                if (x['header'] == 'pacemaker_identity'):
                    print("pacemaker id is ",x['pacemaker_id'])
                
                #this is the gui will recieve the update from the client
                if(x['header'] == "update"):
                        self.update_mode = x["mode"]
                        self.update_battery = x["battery"]
                        self.update_encrypt_status = x["encryption"]
                        #patient_ecg = x["patient_ecg"]
                        #paced_ecg = x["paced_ecg"]
                        
                        print(self.update_mode,self.update_battery,self.update_encrypt_status)

                        self.update_gui()

            print(data)
            
            
    #returns vars for gui to update
    def update_gui(self):
        return self.update_mode,self.update_battery,self.update_encrypt_status

    def decode_message(self,data):
        
        pass
        #decrypt
        return data
        
            
    def client_listener(self):

        while True:
    
            c,a = self._tcp_sock.accept()
            print("client",c," connected")
            self.client_connected = True
            self.connections.append(c)

            client_thread = threading.Thread(target=self.client_handler,args=(c,a))
            client_thread.daemon = True
            client_thread.start()
           
    #sends data to client        
    def send_msg(self,data):
        data  = js.dumps(data)
        #if encrypt is true encrypts data
        if(self.encryption):
            data = self.crypto_tools.encrypt(data)
            print("data type is",type(data))
            
        msg = str(data,encoding='utf-8')
        
        for connection in self.connections:
            connection.send(bytes(msg,encoding='utf-8'))
           
    
   

            
    def set_encrypt_on_off(self,encrypt):
        
        #if stmnt to switch encrypt off 
        if encrypt == False:
            self.encryption = encrypt
            
        #if stmnt to switch encrypt on 
        if encrypt == True:
            self.encryption = encrypt
            
        #encrypt datagram 
        data = {"data":[
                    {"header":"command", "command_name": "set_encryption",
                        "value":encrypt}
                    ]
                }           
    
        self.send_msg(data) 

        
    def set_mode(self,mode):
        data = {"data":[
                    {"header":"command", "command_name": "set_mode",
                        "value":mode}
                    ]
                }
        
        self.send_msg(data) 

            
            
