import base64
import os
import json as js
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from bcrypt import gensalt, kdf

_key_path = "data/pacemakers/keys.json"

class Cryptography_tools:
    
    
    
    def __init__(self):
        
        #bcrypt generates the salt
        self._salt = gensalt(rounds=14)
        self._key_length = 32
        
    def create_key(self):
        
        _password= 'test'
        _password_to_hash = _password.encode()
        
        kdf = PBKDF2HMAC(algorithm=hashes.SHA256(),length=self._key_length, salt=self._salt,iterations=100000,backend=default_backend())
        
        self._key = base64.urlsafe_b64encode(kdf.derive(_password_to_hash))
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
        
    def load_save_key(self): 
        
        try:
            with open(_key_path,"r") as _read_file:
                    _data = js.load(_read_file)
                    _data = _data['shared_keys']
                    print("writing to keys.json")
                    for i in _data:
                       if i["pacemaker_id"] >= 0:
                           id = i["pacemaker_id"]
                           id+=1
                           _keys_dict = {"shared-keys":[{
                                "pacemaker-id":_id,"shared_key":str(self._key)
    
                                }
                            ]}
            
            
        except FileNotFoundError:
            _id = 0
            with open(_key_path,"w",encoding="utf-8") as f:
                
                _keys_dict = {"shared-keys":[{
                    "pacemaker-id":_id,"shared_key":str(self._key)
    
                    }
                ]}

                
                
                
                {"pacemaker-id":_id,"shared_key":str(self._key)}
                    
                    
                
                js.dump(_keys_dict, f,ensure_ascii=False,indent=4 )
                
    
            
        
        
      
        
#key = Cryptography_tools()  

#key.create_key()
#key.encrypt()
 
    