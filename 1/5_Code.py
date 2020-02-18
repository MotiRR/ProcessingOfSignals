import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import csv

def readCSVFile(FILENAME):
 
 with open(FILENAME, "r", newline="") as file:
    reader = csv.DictReader(file)
    for row in reader:
        return float(row["amplitude"]), float(row["offset"]), float(row["frequency"]), int(row["phase"]), int(row["samplingFrequency"])

def writeCSVFile(FILENAME, ar_x, ar_y):
 with open(FILENAME, "w") as file:
    i = 0
    columns = ["Time", "Signal"]
    writer = csv.DictWriter(file, fieldnames=columns)
    writer.writeheader()
    for t in ar_x:
        ar_y.append(funcHarmonicSignal(t))
        row = {"Time": t, "Signal": ar_y[i]}
        writer.writerow(row)
        i = i + 1


def funcForFormatter(x, pos):
    if x < 1 and x != 0 and x > -1:
        return "{x} mB".format(x= x*1e3)
    else:
        return "{x} B".format(x=x)

if __name__ == "__main__":
 
 amplitude, offset, f0, phiDegree, samplingFrequency = readCSVFile("5_data.csv")
 #f0 - циклическая частота в герцах 

 #1 гр = pi/180 радиан
 radian = np.pi/180
 phiRadian = phiDegree*radian
 #w0 - угловая частота в радианах
 #f0 и w0 связаны формулой T=1/f0=2*pi/w0
 w = 2*np.pi*f0
 period = 1/f0
 funcHarmonicSignal = lambda t: offset+amplitude*np.cos(w*t + phiRadian)
 print("{}+{}*np.cos({}*t+{})".format(offset,amplitude,w,phiRadian))
 modelTime = 100*1e-3

 # Частота дискретизации f = 1/(del)t
 samplingFrequency = samplingFrequency*1e3
 
 samplingPeriod = 1/samplingFrequency
 deltaFrequency = samplingFrequency

 
 ar_x = np.linspace(0.0, modelTime, deltaFrequency)
 ar_y = []
 
 writeCSVFile("5_signal.csv", ar_x, ar_y)

 mean = (1/period) * ((amplitude*np.sin(period*w+phiRadian)+offset*period*w-amplitude*np.sin(phiRadian))/w)
 
 ne = offset+amplitude*np.cos(w*6.59592*1e-5 + phiRadian)
 
 print("Значение: {0} В".format(ne))

 print("Амплитуда: {0} В".format(amplitude))
 print("Смещение: {0} В".format(offset))
 print("Циклическая частота: {0} Гц".format(f0))
 print("Угловая частота: {0} рад/с".format(w))
 print("Период: {0} с".format(period))
 print("Начальная фаза: {0} град".format(phiDegree))
 print("Начальная фаза: {0} рад".format(phiRadian))
 print("Время моделирования: {0} с".format(modelTime))
 print("Частота дискретизации: {0} Гц".format(samplingFrequency))
 print("Среднее значение сигнала: {0}".format(mean))
 
 formatterAmplitude = ticker.FuncFormatter(funcForFormatter)
 formatterTime = ticker.StrMethodFormatter("{x:,g} c")

 figFull, axFull = plt.subplots()
 axFull.plot(ar_x[:int(samplingFrequency*0.01)], ar_y[:int(samplingFrequency*0.01)])
 axFull.set_title("Сигнал")
 axFull.set_xlabel("Время")
 axFull.set_ylabel("Амплитуда")
 axFull.xaxis.set_major_formatter(formatterTime)
 axFull.yaxis.set_major_formatter(formatterAmplitude)

 figPart, axPart = plt.subplots()
 axPart.plot(ar_x[:int(samplingFrequency*0.001)], ar_y[:int(samplingFrequency*0.001)])
 axPart.set_title("Сигнал")
 axPart.set_xlabel("Время")
 axPart.set_ylabel("Амплитуда")
 axPart.xaxis.set_major_formatter(formatterTime)
 axPart.yaxis.set_major_formatter(formatterAmplitude)

 plt.show()



