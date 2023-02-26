"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
import math
from gnuradio import gr


class blk(gr.sync_block):  # other base classes are basic_block, decim_block, interp_block
    """Embedded Python Block example - a simple multiply const"""

    def __init__(self, FFT_size=1024, sample_rate=25E6, frequency_low=10.9e6,
                frequency_high=11.1e6):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.sync_block.__init__(
            self,
            name='Selective FFT Vector Averager',   # will show up in GRC
            in_sig=[(np.float32,FFT_size)],
            out_sig=[np.float32]
        )
        # if an attribute with the same name as a parameter is found,
        # a callback is registered (properties work, too).
        self.FFT_size = FFT_size
        self.sample_rate = sample_rate
        self.frequency_low = frequency_low+sample_rate/2
        self.frequency_high = frequency_high+sample_rate/2
        
        # Calculate the bins we are interested in sampling
        self.bin_width = (self.sample_rate)/self.FFT_size
        self.bin_low = math.floor(self.frequency_low/self.bin_width)
        self.bin_high = math.floor(self.frequency_high/self.bin_width)
        print("tesT")

    def work(self, input_items, output_items):
        # Loop through all received vectors
        print("Input: ", len(input_items[0]))
        for i in range(len(input_items[0])):
            output_items[0][i] = input_items[0][i][self.bin_low:self.bin_high].mean()
        print("Output: ", len(output_items[0]))
        print("-----------------------")
        return len(output_items[0])
