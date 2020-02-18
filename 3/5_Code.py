import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import csv
import random as rm

def readCSVFile(FILENAME):
 
 with open(FILENAME, "r", newline="") as file:
    reader = csv.DictReader(file)
    for row in reader:
        return float(row["amplitude"]), float(row["offset"]), float(row["frequency"]), int(row["phase"]), int(row["samplingFrequency"])

def writeCSVFile(FILENAME, ar_x, ar_y):
 with open(FILENAME, "w") as file:
    i = 0
    columns = ["Time", "Signal_Noise", "Signal", "Noise"]
    writer = csv.DictWriter(file, fieldnames=columns)
    writer.writeheader()
    for t in ar_x:
        s = funcHarmonicSignal(t) 
        ns = funcUniform(noiseLeft, noiseRight)
        ar_y.append(s + ns - mean)
        row = {"Time": t, "Signal_Noise": ar_y[i], "Signal": s, "Noise": ns}
        writer.writerow(row)
        i = i + 1

def funcForFormatter(x, pos):
    if x < 1 and x != 0 and x > -1:
        return "{:.1f} mB".format(x*1e3)
    else:
        return "{:.1f} B".format(x)

if __name__ == "__main__":
 
 #+Для гармонического колебания+
 amplitude, offset, f0, phiDegree, samplingFrequency = readCSVFile("5_data.csv")
 #f0 - циклическая частота в герцах 

 #1 гр = pi/180 радиан
 radian = np.pi/180
 phiRadian = phiDegree*radian
 #w0 - угловая частота в радианах
 #f0 и w0 связаны формулой T=1/f0=2*pi/w0
 w = 2*np.pi*f0
 period = 1/f0
 mean = 0.5
 funcHarmonicSignal = lambda t: offset + amplitude*np.cos(w*t + phiRadian) 
 #-Для гармонического колебания-
 
 #+Для шума+
 signalAmplitude = 1
 noiseAmplitude = 0
 SNR = 2

 noiseAmplitude = signalAmplitude/np.power(10, (SNR/20))
 
 noiseLeft = 0.0
 noiseRight = noiseAmplitude
 funcUniform = lambda a, b: rm.uniform(a, b)
 #-Для шума-

 modelTime = 100*1e-3
 samplingFrequency = 100*1e3
 deltaFrequency = samplingFrequency

 ar_x = np.linspace(0.0, modelTime, deltaFrequency)
 ar_y = []

 writeCSVFile("5_signal_noise.csv", ar_x, ar_y)

 print("SNR: {0}".format(SNR))
 print("signalAmplitude: {0}".format(signalAmplitude))
 print("noiseAmplitude: {0}".format(noiseAmplitude))
 print("Время моделирования: {0} с".format(modelTime))
 print("Частота дискретизации: {0} Гц".format(samplingFrequency))

 formatterAmplitude = ticker.FuncFormatter(funcForFormatter)
 formatterTime = ticker.StrMethodFormatter("{x:,g} c")

 maxEl = max(ar_y)
 minEl = min(ar_y)
 ar_y = [A - (0.256) for A in ar_y]

 figFull, axFull = plt.subplots()
 axFull.plot(ar_x[:int(samplingFrequency*0.01)], ar_y[:int(samplingFrequency*0.01)])
 axFull.set_title("Сигнал/Шум")
 axFull.set_xlabel("Время")
 axFull.set_ylabel("Амплитуда")
 axFull.xaxis.set_major_formatter(formatterTime)
 axFull.yaxis.set_major_formatter(formatterAmplitude)

 figPart, axPart = plt.subplots()
 axPart.plot(ar_x[:int(samplingFrequency*0.001)], ar_y[:int(samplingFrequency*0.001)])
 axPart.set_title("Сигнал/Шум")
 axPart.set_xlabel("Время")
 axPart.set_ylabel("Амплитуда")
 axPart.xaxis.set_major_formatter(formatterTime)
 axPart.yaxis.set_major_formatter(formatterAmplitude)

 plt.show()



