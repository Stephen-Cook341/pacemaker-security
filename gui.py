import  threading
import tkinter.font as tkFont
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg,NavigationToolbar2Tk
from PIL import Image, ImageTk
from tkinter import Tk as tk
from tkinter import *
from tkinter import ttk
from cardio_server import Cardio_server
from tools import whitelist_input,load_user
from cryptography_tools import *
matplotlib.use('TkAgg')
#TODO add encrypt, datagrams, history, fix password login
#TODO put server in its own thread
#TODO  add cnavas fro graph and then add plot to fig


class Gui():
    
    
    def __init__(self,main_window):
          
        #load settings hear 
        #encryption is off by default 
        self.encryption_on = False
        
        def_font = tkFont.nametofont("TkDefaultFont")
        def_font.config(size=16)
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
        
        login_btn = Button(self.main_frame,text="login",width=38 ,command = self.verify_credentials)
        login_btn.pack()
        
   
    #settings menu 
    #TODO add status options
    #TODO add lower and upperthreshold selection
    #TODO add save telemetry to file option
    def menu(self):
        
        self.clear_frame()
        #creates canvas for cardio plot 
        canvas = Canvas(self.main_frame,width=300,height=200,bg='white')
        canvas.pack()
        fig = Figure(figsize = (5, 5), dpi = 100)
        y = [i**2 for i in range(101)]
        # adding the subplot 
        plot1 = fig.add_subplot(111) 

        # plotting the graph 
        plot1.plot(y) 

        # creating the Tkinter canvas 
        # containing the Matplotlib figure 
        output = FigureCanvasTkAgg(fig, master = canvas)
        output.draw()

        # placing the canvas on the Tkinter window 
        output.get_tk_widget().pack() 

       
        
        
        #Combo drop down menu to select pacemaker mode
        mode_label = Label(text="Pacemaker mode selection")
        mode_label.pack()
        current_val = StringVar()

        mode_combo = ttk.Combobox(self.main_frame,textvariable=current_val)
        mode_combo['values'] = ('mode1','mode2','mode3')
        current_val = 'mode1' 

        mode_combo['state'] = 'readonly'
        mode_combo.set('mode1')
        mode_combo.pack()
        
        
        self.encryption_button = Button(self.main_frame,text="Turn encryption ON",command=self.encrypt_button_switch)
        self.encryption_button.pack()     

        
    #encyrpt toggle btn function     
    def encrypt_button_switch(self):
    
        if(self.encryption_on == False):
            self.encryption_on = True
            self.encryption_button.config(text="Turn encryption OFF")
            print("encrypt is",self.encryption_on)
            
        else:
            self.encryption_on = False
            self.encryption_button.config(text="Turn encryption ON")
            print("encrypt is",self.encryption_on)

        
    #clears the primary frame    
    def clear_frame(self):
        
        
        frame_info = self.main_frame.winfo_children()
        for widget in frame_info:
            widget.destroy()
        
        
    def verify_credentials(self):
            
        
        if load_user(whitelist_input(self._uname_textfield.get()),whitelist_input(self._password_textfield.get())):
            
            print("terminal check")
            #self.menu()
            server_thread1 = threading.Thread(target=self.c_server.create_server())
            server_thread1.daemon = True
            server_thread1.start()
            self.menu()
                
        else:
            print("Incorrect credentials")
                        
        
       
        
    def create_main_frame(self):
        
        self.main_frame = Frame(self.main_window)
        self.main_frame.pack(pady=50)
        self.login_menu()




main_window = tk() 
main_window.title("Cardio Client")
main_window.geometry("400x300")
gui = Gui(main_window)
main_window.mainloop()
        
