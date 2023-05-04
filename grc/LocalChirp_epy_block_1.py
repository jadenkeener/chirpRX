""" LocalChirp_epy_block_1.py
Last Edited 5/4/24
By Jaden Keener and the NMT Dev Team

Second custom block of the ChirpRX DSP chain.  
Generates a local tone that sweeps the spectrum at the specified slope. 
This tone gets mixed with ionosnde signal in the greater grc flowchart such
that we create a plottable frequency difference term.

Calls ionogrammer.py after processing is complete.
"""

# Imports
import numpy as np
import pmt
from gnuradio import gr
import os
import time


""" blk definition
This is the standard block class declaration for use in gnu radio. 
This file is one custom block in the larger LocalChirp.py flowchart

See gnu radio 'custom py block' documentation for further explanation.
"""
class blk(gr.sync_block):  

    def __init__(
        self, 
        slope=100e3, 
        samp_rate=200e6/12, 
        offset = 10e3, 
        filename=None, 
        decimation=100, 
        fc = 14.25E6):
        
        gr.sync_block.__init__(
            self,
            name='Local Chirp 1.6',   
            in_sig=[np.complex64],
            out_sig=[np.complex64]
        )

        """ Add parameters to class instance """
        self.slope = slope  
        self.fs = samp_rate
        self.fc = fc
        self.offset = offset
        self.filename = filename
        self.decimation = decimation
        self.over = True
        
        """ Initialize vars
        Calculate and initialize some important vars. These are:
        Last Time
        Last Frequency
        Frequency Span
        Time Step
        Frequency Step
        """
        self.lastT = 0
        self.lastF = -self.fs/2 + self.offset
        self.spanF = self.lastF + self.fs/2 - self.offset
        self.dt = 1/self.fs
        self.df = self.slope/self.fs/2 
        
        
    """ work function
    Standard declaration for gnu radio work function.  This is the function
    that is called whenever gnu radio has samples for this block to process.  
    
    This function is not called for every sample individually, but is instead
    fed large batches of samples at once.
    """
    def work(self, input_items, output_items):
    
        # Find number of samples on this call
        n = len(input_items[0]) 

        """ Generate LO
        This if/else statement generates the corresponding LO value for 
        every sample fed into this block. 
        
        We first check to see if we have swept the entire f spectrum, if not,
        then generate. If we have, then this block is over and we can call
        ionogrammer.
        """
        if self.lastF <= self.offset/2: 
        
            # Calculate the values of T and F we prog to on this call
            newT = self.dt*n + self.lastT
            newF = self.df*n + self.lastF
            
            # Make sure arrays are correct size. Can get slightly offsize due
            # to float precision errors
            t = np.resize(np.arange(self.lastT, newT, self.dt), n)
            f = np.resize(np.arange(self.lastF, newF, self.df), n)
            
            # Output is a complex exponential (I/Q)
            output_items[0][:] = np.exp(1j*2*np.pi*f*t)
            
            # Update bookmarks
            self.lastT = newT
            self.lastF = newF
        else:
            
            output_items[0][:] = input_items[0] * 0;
            if self.over:
                print("Locally Chirped at "+time.strftime("%H:%M:%S"))
                os.system("python3 ionogrammer.py"
                          +" -p "+str(self.filename)
                          +" -P "+str(self.slope)
                          +" -B "+str(self.fs)
                          +" -C "+str(self.fc)
                          +" -d "+str(self.decimation))
                self.over = False
            
        return len(output_items[0]) # GNU radio boilerplate
