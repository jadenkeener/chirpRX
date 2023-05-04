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

    def __init__(self, decimation=5000, fc=14.25E6, fs=12.5E6, hour=0, iono_per=12, minute=0, second=0, slope=100E3):
        gr.top_block.__init__(self, "Timer Trigger", catch_exceptions=True)

        ##################################################
        # Parameters
        ##################################################
        self.decimation = decimation
        self.fc = fc
        self.fs = fs
        self.hour = hour
        self.iono_per = iono_per
        self.minute = minute
        self.second = second
        self.slope = slope

        ##################################################
        # Variables
        ##################################################
        self.iono_window = iono_window = fs/slope + 30

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
        self.uhd_usrp_source_0.set_samp_rate(fs)
        self.uhd_usrp_source_0.set_time_now(uhd.time_spec(time.time()), uhd.ALL_MBOARDS)

        self.uhd_usrp_source_0.set_center_freq(fc, 0)
        self.uhd_usrp_source_0.set_antenna('B', 0)
        self.uhd_usrp_source_0.set_bandwidth(fs, 0)
        self.uhd_usrp_source_0.set_gain(50, 0)
        self.epy_block_0 = epy_block_0.blk(hour=hour, min=minute, sec=second, capture_window=iono_window, ionosonde_period=iono_per, samp_rate=fs, slope=slope, decimation=decimation, fc=fc)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.uhd_usrp_source_0, 0), (self.epy_block_0, 0))


    def get_decimation(self):
        return self.decimation

    def set_decimation(self, decimation):
        self.decimation = decimation
        self.epy_block_0.decimation = self.decimation

    def get_fc(self):
        return self.fc

    def set_fc(self, fc):
        self.fc = fc
        self.epy_block_0.fc = self.fc
        self.uhd_usrp_source_0.set_center_freq(self.fc, 0)

    def get_fs(self):
        return self.fs

    def set_fs(self, fs):
        self.fs = fs
        self.set_iono_window(self.fs/self.slope + 30)
        self.epy_block_0.samp_rate = self.fs
        self.uhd_usrp_source_0.set_samp_rate(self.fs)
        self.uhd_usrp_source_0.set_bandwidth(self.fs, 0)

    def get_hour(self):
        return self.hour

    def set_hour(self, hour):
        self.hour = hour
        self.epy_block_0.hour = self.hour

    def get_iono_per(self):
        return self.iono_per

    def set_iono_per(self, iono_per):
        self.iono_per = iono_per

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

    def get_slope(self):
        return self.slope

    def set_slope(self, slope):
        self.slope = slope
        self.set_iono_window(self.fs/self.slope + 30)
        self.epy_block_0.slope = self.slope

    def get_iono_window(self):
        return self.iono_window

    def set_iono_window(self, iono_window):
        self.iono_window = iono_window
        self.epy_block_0.capture_window = self.iono_window



def argument_parser():
    parser = ArgumentParser()
    parser.add_argument(
        "-D", "--decimation", dest="decimation", type=intx, default=5000,
        help="Set Decimation [default=%(default)r]")
    parser.add_argument(
        "-C", "--fc", dest="fc", type=eng_float, default=eng_notation.num_to_str(float(14.25E6)),
        help="Set Center Frequency [default=%(default)r]")
    parser.add_argument(
        "-B", "--fs", dest="fs", type=eng_float, default=eng_notation.num_to_str(float(12.5E6)),
        help="Set Sample Frequency [default=%(default)r]")
    parser.add_argument(
        "-H", "--hour", dest="hour", type=intx, default=0,
        help="Set Hour for trigger [default=%(default)r]")
    parser.add_argument(
        "-T", "--iono-per", dest="iono_per", type=eng_float, default=eng_notation.num_to_str(float(12)),
        help="Set Ionosonde Period (in M) [default=%(default)r]")
    parser.add_argument(
        "-M", "--minute", dest="minute", type=intx, default=0,
        help="Set Minute for trigger [default=%(default)r]")
    parser.add_argument(
        "-S", "--second", dest="second", type=intx, default=0,
        help="Set Second for trigger [default=%(default)r]")
    parser.add_argument(
        "-P", "--slope", dest="slope", type=eng_float, default=eng_notation.num_to_str(float(100E3)),
        help="Set Ionosonde Slope [default=%(default)r]")
    return parser


def main(top_block_cls=timertrigger, options=None):
    if options is None:
        options = argument_parser().parse_args()
    tb = top_block_cls(decimation=options.decimation, fc=options.fc, fs=options.fs, hour=options.hour, iono_per=options.iono_per, minute=options.minute, second=options.second, slope=options.slope)

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
