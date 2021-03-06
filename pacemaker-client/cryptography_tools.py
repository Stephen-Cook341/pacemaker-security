import base64
import os
import json as js
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from bcrypt import gensalt, kdf

#path to keys .json file 
_key_path = "pacemaker-client/data/key.json"

class Cryptography_tools:
    
    
    
    def __init__(self):
        
        #bcrypt generates the salt and sets key length to 32 char
        self._salt = gensalt(rounds=14)
        self._key_length = 32
        
    def create_key(self):
        
        _password= gensalt(rounds=14)
        kdf = PBKDF2HMAC(algorithm=hashes.SHA256(),length=self._key_length, salt=self._salt,iterations=100000,backend=default_backend())
        self._key = base64.urlsafe_b64encode(kdf.derive(_password))
        
        return self._key
    
      
    
    
    def encrypt(self,data_to_encrypt):
        
        data = data_to_encrypt
        self._key = self.load_key()
        self._fernet = Fernet(self._key)
        data = self._fernet.encrypt(bytes(data,encoding="utf-8"))
        
        return data
    
    def decrypt(self,encrypted_data):
        
        data = encrypted_data
        self._key = self.load_key()
        self._fernet = Fernet(self._key)
        data = self._fernet.decrypt(data)
        
        return data
        
        
        
    def load_key(self): 
        #loads key if keys file exists 
        try:
            with open(_key_path,"r") as _read_file:
                    _data = js.load(_read_file)
                    _data = _data['shared_key']
                    print("reading from key.json")
                    for i in _data:
                        self._key = bytes(i["key"],encoding='utf-8')
                        #print("loaded key: ",self._key)
                        return self._key

        #if file does not exist creates json file and generates key     
        except FileNotFoundError:
            self._key = self.create_key()
            
            with open(_key_path,"w",encoding="utf-8") as f:
                _key = str(_key,encoding='utf-8')
                
                _keys_dict = {"shared_key":[{
                    "key":_key}
                ]}                    
                    
                
                js.dump(_keys_dict, f,ensure_ascii=False,indent=4 )

       

            
        
        
      
    
