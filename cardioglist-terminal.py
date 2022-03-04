import pwd
import random
import sys
import bcrypt
from tools import whitelist_input,check_user


#Shared key encryption scheme and Diffiehelman

#TODO Stretch goal: Connect to db 
#TODO Strecth Goal: Store user credentials and pacemaker history

#diffelman, Encrypt and decrypt on Pacemaker and client 


class Cardio_client():
    
    def __init__(self):
        
        #ToDO whitelist the inputs
        self.attempts = 3
        while self.attempts > 0:
    
            username = whitelist_input(input("Enter Username: ")) 
            password = whitelist_input(input("Enter Password: ")) 
        
        #print(username," ", password)
            self.verify_credentials(username,password)
            
    
        
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