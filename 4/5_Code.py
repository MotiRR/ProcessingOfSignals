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


 noiseAmplitude = 0.5623413251903491
 signalAmplitude = 1
 SNR = 20*math.log10(signalAmplitude/noiseAmplitude)
 print("SNR {}".format(round(SNR)))
 
 FD = 100*1e4
 
 spectrum_signal = rfft(ar_signal)
 spectrum_noise = rfft(ar_noise)
 spectrum_signal_noise = rfft(ar_signal_noise)

 formatterAmplitude = ticker.StrMethodFormatter("{x:,g} В")
 formatterTime = ticker.StrMethodFormatter("{x:,g} Гц")

 freq = rfftfreq(N, 1./FD)
 ffreq = fftfreq(N, 1./FD)
 
 abs_spectrum_signal = abs(spectrum_signal)/N
 abs_spectrum_signal[0] = 0
 abs_spectrum_noise = abs(spectrum_noise)/N
 abs_spectrum_noise[0] = 0
 abs_spectrum_signal_noise = abs(spectrum_signal_noise)/N
 abs_spectrum_signal_noise[0] = 0
 
 figFull, axFull = plt.subplots()
 axFull.plot(freq, abs_spectrum_signal)
 axFull.set_title("Частотная область")
 axFull.set_xlabel("Частота")
 axFull.set_ylabel("Амплитуда")
 axFull.xaxis.set_major_formatter(formatterTime)
 axFull.yaxis.set_major_formatter(formatterAmplitude)

 figFull, axFull = plt.subplots()
 axFull.plot(freq, abs_spectrum_noise)
 axFull.set_title("Частотная область")
 axFull.set_xlabel("Частота")
 axFull.set_ylabel("Амплитуда")
 axFull.xaxis.set_major_formatter(formatterTime)
 axFull.yaxis.set_major_formatter(formatterAmplitude)

 figFull, axFull = plt.subplots()
 axFull.plot(freq, abs_spectrum_signal_noise)
 axFull.set_title("Частотная область")
 axFull.set_xlabel("Частота")
 axFull.set_ylabel("Амплитуда")
 axFull.xaxis.set_major_formatter(formatterTime)
 axFull.yaxis.set_major_formatter(formatterAmplitude)
 
 plt.show()



