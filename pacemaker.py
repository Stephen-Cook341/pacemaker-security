import socket
import json as js

class Pacemaker_model():
    
    def __init__(self):
        
        self.mode = ""
        self.lower_threshold = 0 
        self.higher_threshold = 0
        self.battery_capacity = 3500
        #self.battery_current_charge 
        self.decrypt = True
        
        self.client_net_code()
        
        if self.decrypt == True:
            self.decrypt_command()
            
    def decrypt_command(self):
        #run the decrypt function here
        pass 
        
            
    def edit_settings():
         pass
     
    def client_net_code(self):
        self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM) 
        
        self.ip = '127.0.0.1'
        self.port = 8080
        self.sock.connect((self.ip,self.port))
        self.send_connect_msg()
        
     
    def send_connect_msg(self):
        pacemaker_id = 5
        
        msg = {"data":[
                {"header":"pacemaker_identity",
                        "pacemaker_id":pacemaker_id}
                ]
            }
        data = "sent data"
        
        self.sock.send(data.encode())
   
dummy_pacemaker = Pacemaker_model()
