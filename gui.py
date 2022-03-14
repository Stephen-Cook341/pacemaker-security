import  threading
from turtle import bgcolor
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg,NavigationToolbar2Tk
from PIL import Image, ImageTk
from tkinter import Tk as tk
from tkinter import *
from tkinter import ttk    
from numpy import integer
from cardio_server import Cardio_server
from tools import whitelist_input,check_user
from cryptography_tools import *
from tkmacosx import Button
matplotlib.use('TkAgg')


class Gui():
    
    
    def __init__(self,main_window):
          
        #load settings hear 
        #encryption is on by default 
        self.encryption_on = True
        
        server_thread = threading.Thread(target=self.server_wrapper)
        server_thread.daemon = True
        server_thread.start()
        server_thread.join()
        self.main_window = main_window
        self.create_main_frame()
       
        
        
    def server_wrapper(self):

        self.c_server = Cardio_server()

        
    def login_menu(self):
        title = Label(self.main_frame, text="Please enter login details",font=("Arial", 15))  
        title.grid(row=1,column=0,padx=18,pady= 15),

        uname_label = Label(self.main_frame,text="Username")
        uname_label.grid(row=2,column=0,sticky=(W),padx=18),
        
        uname_star = Label(self.main_frame,text="*", fg="red")
        uname_star.grid(row=2,column=0,sticky=(W),padx=82),

        self._uname_textfield = Entry(self.main_frame,width=25,border=2)
        self._uname_textfield.grid(row=3,column=0)
        
        password_label = Label(self.main_frame,text="Password")
        password_label.grid(row=4,column=0,sticky=(W),padx=18)
        uname_star = Label(self.main_frame,text="*", fg="red")
        uname_star.grid(row=4,column=0,sticky=(W),padx=82),

        self._password_textfield = Entry(self.main_frame,show='*',width=25,border=2)
        self._password_textfield.grid(row=5,column=0)
        
        login_btn = Button(self.main_frame,text="Login",width=232 ,command = self.verify_credentials)
        login_btn.grid(row=6,column=0,padx= 20, pady= 25)
        login_btn.config(fg="white", bg="blue")

    #settings menu 
    #TODO add status options
    #TODO add save telemetry to file option
    def menu(self):
        
        self.clear_frame()
        #creates canvas for cardio plot 
        canvas = Canvas(self.main_frame,width=300,height=200,bg='white')
        canvas.grid(row=0,column=0)
        fig = Figure(figsize = (5, 5), dpi = 100)
        y = [i**2 for i in range(101)]
        # adding the subplot 
        fig.suptitle("Pacemaker history")
        plot1 = fig.add_subplot(111) 
        
        # plotting the graph 
        plot1.plot(y) 

        # creating the Tkinter canvas 
        # containing the Matplotlib figure 
        output = FigureCanvasTkAgg(fig, master = canvas)
        output.draw()
        output.get_tk_widget().grid(row=0,column=0) 

       
        #Combo drop down menu to select pacemaker mode
        mode_label = Label(self.main_frame,text="Pacemaker mode selection  ")
        mode_label.grid(row=1,column=0)
        
        current_val = StringVar()
        mode_combo = ttk.Combobox(self.main_frame,textvariable=current_val)
        mode_combo['values'] = ('VVI','AAI','DDD')
        current_val = 'DDD' 

        mode_combo['state'] = 'readonly'
        mode_combo.set('DDD')
        mode_combo.grid(row=2,column=0)
        
        
        self.encryption_button = Button(self.main_frame,text="Turn encryption OFF",command=self.encrypt_button_switch)
        self.encryption_button.grid(row=3,column=0)     

        #allows the user sets the lower activation threshold for the pacemaker 
        lwr_threshold_label = Label(self.main_frame,text="Set Lower Activation Threshold")
        lwr_threshold_label.grid(row=4,column=0)
        lwr_threshold = integer
        scale = Scale(self.main_frame,variable=lwr_threshold,orient='horizontal',width=20)
        scale.grid(row=5,column=0)


        status_label = Label(self.main_frame,text="PACEMAKER STATUS")
        status_label.grid(row=6,column=0)

        
    #encyrpt toggle btn function     
    def encrypt_button_switch(self):
    
        if(self.encryption_on == False):

            self.encryption_on = True
            self.encryption_button.config(text="Turn encryption OFF")
            print("encrypt is",self.encryption_on)
            self.c_server.set_encrypt_on_off(self.encryption_on)
            
        else:

            self.encryption_on = False
            self.encryption_button.config(text="Turn encryption ON")
            print("encrypt is",self.encryption_on)
            self.c_server.set_encrypt_on_off(self.encryption_on)


    
        
    #clears the primary frame    
    def clear_frame(self):
        
        frame_info = self.main_frame.winfo_children()
        for widget in frame_info:
            widget.destroy()
        
        

    def verify_credentials(self):


        if(len(self._password_textfield.get()) >= 8 ):
          
            if check_user(whitelist_input(self._uname_textfield.get()),whitelist_input(self._password_textfield.get())):
                
                server_thread1 = threading.Thread(target=self.c_server.create_server())
                server_thread1.daemon = True
                server_thread1.start()
                self.menu()
            else:
                label = Label(self.main_frame,text="Incorrect credentials")
                label.grid(row=6,column=0)

        else:
            label = Label(self.main_frame,text="password length must be greater than 8")
            label.grid(row=6,column=0)
                        
        
       
        
    def create_main_frame(self):
        
        self.main_frame = Frame(self.main_window)
        self.main_frame.grid()
        self.login_menu()




main_window = tk() 
main_window.title("Cardio Client")
main_window.geometry("500x800")
frame= Frame(main_window)
frame.grid(pady=10)
main_window.resizable(0, 0)
gui = Gui(main_window)  
main_window.mainloop()
        
