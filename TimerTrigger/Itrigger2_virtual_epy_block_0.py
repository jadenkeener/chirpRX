"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
from gnuradio import gr
import pmt
import time
import datetime 


class blk(gr.basic_block):  # other base classes are basic_block, decim_block, interp_block
    """Embedded Python Block example - a simple multiply const"""
    
    def __init__(self, hour=0, min=0, sec=0, capture_window = 10, ionosonde_period = 12):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.basic_block.__init__(
            self,
            name='Real Timer Trigger',   # will show up in GRC
            in_sig=[np.complex64],
            out_sig=None
        )
        # if an attribute with the same name as a parameter is found,
        # a callback is registered (properties work, too).
        self.hour = hour
        self.min = min
        self.sec = sec
        self.capture_window = capture_window
        self.iono_per = ionosonde_period
        #self.portName_fileName = 'File Name'
        #self.message_port_register_out(pmt.intern(self.portName_fileName))
        
        # Calculate start time in unix
        timeTuple = time.localtime()
        timeList = list(timeTuple)
        timeList[3] = self.hour
        timeList[4] = self.min
        timeList[5] = self.sec
        timeTuple = tuple(timeList)
        self.startTime = time.mktime(timeTuple)
        self.writing = False
        
    def general_work(self, input_items, output_items):
        if self.writing:
            #self.file.write(input_items[0][:])
            if time.time() >= self.startTime + self.capture_window:
                self.writing = False
                #self.file.close()
                self.startTime = time.time() + self.iono_per*60-self.capture_window
                print("Stop Writing")
        elif time.time() >= self.startTime:
            self.writing = True
            #self.filename = '{date:%Y%m%d_%H%M%S}.chirp'.format(date=datetime.datetime.now())
            print("Writing")
            #self.file = open(self.filename, "ab")
            #self.file.write(input_items[0][:])
        
        
        self.consume(0, len(input_items[0]))
        return 0

        
        