#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: localChirp
# Author: Jaden Keener
# GNU Radio version: 3.10.5.0

from gnuradio import blocks
import pmt
from gnuradio import filter
from gnuradio.filter import firdes
from gnuradio import gr
from gnuradio.fft import window
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
import LocalChirp_epy_block_1 as epy_block_1  # embedded python block




class LocalChirp(gr.top_block):

    def __init__(self, decimation=9000, fc=14.25E6, length=150, path='None', samp_rate=12.5e6, slope=100E3):
        gr.top_block.__init__(self, "localChirp", catch_exceptions=True)

        ##################################################
        # Parameters
        ##################################################
        self.decimation = decimation
        self.fc = fc
        self.length = length
        self.path = path
        self.samp_rate = samp_rate
        self.slope = slope

        ##################################################
        # Variables
        ##################################################
        self.filt_cutoff = filt_cutoff = samp_rate/decimation*0.8
        self.outfile = outfile = path.split(".")[0] + ".chirp"
        self.filt_transwidth = filt_transwidth = (samp_rate/decimation - filt_cutoff) *2
        self.fftsz = fftsz = 4096

        ##################################################
        # Blocks
        ##################################################
        self.filter_fft_low_pass_filter_0 = filter.fft_filter_ccc(decimation, firdes.low_pass(1, samp_rate, filt_cutoff, filt_transwidth, window.WIN_HAMMING, 6.76), 8)
        self.epy_block_1 = epy_block_1.blk(slope=slope, samp_rate=samp_rate, offset=0, filename=outfile, decimation=decimation, fc=fc)
        self.blocks_throttle_0 = blocks.throttle(gr.sizeof_gr_complex*1, samp_rate,True)
        self.blocks_multiply_conjugate_cc_0 = blocks.multiply_conjugate_cc(1)
        self.blocks_head_0 = blocks.head(gr.sizeof_gr_complex*1, (int(samp_rate*length)))
        self.blocks_file_source_0 = blocks.file_source(gr.sizeof_gr_complex*1, path, False, 0, 0)
        self.blocks_file_source_0.set_begin_tag(pmt.PMT_NIL)
        self.blocks_file_sink_0 = blocks.file_sink(gr.sizeof_gr_complex*1, outfile, False)
        self.blocks_file_sink_0.set_unbuffered(False)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_file_source_0, 0), (self.blocks_throttle_0, 0))
        self.connect((self.blocks_head_0, 0), (self.blocks_multiply_conjugate_cc_0, 1))
        self.connect((self.blocks_head_0, 0), (self.epy_block_1, 0))
        self.connect((self.blocks_multiply_conjugate_cc_0, 0), (self.filter_fft_low_pass_filter_0, 0))
        self.connect((self.blocks_throttle_0, 0), (self.blocks_head_0, 0))
        self.connect((self.epy_block_1, 0), (self.blocks_multiply_conjugate_cc_0, 0))
        self.connect((self.filter_fft_low_pass_filter_0, 0), (self.blocks_file_sink_0, 0))


    def get_decimation(self):
        return self.decimation

    def set_decimation(self, decimation):
        self.decimation = decimation
        self.set_filt_cutoff(self.samp_rate/self.decimation*0.8)
        self.set_filt_transwidth((self.samp_rate/self.decimation - self.filt_cutoff) *2)
        self.epy_block_1.decimation = self.decimation

    def get_fc(self):
        return self.fc

    def set_fc(self, fc):
        self.fc = fc
        self.epy_block_1.fc = self.fc

    def get_length(self):
        return self.length

    def set_length(self, length):
        self.length = length
        self.blocks_head_0.set_length((int(self.samp_rate*self.length)))

    def get_path(self):
        return self.path

    def set_path(self, path):
        self.path = path
        self.blocks_file_source_0.open(self.path, False)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.set_filt_cutoff(self.samp_rate/self.decimation*0.8)
        self.set_filt_transwidth((self.samp_rate/self.decimation - self.filt_cutoff) *2)
        self.blocks_head_0.set_length((int(self.samp_rate*self.length)))
        self.blocks_throttle_0.set_sample_rate(self.samp_rate)
        self.filter_fft_low_pass_filter_0.set_taps(firdes.low_pass(1, self.samp_rate, self.filt_cutoff, self.filt_transwidth, window.WIN_HAMMING, 6.76))

    def get_slope(self):
        return self.slope

    def set_slope(self, slope):
        self.slope = slope
        self.epy_block_1.slope = self.slope

    def get_filt_cutoff(self):
        return self.filt_cutoff

    def set_filt_cutoff(self, filt_cutoff):
        self.filt_cutoff = filt_cutoff
        self.set_filt_transwidth((self.samp_rate/self.decimation - self.filt_cutoff) *2)
        self.filter_fft_low_pass_filter_0.set_taps(firdes.low_pass(1, self.samp_rate, self.filt_cutoff, self.filt_transwidth, window.WIN_HAMMING, 6.76))

    def get_outfile(self):
        return self.outfile

    def set_outfile(self, outfile):
        self.outfile = outfile
        self.blocks_file_sink_0.open(self.outfile)
        self.epy_block_1.filename = self.outfile

    def get_filt_transwidth(self):
        return self.filt_transwidth

    def set_filt_transwidth(self, filt_transwidth):
        self.filt_transwidth = filt_transwidth
        self.filter_fft_low_pass_filter_0.set_taps(firdes.low_pass(1, self.samp_rate, self.filt_cutoff, self.filt_transwidth, window.WIN_HAMMING, 6.76))

    def get_fftsz(self):
        return self.fftsz

    def set_fftsz(self, fftsz):
        self.fftsz = fftsz



def argument_parser():
    parser = ArgumentParser()
    parser.add_argument(
        "-D", "--decimation", dest="decimation", type=intx, default=9000,
        help="Set Decimation [default=%(default)r]")
    parser.add_argument(
        "-C", "--fc", dest="fc", type=eng_float, default=eng_notation.num_to_str(float(14.25E6)),
        help="Set fc [default=%(default)r]")
    parser.add_argument(
        "-W", "--length", dest="length", type=eng_float, default=eng_notation.num_to_str(float(150)),
        help="Set Capture Length (s) [default=%(default)r]")
    parser.add_argument(
        "-P", "--path", dest="path", type=str, default='None',
        help="Set File Path [default=%(default)r]")
    parser.add_argument(
        "-B", "--samp-rate", dest="samp_rate", type=eng_float, default=eng_notation.num_to_str(float(12.5e6)),
        help="Set Sample Rate [default=%(default)r]")
    parser.add_argument(
        "-M", "--slope", dest="slope", type=eng_float, default=eng_notation.num_to_str(float(100E3)),
        help="Set Ionosodne Slope [default=%(default)r]")
    return parser


def main(top_block_cls=LocalChirp, options=None):
    if options is None:
        options = argument_parser().parse_args()
    tb = top_block_cls(decimation=options.decimation, fc=options.fc, length=options.length, path=options.path, samp_rate=options.samp_rate, slope=options.slope)

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        sys.exit(0)

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    tb.start()

    tb.wait()


if __name__ == '__main__':
    main()
