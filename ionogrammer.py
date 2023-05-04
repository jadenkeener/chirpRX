""" ionogrammer.py
Last Edited 5/4/23
By Jaden Keener and the NMT Dev Team

This is the third and final block of the ChirpRX DSP chain.This block  
generates and saves an Ionogram with properly scaled and labeled axes.
"""


# Imports
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.mlab as mlb
import argparse
import os


""" Parse args
These are provided automagically by the previous ChirpRX block (LocalChirp)
"""
parser = argparse.ArgumentParser()
parser.add_argument("-d", "--decimation", help = "Decimation", type=int)
parser.add_argument("-p", "--path", help = "Path to .chirp file", type=str)
parser.add_argument("-B", "--fs", type=float)
parser.add_argument("-P", "--slope", type=float)
parser.add_argument("-C", "--fc", type=float)
args = parser.parse_args()

# Place args in easier to use vars
decimation = args.decimation
fc = args.fc
fs = args.fs
fft_size = 512
ionosonde_slope = args.slope
offset = 0
filename = args.path
ypoints = 5
xpoints = 5



""" Read and plot
Read in .chirp data from LocalChirp, create a figure for a spectrogram,
make the spectrogram
"""
data = np.fromfile(filename, dtype=np.complex64)
fig, ax = plt.subplots()
spectrum, freqs, t, im = plt.specgram(data, 
                                      NFFT=fft_size, 
                                      Fs=fs/decimation, 
                                      noverlap=0, 
                                      mode='psd', 
                                      vmin=-140)

""" Scale and label 
Scale and label axes. We transform x axis unit from s to Hz, and y axis unit
from Hz to s. See report for why and details on how.
"""                                     
ax.set_xlabel("Frequency [MHz]")
ax.set_ylabel("Relative Delay [ms]")

ylocs = np.linspace(-fs/decimation/2, fs/decimation/2, ypoints)
xlocs = np.linspace(0, len(data)/(fs/decimation), xpoints)

ylabels = np.round((ylocs + fs/decimation/2)/ionosonde_slope * 1e3, 2)
xlabels = np.round((xlocs*ionosonde_slope+(fc-(fs/2))+offset)/1e6, 2)

plt.yticks(ylocs, ylabels)
plt.xticks(xlocs, xlabels)
plt.title(filename+" Ionogram")

""" Save and delete
Save newly generated Ionogram and delte the original .RAW file to save 
disk space. We keep the .chirp since it is size efficient and useful.
"""
plt.savefig(filename.split(".")[0] + ".png")
os.remove(filename.split(".")[0] + ".RAW")
