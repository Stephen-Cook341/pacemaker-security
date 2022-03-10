import socket
import json as js

from cryptography_tools import Cryptography_tools
#TODO add boolean to encrypt or not
class Pacemaker_model():
    
    def __init__(self):
        
        self.mode = ""
        self.lower_threshold = 0 
        self.higher_threshold = 0
        self.battery_capacity = 3500
        #self.battery_current_charge 
        self.decrypt = True
        self.client_net_code()
        
         
            
    def decrypt_command(self):
        #run the decrypt function here
        pass 
        
            
    def edit_settings():
         pass
     
    def client_net_code(self):
        
        self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM) 
        self.ip = '127.0.0.1'
        port_list = (8080,10000,7777)

        self.port = 8080
        
        try:
            self.sock.connect((self.ip,self.port))
        
        except socket.gaierror:
            
            for i in port_list:
                self._port = port_list[i]
                self.sock.connect((self.ip,self.port))

        data = bytes("sent data", "utf-8")

        self.send_msg(data)
        self.client_listener()
        
    def client_listener(self):
        
        while True: 
            data = self.sock.recv(2048)
            if not data:
                break
            
            
     
    def send_msg(self,data):
        pacemaker_id = 5
        
        if(self.decrypt):
            data = Cryptography_tools.encrypt(data)
            #here is where the battery would be impacted
        else:
            data = data
            
        msg = {"data":[
                {"header":"pacemaker_identity",
                        "pacemaker_id":pacemaker_id}
                ]
            }
        msg = js.dumps(msg)
        self.sock.send(bytes(msg,'utf-8'))
   
dummy_pacemaker = Pacemaker_model()