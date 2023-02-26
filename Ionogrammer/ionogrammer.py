import numpy as np
import matplotlib.pyplot as plt

# Initialize variables and pull data
sample_rate = 25E6
filename = "test"
data = np.fromfile(filename, dtype=np.complex64)

# Generate raw spectrogram
spectrum, freqs, t = plt.specgram(data, NFFT=1024, Fs=sample_rate, 
                                  window=np.hamming, mode='psd', noverlap=128,
                                  scale='dB')