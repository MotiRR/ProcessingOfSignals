import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from numpy.fft import rfft, rfftfreq, fftshift, fftfreq
import csv
import random as rm
import math
from scipy.io import wavfile
from scipy import signal
import scipy

def windowWeight(sig, window_size):
 output = np.array([], dtype=np.float64)
 w = scipy.blackman(window_size)
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

 data =  windowWeight(data, 800)

 dli = math.log2(len(data))
 N = 2**math.floor(dli) - 1
 print("Длина БПФ {}".format(N))

 freq = rfftfreq(N, 1./fs)
 input_signal = data
 data = data[:N]

 b, a = signal.butter(5, 30000, btype = 'highpass', fs = fs) 
 input_signal = signal.filtfilt(b, a, input_signal) 

 freq_subcarrie = 40000
 carrie = []
 for t in ar_x:
  carrie.append(np.sin(2 * np.pi * freq_subcarrie * t))
 demod = input_signal * carrie

 demod_N = demod[:N]
 demod_new = rfft(demod_N)
 abs_demod_new = abs(demod_new)/N
 formatterAmplitude = ticker.StrMethodFormatter("{x:,g} В")
 formatterTime = ticker.StrMethodFormatter("{x:,g} Гц")
 figFull, axFull = plt.subplots()
 axFull.plot(freq, abs_demod_new)
 axFull.set_title("Частотная область")
 axFull.set_xlabel("Частота")
 axFull.set_ylabel("Амплитуда")
 axFull.xaxis.set_major_formatter(formatterTime)
 axFull.yaxis.set_major_formatter(formatterAmplitude)

 plt.show()
