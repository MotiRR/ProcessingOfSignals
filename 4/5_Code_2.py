import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from numpy.fft import rfft, rfftfreq, fftshift, fftfreq
import csv
import random as rm
import math

def readCSVFile(FILENAME):
 ar_s_ns = np.array([], dtype=np.float64)
 ar_s = np.array([], dtype=np.float64)
 ar_ns = np.array([], dtype=np.float64)
 with open(FILENAME, "r", newline="") as file:
    reader = csv.reader(file)
    for row in reader:
     if row[1] == "Signal" or row[1] == "Noise" or row[1] == "Signal_Noise":
      continue
     #print(row[1])
     ar_s_ns = np.append(ar_s_ns, float(row[1]))
     ar_s = np.append(ar_s, float(row[2]))
     ar_ns = np.append(ar_ns, float(row[3]))
 return ar_s_ns, ar_s, ar_ns

if __name__ == "__main__":
 
 FILENAME_SIGNAL_NOISE = "5_signal_noise.csv"
 #Массивы
 ar_signal_noise, ar_signal, ar_noise  = readCSVFile(FILENAME_SIGNAL_NOISE)
 
 dli = math.log2(len(ar_signal))
 N = 2**math.floor(dli) - 1
 print("Длина БПФ {}".format(N))

 ar_signal = ar_signal[:N]
 ar_noise = ar_noise[:N]
 ar_signal_noise = ar_signal_noise[:N]

 FD = 100000
 
 spectrum_signal = rfft(ar_signal)

 spectrum_noise = rfft(ar_noise)
 spectrum_signal_noise = rfft(ar_signal_noise) 

 formatterAmplitude = ticker.StrMethodFormatter("{x:,g} В")
 formatterTime = ticker.StrMethodFormatter("{x:,g} Гц")

 freq = rfftfreq(N, 1./FD)
 ffreq = fftfreq(N, 1./FD)
 
 abs_spectrum_signal = abs(spectrum_signal)/N
 #abs_spectrum_signal[0] = 0
 abs_spectrum_noise = abs(spectrum_noise)/N
 #abs_spectrum_noise[0] = 0
 abs_spectrum_signal_noise = abs(spectrum_signal_noise)/N
 abs_spectrum_signal_noise[0] = 0
 TimeModeling = 0.093
 print("SNR теоретическая {}".format(5))
 signal_square = [A**2 for A in abs_spectrum_signal]
 noise_square = [A**2/TimeModeling for A in abs_spectrum_noise]
 sum_signal_square = sum(signal_square)
 print("Средняя мощность синала: {}".format(sum_signal_square))
 sum_noise_square = sum(noise_square)/(2*np.pi)
 print("Средняя мощность шума: {}".format(sum_noise_square))
 SNR = 10*math.log10(sum_signal_square/sum_noise_square)
 print("SNR практическая {}".format(SNR))

 NPo = 10
 arNPo = NPo + 1
 print("Частота {}, Амплитуда {}, Номер отсчета {}".format(freq[NPo], abs_spectrum_signal[NPo], arNPo))
 




