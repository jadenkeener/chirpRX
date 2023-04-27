"""
Local Chirp
By Jaden Keener, Last updated 3/27/23

Generates a local tone that sweeps the spectrum at the specified slope

"""

import numpy as np
import pmt
from gnuradio import gr


class blk(gr.sync_block):  

    def __init__(self, slope=100e3, samp_rate=200e6/12, offset = 10e3):
        gr.sync_block.__init__(
            self,
            name='Local Chirp Test 1.0',   
            in_sig=[np.complex64],
            out_sig=[np.complex64]
        )

        self.slope = slope  
        self.fs = samp_rate
        self.offset = offset
        self.debug = False
        
        self.lastT = 0
        self.lastF = -self.fs/2 + self.offset
        self.spanF = self.lastF + self.fs/2 - self.offset
        self.dt = 1/self.fs
        self.df = self.slope/self.fs/2 #why /2 ?? I have no idea, but it has to be
        # over 2 has something to do with span of f not being -fs/2 to fs/2 but
        # just fs..???
        
        
        self.controlPortName = 'controlIn'
        self.message_port_register_in(pmt.intern(self.controlPortName))
        self.set_msg_handler(pmt.intern(self.controlPortName), self.handle_msg)
        self.control = False
        
            
        
    def handle_msg(self, msg):
        controlIn = pmt.to_bool(msg)
        
        if controlIn > self.controlLast+self.trigger_Power:
            self.control = True
        
        self.controlLast = controlIn
        
    def work(self, input_items, output_items):
    
        # Find number of samples on this call
        n = len(input_items[0]) 

        # If we havent progged the whole spectrum
        if self.lastF <= self.offset/2: # WHY OFFSET/2 ??????????? IDK
        
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
        
        # Otherwise do nothing
        else:
            output_items[0][:] = input_items[0] * 0;
            if self.debug:
                self.debug = False
                raise ValueError(self.lastF)
            
        
        return len(output_items[0])
