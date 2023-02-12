""" Ionosonde Trigger Block
    By Jaden Keener, 2/5/23
    
    Last updated 2/12/23 12:55
    - Added moving average functionality. Now we shouldn't have to manually set
      trigger threshold
    
    This block records the raw SDR output when a strong enough input is 
    provided. This block is meant to be used alongside a filter. The filter 
    should bandpass the trigger frequency, then go to an average power block
    which then feeds into this blocks first input.
    
    Outputs are purely debug.
    
    See __init__ for additional i/o information
"""

import numpy as np
import datetime
from gnuradio import gr

class blk(gr.sync_block):  

    def __init__(self, trigger_delta_dB=5, samp_rate = 32E3, capture_window = 5): 
        
        """ INPUTS/OUTPUTS:
                input[0]: Signal average power
                input[1]: Raw data from SDR
                input[2]: Moving average of [0]
                
                output[0]: debug state information
                output[1]: debug timer information
            """
        gr.sync_block.__init__(
            self,
            name='Ionosonde Trigger 2.0', 
            in_sig=[np.float32, np.complex64, np.float32],
            out_sig=[np.float32, np.float32]
        )
        
        self.trigger_Power = trigger_delta_dB
        self.samp_rate = samp_rate
        self.capture_window = capture_window
        # timer max is calculated as sample rate * capture window in seconds.
        self.timerMax = self.timer = self.samp_rate * self.capture_window
        self.writing = False
       

    def work(self, input_items, output_items):
        
        self.power_movavg = input_items[2]
        
        # Check if we are writing
        if self.writing:
            # If we are and we still have time on the clock
            if self.timer < self.timerMax:
                # Then write data to file
                self.file.write(input_items[1][:])
                self.timer += len(input_items[1])
                output_items[0][:] = 2
            else:
                # Otherwise close the file and reset flags
                self.file.close()
                self.writing = False
                output_items[0][:] = 0
        
        # If not writing, do we have high power on trigger?
        elif np.any(input_items[0] > self.trigger_Power+self.power_movavg):
            # Set status variables
            self.writing = True
            self.timer = 0
            output_items[0][:] = 1
            
            # Open new file and do first write
            self.filename = '{date:%Y%m%d_%H%M%S}.chirp'.format(date=datetime.datetime.now())
            self.file = open(self.filename, "ab")
            self.file.write(input_items[1][:])
        # Show debug state of none
        else:
            output_items[0][:] = 0
        
        # For debugging timer
        output_items[1][:] = self.timer
        
        # gnuradio needs this return
        return len(output_items[0])
