from datetime import datetime
import imp
from os import uname
import re
import secrets
import bcrypt
#import pycryptodome
import sys
import json as js

file = "data/user.json"

def whitelist_input(string_to_whitelist):
    
    #add addtitonal char to whielist 
    new_string = re.sub('[^a-zA-Z0-9]', '',string_to_whitelist)
        
    return new_string


#pass username to check
def check_user(username,password):
    
    #loads user json data
    try:
        with open(file, "r") as read_file:
            data = js.load(read_file)
            data = data['user']
            print("reading user.json")
        for x in data:
            if(x['username'] == username):
                salt = x['salt']
                stored_password = x['password']
                hashed_password = hash_pwd(salt,password)
                if(stored_password == hashed_password):
                    return True
                
                
    except FileNotFoundError:
        #if no user.sjon file in data directory create new user
        print("no user found creating user")
        
        salt = gen_salt()
        hashed_password = hash_pwd(password,salt)
        
        user_dictionary = {"username" : username,"salt":str(salt),"password":hashed_password}
        print(user_dictionary)
        
        with open("data/user.json","w",encoding="utf-8") as f:
            js.dump(user_dictionary, f,ensure_ascii=False,indent=4 )
            return True
        
             
        #print("user file not found\n App shutting down")
        #sys.exit(0)
        
def create_user():
    pass

def gen_salt():
    
    salt = bcrypt.gensalt(rounds=14)
    
    return salt
    
def hash_pwd(password,salt): 
    
    password_to_hash = password.encode("utf-8")
    hashed_pwd = bcrypt.hashpw(password_to_hash,bytes(salt))
    
    return str(hashed_pwd)
    
    
    
#encrypt and decrypt functions 

    
    

    
    