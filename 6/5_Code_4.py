import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from numpy.fft import rfft, rfftfreq, fftshift, fftfreq
import csv
import random as rm
import math
from scipy.io import wavfile
from scipy import signal
import scipy as sc

def windowWeight(sig, window_size):
 output = np.array([], dtype=np.float64)
 w = sc.blackman(window_size)
 l = len(sig) - window_size
 for i in range(0, l, window_size):
  output = np.append(output, w*sig[i:i+window_size])
 output = np.append(output, w*sig[len(sig)-window_size:len(sig)])
 return output

if __name__ == "__main__":

 FILENAME_WAV = "sample5.wav"

 fs, data = wavfile.read(FILENAME_WAV)
 time = len(data)/fs
 ar_x = np.linspace(0.0, time, len(data))

 dli = math.log2(len(data))
 N = 2**math.floor(dli) - 1
 print("Длина БПФ {}".format(N))

 #data = windowWeight(data, 800)

 freq = rfftfreq(N, 1./fs)
 input_signal = data
 f = data
 data = data[:N]

 input_signal =  windowWeight(input_signal, 800)

 b, a = signal.butter(8, 15000, fs = fs) 
 mono_signal = signal.filtfilt(b, a, input_signal)

 b, a = signal.butter(8, 30000, btype = 'highpass', fs = fs) 
 diff_signal = signal.filtfilt(b, a, input_signal) 

 freq_subcarrie = 40000
 carrie = []
 for t in ar_x:
  carrie.append(np.sin(2 * np.pi * freq_subcarrie * t))
 demod_diff_signal = diff_signal * carrie

 b, a = signal.butter(8, 15000, fs = fs) 
 re_demod = signal.filtfilt(b, a, demod_diff_signal) 
 re_demod = [A * 2 for A in re_demod]

 #d = max(mono_signal)/(max(re_demod))
 #print(d)
 #re_demod = [A * d for A in re_demod]
 
 s1 = (mono_signal+re_demod)/2
 s2 = (mono_signal-re_demod)/2

 wavfile.write("new_sample5_1.wav", fs, s1)
 wavfile.write("new_sample5_2.wav", fs, s2) 


 plt.show()
