import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, lfilter, freqz
from scipy import signal
from pylab import rcParams
from os import path


def differences(name):
    dname = "Data/Data" + name + ".out"
    # dtsname = "Data/DataTimes" + name + ".out"
    if path.exists(dname):
        dout = np.loadtxt(dname, delimiter=',')
        # dtsout = np.loadtxt(dtsname, delimiter=',')
        maxes = np.max(dout[1:] - dout[:-1], axis=1)
        print(name)
        return maxes
    print("whoooops")


def readfile(file):
    sd = []
    with open(file, 'r') as f:
        for x in f:
            sd.append([float(n) for n in x.strip().split(',')])
    return sd


# filesit = "sitoutput_in30s.out"
# filestand = "standoutput_in30s.out"
# filewalk = "walkoutput_in30s.out"
# filejog = "jogoutput_in30s.out"

# cfilesit = readfile(filesit)
# cfilestand = readfile(filestand)
# cfilewalk = readfile(filewalk)
# cfilejog = readfile(filejog)


y = np.array(differences('standsit5s')).flatten()
# print(y)
y1 = np.array(differences('Null')).flatten()
y2 = np.array(differences('walk')).flatten()
y3 = np.array(differences('run')).flatten()


def output(y):
    yx = np.array(y) / 450
    t = np.arange(len(yx))
    fs = len(yx)
    Ts = 1 / fs
    # yf = np.fft.fft(yx)
    # xf = np.fft.fftfreq(len(yf), Ts)
    cuttoff_freq = 0.33  # 0.22 #0.33
    samp_rate = 20
    norm_pass = cuttoff_freq / (samp_rate / 2)
    norm_stop = 1.5 * norm_pass
    (N, Wn) = signal.buttord(wp=norm_pass, ws=norm_stop, gpass=2, gstop=30, analog=0)
    (b, a) = signal.butter(N, Wn, btype='low', analog=0, output='ba')
    yaxis = signal.lfilter(b, a, yx)
    return t, yaxis


print(output(y)[0])
print(output(y)[1])

rcParams['ytick.labelsize'] = 15
rcParams['xtick.labelsize'] = 15
fig1 = plt.figure(figsize=(12, 8))
plt.subplot(221)  # 222
plt.plot(output(y3)[0], np.abs(output(y3)[1]))
plt.title('(a) Jog', fontsize=16)

plt.subplot(222)  # 222
plt.plot(output(y2)[0], np.abs(output(y2)[1]))
plt.title('(b) Walk', fontsize=16)

plt.subplot(223)  # 222
plt.plot(output(y)[0], np.abs(output(y)[1]))
plt.title('(c) Stand-to-Sit', fontsize=16)

plt.subplot(224)  # 222
plt.plot(output(y1)[0], np.abs(output(y1)[1]))
plt.title('(d) Null', fontsize=16)

fig1.savefig('Features_filting.png', bbox_inches='tight', format='png', dpi=400)
plt.show()
