from ctypes import alignment
from curses.textpad import Textbox
from pickle import FRAME
from tkinter import Tk as tk
from tkinter import *
from turtle import left, width

from matplotlib.pyplot import title



class Gui():
    
    
    def __init__(self,root):
       
       
        self.main_win = Frame(root)
        self.main_win.pack()
        self.login_menu()
        
        
        
        
    def login_menu(self):

        
        self.frame = LabelFrame(self.main_win,text="Login",labelanchor='n',width=40,border=5)
        self.frame.pack(pady=50)
        
        uname_label = Label(self.frame,text="enter username")
        uname_label.pack()
        
        _uname_textfield = Entry(self.frame)
        _uname_textfield.pack()
        
        password_label = Label(self.frame,text="enter password")
        password_label.pack()
        _password_textfield = Entry(self.frame,show='*')
        _password_textfield.pack()
        
        login_btn = Button(text="login",width=40)# ,command=verify_user(_uname_textfield.get(),_password_textfield.get()))
        login_btn.pack()

root = tk()
root.title("cardio client")
root.geometry("400x300")
gui = Gui(root)
root.mainloop()        
#gui = Gui(root)
