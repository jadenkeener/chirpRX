#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Trigger Virtual
# GNU Radio version: 3.10.5.0

from packaging.version import Version as StrictVersion

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print("Warning: failed to XInitThreads()")

from PyQt5 import Qt
from gnuradio import qtgui
import sip
from gnuradio import analog
from gnuradio import blocks
from gnuradio import gr
from gnuradio.filter import firdes
from gnuradio.fft import window
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio.fft import logpwrfft
from gnuradio.qtgui import Range, RangeWidget
from PyQt5 import QtCore
import Itrigger2_virtual_epy_block_1 as epy_block_1  # embedded python block
import math



from gnuradio import qtgui

class Itrigger2_virtual(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Trigger Virtual", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Trigger Virtual")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "Itrigger2_virtual")

        try:
            if StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
                self.restoreGeometry(self.settings.value("geometry").toByteArray())
            else:
                self.restoreGeometry(self.settings.value("geometry"))
        except:
            pass

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 200e6/16
        self.filt_low = filt_low = 9e6
        self.filt_high = filt_high = 9.1e6
        self.fftsz = fftsz = 1024
        self.fc = fc = 14.25e6
        self.movavg_length = movavg_length = 10
        self.freq = freq = 1e3
        self.bin_low = bin_low = int((filt_low-(fc-samp_rate/2))/samp_rate*fftsz)
        self.bin_high = bin_high = int((filt_high-(fc-samp_rate/2))/samp_rate*fftsz)

        ##################################################
        # Blocks
        ##################################################
        self.qtgui_vector_sink_f_1_0 = qtgui.vector_sink_f(
            fftsz,
            0,
            1.0,
            "x-Axis",
            "y-Axis",
            "Super avg",
            1, # Number of inputs
            None # parent
        )
        self.qtgui_vector_sink_f_1_0.set_update_time(0.10)
        self.qtgui_vector_sink_f_1_0.set_y_axis((-140), 10)
        self.qtgui_vector_sink_f_1_0.enable_autoscale(False)
        self.qtgui_vector_sink_f_1_0.enable_grid(False)
        self.qtgui_vector_sink_f_1_0.set_x_axis_units("")
        self.qtgui_vector_sink_f_1_0.set_y_axis_units("")
        self.qtgui_vector_sink_f_1_0.set_ref_level(0)


        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_vector_sink_f_1_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_vector_sink_f_1_0.set_line_label(i, labels[i])
            self.qtgui_vector_sink_f_1_0.set_line_width(i, widths[i])
            self.qtgui_vector_sink_f_1_0.set_line_color(i, colors[i])
            self.qtgui_vector_sink_f_1_0.set_line_alpha(i, alphas[i])

        self._qtgui_vector_sink_f_1_0_win = sip.wrapinstance(self.qtgui_vector_sink_f_1_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_vector_sink_f_1_0_win)
        self.qtgui_vector_sink_f_1 = qtgui.vector_sink_f(
            fftsz,
            0,
            1.0,
            "x-Axis",
            "y-Axis",
            "Avg",
            1, # Number of inputs
            None # parent
        )
        self.qtgui_vector_sink_f_1.set_update_time(0.10)
        self.qtgui_vector_sink_f_1.set_y_axis((-140), 10)
        self.qtgui_vector_sink_f_1.enable_autoscale(False)
        self.qtgui_vector_sink_f_1.enable_grid(False)
        self.qtgui_vector_sink_f_1.set_x_axis_units("")
        self.qtgui_vector_sink_f_1.set_y_axis_units("")
        self.qtgui_vector_sink_f_1.set_ref_level(0)


        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_vector_sink_f_1.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_vector_sink_f_1.set_line_label(i, labels[i])
            self.qtgui_vector_sink_f_1.set_line_width(i, widths[i])
            self.qtgui_vector_sink_f_1.set_line_color(i, colors[i])
            self.qtgui_vector_sink_f_1.set_line_alpha(i, alphas[i])

        self._qtgui_vector_sink_f_1_win = sip.wrapinstance(self.qtgui_vector_sink_f_1.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_vector_sink_f_1_win)
        self.qtgui_vector_sink_f_0_0 = qtgui.vector_sink_f(
            1024,
            0,
            1.0,
            "x-Axis",
            "y-Axis",
            "Filter",
            1, # Number of inputs
            None # parent
        )
        self.qtgui_vector_sink_f_0_0.set_update_time(0.10)
        self.qtgui_vector_sink_f_0_0.set_y_axis((-140), 10)
        self.qtgui_vector_sink_f_0_0.enable_autoscale(False)
        self.qtgui_vector_sink_f_0_0.enable_grid(False)
        self.qtgui_vector_sink_f_0_0.set_x_axis_units("")
        self.qtgui_vector_sink_f_0_0.set_y_axis_units("")
        self.qtgui_vector_sink_f_0_0.set_ref_level(0)


        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_vector_sink_f_0_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_vector_sink_f_0_0.set_line_label(i, labels[i])
            self.qtgui_vector_sink_f_0_0.set_line_width(i, widths[i])
            self.qtgui_vector_sink_f_0_0.set_line_color(i, colors[i])
            self.qtgui_vector_sink_f_0_0.set_line_alpha(i, alphas[i])

        self._qtgui_vector_sink_f_0_0_win = sip.wrapinstance(self.qtgui_vector_sink_f_0_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_vector_sink_f_0_0_win)
        self.qtgui_vector_sink_f_0 = qtgui.vector_sink_f(
            1024,
            0,
            1.0,
            "x-Axis",
            "y-Axis",
            "",
            1, # Number of inputs
            None # parent
        )
        self.qtgui_vector_sink_f_0.set_update_time(0.10)
        self.qtgui_vector_sink_f_0.set_y_axis((-140), 10)
        self.qtgui_vector_sink_f_0.enable_autoscale(False)
        self.qtgui_vector_sink_f_0.enable_grid(False)
        self.qtgui_vector_sink_f_0.set_x_axis_units("")
        self.qtgui_vector_sink_f_0.set_y_axis_units("")
        self.qtgui_vector_sink_f_0.set_ref_level(0)


        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_vector_sink_f_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_vector_sink_f_0.set_line_label(i, labels[i])
            self.qtgui_vector_sink_f_0.set_line_width(i, widths[i])
            self.qtgui_vector_sink_f_0.set_line_color(i, colors[i])
            self.qtgui_vector_sink_f_0.set_line_alpha(i, alphas[i])

        self._qtgui_vector_sink_f_0_win = sip.wrapinstance(self.qtgui_vector_sink_f_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_vector_sink_f_0_win)
        self.logpwrfft_x_0 = logpwrfft.logpwrfft_c(
            sample_rate=samp_rate,
            fft_size=fftsz,
            ref_scale=2,
            frame_rate=30,
            avg_alpha=1.0,
            average=False,
            shift=True)
        self._freq_range = Range(-samp_rate/2, samp_rate/2, 100, 1e3, 200)
        self._freq_win = RangeWidget(self._freq_range, self.set_freq, "Frequency", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._freq_win)
        self.epy_block_1 = epy_block_1.blk(slope=100e3, samp_rate=samp_rate, offset=0)
        self.blocks_throttle_0_0 = blocks.throttle(gr.sizeof_gr_complex*1, samp_rate,True)
        self.blocks_moving_average_xx_0_0 = blocks.moving_average_ff((movavg_length*10), (1/(movavg_length*10)), 4000, fftsz)
        self.blocks_moving_average_xx_0 = blocks.moving_average_ff(movavg_length, (1/movavg_length), 4000, fftsz)
        self.blocks_add_const_vxx_0 = blocks.add_const_vff((-1e16,)*bin_low+(0,)*(bin_high-bin_low)+(-1e6,)*(fftsz-bin_high))
        self.analog_sig_source_x_0 = analog.sig_source_c(samp_rate, analog.GR_COS_WAVE, 500e3, 1, 0, 0)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_sig_source_x_0, 0), (self.blocks_throttle_0_0, 0))
        self.connect((self.blocks_add_const_vxx_0, 0), (self.blocks_moving_average_xx_0, 0))
        self.connect((self.blocks_add_const_vxx_0, 0), (self.qtgui_vector_sink_f_0_0, 0))
        self.connect((self.blocks_moving_average_xx_0, 0), (self.blocks_moving_average_xx_0_0, 0))
        self.connect((self.blocks_moving_average_xx_0, 0), (self.qtgui_vector_sink_f_1, 0))
        self.connect((self.blocks_moving_average_xx_0_0, 0), (self.qtgui_vector_sink_f_1_0, 0))
        self.connect((self.blocks_throttle_0_0, 0), (self.epy_block_1, 0))
        self.connect((self.epy_block_1, 0), (self.logpwrfft_x_0, 0))
        self.connect((self.logpwrfft_x_0, 0), (self.blocks_add_const_vxx_0, 0))
        self.connect((self.logpwrfft_x_0, 0), (self.qtgui_vector_sink_f_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "Itrigger2_virtual")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.set_bin_high(int((self.filt_high-(self.fc-self.samp_rate/2))/self.samp_rate*self.fftsz))
        self.set_bin_low(int((self.filt_low-(self.fc-self.samp_rate/2))/self.samp_rate*self.fftsz))
        self.analog_sig_source_x_0.set_sampling_freq(self.samp_rate)
        self.blocks_throttle_0_0.set_sample_rate(self.samp_rate)
        self.logpwrfft_x_0.set_sample_rate(self.samp_rate)

    def get_filt_low(self):
        return self.filt_low

    def set_filt_low(self, filt_low):
        self.filt_low = filt_low
        self.set_bin_low(int((self.filt_low-(self.fc-self.samp_rate/2))/self.samp_rate*self.fftsz))

    def get_filt_high(self):
        return self.filt_high

    def set_filt_high(self, filt_high):
        self.filt_high = filt_high
        self.set_bin_high(int((self.filt_high-(self.fc-self.samp_rate/2))/self.samp_rate*self.fftsz))

    def get_fftsz(self):
        return self.fftsz

    def set_fftsz(self, fftsz):
        self.fftsz = fftsz
        self.set_bin_high(int((self.filt_high-(self.fc-self.samp_rate/2))/self.samp_rate*self.fftsz))
        self.set_bin_low(int((self.filt_low-(self.fc-self.samp_rate/2))/self.samp_rate*self.fftsz))
        self.blocks_add_const_vxx_0.set_k((-1e16,)*self.bin_low+(0,)*(self.bin_high-self.bin_low)+(-1e6,)*(self.fftsz-self.bin_high))

    def get_fc(self):
        return self.fc

    def set_fc(self, fc):
        self.fc = fc
        self.set_bin_high(int((self.filt_high-(self.fc-self.samp_rate/2))/self.samp_rate*self.fftsz))
        self.set_bin_low(int((self.filt_low-(self.fc-self.samp_rate/2))/self.samp_rate*self.fftsz))

    def get_movavg_length(self):
        return self.movavg_length

    def set_movavg_length(self, movavg_length):
        self.movavg_length = movavg_length
        self.blocks_moving_average_xx_0.set_length_and_scale(self.movavg_length, (1/self.movavg_length))
        self.blocks_moving_average_xx_0_0.set_length_and_scale((self.movavg_length*10), (1/(self.movavg_length*10)))

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq

    def get_bin_low(self):
        return self.bin_low

    def set_bin_low(self, bin_low):
        self.bin_low = bin_low
        self.blocks_add_const_vxx_0.set_k((-1e16,)*self.bin_low+(0,)*(self.bin_high-self.bin_low)+(-1e6,)*(self.fftsz-self.bin_high))

    def get_bin_high(self):
        return self.bin_high

    def set_bin_high(self, bin_high):
        self.bin_high = bin_high
        self.blocks_add_const_vxx_0.set_k((-1e16,)*self.bin_low+(0,)*(self.bin_high-self.bin_low)+(-1e6,)*(self.fftsz-self.bin_high))




def main(top_block_cls=Itrigger2_virtual, options=None):

    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()

    tb.show()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    qapp.exec_()

if __name__ == '__main__':
    main()
