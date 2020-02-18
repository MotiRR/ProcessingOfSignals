import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from numpy.fft import rfft, rfftfreq, fftshift, fftfreq
import csv
import random as rm
import math
from scipy.io import wavfile
from scipy import signal

if __name__ == "__main__":

 FILENAME_WAV = "sample5.wav"

 fs, data = wavfile.read(FILENAME_WAV)
 time = len(data)/fs
 ar_x = np.linspace(0.0, time, len(data))

 dli = math.log2(len(data))
 N = 2**math.floor(dli) - 1
 print("Длина БПФ {}".format(N))

 freq = rfftfreq(N, 1./fs)
 input_signal = data
 f = data
 data = data[:N]

 #b, a = signal.butter(10, 15000, fs = fs) 
 b, a =signal.cheby1(1, 20, 15000, fs=fs)
 mono_signal = signal.filtfilt(b, a, input_signal)

 #b, a = signal.butter(10, 23000, btype = 'highpass', fs = fs)
 b, a =signal.cheby1(1, 10, 23000, btype = 'highpass', fs=fs) 
 diff_signal = signal.filtfilt(b, a, input_signal) 

 freq_subcarrie = 40000
 carrie = []
 for t in ar_x:
  carrie.append(np.cos(2 * np.pi * freq_subcarrie * t))
 demod_diff_signal = diff_signal * carrie

 #b, a = signal.butter(10, 15000, fs = fs) 
 b, a =signal.cheby1(1, 20, 15000, fs=fs)
 re_demod = signal.filtfilt(b, a, demod_diff_signal) 
 d = mono_signal[0]/re_demod[0]
 re_demod = [A * d for A in re_demod]
 
 s1 = (mono_signal+re_demod)/2
 s2 = (mono_signal-re_demod)/2
 wavfile.write("new_sample5_1.wav", fs, mono_signal)
 wavfile.write("new_sample5_2.wav", fs, s2) 


 plt.show()
