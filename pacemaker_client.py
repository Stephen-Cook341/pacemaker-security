from crypt import crypt
import socket
import json as js
from time import sleep
from cryptography_tools import Cryptography_tools
import threading
import sys

class Pacemaker_model():
    
    def __init__(self):
        
        
        
        #define socket, port and IP
        self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM) 
        self._ip = '127.0.0.1'
        self._port = 8080
        self._buff_size = 8196
        
        self.mode = ""
        self.lower_threshold = 0 
        self.higher_threshold = 0
        
        #initiliazes battery settings 
        self.capacity = float(30.00) # battery capacity in AH

        #sets discharge rate, increase rate when encrypt/decrypt 
        self.discharge_rate = float((self.capacity/100)/2)
        battery_thread = threading.Thread(target=self.battery_sim)
        battery_thread.daemon = True
        battery_thread.start()
        
        self.crypto_tools = Cryptography_tools()
        self.encrypt = True
        self.connect_to_server()

    # simulates the battery being used   
    def battery_sim(self):

        self.current_battery_charge = self.capacity
        while True:
            sleep(3)
            self.current_battery_charge = (self.current_battery_charge - self.discharge_rate)
            print(" current battery charge is at: ",self.current_battery_charge/self.capacity*100,"\n current battery discharging rate is at: ",self.discharge_rate) 

            if(self.current_battery_charge/self.capacity*100 <= 0):
                print("battery depleted")
                sys.exit(0)

            
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

        print("connected")
        self.client_listener()

        


    #listener for data from server         
    def client_listener(self):
        print("client listnener running")
        self.send_id()
        while True: 
            data = self.sock.recv(self._buff_size)
            print("data is ",data)
            
            #if encrypt is true decrypt message 
            if(self.encrypt):
                #decrypt
                data = self.crypto_tools.decrypt(data)
                print("decrypted data",data)
                
           
            data = js.loads(str(data,encoding="utf-8"))
            
            
            data = data['data']
                
            for x in data:
                
            #if header is command get command and value before passing it 
                if str(x['header']) == 'command':
                    print(x['command_name'],x["value"])

                    if(x["command_name"]=="set_encryption"):
                        self.set_encryption(str(x["value"]))
                    if(x["command_name"]=="set_mode"):
                        self.set_mode(str(x))
                    if(x["command_name"]=="bpm"):
                        self.set_bpm(str(x))

                

            if not data:
                break
    def send_id(self):

        data = {"data":[
                {"header":"pacemaker_identity",
                        "pacemaker_id":"test_maker"}
                ]
            }
            
       #self.send_msg(data)



    def set_encryption(self,encrption):
        self.encrypt = encrption      
    
    
    #send data function readd pass data
    def send_msg(self,data):
        
        if(self.encrypt):
            data = str(data,encoding='utf-8')
            data = self.crypto_tools.encrypt(data)
         
        else:
            data = data
        
        
        msg = js.dumps(data)
        self.sock.send(bytes(msg,'utf-8'))

    def update_cardio_client(self):
        mode = self.get_mode()
        bat_percent = self.current_battery_charge/self.capacity*100
        pace = self.get_pace()
        encrypt = self.encrypt
        data = {"data":[
            {"header":"update",
                    "mode":mode,"battery":bat_percent,"pace":pace,"encryption":encrypt}
            ]
        }

        return mode,bat_percent,pace,encrypt
    

dummy_pacemaker = Pacemaker_model()
