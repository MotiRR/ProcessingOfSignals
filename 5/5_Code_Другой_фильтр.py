import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from numpy.fft import rfft, rfftfreq, fftshift, fftfreq
import csv
import random as rm
import math
from scipy.io import wavfile
import scipy


def low_pass_filter(max_freq, window_size, sample_rate):
 fft_bin_width = sample_rate / window_size
 max_freq_bin = max_freq / fft_bin_width
 filter_block = np.ones(window_size)
 filter_block[int(max_freq_bin):int(window_size - max_freq_bin)] = 0
 return filter_block

def stft(input_data, sample_rate, window_size, hop_size):
 window = scipy.hamming(window_size)
 output = scipy.array([scipy.fft(window*input_data[i:i+window_size]) for i in range(0, len(input_data) - window_size, hop_size)])
 return output

def istft(input_data, sample_rate, window_size, hop_size, total_time):
 output = scipy.zeros(int(total_time*sample_rate))
 for n, i in enumerate(range(0, len(output) - window_size, hop_size)):
  output[i:i + window_size] += scipy.real(scipy.ifft(input_data[n]))
 return output

def filter_audio(input_signal, sample_rate, filter_window, window_size):
 hop_size = window_size // 2
 total_time = len(input_signal) / sample_rate

 stft_output = stft(input_signal, sample_rate, window_size, hop_size)
 filtered_result = [original * filter_window for original in stft_output]
 resynth = istft(filtered_result, sample_rate, window_size, hop_size, total_time)
 return resynth

if __name__ == "__main__":

 FILENAME_WAV = "sample5.wav"
 WINDOW_SIZE = 256
 LOWER_BORDER = 5000

 fs, data = wavfile.read(FILENAME_WAV)
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
 N = 2**math.floor(dli) - 1
 print("Длина БПФ {}".format(N))

 freq = rfftfreq(N, 1./fs)
 input_signal = data
 data = data[:N]
 
 spectrum_old_wav = rfft(data)
 abs_spectrum_old_wav = abs(spectrum_old_wav)/N

 formatterTime = ticker.StrMethodFormatter("{x:,g} Гц")
 figFull, axFull = plt.subplots()
 axFull.plot(freq, abs_spectrum_old_wav)
 axFull.set_title("Частотная область")
 axFull.set_xlabel("Частота")
 axFull.set_ylabel("Амплитуда")
 axFull.xaxis.set_major_formatter(formatterTime)
 axFull.yaxis.set_major_formatter(formatterAmplitude)

 filter_window = low_pass_filter(LOWER_BORDER, WINDOW_SIZE, fs)
 resynth = filter_audio(input_signal, fs, filter_window, WINDOW_SIZE)
 
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



