"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
import pmt
from gnuradio import gr


class blk(gr.sync_block):  # other base classes are basic_block, decim_block, interp_block
    """Embedded Python Block example - a simple multiply const"""

    def __init__(self, slope=100e3, samp_rate=200e6/12):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.sync_block.__init__(
            self,
            name='Local Chirp Test',   # will show up in GRC
            in_sig=[np.complex64],
            out_sig=[np.complex64]
        )
        # if an attribute with the same name as a parameter is found,
        # a callback is registered (properties work, too).
        self.slope = slope
        self.fs = samp_rate
        self.sample_count = 0
        
        self.lastT = 0
        self.lastF = -400e3
        self.dt = 1/self.fs
        self.df = self.slope/self.fs
        
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
        n = len(input_items[0]) 
    
        if self.lastT <= 4 & self.control:
            newT = self.dt*n + self.lastT
            newF = self.df*n + self.lastF
                
            t = np.arange(self.lastT, newT+self.dt, self.dt)
            f = np.arange(self.lastF, newF+self.df, self.df)
            
            for i in range(0, n):
                output_items[0][i] = np.cos(2*np.pi*f[i]*t[i]) + 1j*np.sin(2*np.pi*f[i]*t[i]) 
            
            self.lastT = newT
            self.lastF = newF
            
        else:
            output_items[0][:] = input_items[0] * 0;
        
        return len(output_items[0])
