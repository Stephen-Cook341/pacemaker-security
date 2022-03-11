import base64
import os
import json as js
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from bcrypt import gensalt, kdf

_key_path = "data/keys.json"

class Cryptography_tools:
    
    
    
    def __init__(self):
        
        #bcrypt generates the salt
        self._salt = gensalt(rounds=14)
        self._key_length = 32
        
    def create_key(self):
        
        _password= gensalt(rounds=14)
        
        kdf = PBKDF2HMAC(algorithm=hashes.SHA256(),length=self._key_length, salt=self._salt,iterations=100000,backend=default_backend())
        
        self._key = base64.urlsafe_b64encode(kdf.derive(_password))
        print(self._key)
    
      
        
    #TODO each pacemaker has a unique ID and shared key, 
    #TODO if no paceaker is stored. create  key 
    
    
    def encrypt(self,data):
        
        data = str(data)
        data_to_encrypt = data.encode()
        self._fernet = Fernet(self._key)
        self._encrypted_data = self._fernet.encrypt(bytes(data_to_encrypt,"utf-8"))
        print ("encryoted data:",self._encrypted_data)
        
        return self._encrypted_data
    
    def decrypt(self,data):
        data = self._fernet.decrypt(bytes(self._encrypted_data,'utf-8'))
        print("decrypted data: ",data)
        return data
        
        
    #TODO fix bug with saving keys
    #TODO add load keys 
        
    def load_key(self,_key): 
        
        try:
            with open(_key_path,"r") as _read_file:
                    _data = js.load(_read_file)
                    _data = _data['shared_keys']
                    print("reading from keys.json")
                    for i in _data ["keys"]:
                        _key = _data["key"]
                        return _key
                 
        except FileNotFoundError:
            __key = self.create_key()
            with open(_key_path,"w",encoding="utf-8") as f:
                
                _keys_dict = {"keys-keys":[{
                    "key":__key}
                ]}                    
                    
                
                js.dump(_keys_dict, f,ensure_ascii=False,indent=4 )
                
    
            
        
        
      
        
#key = Cryptography_tools()  

#key.create_key()
#key.encrypt()
 
    