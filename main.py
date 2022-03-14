import random

import matplotlib
import matplotlib.pyplot as plt
from matplotlib import animation
from matplotlib.animation import FuncAnimation
import numpy as np

import heart
import pacemaker

# pip install neurokit2
# pip install tk
plt.rcParams['figure.figsize'] = [18, 5]  # Bigger images

matplotlib.use('TkAgg')

if __name__ == '__main__':
    # Makes 3 patients with different heart rates
    patient_1 = heart.Heart()
    patient_2 = heart.Heart(100)
    patient_3 = heart.Heart(60)
    # associate patients with the pacemaker
    pacemaker_1 = pacemaker.Pacemaker(patient_1, 'AAI')
    pacemaker_2 = pacemaker.Pacemaker(patient_2, 'VVI')
    pacemaker_3 = pacemaker.Pacemaker(patient_3, 'DDD')
    # pace to generate paced ecg
    ecg_signal_pacedAAI = pacemaker_1.pace()
    ecg_signal_pacedVVI = pacemaker_2.pace()
    ecg_signal_pacedDDD = pacemaker_3.pace()
    # Rest is just plotting code
    # ecg_df = pd.DataFrame({"patient's heart rate": patient_1.getECG()})
    # nk.signal_plot(ecg_df)
    y = np.array(patient_1.getECG())
    x = np.array(range(0, 30000))
    # ecg_df = pd.DataFrame({"paced heart rate": pacemaker_1.pace()})
    # nk.signal_plot(ecg_df)
    
    
    #AAI Mode
    y1 = np.array(ecg_signal_pacedAAI)
    x1 = np.array(range(0, 30000))
    fig, (ax1, ax2) = plt.subplots(2)
    fig.suptitle('AAI pacing mode')
    ax1.plot(x, y)
    ax1.plot(x, y, label="patient's heart rate")
    ax1.legend(loc="upper right")
    ax2.plot(x1, y1)
    ax2.plot(x1, y1, label="paced heart rate")
    ax2.legend(loc="upper right")
    plt.show()

    # create empty lists for the x and y data
    x1 = np.array(range(0, 30000))
    y1 = np.array(patient_1.getECG())
    x2 = np.array(range(0, 30000))
    y2 = np.array(ecg_signal_pacedAAI)
    # create the figure and axes objects
    fig = plt.figure()
    ax1 = plt.subplot(2, 1, 1)
    ax2 = plt.subplot(2, 1, 2)
    data_skip = 100


    def init_func():
        ax1.clear()
        ax2.clear()
        ax1.set_xlabel('Sampling rate')
        ax1.set_ylabel('mV')
        ax2.set_xlabel('Sampling rate')
        ax2.set_ylabel('mV')
        ax1.set_xlim(x1[0], x1[-1])
        ax1.set_ylim(-0.5, 1.75)
        ax2.set_xlim(x2[0], x2[-1])
        ax2.set_ylim(-0.5, 1.75)


    def animate(i):
        ax1.plot(x1[i:i + data_skip], y1[i:i + data_skip], label="patient's heart rate", color='tab:blue')
        ax1.legend(["patient's heart rate"])
        ax2.plot(x2[i:i + data_skip], y2[i:i + data_skip], label="paced heart rate", color='tab:orange')
        ax2.legend(["paced heart rate"])


    # run the animation
    ani = FuncAnimation(fig, animate, frames=np.arange(0, len(x1), data_skip), init_func=init_func(), interval=50,
                        repeat=True)
    plt.show()
    
    #shows VVI static graphs, return to cardio client
    y = np.array(patient_2.getECG())
    x = np.array(range(0, 30000))
    y1 = np.array(ecg_signal_pacedVVI)
    x1 = np.array(range(0, 30000))
    fig, (ax1, ax2) = plt.subplots(2)
    fig.suptitle('VVI pacing mode')
    ax1.plot(x, y, label="patient's heart rate")
    ax1.legend(loc="upper right")
    ax2.plot(x1, y1, label="paced heart rate")
    ax2.legend(loc="upper right")
    plt.show()

    #creetes graph for animation 
    fig = plt.figure()
    fig.suptitle('VVI pacing mode')
    ax1 = plt.subplot(2, 1, 1)
    ax2 = plt.subplot(2, 1, 2)
    y1 = np.array(patient_2.getECG())
    y2 = np.array(ecg_signal_pacedVVI)
    ani = FuncAnimation(fig, animate, frames=np.arange(0, len(x1), data_skip), init_func=init_func(), interval=50,
                        repeat=True)
    plt.show()


    #shows DDD static graphs, return to cardio client
    y = np.array(patient_3.getECG())
    x = np.array(range(0, 30000))
    y1 = np.array(ecg_signal_pacedDDD)
    x1 = np.array(range(0, 30000))
    fig, (ax1, ax2) = plt.subplots(2)
    fig.suptitle('DDD pacing mode')
    ax1.plot(x, y)
    ax1.plot(x, y, label="patient's heart rate")
    ax1.legend(loc="upper right")
    ax2.plot(x1, y1)
    ax2.plot(x1, y1, label="paced heart rate")
    ax2.legend(loc="upper right")
    plt.show()


    fig = plt.figure()
    fig.suptitle('DDD pacing mode')
    ax1 = plt.subplot(2, 1, 1)
    ax2 = plt.subplot(2, 1, 2)
    y1 = np.array(patient_3.getECG())
    y2 = np.array(ecg_signal_pacedDDD)
    ani = FuncAnimation(fig, animate, frames=np.arange(0, len(x1), data_skip), init_func=init_func(), interval=50,
                        repeat=True)
    plt.show()

'''ecg_df = pd.DataFrame({"patient's heart rate": patient_2.getECG()})
    nk.signal_plot(ecg_df)
    ecg_df = pd.DataFrame({"paced heart rate": pacemaker_2.pace()})
    nk.signal_plot(ecg_df)
    ecg_df = pd.DataFrame({"patient's heart rate": patient_3.getECG()})
    nk.signal_plot(ecg_df)
    ecg_df = pd.DataFrame({"paced heart rate": pacemaker_3.pace()})
    nk.signal_plot(ecg_df)'''
