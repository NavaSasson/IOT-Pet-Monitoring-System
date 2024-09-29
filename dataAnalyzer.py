# data collection and analyzing module 

from manager import *
import time
from scipy.spatial import distance
import statistics
import matplotlib.pyplot as plt
import numpy as np
from data_acq import *
from init import *


def thrh_comp(Y):
    ''' Used for Dynamic Threshold calculation and therein carries scattered energy info'''
    #percen_thr=0.05 # 5% of max energy holds - defined in init.py
    return np.mean(np.sort(abs(Y))[-int(len(Y)*percen_thr):-1])
 

def fft_block(Xdata, isplot, issave, fname='data/AxisX_pass.png'):
    #Fs = 2048.0  # sampling rate - defined in init.py
    Ts = 1.0/Fs # sampling interval
    t = np.arange(0,len(Xdata)/Fs,Ts) # time vector
    y = Xdata - np.mean(Xdata)
    n = len(y) # length of the signal
    k = np.arange(n)
    T = n/Fs
    frq = k/T # two sides frequency range    
    frq = frq[range(int(n/2))] # one side frequency range
    Y = np.fft.fft(y)/n # fft computing and normalization
    Y = Y[range(int(n/2))]    
    thrh=thrh_comp(Y)
    if isplot:
        fig, ax = plt.subplots(2, 1)
        ax[0].plot(t,y)
        ax[0].set_xlabel('Time')
        ax[0].set_ylabel('Amplitude')
        ax[1].plot(frq,abs(Y),'b',frq,thrh+abs(Y)*0,'r') # plotting the spectrum
        ax[1].vlines([230, 240 ], 0, np.max(abs(Y)),  colors='g')
        ax[1].vlines([ 470, 480 ], 0, np.max(abs(Y)),  colors='g')
        ax[1].vlines([ 710, 720 ], 0, np.max(abs(Y)),  colors='g')
        ax[1].vlines([ 565, 630 ], 0, np.max(abs(Y)),  colors='g')
        ax[1].set_xlabel('Freq (Hz)')
        ax[1].set_ylabel('|Y(freq)|')
        ax[0].grid(True)
        ax[1].grid(True)
        if issave:
            plt.savefig(fname)        
        plt.show()
    return thrh*10000 # 1000 - imperical normalization factor   

def fft_main():
    data = acq_data()
    datapool=[  data.AxisX.to_numpy(),
                data.AxisY.to_numpy(),
                data.AxisZ.to_numpy()]
    Ax_thrh=[]
    for cnt, Xdata in enumerate(datapool):
        Ax_thrh.append(fft_block(Xdata, isplot, issave, fname='data/Axis'+str(cnt)+'.png'))
    return Ax_thrh


def vib_dsp():
   current = fft_main()
   d = distance.euclidean(current, Axes_Threshold)
   print("Euclidean distance: ",d)
   std = statistics.stdev([abs(j-i) for i,j in zip(current , Axes_Threshold)])
   print("Standard Deviation of sample is % s " 
                % (std))
   if d > max_eucl or std*100 > deviation_percentage:
      return True
   return False
   
