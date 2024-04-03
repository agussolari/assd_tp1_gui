import input_signals as isig
import filters as ft

import numpy as np
from PyQt5.QtWidgets import QFileDialog
from enum import IntEnum
import pyqtgraph as pg
from pyqtgraph import mkPen

Node = IntEnum('Nodes', ['IN', 'AAF', 'SH', 'AS', 'RF', 'CUSTOM'], start=0)
NodePlotTitle = ['Input', 'Anti-Aliasing Filter (AAF)', 'Sample and Hold', 'Analog Switch', 'Reconstruction Filter', 'Custom Traces']

def fft_signal(self, signal, time, padding_length):
    if len(time) != 0 and len(signal) != 0 and padding_length != 0:
        tf, sf = [], []
        tf = np.fft.fftfreq(len(np.pad(time, (0, padding_length), 'constant')), np.pad(time, (0, padding_length), 'constant')[1]-np.pad(time, (0, padding_length), 'constant')[0])
        sf = np.abs(np.fft.fft(np.pad(signal, (0, padding_length), 'constant')))
    
        return tf, sf

def plot_signals(self, tt, st, tf, sf, node, color = 'r', customNames = []):
    NodeTimePlot = [self.plot_a_time_in, self.plot_a_time_aaf, self.plot_a_time_sh, self.plot_a_time_as, self.plot_a_time_rf, self.plot_a_time_custom]
    NodeFreqPlot = [self.plot_a_freq_in, self.plot_a_freq_aaf, self.plot_a_freq_sh, self.plot_a_freq_as, self.plot_a_freq_rf, self.plot_a_freq_custom]

    # print('Plotting signals')
    #plot tt and st in "plot_a" QFrame with pyqtgraph
    NodeTimePlot[node].clear()
    if node == Node.CUSTOM:
        for i in range(len(st)):
            NodeTimePlot[node].plot(tt, st[i], pen=color[i], name=customNames[i])
    else:
        NodeTimePlot[node].plot(tt, st, pen=mkPen(color, width=3))
    NodeTimePlot[node].setTitle(NodePlotTitle[node])
    NodeTimePlot[node].setLabel('left', 'Amplitude', units='V')
    NodeTimePlot[node].setLabel('bottom', 'Time', units='s')
    NodeTimePlot[node].showGrid(x=True, y=True)
    # NodeTimePlot[node].setBackground('w')

    #plot espectro de la señal en "plot_a_frec" QFrame with pyqtgraph
    NodeFreqPlot[node].clear()
    if node == Node.CUSTOM:
        NodeFreqPlot[node].addLegend(brush='k', pen='w')
        for i in range(len(st)):
            NodeFreqPlot[node].plot(tf[i], sf[i], pen=color[i], name=customNames[i])
    else:
        NodeFreqPlot[node].plot(tf, sf, pen=color)
    NodeFreqPlot[node].setTitle(NodePlotTitle[node]+' Spectrum')
    NodeFreqPlot[node].setLabel('left', 'Amplitude', units='V')
    NodeFreqPlot[node].setLabel('bottom', 'Frequency', units='Hz')
    NodeFreqPlot[node].showGrid(x=True, y=True)
        
def import_file(self):
    N = self.spin_samplesInputSignal.value()
    filename = QFileDialog.getOpenFileName(self, 'Open file', 'c:\\', "WAV files (*.wav)")
    self.data.input_signal.tt, self.data.input_signal.st = isig.generate_audio_signal(filename)
    self.data.input_signal.st = self.data.input_signal.st/N
    
    generate_node_signal(self)



