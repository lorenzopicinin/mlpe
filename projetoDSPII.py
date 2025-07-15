#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Not titled yet
# Author: picinin
# GNU Radio version: 3.10.10.0

from PyQt5 import Qt
from gnuradio import qtgui
from PyQt5 import QtCore
from gnuradio import blocks
from gnuradio import channels
from gnuradio import digital
from gnuradio import filter
from gnuradio.filter import firdes
from gnuradio import gr
from gnuradio.fft import window
import sys
import signal
from PyQt5 import Qt
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
import pmt
import projetoDSPII_epy_block_0 as epy_block_0  # embedded python block
import sip



class projetoDSPII(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Not titled yet", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Not titled yet")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except BaseException as exc:
            print(f"Qt GUI: Could not set Icon: {str(exc)}", file=sys.stderr)
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

        self.settings = Qt.QSettings("GNU Radio", "projetoDSPII")

        try:
            geometry = self.settings.value("geometry")
            if geometry:
                self.restoreGeometry(geometry)
        except BaseException as exc:
            print(f"Qt GUI: Could not restore geometry: {str(exc)}", file=sys.stderr)

        ##################################################
        # Variables
        ##################################################
        self.QAM4 = QAM4 = digital.constellation_calcdist([-1-1j, -1+1j, 1+1j, 1-1j], [0, 1, 2, 3],
        4, 1, digital.constellation.AMPLITUDE_NORMALIZATION).base()
        self.QAM4.set_npwr(1.0)
        self.sym_dly = sym_dly = 0
        self.samp_rate = samp_rate = 32000
        self.preamble = preamble = list(ord(i) for i in "Sequencia de treinamento do preambulo da mensagem...")
        self.message = message = list(ord(i) for i in 'Teste QPSK...')
        self.interp = interp = 10
        self.head = head = gr.tag_utils.python_to_tag((1, pmt.intern("training_start"), pmt.intern("Training Sequence"), pmt.intern("src")))
        self.bb_rate = bb_rate = 5e5
        self.alpha = alpha = 0
        self.alga = alga = digital.adaptive_algorithm_lms( QAM4, .005).base()

        ##################################################
        # Blocks
        ##################################################

        self._sym_dly_range = qtgui.Range(0, 16, 1, 0, 200)
        self._sym_dly_win = qtgui.RangeWidget(self._sym_dly_range, self.set_sym_dly, "'sym_dly'", "counter_slider", int, QtCore.Qt.Horizontal)
        self.top_grid_layout.addWidget(self._sym_dly_win, 0, 1, 1, 1)
        for r in range(0, 1):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(1, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.root_raised_cosine_filter_1_0_0 = filter.fir_filter_ccf(
            interp,
            firdes.root_raised_cosine(
                4,
                (interp*bb_rate),
                bb_rate,
                0.3,
                (2*interp)))
        self.root_raised_cosine_filter_1 = filter.interp_fir_filter_ccf(
            interp,
            firdes.root_raised_cosine(
                4,
                (interp*bb_rate),
                bb_rate,
                0.3,
                (2*interp)))
        self.qtgui_const_sink_x_1_0 = qtgui.const_sink_c(
            1024, #size
            "Saída Equalizador", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_const_sink_x_1_0.set_update_time(0.10)
        self.qtgui_const_sink_x_1_0.set_y_axis((-2), 2)
        self.qtgui_const_sink_x_1_0.set_x_axis((-2), 2)
        self.qtgui_const_sink_x_1_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, "")
        self.qtgui_const_sink_x_1_0.enable_autoscale(False)
        self.qtgui_const_sink_x_1_0.enable_grid(False)
        self.qtgui_const_sink_x_1_0.enable_axis_labels(True)


        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        styles = [0, 0, 0, 0, 0,
            0, 0, 0, 0, 0]
        markers = [0, 0, 0, 0, 0,
            0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_const_sink_x_1_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_const_sink_x_1_0.set_line_label(i, labels[i])
            self.qtgui_const_sink_x_1_0.set_line_width(i, widths[i])
            self.qtgui_const_sink_x_1_0.set_line_color(i, colors[i])
            self.qtgui_const_sink_x_1_0.set_line_style(i, styles[i])
            self.qtgui_const_sink_x_1_0.set_line_marker(i, markers[i])
            self.qtgui_const_sink_x_1_0.set_line_alpha(i, alphas[i])

        self._qtgui_const_sink_x_1_0_win = sip.wrapinstance(self.qtgui_const_sink_x_1_0.qwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_const_sink_x_1_0_win, 2, 0, 1, 1)
        for r in range(2, 3):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_const_sink_x_1 = qtgui.const_sink_c(
            1024, #size
            "Saída do Canal", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_const_sink_x_1.set_update_time(0.10)
        self.qtgui_const_sink_x_1.set_y_axis((-2), 2)
        self.qtgui_const_sink_x_1.set_x_axis((-2), 2)
        self.qtgui_const_sink_x_1.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, "")
        self.qtgui_const_sink_x_1.enable_autoscale(False)
        self.qtgui_const_sink_x_1.enable_grid(False)
        self.qtgui_const_sink_x_1.enable_axis_labels(True)


        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        styles = [0, 0, 0, 0, 0,
            0, 0, 0, 0, 0]
        markers = [0, 0, 0, 0, 0,
            0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_const_sink_x_1.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_const_sink_x_1.set_line_label(i, labels[i])
            self.qtgui_const_sink_x_1.set_line_width(i, widths[i])
            self.qtgui_const_sink_x_1.set_line_color(i, colors[i])
            self.qtgui_const_sink_x_1.set_line_style(i, styles[i])
            self.qtgui_const_sink_x_1.set_line_marker(i, markers[i])
            self.qtgui_const_sink_x_1.set_line_alpha(i, alphas[i])

        self._qtgui_const_sink_x_1_win = sip.wrapinstance(self.qtgui_const_sink_x_1.qwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_const_sink_x_1_win, 1, 1, 1, 1)
        for r in range(1, 2):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(1, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_const_sink_x_0 = qtgui.const_sink_c(
            1024, #size
            'Entrada do Filtro TX', #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_const_sink_x_0.set_update_time(0.10)
        self.qtgui_const_sink_x_0.set_y_axis((-2), 2)
        self.qtgui_const_sink_x_0.set_x_axis((-2), 2)
        self.qtgui_const_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, "")
        self.qtgui_const_sink_x_0.enable_autoscale(False)
        self.qtgui_const_sink_x_0.enable_grid(False)
        self.qtgui_const_sink_x_0.enable_axis_labels(True)


        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "red", "red", "red",
            "red", "red", "red", "red", "red"]
        styles = [0, 0, 0, 0, 0,
            0, 0, 0, 0, 0]
        markers = [0, 0, 0, 0, 0,
            0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_const_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_const_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_const_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_const_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_const_sink_x_0.set_line_style(i, styles[i])
            self.qtgui_const_sink_x_0.set_line_marker(i, markers[i])
            self.qtgui_const_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_const_sink_x_0_win = sip.wrapinstance(self.qtgui_const_sink_x_0.qwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_const_sink_x_0_win, 1, 0, 1, 1)
        for r in range(1, 2):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.epy_block_0 = epy_block_0.blk(training_sequence=[(-1+1j), (-1+1j), (-1-1j), (1-1j), (-1+1j), (1+1j), (-1+1j), (-1+1j), (-1+1j), (1-1j), (-1-1j), (-1+1j), (-1+1j), (1-1j), (-1+1j), (-1+1j), (-1+1j), (1+1j), (-1+1j), (-1+1j), (-1+1j), (1+1j), (1-1j), (1+1j), (-1+1j), (1+1j), (-1-1j), (1-1j), (-1+1j), (1+1j), (1+1j), (-1+1j), (-1+1j), (1+1j), (-1-1j), (-1+1j), (-1-1j), (1+1j), (-1-1j), (-1-1j), (-1+1j), (1+1j), (-1+1j), (-1-1j), (-1+1j), (1+1j), (-1+1j), (-1+1j), (-1-1j), (1+1j), (-1-1j), (-1-1j), (-1+1j), (1-1j), (-1+1j), (-1-1j), (-1+1j), (1-1j), (-1-1j), (1+1j), (-1+1j), (1+1j), (-1+1j), (-1+1j), (-1+1j), (1+1j), (1+1j), (-1+1j), (-1+1j), (1+1j), (1-1j), (1+1j), (-1+1j), (1+1j), (-1-1j), (-1+1j), (-1+1j), (1+1j), (1-1j), (-1+1j), (-1+1j), (1+1j), (-1+1j), (-1+1j), (-1+1j), (1+1j), (1-1j), (1+1j), (-1+1j), (1-1j), (-1+1j), (-1-1j), (-1+1j), (1+1j), (1-1j), (1-1j), (-1-1j), (1+1j), (-1-1j), (-1-1j), (-1+1j), (1+1j), (-1+1j), (-1-1j), (-1+1j), (1+1j), (1-1j), (1-1j), (-1-1j), (1+1j), (-1-1j), (-1-1j), (-1+1j), (1-1j), (-1-1j), (-1-1j), (-1+1j), (1-1j), (-1-1j), (1+1j), (-1+1j), (1+1j), (-1+1j), (-1+1j), (-1+1j), (1+1j), (-1-1j), (-1+1j), (-1+1j), (1+1j), (1-1j), (-1+1j), (-1+1j), (1+1j), (-1-1j), (1+1j), (-1+1j), (1-1j), (-1+1j), (-1+1j), (-1+1j), (1+1j), (1-1j), (-1-1j), (-1+1j), (1+1j), (1-1j), (1-1j), (-1-1j), (1+1j), (-1-1j), (-1-1j), (-1+1j), (1+1j), (-1+1j), (-1-1j), (-1+1j), (1+1j), (-1-1j), (-1+1j), (-1-1j), (1+1j), (-1-1j), (-1-1j), (-1+1j), (1+1j), (1-1j), (-1+1j), (-1+1j), (1+1j), (-1+1j), (-1+1j), (-1+1j), (1+1j), (1-1j), (1+1j), (-1+1j), (1-1j), (-1-1j), (1-1j), (-1+1j), (1+1j), (-1-1j), (-1+1j), (-1+1j), (1+1j), (-1+1j), (1-1j), (-1+1j), (1+1j), (-1+1j), (-1+1j), (-1+1j), (1+1j), (1-1j), (-1+1j), (-1-1j), (1+1j), (1-1j), (1+1j), (-1-1j), (1+1j), (1-1j), (1+1j), (-1-1j), (1+1j), (1-1j), (1+1j)], tag_key="training_start")
        self.digital_constellation_soft_decoder_cf_0 = digital.constellation_soft_decoder_cf(QAM4, -1)
        self.digital_constellation_encoder_bc_0 = digital.constellation_encoder_bc(QAM4)
        self.digital_binary_slicer_fb_0 = digital.binary_slicer_fb()
        self.channels_dynamic_channel_model_0 = channels.dynamic_channel_model(
            (interp*bb_rate),
            0.01,
            1e3,
            0.01,
            1e3,
            8,
            1.0,
            False,
            4.0,
            [0.0,0.1,1.3],
            [1,0.99,0.97],
            8,
            0.2,
            1235472534997635)
        self.blocks_vector_source_x_0 = blocks.vector_source_b(preamble+message, True, 1, [head])
        self.blocks_unpacked_to_packed_xx_0 = blocks.unpacked_to_packed_bb(1, gr.GR_MSB_FIRST)
        self.blocks_throttle2_0_0 = blocks.throttle( gr.sizeof_char*1, bb_rate, False, 0 if "auto" == "auto" else max( int(float(0.1) * bb_rate) if "auto" == "time" else int(0.1), 1) )
        self.blocks_tag_gate_0 = blocks.tag_gate(gr.sizeof_gr_complex * 1, False)
        self.blocks_tag_gate_0.set_single_key("")
        self.blocks_packed_to_unpacked_xx_0 = blocks.packed_to_unpacked_bb(2, gr.GR_MSB_FIRST)
        self.blocks_file_sink_0 = blocks.file_sink(gr.sizeof_char*1, '/dev/pts/0', False)
        self.blocks_file_sink_0.set_unbuffered(False)
        self.blocks_delay_0 = blocks.delay(gr.sizeof_char*1, sym_dly)
        self._alpha_range = qtgui.Range(0, 16, 1, 0, 200)
        self._alpha_win = qtgui.RangeWidget(self._alpha_range, self.set_alpha, "'alpha'", "counter_slider", int, QtCore.Qt.Horizontal)
        self.top_grid_layout.addWidget(self._alpha_win, 0, 0, 1, 1)
        for r in range(0, 1):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_delay_0, 0), (self.blocks_unpacked_to_packed_xx_0, 0))
        self.connect((self.blocks_packed_to_unpacked_xx_0, 0), (self.digital_constellation_encoder_bc_0, 0))
        self.connect((self.blocks_tag_gate_0, 0), (self.digital_constellation_soft_decoder_cf_0, 0))
        self.connect((self.blocks_throttle2_0_0, 0), (self.blocks_packed_to_unpacked_xx_0, 0))
        self.connect((self.blocks_unpacked_to_packed_xx_0, 0), (self.blocks_file_sink_0, 0))
        self.connect((self.blocks_vector_source_x_0, 0), (self.blocks_throttle2_0_0, 0))
        self.connect((self.channels_dynamic_channel_model_0, 0), (self.root_raised_cosine_filter_1_0_0, 0))
        self.connect((self.digital_binary_slicer_fb_0, 0), (self.blocks_delay_0, 0))
        self.connect((self.digital_constellation_encoder_bc_0, 0), (self.qtgui_const_sink_x_0, 0))
        self.connect((self.digital_constellation_encoder_bc_0, 0), (self.root_raised_cosine_filter_1, 0))
        self.connect((self.digital_constellation_soft_decoder_cf_0, 0), (self.digital_binary_slicer_fb_0, 0))
        self.connect((self.epy_block_0, 0), (self.blocks_tag_gate_0, 0))
        self.connect((self.epy_block_0, 0), (self.qtgui_const_sink_x_1_0, 0))
        self.connect((self.root_raised_cosine_filter_1, 0), (self.channels_dynamic_channel_model_0, 0))
        self.connect((self.root_raised_cosine_filter_1_0_0, 0), (self.epy_block_0, 0))
        self.connect((self.root_raised_cosine_filter_1_0_0, 0), (self.qtgui_const_sink_x_1, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "projetoDSPII")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_QAM4(self):
        return self.QAM4

    def set_QAM4(self, QAM4):
        self.QAM4 = QAM4
        self.digital_constellation_encoder_bc_0.set_constellation(self.QAM4)
        self.digital_constellation_soft_decoder_cf_0.set_constellation(self.QAM4)

    def get_sym_dly(self):
        return self.sym_dly

    def set_sym_dly(self, sym_dly):
        self.sym_dly = sym_dly
        self.blocks_delay_0.set_dly(int(self.sym_dly))

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate

    def get_preamble(self):
        return self.preamble

    def set_preamble(self, preamble):
        self.preamble = preamble
        self.blocks_vector_source_x_0.set_data(self.preamble+self.message, [self.head])

    def get_message(self):
        return self.message

    def set_message(self, message):
        self.message = message
        self.blocks_vector_source_x_0.set_data(self.preamble+self.message, [self.head])

    def get_interp(self):
        return self.interp

    def set_interp(self, interp):
        self.interp = interp
        self.channels_dynamic_channel_model_0.set_samp_rate((self.interp*self.bb_rate))
        self.root_raised_cosine_filter_1.set_taps(firdes.root_raised_cosine(4, (self.interp*self.bb_rate), self.bb_rate, 0.3, (2*self.interp)))
        self.root_raised_cosine_filter_1_0_0.set_taps(firdes.root_raised_cosine(4, (self.interp*self.bb_rate), self.bb_rate, 0.3, (2*self.interp)))

    def get_head(self):
        return self.head

    def set_head(self, head):
        self.head = head
        self.blocks_vector_source_x_0.set_data(self.preamble+self.message, [self.head])

    def get_bb_rate(self):
        return self.bb_rate

    def set_bb_rate(self, bb_rate):
        self.bb_rate = bb_rate
        self.blocks_throttle2_0_0.set_sample_rate(self.bb_rate)
        self.channels_dynamic_channel_model_0.set_samp_rate((self.interp*self.bb_rate))
        self.root_raised_cosine_filter_1.set_taps(firdes.root_raised_cosine(4, (self.interp*self.bb_rate), self.bb_rate, 0.3, (2*self.interp)))
        self.root_raised_cosine_filter_1_0_0.set_taps(firdes.root_raised_cosine(4, (self.interp*self.bb_rate), self.bb_rate, 0.3, (2*self.interp)))

    def get_alpha(self):
        return self.alpha

    def set_alpha(self, alpha):
        self.alpha = alpha

    def get_alga(self):
        return self.alga

    def set_alga(self, alga):
        self.alga = alga




def main(top_block_cls=projetoDSPII, options=None):

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
