import socket
import json as js
import threading
import sys
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import animation
from matplotlib.animation import FuncAnimation
from time import sleep
from cryptography_tools import Cryptography_tools
from pacemaker_core import Pacemaker_core
from numpyencoder import NumpyEncoder
class Pacemaker_client():
    
    def __init__(self):
        
        
        
        #define socket, port and IP
        self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM) 
        self._ip = '127.0.0.1'
        self._port = 8080
        self._buff_size = 8196
        
        #default mode
        self.default_mode = 'DDD'
        
        #initiliazes battery settings 
        self.capacity = float(30.00) # battery capacity in AH

        #sets discharge rate, increase rate when encrypt/decrypt by default et to 0.5% of current battery capacity  
        self.discharge_rate = float((self.capacity/100)/2)
        battery_thread = threading.Thread(target=self.battery_sim)
        battery_thread.daemon = True
        battery_thread.start()
        
        #runs update thread for remote terminal
        update_thread = threading.Thread(target=self.update_remote_terminal)
        update_thread.daemon = True
        update_thread.start()
        
        self.crypto_tools = Cryptography_tools()
        self.encrypt = True
        self.pacemaker_core = Pacemaker_core()
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

        
     
    #connects to server if server port is unaible will attempt alternative port 
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
        #sends pacemaker ID
        print("client listnener running")
        #self.send_id()
        self.set_mode(self.default_mode)
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
                    
                    #passes encryption value to set encryption 
                    if(x["command_name"]=="set_encryption"):
                        self.set_encryption(str(x["value"]))
                        
                    if(x["command_name"]=="set_mode"):
                        self.set_mode(str(x['value']))
                        print(str(x['value']))
                 

                

            if not data:
                break
            
            
    def send_id(self):

        data = {"data":[
                {"header":"pacemaker_identity",
                        "pacemaker_id":"test_maker"}
                ]
            }
            
       #self.send_msg(data)


    #sets encryption 
    def set_encryption(self,encryption):
        
        self.encrypt = encryption
            
  
    
    
    #send data to server 
    def send_msg(self,data):
        
        self.discharge_rate = float((self.capacity/100)*5)

        data  = js.dumps(data)
        #if encrypt is true encrypts data
        if(self.encrypt):
            data = self.crypto_tools.encrypt(data)
            print("data type is",type(data))
            
        msg = str(data,encoding='utf-8')
        self.sock.send(bytes(msg,encoding='utf-8'))
        self.discharge_rate = float((self.capacity/100)/2)

        
        ##################
    







    #Combine both update functions 
    def update_remote_terminal(self):
        while True:
            sleep(10)
            battery_percent = self.current_battery_charge/self.capacity*100
            encrypt = self.encrypt
            
            data = {"data":[
                {"header":"update",
                        "mode":self.mode,
                        "battery":battery_percent,
                        "encryption":encrypt,
                        #"patient_ecg":self.patient_ecg.tolist(),
                        #"paced_ecg":self.paced_ecg
                        }
                ]
            }
            
            self.send_msg(data)
      
    
    #sets pacemaker mode 
    def set_mode(self,mode):
        
        self.mode = mode 
        #sets mode 
        if(self.mode =="AAI"):
            self.patient_ecg,self.paced_ecg = self.pacemaker_core.get_aai_mode()
            
        if(self.mode =="VVI"):
            self.patient_ecg,self.paced_ecg = self.pacemaker_core.get_vvi_mode()

            
        if(self.mode =="DDD"):
            self.patient_ecg,self.paced_ecg = self.pacemaker_core.get_ddd_mode()
        
        #self.update_server_mode
        graph_thread = threading.Thread(target=self.draw_graph)
        graph_thread.daemon = True
        graph_thread.start()
        self.update_remote_terminal()

          
    
    #draws the graph 
    def draw_graph(self):
            
        #pass modes 
        self.y = np.array(self.patient_ecg)
        self.x = np.array(range(0, 30000))
        self.y1 = np.array(self.paced_ecg)
        self.x1 = np.array(range(0, 30000))
        x1_size = self.x1.size
        self.fig, (self.ax1, self.ax2) = plt.subplots(2)
        self.fig.suptitle(self.mode)
        self.ax1.plot(self.x, self.y)
        self.ax1.plot(self.x, self.y, label="patient's heart rate")
        self.ax1.legend(loc="upper right")
        self.ax2.plot(self.x1, self.y1)
        self.ax2.plot(self.x1, self.y1, label="paced heart rate")
        self.ax2.legend(loc="upper right")
        plt.show()
        self.data_skip = 100

        
    
        self.fig = plt.figure()
        self.fig.suptitle(self.mode)
        
        self.x1 = plt.subplot(2, 1, 1)
        self.ax2 = plt.subplot(2, 1, 2)
        self.y1 = np.array(self.patient_ecg)
        self.y2 = np.array(self.paced_ecg)
        self.ani = FuncAnimation(self.fig, self.animate, frames=np.arange(0, x1_size, self.data_skip), init_func=self.init_func(), interval=50,
                            repeat=True)
        plt.show()
        
    def animate(i,self):
        self.ax1.plot(self.x1[i:i + self.data_skip], self.y1[i:i + self.data_skip], label="patient's heart rate", color='tab:blue')
        self.ax1.legend(["patient's heart rate"])
        self.ax2.plot(self.x2[i:i + self.data_skip], self.y2[i:i + self.data_skip], label="paced heart rate", color='tab:orange')
        self.ax2.legend(["paced heart rate"])
       
    def init_func(self):
        self.ax1.clear()
        self.ax2.clear()
        self.ax1.set_xlabel('Sampling rate')
        self.ax1.set_ylabel('mV')
        self.ax2.set_xlabel('Sampling rate')
        self.ax2.set_ylabel('mV')
        self.ax1.set_xlim(self.x1[0], self.x1[-1])
        self.ax1.set_ylim(-0.5, 1.75)
        self.ax2.set_xlim(self.x2[0], self.x2[-1])
        self.ax2.set_ylim(-0.5, 1.75)


pacemaker_client = Pacemaker_client()

