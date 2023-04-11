import numpy as np
import matplotlib.pyplot as plt
import matplotlib.mlab as mlb

decimation = 6000
fs = 200e6/16
fft_size = 512
ionosonde_slope = 100e3
filename = r"LCgram3_220.chirp"
ypoints = 5
xpoints = 5

data = np.fromfile(filename, dtype=np.complex64)

fig, ax = plt.subplots()
spectrum, freqs, t, im = plt.specgram(data, NFFT=fft_size, Fs=fs/decimation, noverlap=0, mode='psd', cmap='cool', vmin=-140)
#plt.set_xlabel("test")
#print(np.max(10*np.log10(spectrum)))
#print(np.min(10*np.log10(spectrum)))
ax.set_xlabel("Frequency [MHz]")
ax.set_ylabel("Relative Delay [ms]")

ylocs = np.linspace(-fs/decimation/2, fs/decimation/2, ypoints)
xlocs = np.linspace(0, len(data)/(fs/decimation), xpoints)

ylabels = np.round((ylocs + fs/decimation/2)/ionosonde_slope * 1e3, 2)
xlabels = np.round((xlocs*100e3+8e6)/1e6, 2)

plt.yticks(ylocs, ylabels)
plt.xticks(xlocs, xlabels)

plt.show()