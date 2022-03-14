import socket
import json as js
from time import sleep
import cryptography_tools
import threading
import neurokit

class Pacemaker_model():
    
    def __init__(self):
        
        
        
        #define socket, port and IP
        self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM) 
        self._ip = '127.0.0.1'
        self._port = 8080
        
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

        self.encrypt = True
        self.connect_to_server()

    # simulates the battery being used   
    def battery_sim(self):

        current_battery_charge = self.capacity

        while True:
            sleep(5)
            current_battery_charge = (current_battery_charge - self.discharge_rate)
            print(current_battery_charge/self.capacity*100)  
            
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


    def dummy_fuc():
        
        key = Cryptography_tools.load_save_key()


    #listener for data from server         
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
