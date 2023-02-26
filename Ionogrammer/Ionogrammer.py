# Ionogrammer.py
# By Jaden Keener / NMT Chirp Team
# Last updated 2/26/23 14:54
#
# This program reads raw IQ data into memory and generates spectrograms
# and Ionograms based on preset parameters.
#
# The most important parameters to set are file path, sample rate, fft size,
# and sweep rate.
#
# TODO: Optimize program to read only parts of IQ file into memory at a time.
#       This will allow us to work on large data sets without memory constraints

import numpy as np
import matplotlib.pyplot as plt
import math

##################################################################

# Initialize variables and pull data
sample_rate = 32E3 # Data sample rate in hz
fft_size = 512 # Samples/Bins per FFT
sweep_rate = 3.05e3 # Theoretical sweep rate of ionosonde in hz/s
filename = r"samp32k_sweep3000_trans5k.raw" # Path to data 
spectrogram_length_t = 2 # Time length of spectrogram in seconds
freq_offset=0 # This parameter is not necessary, but can help shift your time baseline

data = np.fromfile(filename, dtype=np.complex64) # Read data from file. 

###############################################################


# Generate raw spectrogram via plt. 
# This is a convenient way to do the sequential FFTs without writing our own code.
plt.figure(1)
spectrum, freqs, t, im = plt.specgram(data, NFFT=fft_size, Fs=sample_rate, noverlap=0)

# Calculate some important constants
delta_t = t[1]-t[0] # Time between successive FFTs (time between each row of spectrum)
bin_width = sample_rate/fft_size # Bin width in hz
spectrogram_length_n = math.ceil(spectrogram_length_t/delta_t-1)
plt.title("PLT Spectrogram")
plt.xlabel("Time")
plt.ylabel("Frequency")

# Initalize arrays
truncated_spectrum = np.ones([fft_size, spectrogram_length_n], dtype=np.float64)*6e-20

# Main work loop. Loop through each frequency (row) and grab the desired
# Time values for the ionogram
for row in range(0+freq_offset, len(spectrum)):
    # Calculate the time range for the current bin. This is continuous time and will be discretized.
    bin_start_t = (bin_width*(row-freq_offset))/sweep_rate

    # Now discretize these times
    bin_start_n = math.floor(bin_start_t/delta_t) - math.floor(spectrogram_length_n/2) # Subtract to see time before expected
    bin_end_n = bin_start_n+spectrogram_length_n
    # If we are at the beginning of the recording we won't be able to see into the past, so set to 0
    if bin_start_n < 0:
        bin_start_n = 0

    # Now use these values to grab the wanted values from data
    selected_times = spectrum[row][bin_start_n:bin_end_n]
    truncated_spectrum[row][spectrogram_length_n-len(selected_times):spectrogram_length_n] = selected_times


# In this block we will generate a transposed spectrogram. Not necessary
# but useful for debugging and presentation
plt.figure(2)
spectrum = 10. * np.log10(spectrum) #psd
spectrum = np.transpose(spectrum)
plt.imshow(spectrum, cmap='hot',origin='lower')
plt.axis('auto')
plt.title("Transposed Spectrogram")
plt.xlabel("Frequency")
plt.ylabel("Time")
#plt.xticks(range(math.floor(min(t)), math.ceil(max(t))))
#plt.yticks(range(math.floor(min(freqs)), math.ceil(max(freqs))))
#plt.show()


# Now we plot the ionogram itself beased on the truncated spectrum
plt.figure(3)
Z = 10. * np.log10(truncated_spectrum) #psd
Z = np.transpose(Z) 
plt.imshow(Z, origin='lower')
plt.axis('auto')
plt.title("Ionogram")
plt.xlabel("Frequency")
plt.ylabel("Relative Time")
plt.show()


print("Done.")
