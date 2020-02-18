import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import csv
import random as rm

def writeCSVFile(FILENAME, ar_x, ar_y):
 with open(FILENAME, "w") as file:
    i = 0
    columns = ["Time", "Noise"]
    writer = csv.DictWriter(file, fieldnames=columns)
    writer.writeheader()
    for t in ar_x:
        ar_y.append(funcUniform(noiseMin, noiseMax))
        row = {"Time": t, "Noise": ar_y[i]}
        writer.writerow(row)
        i = i + 1


def funcForFormatter(x, pos):
    if x < 1 and x != 0 and x > -1:
        return "{:.1f} mB".format(x*1e3)
    else:
        return "{:.1f} B".format(x)

if __name__ == "__main__":
 
 modelTime = 100*1e-3
 samplingFrequency = 100*1e3
 deltaFrequency = samplingFrequency

 noiseMin = 0.0
 noiseMax = 1.0

 funcUniform = lambda a, b: rm.uniform(a, b)

 ar_x = np.linspace(0.0, modelTime, deltaFrequency)
 ar_y = []

 writeCSVFile("5_noise.csv", ar_x, ar_y)

 mathematicalExpectation = (noiseMin+noiseMax)/2
 dispersion = ((noiseMax-noiseMin)**2)/12
 
 sample = ar_y[0:1000]

 mathematicalExpectationSample = np.mean(sample)
 dispersionSample = np.var(sample)

 print("noiseMin: {0}".format(noiseMin))
 print("noiseMax: {0}".format(noiseMax))
 print("Математическое ожидание: {0}".format(mathematicalExpectation))
 print("Дисперсия: {0}".format(dispersion))
 print("Среднее по выборке: {0}".format(mathematicalExpectationSample))
 print("Дисперсия по выборке: {0}".format(dispersionSample))
 print("Время моделирования: {0} с".format(modelTime))
 print("Частота дискретизации: {0} Гц".format(samplingFrequency))

 formatterAmplitude = ticker.FuncFormatter(funcForFormatter)
 formatterTime = ticker.StrMethodFormatter("{x:,g} c")

 figFull, axFull = plt.subplots()
 axFull.plot(ar_x[:int(samplingFrequency*0.01)], ar_y[:int(samplingFrequency*0.01)])
 axFull.set_title("Шум")
 axFull.set_xlabel("Время")
 axFull.set_ylabel("Амплитуда")
 axFull.xaxis.set_major_formatter(formatterTime)
 axFull.yaxis.set_major_formatter(formatterAmplitude)

 figPart, axPart = plt.subplots()
 axPart.plot(ar_x[:int(samplingFrequency*0.001)], ar_y[:int(samplingFrequency*0.001)])
 axPart.set_title("Шум")
 axPart.set_xlabel("Время")
 axPart.set_ylabel("Амплитуда")
 axPart.xaxis.set_major_formatter(formatterTime)
 axPart.yaxis.set_major_formatter(formatterAmplitude)

 plt.show()



