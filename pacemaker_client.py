import socket
import json as js

import cryptography

from cryptography_tools import Cryptography_tools
#TODO add boolean to encrypt or not
class Pacemaker_model():
    
    def __init__(self):
        
        
        crypto_tools = Cryptography_tools()
        crypto_tools.create_key()
        
        #define socket, port and IP
        self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM) 
        self._ip = '127.0.0.1'
        self._port = 8080
        
        self.mode = ""
        self.lower_threshold = 0 
        self.higher_threshold = 0
        self.battery_capacity = 3500
        #self.battery_current_charge 
        self.encrypt = True
        self.connect_to_server()
        self.client_listener()
        
         
            
    def decrypt_command(self):
        #run the decrypt function here
        pass 
        
            
    def edit_settings():
         pass
     
     
    #connects to server 
    def connect_to_server(self):
       
        
        try:
            self.sock.connect((self._ip,self._port))

        except socket.error as error:
            print("Using alt port")
            self._port = 10080
            self.sock.connect((self._ip,self._port))

    def dummy_fuc():
        
        key = Cryptography_tools.load_save_key()
    #listener for dat from server         
    def client_listener(self):
        
        while True: 
            data = self.sock.recv(2048)
            if(self.encrypt):
                #decrypt
                print(data)
            else:
                print(data)
                pass
            
            
            
            data = js.loads(str(data,"utf-8"))
            data = data['data']
            for x in data:
                
            #if header is command get command and value before passing it 
                if str(x['header']) == 'command':
                    print(x['command_name'])
                    called_func = x['call_function']
                    func_value = x['value']
            if not data:
                break
            
            
    #send data function 
    def send_msg(self,data):
        pacemaker_id = 5
        
        if(self.encrypt):
            pass
            #data = Cryptography_tools.encrypt(data)
            #here is where the battery would be impacted
        else:
            data = data
            pass
        msg = {"data":[
                {"header":"pacemaker_identity",
                        "pacemaker_id":pacemaker_id}
                ]
            }
        msg = js.dumps(msg)
        self.sock.send(bytes(msg,'utf-8'))
   
dummy_pacemaker = Pacemaker_model()
