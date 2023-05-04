"""
Real Timer Trigger
"""

import numpy as np
from gnuradio import gr
import pmt
import time
import datetime 
import os



class blk(gr.basic_block):  
    
    def __init__(self, hour=0, min=0, sec=0, capture_window = 10, ionosonde_period = 12, samp_rate=12.5E6, slope = 100E3, decimation=5e3, fc=14.25E6):  # only default arguments here
        gr.basic_block.__init__(
            self,
            name='Timer Trigger 1.1',   # will show up in GRC
            in_sig=[np.complex64],
            out_sig=None
        )
     
        self.hour = hour
        self.min = min
        self.sec = sec
        self.capture_window = capture_window
        self.iono_per = ionosonde_period
        self.samp_rate = samp_rate
        self.slope = slope
        self.decimation = decimation
        self.fc = fc

        
        # Calculate start time in unix
        timeTuple = time.localtime()
        timeList = list(timeTuple)
        timeList[3] = self.hour
        timeList[4] = self.min
        timeList[5] = self.sec
        timeTuple = tuple(timeList)
        self.startTime = time.mktime(timeTuple)
        
        # Make sure we are in the present
        while self.startTime <= time.time():
            self.startTime = self.startTime + self.iono_per*60
        
        self.writing = False
        
        
    def general_work(self, input_items, output_items):
        if self.writing:
            self.file.write(input_items[0][:])
            if time.time() >= self.startTime + self.capture_window:
                self.writing = False
                self.file.close()
                self.startTime = time.time() + self.iono_per*60-self.capture_window
                print("Stop Writing, Running LocalChirp")
                os.system("python3 LocalChirp.py"
                          +" -P "+str(self.filename)
                          +" -W "+str(self.capture_window)
                          +" -D "+str(self.decimation)
                          +" -M "+str(self.slope)
                          +" -C "+str(self.fc)
                          +" -B "+str(self.samp_rate))
                
                
        elif time.time() >= self.startTime:
            self.writing = True
            self.filename = '{date:%Y%m%d_%H%M%S}.RAW'.format(date=datetime.datetime.now())
            print("Writing to "+self.filename)
            self.file = open(self.filename, "ab")
            self.file.write(input_items[0][:])
        
        
        self.consume(0, len(input_items[0]))
        return 0

