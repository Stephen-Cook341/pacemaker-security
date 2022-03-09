from genericpath import exists
from http import client
import sys
from tools import whitelist_input,check_user
import socket
import errno
import threading
from getpass import getpass

#Shared key encryption scheme and Diffiehelman

#TODO Stretch Goal: Store user credentials and pacemaker history

#diffelman, Encrypt and decrypt on Pacemaker and client 


class Cardio_client():
    
    def __init__(self):
        
        #ToDO whitelist the inputs
        #self.attempts = 3
        #while self.attempts > 0:
    
            #username = whitelist_input(input("Enter Username: ")) 
           # password = whitelist_input(input('Enter Password: ')) 
        
        #print(username," ", password)
        self.server_running = False
        menu_thread = threading.Thread(target=self.menu)
        menu_thread.daemon = True
        menu_thread.start()
        menu_thread.join()
            #self.verify_credentials(username,password)
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
        
        self.server_running = True
        #tcp socket
        self._ip = '127.0.0.1'
        self._port = 8080
        self._buff_size = 2048
        
        self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.sock.bind((self._ip,self._port))
        self.sock.listen(1)
        #self.connections =[]
       
        listener_thread = threading.Thread(target=self.client_listener)
        listener_thread.daemon = True
        listener_thread.start()
        listener_thread.join()
        
        
    #handles client connections
    def client_handler(self,c,a):
        while True:
            data = c.recv(self._buff_size)
            #for connection in self.connections:
                #connection.send(data)
            if not data:
                break
            print(str(data,"utf-8"))

            
    def decode_message(self):
        pass
        #decrypt
        
            
    def client_listener(self):
        
        while True:
            
            c,a = self.sock.accept()
            client_thread = threading.Thread(target=self.client_handler,args=(c,a))
            client_thread.daemon = True
            client_thread.start()
            client_thread.join()
            #self.connections.append(c)
            #print(self.connections)
            
     
            
        
        

        
    def verify_credentials(self,username,password):
        
        if check_user(username,password):
            print("terminal check")
                
            #check if hashed password == pword+salt 
                #if credentails are true then create secure connection with server
        else:
            self.attempts -= 1
            print("Incorrect credentials Attempts remaining: ",self.attempts)
                
        if(self.attempts == 0):
            print("User verification failed")
            sys.exit(0) 
            
            
            
cardio_client = Cardio_client()