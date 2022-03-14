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
        #self.load_key()
        
    def create_key(self):
        
        _password= gensalt(rounds=14)
        
        kdf = PBKDF2HMAC(algorithm=hashes.SHA256(),length=self._key_length, salt=self._salt,iterations=100000,backend=default_backend())
        
        self._key = base64.urlsafe_b64encode(kdf.derive(_password))
        return self._key
    
      
    
    
    def encrypt(self,data):
        
        data = data
        self._key = self.load_key()
        self._fernet = Fernet(self._key)
        self._encrypted_data = self._fernet.encrypt(bytes(data,encoding="utf-8"))
        print ("encrypted data:",self._encrypted_data)
        
        return self._encrypted_data
    
    def decrypt(self,data):
        data = self._fernet.decrypt(bytes(self._encrypted_data,'utf-8'))
        print("decrypted data: ",data)
        return data
        
        
        
    def load_key(self): 

        #loads key if keys file exists 
        try:
            with open(_key_path,"r") as _read_file:
                    _data = js.load(_read_file)
                    _data = _data['shared_key']
                    print("reading from keys.json")
                    for i in _data:
                        self._key = bytes(i["key"],encoding='utf-8')
                        print("loaded key: ",self._key)
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

       

            
        
        
      
    
