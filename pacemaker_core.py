import random

import matplotlib
import matplotlib.pyplot as plt
from matplotlib import animation
from matplotlib.animation import FuncAnimation
import numpy as np
from numpy import size 

import heart
import pacemaker

# pip install neurokit2
# pip install tk
plt.rcParams['figure.figsize'] = [18, 5]  # Bigger images

matplotlib.use('TkAgg')


class Pacemaker_core():

    def __init__(self):

        # Makes 3 patients with different heart rates
        self.patient_1 = heart.Heart()
        self.patient_2 = heart.Heart(100)
        self.patient_3 = heart.Heart(60)
        # associate patients with the pacemaker
        self.pacemaker_1 = pacemaker.Pacemaker(self.patient_1, 'AAI')
        self.pacemaker_2 = pacemaker.Pacemaker(self.patient_2, 'VVI')
        self.pacemaker_3 = pacemaker.Pacemaker(self.patient_3, 'DDD')
        # pace to generate paced ecg
        self.ecg_signal_pacedAAI = self.pacemaker_1.pace()
        self.ecg_signal_pacedVVI = self.pacemaker_2.pace()
        self.ecg_signal_pacedDDD = self.pacemaker_3.pace()
        # Rest is just plotting code
        # ecg_df = pd.DataFrame({"patient's heart rate": patient_1.getECG()})
        # nk.signal_plot(ecg_df)
        self.y = np.array(self.patient_1.getECG())
        self.x = np.array(range(0, 30000))
        # ecg_df = pd.DataFrame({"paced heart rate": pacemaker_1.pace()})
        # nk.signal_plot(ecg_df)
       
        #patient_3_ecg = self.patient_3.getECG()
        #patient_3_ecg_signal = self.ecg_signal_pacedDDD
        #mode = "DDD Pacing Mode "
        #self.get_ddd_mode(mode)
        #self.set_mode("DDD")
        #self.draw_graph(mode,patient_ecg,ecg_signal)
        
        #self.vvi_mode()
        
    def aai_mode(self):
        #AAI Mode
        self.y1 = np.array(self.ecg_signal_pacedAAI)
        self.x1 = np.array(range(0, 30000))
        self.fig, (self.ax1, self.ax2) = plt.subplots(2)
        self.fig.suptitle('AAI pacing mode')
        self.ax1.plot(self.x, self.y)
        self.ax1.plot(self.x, self.y, label="patient's heart rate")
        self.ax1.legend(loc="upper right")
        self.ax2.plot(self.x1, self.y1)
        self.ax2.plot(self.x1, self.y1, label="paced heart rate")
        self.ax2.legend(loc="upper right")
        plt.show()

        # create empty lists for the x and y data
        self.x1 = np.array(range(0, 30000))
        self.y1 = np.array(self.patient_1.getECG())
        self.x2 = np.array(range(0, 30000))
        self.y2 = np.array(self.ecg_signal_pacedAAI)
        # create the figure and axes objects
        self.fig = plt.figure()
        self.ax1 = plt.subplot(2, 1, 1)
        self.ax2 = plt.subplot(2, 1, 2)
        self.data_skip = 100


    def init_func(self):
        self.ax1.clear()
        self.ax2.clear()
        self.ax1.set_xlabel('Sampling rate')
        self.ax1.set_ylabel('mV')
        self.ax2.set_xlabel('Sampling rate')
        self.ax2.set_ylabel('mV')
        self.ax1.set_xlim(self.x1[0], self.x1[-1])
        self.ax1.set_ylim(-0.5, 1.75)
        self.ax2.set_xlim(self.x2[0], self.x2[-1])
        self.ax2.set_ylim(-0.5, 1.75)


    def animate(i,self):
        self.ax1.plot(self.x1[i:i + self.data_skip], self.y1[i:i + self.data_skip], label="patient's heart rate", color='tab:blue')
        self.ax1.legend(["patient's heart rate"])
        self.ax2.plot(self.x2[i:i + self.data_skip], self.y2[i:i + self.data_skip], label="paced heart rate", color='tab:orange')
        self.ax2.legend(["paced heart rate"])


        # run the animation for aai 
        self.ani = FuncAnimation(self.fig, self.animate, frames=np.arange(0, len(self.x1), self.data_skip), init_func=self.init_func(), interval=50,
                            repeat=True)
        plt.show()
        
    def vvi_mode(self): 
        #shows VVI static graphs, return to cardio client
        y = np.array(self.patient_2.getECG())
        x = np.array(range(0, 30000))
        self.y1 = np.array(self.ecg_signal_pacedVVI)
        self.x1 = np.array(range(0, 30000))
        fig, (self.ax1, self.ax2) = plt.subplots(2)
        fig.suptitle('VVI pacing mode')
        self.ax1.plot(x, y, label="patient's heart rate")
        self.ax1.legend(loc="upper right")
        self.ax2.plot(self.x1, self.y1, label="paced heart rate")
        self.ax2.legend(loc="upper right")
        plt.show()

        #creetes graph for animation 
        fig = plt.figure()
        fig.suptitle('VVI pacing mode')
        self.x1 = plt.subplot(2, 1, 1)
        self.ax2 = plt.subplot(2, 1, 2)
        self.y1 = np.array(self.patient_2.getECG())
        y2 = np.array(self.ecg_signal_pacedVVI)
        self.ani = FuncAnimation(fig, self.animate, frames=np.arange(0, len(self.x1), self.data_skip), init_func=self.init_func(), interval=50,
                            repeat=True)
        plt.show()

    def ddd_mode(self):
        #shows DDD static graphs, return to cardio client
        y = np.array(self.patient_3.getECG())
        x = np.array(range(0, 30000))
        self.y1 = np.array(self.ecg_signal_pacedDDD)
        self.x1 = np.array(range(0, 30000))
        fig, (self.ax1, self.ax2) = plt.subplots(2)
        fig.suptitle('DDD pacing mode')
        self.ax1.plot(x, y)
        self.ax1.plot(x, y, label="patient's heart rate")
        self.ax1.legend(loc="upper right")
        self.ax2.plot(self.x1, self.y1)
        self.ax2.plot(self.x1, self.y1, label="paced heart rate")
        self.ax2.legend(loc="upper right")
        plt.show()


        fig = plt.figure()
        fig.suptitle('DDD pacing mode')
        self.x1 = plt.subplot(2, 1, 1)
        self.ax2 = plt.subplot(2, 1, 2)
        self.y1 = np.array(self.patient_3.getECG())
        self.y2 = np.array(self.ecg_signal_pacedDDD)
        self.ani = FuncAnimation(fig, self.animate, frames=np.arange(0, len(self.x1), self.data_skip), init_func=self.init_func(), interval=50,
                            repeat=True)
        plt.show()

    #setters for the mode   
    def set_mode(self,mode):
        
        mode = mode 
        patient_ecg = ""
        paced_ecg = ""
        
        #sets mode 
        if(mode =="AAI"):
            patient_ecg = self.patient_1.ecg_signal#check if correct 
            paced_ecg = self.ecg_signal_pacedAAI
            
            
        if(mode =="VVI"):
            patient_ecg = self.patient_2.ecg_signal#check if correct 
            paced_ecg = self.ecg_signal_pacedVVI
            
        if(mode =="DDD"):
            
            patient_ecg = self.patient_3.ecg_signal#check if correct 
            paced_ecg = self.ecg_signal_pacedDDD  
            
            
            
        #getters for all three modes 
    def get_ddd_mode(self):
       
        patient_3_ecg = self.patient_3.getECG()
        patient_3_ecg_signal = self.ecg_signal_pacedDDD
        
        return patient_3_ecg,patient_3_ecg_signal
            
    def get_vvi_mode(self):
            
        print(self.patient_2.getECG(),self.ecg_signal_pacedVVI)
        return self.patient_2.getECG(),self.ecg_signal_pacedVVI
        
    def get_aai_mode(self):
            
        print(self.patient_1.getECG(),self.ecg_signal_pacedAAI)
        return self.patient_1.getECG(),self.ecg_signal_pacedAAI
                
            #self.draw_graph(mode,patient_ecg,paced_ecg)
            
    
    #----------------------------------------------------------------------------------------------#
    #draws he graph but needs to be passed  mode,
    def draw_graph(self,mode,patient_ecg,ecg_signal):
        
        #pass modes 
        self.y = np.array(patient_ecg)
        self.x = np.array(range(0, 30000))
        self.y1 = np.array(ecg_signal)
        self.x1 = np.array(range(0, 30000))
        x1_size = self.x1.size
        self.fig, (self.ax1, self.ax2) = plt.subplots(2)
        self.fig.suptitle(mode)
        self.ax1.plot(self.x, self.y)
        self.ax1.plot(self.x, self.y, label="patient's heart rate")
        self.ax1.legend(loc="upper right")
        self.ax2.plot(self.x1, self.y1)
        self.ax2.plot(self.x1, self.y1, label="paced heart rate")
        self.ax2.legend(loc="upper right")
        plt.show()
        self.data_skip = 100

        
    
        fig = plt.figure()
        fig.suptitle(mode)
        
        self.x1 = plt.subplot(2, 1, 1)
        self.ax2 = plt.subplot(2, 1, 2)
        self.y1 = np.array(patient_ecg)
        self.y2 = np.array(ecg_signal)
        self.ani = FuncAnimation(fig, self.animate, frames=np.arange(0, x1_size, self.data_skip), init_func=self.init_func(), interval=50,
                            repeat=True)
        plt.show()
    
   
        

