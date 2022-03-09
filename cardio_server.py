from email import header
import sys
import cryptography_tools
from tools import whitelist_input,load_user
import socket
import threading
import json as js
#Shared key encryption scheme and Diffiehelman

#TODO Stretch Goal: Store user credentials and pacemaker history

#diffelman, Encrypt and decrypt on Pacemaker and client 


class Cardio_server():
    
    def __init__(self):
        pass
        #ToDO whitelist the inputs
    
        #username = whitelist_input(input("Enter Username: ")) 
        #password = whitelist_input(input('Enter Password: ')) 
        
        #print(username," ", password)
        #self.server_running = False
        #menu_thread = threading.Thread(target=self.menu)
        #menu_thread.daemon = True
        #menu_thread.start()
        #menu_thread.join()
        #self.create_server()
        
        
    def menu(self):
        print("Command List \n 1: exit\n 2: run server")
        while True:
            command = input("enter command:  ")
            if command == '1':
                if self.server_running is False:
                #self.sock.shutdown()
                    print("run server must be ran befoe shutting down ")

                else:
                    self.sock.close()
                    sys.exit(0)
            if command == '2':
                self.create_server()
                
        
        
    def create_server(self):
        
        port_list = (8080,10000,7777)
        print("Server running")
        self.server_running = True
        #tcp socket
        self._ip = '127.0.0.1'
        self._port = port_list[0]
        self._buff_size = 2048
        self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        #if port in use, try other ports 
        try:
            self.sock.bind((self._ip,self._port))
        
        except socket.gaierror:
            
            for i in len(port_list):
                self._port = port_list[i]

            self.sock.bind((self._ip,self._port))

        self.sock.listen(1)
        #self.connections =[]
       
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
            #if header is id print id
                if str(x['header']) == 'pacemaker_identity':
                    print(x['pacemaker_id'])
                
            print(data)

            
    def decode_message(self,data):
        
        pass
        #decrypt
        return data
        
            
    def client_listener(self):
        
        while True:
            
            c,a = self.sock.accept()
            client_thread = threading.Thread(target=self.client_handler,args=(c,a))
            client_thread.daemon = True
            client_thread.start()
            #self.connections.append(c)
            #print(self.connections)
            
     
            
        
        

       
            
            
