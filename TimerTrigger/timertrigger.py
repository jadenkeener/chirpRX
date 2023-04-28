#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Timer Trigger
# Author: Jaden Keener
# GNU Radio version: 3.10.5.0

from gnuradio import gr
from gnuradio.filter import firdes
from gnuradio.fft import window
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import uhd
import time
import timertrigger_epy_block_0 as epy_block_0  # embedded python block




class timertrigger(gr.top_block):

    def __init__(self, freq_offset=0, hour=0, iono_per=12, iono_window=150, minute=0, second=0):
        gr.top_block.__init__(self, "Timer Trigger", catch_exceptions=True)

        ##################################################
        # Parameters
        ##################################################
        self.freq_offset = freq_offset
        self.hour = hour
        self.iono_per = iono_per
        self.iono_window = iono_window
        self.minute = minute
        self.second = second

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 200e6/16
        self.fc = fc = 8e6+samp_rate/2

        ##################################################
        # Blocks
        ##################################################
        self.uhd_usrp_source_0 = uhd.usrp_source(
            ",".join(("", '')),
            uhd.stream_args(
                cpu_format="fc32",
                args='',
                channels=list(range(0,1)),
            ),
        )
        self.uhd_usrp_source_0.set_samp_rate(samp_rate)
        self.uhd_usrp_source_0.set_time_now(uhd.time_spec(time.time()), uhd.ALL_MBOARDS)

        self.uhd_usrp_source_0.set_center_freq(fc, 0)
        self.uhd_usrp_source_0.set_antenna('B', 0)
        self.uhd_usrp_source_0.set_bandwidth(samp_rate, 0)
        self.uhd_usrp_source_0.set_gain(50, 0)
        self.epy_block_0 = epy_block_0.blk(hour=hour, min=minute, sec=second, capture_window=iono_window, ionosonde_period=iono_per, samp_rate=samp_rate)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.uhd_usrp_source_0, 0), (self.epy_block_0, 0))


    def get_freq_offset(self):
        return self.freq_offset

    def set_freq_offset(self, freq_offset):
        self.freq_offset = freq_offset

    def get_hour(self):
        return self.hour

    def set_hour(self, hour):
        self.hour = hour
        self.epy_block_0.hour = self.hour

    def get_iono_per(self):
        return self.iono_per

    def set_iono_per(self, iono_per):
        self.iono_per = iono_per

    def get_iono_window(self):
        return self.iono_window

    def set_iono_window(self, iono_window):
        self.iono_window = iono_window
        self.epy_block_0.capture_window = self.iono_window

    def get_minute(self):
        return self.minute

    def set_minute(self, minute):
        self.minute = minute
        self.epy_block_0.min = self.minute

    def get_second(self):
        return self.second

    def set_second(self, second):
        self.second = second
        self.epy_block_0.sec = self.second

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.set_fc(8e6+self.samp_rate/2)
        self.epy_block_0.samp_rate = self.samp_rate
        self.uhd_usrp_source_0.set_samp_rate(self.samp_rate)
        self.uhd_usrp_source_0.set_bandwidth(self.samp_rate, 0)

    def get_fc(self):
        return self.fc

    def set_fc(self, fc):
        self.fc = fc
        self.uhd_usrp_source_0.set_center_freq(self.fc, 0)



def argument_parser():
    parser = ArgumentParser()
    parser.add_argument(
        "-O", "--freq-offset", dest="freq_offset", type=eng_float, default=eng_notation.num_to_str(float(0)),
        help="Set Frequency Offset [default=%(default)r]")
    parser.add_argument(
        "-H", "--hour", dest="hour", type=intx, default=0,
        help="Set Hour for trigger [default=%(default)r]")
    parser.add_argument(
        "-T", "--iono-per", dest="iono_per", type=intx, default=12,
        help="Set Ionosonde Period (in M) [default=%(default)r]")
    parser.add_argument(
        "-w", "--iono-window", dest="iono_window", type=intx, default=150,
        help="Set Ionosonde Capture Window (s) [default=%(default)r]")
    parser.add_argument(
        "-M", "--minute", dest="minute", type=intx, default=0,
        help="Set Minute for trigger [default=%(default)r]")
    parser.add_argument(
        "-S", "--second", dest="second", type=intx, default=0,
        help="Set Second for trigger [default=%(default)r]")
    return parser


def main(top_block_cls=timertrigger, options=None):
    if options is None:
        options = argument_parser().parse_args()
    tb = top_block_cls(freq_offset=options.freq_offset, hour=options.hour, iono_per=options.iono_per, iono_window=options.iono_window, minute=options.minute, second=options.second)

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        sys.exit(0)

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    tb.start()

    try:
        input('Press Enter to quit: ')
    except EOFError:
        pass
    tb.stop()
    tb.wait()


if __name__ == '__main__':
    main()
