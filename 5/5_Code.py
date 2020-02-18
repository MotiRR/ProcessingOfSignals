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
import copy


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
 print(fs)
 time = len(data)/fs
 ar_x = np.linspace(0.0, time, len(data))

 formatterAmplitude = ticker.StrMethodFormatter("{x:,g} В")
 formatterTime = ticker.StrMethodFormatter("{x:,g} с")
 figFull, axFull = plt.subplots()
 axFull.plot(ar_x, data)
 axFull.set_title("Исходный wav файл")
 axFull.set_xlabel("Время")
 axFull.set_ylabel("Амплитуда")
 axFull.xaxis.set_major_formatter(formatterTime)
 axFull.yaxis.set_major_formatter(formatterAmplitude)

 dli = math.log2(len(data))
 N = 2**math.floor(dli)
 print("Длина БПФ {}".format(N))

 
 data = windowWeight(data, 255)
 #print(len(data))
 freq = rfftfreq(N, 1./fs)
 input_signal = data

 data = data[:N]

 spectrum_old_wav = rfft(data)
 abs_spectrum_old_wav = abs(spectrum_old_wav)/N
 abs_spectrum_old_wav

 ana = copy.copy(abs_spectrum_old_wav) 
 ana[:10000] = 0     
 cou = 0
 print("Три значения частоты для точечных источников шума")
 while cou != 3:
  i = np.argmax(ana[:20000]) 
  print("Частота {}, Амплитуда {}".format(freq[i], ana[i]))
  ana[i] = 0
  cou = cou + 1
 print("Начало и конец частотного интервала полосового шума")
 ana[:20000] = 0 
 i = 0
 leftBorder = 0
 rightBorder = 0
 for i in range(len(ana)):
  if ana[i] > 0.01 and leftBorder == 0:
   leftBorder = i
  if ana[i] < 0.09 and ana[i] > 0.01:
   rightBorder = i

 frequencyStart = freq[leftBorder] # частота сигнала для начала полосового шума
 frequencyEnd = freq[rightBorder] # частота сигнала для конца полосового шума
 samplingFrequency = 1. / fs # дискретизация
 # N - общее число отсчетов

 print("Начало {} Гц, Номер отчета {}".format(freq[leftBorder], int(frequencyStart*N*samplingFrequency)))
 print("Конец {} Гц, Номер отчета {}".format(freq[rightBorder], int(frequencyEnd*N*samplingFrequency)))

 formatterTime = ticker.StrMethodFormatter("{x:,g} Гц")
 figFull, axFull = plt.subplots()
 axFull.plot(freq, abs_spectrum_old_wav)
 axFull.set_title("Частотная область")
 axFull.set_xlabel("Частота")
 axFull.set_ylabel("Амплитуда")
 axFull.xaxis.set_major_formatter(formatterTime)
 axFull.yaxis.set_major_formatter(formatterAmplitude)
   
 b, a = signal.butter(8, 3000, fs = fs) 
 resynth = signal.filtfilt(b, a, input_signal) 

 wavfile.write("new_sample5.wav", fs, resynth)

 formatterTime = ticker.StrMethodFormatter("{x:,g} с")
 figFull, axFull = plt.subplots()
 axFull.plot(ar_x, resynth)
 axFull.set_title("Новый wav файл")
 axFull.set_xlabel("Время")
 axFull.set_ylabel("Амплитуда")
 axFull.xaxis.set_major_formatter(formatterTime)
 axFull.yaxis.set_major_formatter(formatterAmplitude)
 
 resynth = resynth[:N]
 spectrum_new_wav = rfft(resynth)
 abs_spectrum_new_wav = abs(spectrum_new_wav)/N

 formatterTime = ticker.StrMethodFormatter("{x:,g} Гц")
 figFull, axFull = plt.subplots()
 axFull.plot(freq, abs_spectrum_new_wav)
 axFull.set_title("Частотная область")
 axFull.set_xlabel("Частота")
 axFull.set_ylabel("Амплитуда")
 axFull.xaxis.set_major_formatter(formatterTime)
 axFull.yaxis.set_major_formatter(formatterAmplitude)
 
 plt.show()



