import  threading
from turtle import bgcolor, width
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
        #encryption is on by default 
        self.encryption_on = True
        #runs the cardio server on a seperate thread 
        server_thread = threading.Thread(target=self.server_wrapper)
        server_thread.daemon = True
        server_thread.start()
        server_thread.join()
        self.main_window = main_window
        self.create_main_frame()
       
        
    #wrapper function that allows the cardio srver to be ran in its own thread   
    def server_wrapper(self):

        self.c_server = Cardio_server()

        
    def login_menu(self):
        #sets title of login menu 
        title = Label(self.main_frame, text="Please enter login details",font=("Arial", 15,'bold'),bg='white')  
        title.grid(row=1,column=0,padx=18,pady= 15),
        
        #creates username label,entry box and *  
        uname_label = Label(self.main_frame,text="Username",width=20,bg="white")
        uname_label.grid(row=2,column=0,sticky=(N),padx=330),
        uname_star = Label(self.main_frame,text="*", fg="Black",bg="white")
        uname_star.grid(row=2,column=0,sticky=(E),padx=350),
        self._uname_textfield = Entry(self.main_frame,width=25,border=2,borderwidth=5,highlightbackground="black")
        self._uname_textfield.grid(row=3,column=0,sticky=(N))

        #creates password label,entry box and *  
        password_label = Label(self.main_frame,text="Password",width=20,bg="white")
        password_label.grid(row=4,column=0,sticky=(N),padx=330)
        uname_star = Label(self.main_frame,text="*", fg="Black",bg="white")
        uname_star.grid(row=4,column=0,sticky=(E),padx=350),
        self._password_textfield = Entry(self.main_frame,show='*',width=25,borderwidth=5,highlightbackground="black")
        self._password_textfield.grid(row=5,column=0,sticky=(N))
        
        #crreates login button and sets command to verify_credentials 
        login_btn = Button(self.main_frame,text="Login",font='bold',width=232 ,command = self.verify_credentials)
        login_btn.grid(row=6,column=0,padx= 20,sticky=(N),pady= 25)
        login_btn.config(fg="black", bg="white")

    #settings menu 
    #TODO add status options
    #TODO add save telemetry to file option
    #TODO make create graph function
    def menu(self):
        
        self.clear_frame()
        #creates canvas for cardio plot 
        canvas = Canvas(self.main_frame,width=500,height=200,bg='white')
        canvas.grid(row=0,column=0,sticky=(W),padx=0)
        
        self.fig = Figure(figsize = (10, 2), dpi = 100)
        y = [i**2 for i in range(101)]
        # adding the subplot 
        self.fig.suptitle("Pacemaker history")
        plot1 = self.fig.add_subplot(111) 
        
        # plotting the graph 
        plot1.plot(y) 

        # creating the Tkinter canvas 
        # containing the Matplotlib self.figure 
        output = FigureCanvasTkAgg(self.fig, master = canvas)
        output.draw()
        output.get_tk_widget().grid(row=0,column=0,sticky=(W),padx=0) 
        
        #creates settings label 
        settings_label = Label(self.main_frame,text="SETTINGS",bg='white',font=("Arial 10 underline"))
        settings_label.grid(row=1,column=0,sticky=(N),pady=50,padx=200)

        #Combo drop down menu to select pacemaker mode
        mode_label = Label(self.main_frame,text="Pacemaker mode selection  ",bg='white')
        mode_label.grid(row=2,column=0,sticky=(W))
        self.current_val = StringVar()
        self.mode_combo = ttk.Combobox(self.main_frame,textvariable=self.current_val,width=10)
        #sets drop down values 
        self.mode_combo['values'] = ('VVI','AAI','DDD')
        self.current_val = 'DDD' 
        self.mode_combo['state'] = 'readonly'
        self.mode_combo.set(self.current_val)
        self.mode_combo.grid(row=2,column=0,sticky=(W),padx=300)
        set_mode_btn = Button(self.main_frame,text="set mode",bg="White",font=("Arial 10 bold"),command=self.set_mode)
        set_mode_btn.grid(row=2,column=0,sticky=(W),padx=400)
        
        #creates encryption label and toggle button 
        set_encrypt_label = Label(self.main_frame,text="Set encryption",bg='white')
        set_encrypt_label.grid(row=4,column=0,sticky=(W))
        self.encryption_button = Button(self.main_frame,text="Turn encryption OFF",bg='white',command=self.encrypt_button_switch,font=("Arial 10 bold"))
        self.encryption_button.grid(row=4,column=0,sticky=(W),padx=300)     

        #allows the user sets the lower activation threshold for the pacemaker 
        set_pacing = Label(self.main_frame,text="Set pacing",bg='white')
        set_pacing.grid(row=5,column=0,sticky=(W))
        set_pacing = integer
       
        scale = Scale(self.main_frame,from_=0,to=100,variable=set_pacing,sliderrelief='flat', orient="horizontal", highlightthickness=0,tickinterval=100, width=10,sliderlength=10,bg='white',fg='black')
        scale.grid(row=5,column=0,sticky=(W),padx=300)

        set_pacing = Button(self.main_frame,text="Set Pacing",bg='white',command=self.encrypt_button_switch,font=("Arial 10 bold"))
        set_pacing.grid(row=5,column=0,sticky=(W),padx=400)     

        #pacemaker status updates menu labels 
        status_label = Label(self.main_frame,text="PACEMAKER STATUS",bg='white',font=("Arial 10 underline"))
        status_label.grid(row=6,column=0,sticky=(N),pady=50,padx=200)

        current_mode = Label(self.main_frame,text="Pacemaker current Mode: ",bg='white')
        current_mode.grid(row=7,column=0,sticky=(W))

        current_battery = Label(self.main_frame,text="current battery: ",bg='white')
        current_battery.grid(row=8,column=0,sticky=(W))

        current_pacing = Label(self.main_frame,text="current pacing: ",bg='white')
        current_pacing.grid(row=9,column=0,sticky=(W))

        encrypt_status = Label(self.main_frame,text="encrypt status: ",bg='white')
        encrypt_status.grid(row=10,column=0,sticky=(W))

    #dummy values 
        self.mode_label = Label(self.main_frame,text="AAI",bg="White",font=("Arial 10 bold"))
        self.mode_label.grid(row=7,column=0,sticky=(W),padx=400)
        self.fig.suptitle("AAI Mode")

        bat_label = Label(self.main_frame,text="82%",bg="White",font=("Arial 10 bold"))
        bat_label.grid(row=8,column=0,sticky=(W),padx=400)

        pace = Label(self.main_frame,text="60",bg="White",font=("Arial 10 bold"))
        pace.grid(row=9,column=0,sticky=(W),padx=400)
        
        encr = Label(self.main_frame,text="ON",bg="White",font=("Arial 10 bold"))
        encr.grid(row=10,column=0,sticky=(W),padx=400)

        
    #encyrpt toggle btn function     
    def encrypt_button_switch(self):
        #if encryption is false sets encryption to true and chnages encrypt button value sends encrypt command to client 
        if(self.encryption_on == False):

            self.encryption_on = True
            self.encryption_button.config(text="Turn encryption OFF")
            print("encrypt is",self.encryption_on)
            self.c_server.set_encrypt_on_off(self.encryption_on)
            
        else:
            #if encryption is TRue sets encryption to False and chnages encrypt button value sends encrypt command to client 
            self.encryption_on = False
            self.encryption_button.config(text="Turn encryption ON")
            print("encrypt is",self.encryption_on)
            self.c_server.set_encrypt_on_off(self.encryption_on)


    
        
    #clears the primary frame    
    def clear_frame(self):
        
        frame_info = self.main_frame.winfo_children()
        for widget in frame_info:
            widget.destroy()
        
    def set_mode(self):
        print(self.mode_combo.get())

    def verify_credentials(self):
        #if string lenght is greater or equal to 8 will check username 
        if(len(self._password_textfield.get()) >= 8 ):
            if check_user(whitelist_input(self._uname_textfield.get()),whitelist_input(self._password_textfield.get())):
                
                server_thread1 = threading.Thread(target=self.c_server.create_server())
                server_thread1.daemon = True
                server_thread1.start()
                self.menu()
            else:
                label = Label(self.main_frame,text="Incorrect credentials",bg="white")
                label.grid(row=6,column=0,pady=50)

        else:
            label = Label(self.main_frame,text="password length must be greater than 8",bg="white")
            label.grid(row=6,column=0,pady=50)
                        
        
       
    #creates main window 
    def create_main_frame(self):
        
        self.main_frame = Frame(self.main_window,bg="WHITE")
        self.main_frame.grid()
        self.login_menu()




main_window = tk() 
main_window.title("Cardio Client")
main_window.geometry("800x700")
main_window.resizable(0, 0)
main_window.config(bg="WHITE")
gui = Gui(main_window)  
main_window.mainloop()
        
