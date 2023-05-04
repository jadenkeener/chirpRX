"""TimerTrigger_epy_block_0.py
Last Edited 5/4/24
By Jaden Keener and the NMT Dev Team

First custom block of the ChirpRX DSP chain.
Creates a local timer that records a received Ionosonde signal. 
Timer length and recording window are specified by user input parameters.

Calls LocalChirp.py after recording is complete.
"""

# Imports
import numpy as np
from gnuradio import gr
import pmt
import time
import datetime 
import os

""" blk definition
This is the standard block class declaration for use in gnu radio. 
This file is one custom block in the larger TimerTrigger.py flowchart

See gnu radio 'custom py block' documentation for further explanation.
"""
class blk(gr.basic_block):  
    
    def __init__(
        self, 
        hour=0, 
        min=0, 
        sec=0, 
        capture_window = 10, 
        ionosonde_period = 12, 
        samp_rate=12.5E6, 
        slope = 100E3, 
        decimation=5e3, 
        fc=14.25E6):  
    
        gr.basic_block.__init__(
            self,
            name='Timer Trigger 1.1',  
            in_sig=[np.complex64],
            out_sig=None
        )
        
        """ Add parameters to class instance """
        self.hour = hour
        self.min = min
        self.sec = sec
        self.capture_window = capture_window
        self.iono_per = ionosonde_period
        self.samp_rate = samp_rate
        self.slope = slope
        self.decimation = decimation
        self.fc = fc

        """ Calculate inital timer start time
        This is the first time the timer will trigger.  We must convert
        the HH:MM:SS user input to the correct unix time.  Assumes that the
        time given is today.
        
        If the time given is in the past, forward calculate to the next future
        time based on the given period.
        """
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
        
        # Set a writing flag
        self.writing = False
        
    
    """ work function
    Standard declaration for gnu radio work function.  This is the function
    that is called whenever gnu radio has samples for this block to process.  
    
    This function is not called for every sample individually, but is instead
    fed large batches of samples at once.
    """
    def general_work(self, input_items, output_items):
    
        """ Wait and write
        This if/elif statement controls the timer and data capture. 
        If the writing flag is true, then we write whatever samples we have 
        gathered to disk and check if time is up. If time is up, then close the
        file and call LocalChirp.py
        
        If the writing flag isnt active, we check to see if we the timer has
        'gone off' and we should set it to true.
        """
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
        
        
        self.consume(0, len(input_items[0]))  # GNU radio boilerplate
        return 0                              # GNU radio boilerplate

