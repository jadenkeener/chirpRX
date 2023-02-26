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
from gnuradio.filter import firdes
import sip
from gnuradio import analog
from gnuradio import blocks
from gnuradio import fft
from gnuradio.fft import window
from gnuradio import gr
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio.qtgui import Range, RangeWidget
from PyQt5 import QtCore
import Itrigger2_virtual_epy_block_0 as epy_block_0  # embedded python block
import Itrigger2_virtual_epy_block_1_0 as epy_block_1_0  # embedded python block
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
        self.samp_rate = samp_rate = 32e3
        self.movavg_length = movavg_length = 10000
        self.freq = freq = 1e3
        self.fftsz = fftsz = 1024

        ##################################################
        # Blocks
        ##################################################
        self._freq_range = Range(0, samp_rate/2, 100, 1e3, 200)
        self._freq_win = RangeWidget(self._freq_range, self.set_freq, "Frequency", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._freq_win)
        self.qtgui_time_sink_x_0 = qtgui.time_sink_c(
            1024, #size
            samp_rate, #samp_rate
            "Raw", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_0.set_update_time(0.10)
        self.qtgui_time_sink_x_0.set_y_axis(-1, 1)

        self.qtgui_time_sink_x_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0.enable_tags(True)
        self.qtgui_time_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_0.enable_autoscale(False)
        self.qtgui_time_sink_x_0.enable_grid(False)
        self.qtgui_time_sink_x_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0.enable_control_panel(False)
        self.qtgui_time_sink_x_0.enable_stem_plot(False)


        labels = ['Signal 1', 'Signal 2', 'Signal 3', 'Signal 4', 'Signal 5',
            'Signal 6', 'Signal 7', 'Signal 8', 'Signal 9', 'Signal 10']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['blue', 'red', 'green', 'black', 'cyan',
            'magenta', 'yellow', 'dark red', 'dark green', 'dark blue']
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(2):
            if len(labels[i]) == 0:
                if (i % 2 == 0):
                    self.qtgui_time_sink_x_0.set_line_label(i, "Re{{Data {0}}}".format(i/2))
                else:
                    self.qtgui_time_sink_x_0.set_line_label(i, "Im{{Data {0}}}".format(i/2))
            else:
                self.qtgui_time_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_time_sink_x_0_win)
        self.qtgui_number_sink_1_1_0 = qtgui.number_sink(
            gr.sizeof_float,
            0,
            qtgui.NUM_GRAPH_HORIZ,
            1,
            None # parent
        )
        self.qtgui_number_sink_1_1_0.set_update_time(0.10)
        self.qtgui_number_sink_1_1_0.set_title("Timer")

        labels = ['', '', '', '', '',
            '', '', '', '', '']
        units = ['', '', '', '', '',
            '', '', '', '', '']
        colors = [("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"),
            ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black")]
        factor = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]

        for i in range(1):
            self.qtgui_number_sink_1_1_0.set_min(i, 0)
            self.qtgui_number_sink_1_1_0.set_max(i, 200E3)
            self.qtgui_number_sink_1_1_0.set_color(i, colors[i][0], colors[i][1])
            if len(labels[i]) == 0:
                self.qtgui_number_sink_1_1_0.set_label(i, "Data {0}".format(i))
            else:
                self.qtgui_number_sink_1_1_0.set_label(i, labels[i])
            self.qtgui_number_sink_1_1_0.set_unit(i, units[i])
            self.qtgui_number_sink_1_1_0.set_factor(i, factor[i])

        self.qtgui_number_sink_1_1_0.enable_autoscale(False)
        self._qtgui_number_sink_1_1_0_win = sip.wrapinstance(self.qtgui_number_sink_1_1_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_number_sink_1_1_0_win)
        self.qtgui_number_sink_1_0 = qtgui.number_sink(
            gr.sizeof_float,
            0,
            qtgui.NUM_GRAPH_HORIZ,
            1,
            None # parent
        )
        self.qtgui_number_sink_1_0.set_update_time(0.10)
        self.qtgui_number_sink_1_0.set_title("TrigOut")

        labels = ['', '', '', '', '',
            '', '', '', '', '']
        units = ['', '', '', '', '',
            '', '', '', '', '']
        colors = [("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"),
            ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black")]
        factor = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]

        for i in range(1):
            self.qtgui_number_sink_1_0.set_min(i, -1)
            self.qtgui_number_sink_1_0.set_max(i, 3)
            self.qtgui_number_sink_1_0.set_color(i, colors[i][0], colors[i][1])
            if len(labels[i]) == 0:
                self.qtgui_number_sink_1_0.set_label(i, "Data {0}".format(i))
            else:
                self.qtgui_number_sink_1_0.set_label(i, labels[i])
            self.qtgui_number_sink_1_0.set_unit(i, units[i])
            self.qtgui_number_sink_1_0.set_factor(i, factor[i])

        self.qtgui_number_sink_1_0.enable_autoscale(False)
        self._qtgui_number_sink_1_0_win = sip.wrapinstance(self.qtgui_number_sink_1_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_number_sink_1_0_win)
        self.qtgui_number_sink_0 = qtgui.number_sink(
            gr.sizeof_float,
            0,
            qtgui.NUM_GRAPH_HORIZ,
            1,
            None # parent
        )
        self.qtgui_number_sink_0.set_update_time(1/samp_rate)
        self.qtgui_number_sink_0.set_title("Power")

        labels = ['', '', '', '', '',
            '', '', '', '', '']
        units = ['', '', '', '', '',
            '', '', '', '', '']
        colors = [("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"),
            ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black")]
        factor = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]

        for i in range(1):
            self.qtgui_number_sink_0.set_min(i, -1)
            self.qtgui_number_sink_0.set_max(i, 2)
            self.qtgui_number_sink_0.set_color(i, colors[i][0], colors[i][1])
            if len(labels[i]) == 0:
                self.qtgui_number_sink_0.set_label(i, "Data {0}".format(i))
            else:
                self.qtgui_number_sink_0.set_label(i, labels[i])
            self.qtgui_number_sink_0.set_unit(i, units[i])
            self.qtgui_number_sink_0.set_factor(i, factor[i])

        self.qtgui_number_sink_0.enable_autoscale(False)
        self._qtgui_number_sink_0_win = sip.wrapinstance(self.qtgui_number_sink_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_number_sink_0_win)
        self._movavg_length_range = Range(1000, 16383, 1, 10000, 200)
        self._movavg_length_win = RangeWidget(self._movavg_length_range, self.set_movavg_length, "Moving Average Length", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._movavg_length_win)
        self.fft_vxx_0 = fft.fft_vcc(fftsz, True, window.blackmanharris(fftsz), True, 1)
        self.epy_block_1_0 = epy_block_1_0.blk(trigger_delta_dB=300, samp_rate=samp_rate, capture_window=10)
        self.epy_block_0 = epy_block_0.blk(FFT_size=fftsz, sample_rate=samp_rate, frequency_low=4.9e3, frequency_high=5.1e3)
        self.blocks_throttle_1 = blocks.throttle(gr.sizeof_float*1, 32,True)
        self.blocks_throttle_0 = blocks.throttle(gr.sizeof_gr_complex*1, samp_rate,True)
        self.blocks_stream_to_vector_0 = blocks.stream_to_vector(gr.sizeof_gr_complex*1, fftsz)
        self.blocks_null_sink_0 = blocks.null_sink(gr.sizeof_float*1)
        self.blocks_nlog10_ff_0_0 = blocks.nlog10_ff(10, fftsz, 0)
        self.blocks_multiply_const_xx_0 = blocks.multiply_const_cc(1/fftsz, 1024)
        self.blocks_complex_to_mag_squared_0_0 = blocks.complex_to_mag_squared(fftsz)
        self.analog_sig_source_x_0 = analog.sig_source_c(samp_rate, analog.GR_COS_WAVE, freq, 1, 0, 0)
        self.analog_const_source_x_0 = analog.sig_source_f(0, analog.GR_CONST_WAVE, 0, 0, 10)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_const_source_x_0, 0), (self.blocks_throttle_1, 0))
        self.connect((self.analog_sig_source_x_0, 0), (self.blocks_throttle_0, 0))
        self.connect((self.blocks_complex_to_mag_squared_0_0, 0), (self.blocks_nlog10_ff_0_0, 0))
        self.connect((self.blocks_multiply_const_xx_0, 0), (self.blocks_complex_to_mag_squared_0_0, 0))
        self.connect((self.blocks_nlog10_ff_0_0, 0), (self.epy_block_0, 0))
        self.connect((self.blocks_stream_to_vector_0, 0), (self.fft_vxx_0, 0))
        self.connect((self.blocks_throttle_0, 0), (self.blocks_stream_to_vector_0, 0))
        self.connect((self.blocks_throttle_0, 0), (self.epy_block_1_0, 1))
        self.connect((self.blocks_throttle_0, 0), (self.qtgui_time_sink_x_0, 0))
        self.connect((self.blocks_throttle_1, 0), (self.epy_block_1_0, 0))
        self.connect((self.blocks_throttle_1, 0), (self.qtgui_number_sink_0, 0))
        self.connect((self.epy_block_0, 0), (self.blocks_null_sink_0, 0))
        self.connect((self.epy_block_1_0, 0), (self.qtgui_number_sink_1_0, 0))
        self.connect((self.epy_block_1_0, 1), (self.qtgui_number_sink_1_1_0, 0))
        self.connect((self.fft_vxx_0, 0), (self.blocks_multiply_const_xx_0, 0))


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
        self.analog_sig_source_x_0.set_sampling_freq(self.samp_rate)
        self.blocks_throttle_0.set_sample_rate(self.samp_rate)
        self.epy_block_0.sample_rate = self.samp_rate
        self.epy_block_1_0.samp_rate = self.samp_rate
        self.qtgui_number_sink_0.set_update_time(1/self.samp_rate)
        self.qtgui_time_sink_x_0.set_samp_rate(self.samp_rate)

    def get_movavg_length(self):
        return self.movavg_length

    def set_movavg_length(self, movavg_length):
        self.movavg_length = movavg_length

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq
        self.analog_sig_source_x_0.set_frequency(self.freq)

    def get_fftsz(self):
        return self.fftsz

    def set_fftsz(self, fftsz):
        self.fftsz = fftsz
        self.blocks_multiply_const_xx_0.set_k(1/self.fftsz)
        self.epy_block_0.FFT_size = self.fftsz




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
