from asyncio import FastChildWatcher
from socket import create_server
import  threading
from tkinter import Tk as tk
from tkinter import *
from cardio_server import Cardio_server
from tools import whitelist_input,load_user
from cryptography_tools import *
#TODO add encrypt, datagrams, history, fix password login
#TODO put server in its own thread


class Gui():
    
    
    def __init__(self,main_window):
          
        #load settings hear 
        server_thread = threading.Thread(target=self.server_wrapper)
        server_thread.daemon = True
        server_thread.start()
        server_thread.join()
        self.main_window = main_window
        self.create_main_frame()
       
        
        
    def server_wrapper(self):
        self.c_server = Cardio_server()

        
    def login_menu(self):

        
        self.frame = Frame(self.main_frame,width=40,border=5)
        self.frame.pack(pady=50)
        
        uname_label = Label(self.frame,text="enter username",)
        uname_label.pack()
        
        self._uname_textfield = Entry(self.frame,width=40,border=5)
        self._uname_textfield.pack()
        
        password_label = Label(self.frame,text="enter password")
        password_label.pack()
        self._password_textfield = Entry(self.frame,show='*',width=40,border=5)
        self._password_textfield.pack()
        
        login_btn = Button(text="login",width=38 ,command = self.verify_credentials)
        login_btn.pack()
        
   
        
    def menu(self):
        
        self.frame.children.clear()
        
    def verify_credentials(self):
            
        
        if load_user(whitelist_input(self._uname_textfield.get()),whitelist_input(self._password_textfield.get())):
            print("terminal check")
            #self.menu()
            server_thread1 = threading.Thread(target=self.c_server.create_server())
            server_thread1.daemon = True
            server_thread1.start()
                
        else:
            print("Incorrect credentials")
                    
        
        
    
        
        
       
        
    def create_main_frame(self):
        self.main_frame = Frame(self.main_window)
        self.main_frame.pack()
        self.login_menu()

main_window = tk() 
main_window.title("Cardio Client")
main_window.geometry("400x300")
gui = Gui(main_window)
main_window.mainloop()
        
