import numpy as np
import time
import matplotlib.pyplot as plt
import sys

# User params
fs = 200E6/12
f_start = -300e3
f_end = 300e3
test_slope = 100e3
file = open("test.chirp", "wb") # Jank way to ensure file gets overwritten
print("Generating File... \n")

# Calculated
deltaT = 1/fs
deltaF = test_slope/fs/2  #I don't know why I need this factor of 1/2, but I do..
spanT = (f_end-f_start)/test_slope

lastT = 0
debugI = 0
for sectionT in np.linspace(0, spanT, 50):
    debugI += 1
    tic = time.time()
    t = deltaT * np.arange(lastT*fs, sectionT*fs)
    f = deltaF * np.arange(lastT*fs, sectionT*fs) + f_start
    tone = np.sin(2*np.pi*f*t)
    lastT = sectionT
    #test = np.complex64(1j*tone)
    file.write(np.complex64(1j*tone))
    toc = time.time()
    sys.stdout.write("\rCycle Time: "+str(toc-tic)+"   "+str(debugI)+"/50")



file.close()
data = np.fromfile(r"test.chirp", dtype=np.complex64)
plt.specgram(data, NFFT=1024, Fs=fs)
plt.show()

print("debug")