def generate_node_signal(self):

    f0 = self.spin_frecInputSignal.value()
    dc = self.spin_dutyInputSignal.value()
    N = self.spin_samplesInputSignal.value()
    fs = self.spin_frecControlSignal.value()
    dsh = self.spin_dutyControlSignalSH.value()
    das = self.spin_dutyControlSignalAS.value()
    fp_AAF = self.spin_freqAAF.value()
    fp_RF = self.spin_freqRF.value()
    padding_length = self.spin_paddingLength.value()  # Adjust this value as needed

    # # Plotting options

    # def selectBlackBg(self):
    #     if(self.menu_bgColorBlack.isChecked()):
    #         self.menu_bgColorWhite.setChecked(False)
    #         self.configPlots()
    #     else:
    #         self.menu_bgColorWhite.setChecked(True)
    #         self.selectWhiteBg()

    # def selectWhiteBg(self):
    #     if(self.menu_bgColorWhite.isChecked()):
    #         self.menu_bgColorBlack.setChecked(False)
    #         self.configPlots()
    #     else:
    #         self.menu_bgColorBlack.setChecked(True)
    #         self.selectBlackBg()

    # if self.menu_bgColorBlack.isChecked():
    #     pg.setConfigOption('background', 'w')
    #     pg.setConfigOption('foreground', 'k')
    # else:
    #     pg.setConfigOption('background', 'k')
    #     pg.setConfigOption('foreground', 'w')
    # if self.menu_aa.isChecked():
    #     pg.setConfigOption('antialias', True)
    # else:
    #     pg.setConfigOption('antialias', False)

    if f0 != 0 and N != 0:
        if self.box_typeInputSignal.currentIndex() == 0:
            self.data.input_signal.tt, self.data.input_signal.st = isig.generate_sinusoidal_signal(f0, N)

        elif self.box_typeInputSignal.currentIndex() == 1:
            self.data.input_signal.tt, self.data.input_signal.st = isig.generate_exponential_signal(f0,N)

        elif self.box_typeInputSignal.currentIndex() == 2 and dc != 0:
            self.data.input_signal.tt, self.data.input_signal.st = isig.generate_triangular_signal(f0, N, dc/100)

        elif self.box_typeInputSignal.currentIndex() == 3 and dc != 0:
            self.data.input_signal.tt, self.data.input_signal.st = isig.generate_square_signal(f0, N, dc/100)

        elif self.box_typeInputSignal.currentIndex() == 4:
            self.import_button.setEnabled(True)

        elif ( self.box_typeInputSignal.currentIndex() != 4):
            self.import_button.setEnabled(False)



        #Make fft of the input signal
        self.data.input_signal.tf, self.data.input_signal.sf = fft_signal(self, self.data.input_signal.st, self.data.input_signal.tt, padding_length)
        self.data.input_signal.sf = self.data.input_signal.sf/N
        plot_signals(self, self.data.input_signal.tt, self.data.input_signal.st, self.data.input_signal.tf, self.data.input_signal.sf, Node.IN)


    elif self.box_typeInputSignal.currentIndex() != 3 and f0 == 0 and N == 0:
        return None

    self.data.aaf_signal.st = self.data.input_signal.st
    if self.check_AAF.isChecked() and fp_AAF != 0:              # Hace falta chequear f=0 o ploteamos igual
        self.data.aaf_signal.st = ft.AntiAliasFilter(fp_AAF, self.data.input_signal.st, self.data.input_signal.tt)
    self.data.aaf_signal.tf, self.data.aaf_signal.sf = fft_signal(self, self.data.aaf_signal.st, self.data.input_signal.tt, padding_length)
    self.data.aaf_signal.sf = self.data.aaf_signal.sf/N
    plot_signals(self, self.data.input_signal.tt, self.data.aaf_signal.st, self.data.aaf_signal.tf, self.data.aaf_signal.sf, Node.AAF, color = 'g')

    self.data.sh_signal.st = self.data.aaf_signal.st
    if self.check_sampleHold.isChecked() and fs != 0 and dsh != 0:
        self.data.sh_signal.st = ft.SampleAndHold(self.data.input_signal.tt , self.data.aaf_signal.st, fs, dsh/100)
    self.data.sh_signal.tf, self.data.sh_signal.sf = fft_signal(self, self.data.sh_signal.st, self.data.input_signal.tt, padding_length)
    self.data.sh_signal.sf = self.data.sh_signal.sf/N    
    plot_signals(self, self.data.input_signal.tt, self.data.sh_signal.st, self.data.sh_signal.tf, self.data.sh_signal.sf, Node.SH, color = 'b')

    self.data.as_signal.st = self.data.sh_signal.st
    if self.check_analogSwitch.isChecked() and fs != 0 and das != 0:
        self.data.as_signal.st = ft.AnalogSwitch(self.data.input_signal.tt , self.data.sh_signal.st, fs, das/100)
    self.data.as_signal.tf, self.data.as_signal.sf = fft_signal(self, self.data.as_signal.st, self.data.input_signal.tt, padding_length)
    self.data.as_signal.sf = self.data.as_signal.sf/N
    plot_signals(self, self.data.input_signal.tt, self.data.as_signal.st, self.data.as_signal.tf, self.data.as_signal.sf, Node.AS , color = 'y')

    self.data.rf_signal.st = self.data.as_signal.st
    if self.check_RF.isChecked() and fp_RF != 0:    # and len(self.data.sample_signal.tt) != 0 and len(self.data.sample_signal.st) != 0:
        self.data.rf_signal.st = ft.RegenerativeFilter(fp_RF, self.data.as_signal.st, self.data.input_signal.tt)
    self.data.rf_signal.tf, self.data.rf_signal.sf = fft_signal(self, self.data.rf_signal.st, self.data.input_signal.tt, padding_length)
    self.data.rf_signal.sf = self.data.rf_signal.sf/N
    plot_signals(self, self.data.input_signal.tt, self.data.rf_signal.st, self.data.rf_signal.tf, self.data.rf_signal.sf, Node.RF, color = 'm')

    NodeCustomTrace = [self.check_customInput, self.check_customAAF, self.check_customSH, self.check_customAS, self.check_customRF]
    NodeData = [self.data.input_signal, self.data.aaf_signal, self.data.sh_signal, self.data.as_signal, self.data.rf_signal]
    NodePlotTitle = ['IN', 'AAF', 'S&H', 'AS', 'RF']
    NodeColor = ['r', 'g', 'b', 'y', 'm']
    if self.tab_plots.currentIndex() == 5:
        self.box_custom.setEnabled(True)
        self.data.custom_signal.st.clear()
        self.data.custom_signal.tf.clear()
        self.data.custom_signal.sf.clear()

        colors = []
        names = []
        for i in range(len(NodeCustomTrace)):   # Sería más facil cambiar plot_signals para que reciba el objeto (o una lista de objetos)
            if NodeCustomTrace[i].isChecked():
                self.data.custom_signal.st.append(NodeData[i].st)
                self.data.custom_signal.tf.append(NodeData[i].tf)
                self.data.custom_signal.sf.append(NodeData[i].sf)
                colors.append(NodeColor[i])
                names.append(NodePlotTitle[i])
        
        plot_signals(self, self.data.input_signal.tt, self.data.custom_signal.st, self.data.custom_signal.tf, self.data.custom_signal.sf, Node.CUSTOM, colors, names)

    else:
        self.box_custom.setEnabled(False)