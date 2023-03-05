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
import os


############ USER VARS ##################

sample_rate = 25E6 # Data sample rate in hz
fft_size =  1024 # Samples/Bins per FFT
sweep_rate = 100E3 # Theoretical sweep rate of ionosonde in hz/s
fileName = r"../../sdrtest.raw" # Path to data
ionogram_length_t = 0.1 # Time length of ionogram in seconds
freq_offset=0 # This parameter is not necessary, but can help shift your time baseline
dataRate=int(1.25e8) # Maximum number of samples to load into memory at any given moment

# sample_rate = 32E3 # Data sample rate in hz
# fft_size =  512 # Samples/Bins per FFT
# sweep_rate = 3.05E3 # Theoretical sweep rate of ionosonde in hz/s
# fileName = r"./samp32k_sweep3000_trans5k.raw" # Path to data
# ionogram_length_t = 1.5 # Time length of ionogram in seconds
# freq_offset=0 # This parameter is not necessary, but can help shift your time baseline
# dataRate=int(100e3) # Maximum number of samples to load into memory at any given moment

#########################################



# Do some readout
print("#### IONOGRAMMER v0.1 ####")
print("Sample Rate: ", sample_rate)
print("Sweep Rate: ", sweep_rate)
print("File: ", fileName)

# Open file and define some useful values
dataFile = open(fileName,"rb") # Data file
#readPointer = 0 # Keeps track of where we are in the file
delta_t = fft_size/sample_rate # Time between successive FFTs (time between each row of spectrum)
bin_width = sample_rate/fft_size # Bin width in hz
ionogram_length_n = math.ceil(ionogram_length_t/delta_t-1) # Number of time instances in our spectrogram
absolute_n = 0
rows_completed = 0

# Initalize arrays
ionogram_spectrum = np.ones([fft_size, ionogram_length_n], dtype=np.float64)*6e-20







def readData(readPointer):
    print("data start")
    data = np.fromfile(fileName, dtype=np.complex64, count=dataRate, offset=readPointer)
    print("data end")
    return data


def rawSpectrogram(data):
    # Generate raw spectrogram via plt. 
    # This is a convenient way to do the sequential FFTs without writing our own code.
    print("plt start")
    spectrum, freqs, t, im = plt.specgram(data, NFFT=fft_size, Fs=sample_rate, noverlap=0)
    plt.clf()
    plt.close()
    print("plt end")
    return spectrum



def ionograte(spectrum):
    global rows_completed, absolute_n, ionogram_spectrum, slope_fix
    print("ion start")
    for row in range(0+freq_offset+rows_completed, len(spectrum)):
        # Calculate the time range for the current bin. This is continuous time and will be discretized.
        bin_start_t = (bin_width*(row-freq_offset))/sweep_rate

        # Now discretize these times
        bin_start_n = math.floor(bin_start_t/delta_t) - math.floor(ionogram_length_n/2) - absolute_n  # Subtract to see time before expected
        bin_end_n = bin_start_n+ionogram_length_n
        # If we are at the beginning of the recording we won't be able to see into the past, so set to 0
        if bin_start_n < 0:
            bin_start_n = 0
        if bin_end_n > len(spectrum[0]):
            readPointer = (bin_start_n+absolute_n)*fft_size*8
            absolute_n += bin_start_n

            #readPointer = bin_end_n-bin_start_n*fft_size*-1
            rows_completed = row # real number is this minus 1, but this value is more useful
            print(rows_completed)
            break

        # Now use these values to grab the wanted values from data
        selected_times = spectrum[row][bin_start_n:bin_end_n]
        ionogram_spectrum[row][ionogram_length_n-len(selected_times):ionogram_length_n] = selected_times

    print("ion end")
    try:
        return readPointer
    except:
        return 1e10


def plotIonogram(ionogram_spectrum):
    plt.figure(3)
    ionogram_spectrum = 10. * np.log10(ionogram_spectrum) #psd
    ionogram_spectrum = np.transpose(ionogram_spectrum) 
    plt.imshow(ionogram_spectrum, origin='lower')
    del ionogram_spectrum
    plt.axis('auto')
    plt.title("Ionogram")
    plt.xlabel("Frequency")
    plt.ylabel("Relative Time")
    plt.show()


    print("Done.")




def main():
    global rows_completed, ionogram_spectrum
    readPointer = 0
    while (readPointer/8 < os.stat(fileName).st_size) & (rows_completed<=1023):
        data = readData(readPointer)
        spectrum = rawSpectrogram(data)
        readPointer = ionograte(spectrum)
       



    # In this block we will generate a transposed spectrogram. Not necessary
    # but useful for debugging and presentation
    plt.figure(2)
    spectrum = 10. * np.log10(spectrum) #psd
    spectrum = np.transpose(spectrum)
    plt.imshow(spectrum, cmap='hot',origin='lower')
    del spectrum
    plt.axis('auto')
    plt.title("Transposed Spectrogram")
    plt.xlabel("Frequency")
    plt.ylabel("Time")
    #plt.xticks(range(math.floor(min(t)), math.ceil(max(t))))
    #plt.yticks(range(math.floor(min(freqs)), math.ceil(max(freqs))))
    #plt.show()


    # Now we plot the ionogram itself beased on the truncated spectrum
    plt.figure(3)
    ionogram_spectrum = 10. * np.log10(ionogram_spectrum) #psd
    ionogram_spectrum = np.transpose(ionogram_spectrum) 
    plt.imshow(ionogram_spectrum, origin='lower')
    del ionogram_spectrum
    plt.axis('auto')
    plt.title("Ionogram")
    plt.xlabel("Frequency")
    plt.ylabel("Relative Time")
    plt.show()


    print("Done.")









if __name__ == "__main__":
    main()