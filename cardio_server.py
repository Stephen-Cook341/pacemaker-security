import sys
import cryptography_tools
import errno
from pacemaker import Pacemaker
import socket
import threading
import json as js
#Shared key encryption scheme and Diffiehelman

#TODO Stretch Goal: Store user credentials and pacemaker history

#diffelman, Encrypt and decrypt on Pacemaker and client 


class Cardio_server():

    def __init__(self):
        
        #tcp_socket settings
        self._tcp_ip = "127.0.0.1"
        self._buff_size = 2048
        self._tcp_port = 8080
        self._tcp_sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        
    
   
    #debug menu     
    def menu(self):
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
        
        #if port in use, try other ports 
        try:
            self._tcp_sock.bind((self._tcp_ip,self._tcp_port))
            
        except socket.error as e:
            if e.errno == errno.EADDRINUSE:
                    print(("Port %s in use, using alternative port"%(str(self._tcp_port))))
                    self._tcp_port = 1080
                    self._tcp_sock.bind((self._tcp_ip,self._tcp_port))
            
        self.server_running = True
        self._tcp_sock.listen(1)
        print('Server running')
        
        listener_thread = threading.Thread(target=self.client_listener)
        listener_thread.daemon = True
        listener_thread.start()
        print("listener started")
        
        
    #handles client connections
    def client_handler(self,c,a):
        
        
        while True:
            data = c.recv(self._buff_size)
            #for connection in self.connections:
                #connection.send(data)
            if not data:
                print('Pacemaker: ',c," is disconnected")
                break
            #converts from bytes back to json
            data = js.loads(str(data,"utf-8"))
            data = data['data']
            for x in data:
                
            #if header is id print id and save to list 
                if str(x['header']) == 'pacemaker_identity':
                    print(x['pacemaker_id'])
                    pacemaker = Pacemaker(x['pacemaker_id'],c)
                    self.connections.append(pacemaker)
                    client = self.connections[0]
                    print(pacemaker.get_pacemaker_id())
            print(data)

            
    def decode_message(self,data):
        
        pass
        #decrypt
        return data
        
            
    def client_listener(self):
        
        while True:
            
            c,a = self._tcp_sock.accept()
            client_thread = threading.Thread(target=self.client_handler,args=(c,a))
            client_thread.daemon = True
            client_thread.start()
           
            
    def send_msg(self,data):
      
        msg = js.dumps(msg)
        self._tcp_sock.send(bytes(msg,'utf-8'))


            
    def set_encrypt_on_off(self):

        
        msg = {"data":[
                {"header":"command",
                    "encrypt_on/off":"off"}
                ]
            }
        self.send_msg(msg) 

        #create
        

       
            
            
