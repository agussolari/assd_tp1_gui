import input_signals as isig
import filters as ft

import numpy as np
from PyQt5.QtWidgets import QFileDialog
from enum import IntEnum

Node = IntEnum('Nodes', ['IN', 'AAF', 'SH', 'AS', 'RF', 'CUSTOM'], start=0)
NodePlotTitle = ['Input', 'Anti-Aliasing Filter (AAF)', 'Sample and Hold', 'Analog Switch', 'Reconstruction Filter', 'Custom']

class NodeSignal:
    """Class for plotting signals in each node of the sampling process"""
    def __init__(self, tt, st, tf, sf):
        self.tt = tt
        self.st = st
        self.tf = tf
        self.sf = sf

class SampledSignalNodes:
    """Class for storing signals in each node of the sampling process"""
    def __init__(self, inSig: NodeSignal, aafSig: NodeSignal, shSig: NodeSignal, asSig: NodeSignal, rfSig: NodeSignal):
        self.inSig = inSig
        self.aafSig = aafSig
        self.shSig = shSig
        self.asSig = asSig
        self.sfrfSig = rfSig

# sampledSignal = SampledSignalNodes()

# NodeSignal = 

def fft_signal(self, signal, time, padding_length):
    if len(time) != 0 and len(signal) != 0 and padding_length != 0:
        tf, sf = [], []
        tf = np.fft.fftfreq(len(np.pad(time, (0, padding_length), 'constant')), np.pad(time, (0, padding_length), 'constant')[1]-np.pad(time, (0, padding_length), 'constant')[0])
        sf = np.abs(np.fft.fft(np.pad(signal, (0, padding_length), 'constant')))
    
        return tf, sf

def plot_signals(self, tt, st, tf, sf, node):
    NodeTimePlot = [self.plot_a_time_in, self.plot_a_time_aaf, self.plot_a_time_sh, self.plot_a_time_as, self.plot_a_time_rf]
    NodeFreqPlot = [self.plot_a_freq_in, self.plot_a_freq_aaf, self.plot_a_freq_sh, self.plot_a_freq_as, self.plot_a_freq_rf]

    # print('Plotting signals')
    #plot tt and st in "plot_a" QFrame with pyqtgraph
    NodeTimePlot[node].clear()
    NodeTimePlot[node].plot(tt, st, pen='r')
    NodeTimePlot[node].setTitle(NodePlotTitle[node])
    NodeTimePlot[node].setLabel('left', 'Amplitude', units='V')
    NodeTimePlot[node].setLabel('bottom', 'Time', units='s')
    NodeTimePlot[node].showGrid(x=True, y=True)
    
    #plot espectro de la señal en "plot_a_frec" QFrame with pyqtgraph
    NodeFreqPlot[node].clear()
    NodeFreqPlot[node].plot(tf, sf, pen='r')
    NodeFreqPlot[node].setTitle(NodePlotTitle[node]+' Spectrum')
    NodeFreqPlot[node].setLabel('left', 'Amplitude', units='V')
    NodeFreqPlot[node].setLabel('bottom', 'Frequency', units='Hz')
    NodeFreqPlot[node].showGrid(x=True, y=True)
        
def import_file(self):
    print("Importing file")
    filename = QFileDialog.getOpenFileName(self, 'Open file', 'c:\\', "WAV files (*.wav)")
    self.data.input_signal.tt, self.data.input_signal.st = isig.generate_audio_signal(filename)



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

    if f0 != 0 and N != 0:
        if self.box_typeInputSignal.currentIndex() == 0:
            self.data.input_signal.tt, self.data.input_signal.st = isig.generate_sinusoidal_signal(f0, N)

        elif self.box_typeInputSignal.currentIndex() == 1 and dc != 0:
            self.data.input_signal.tt, self.data.input_signal.st = isig.generate_square_signal(f0, N, dc/100)

        elif self.box_typeInputSignal.currentIndex() == 2 and dc != 0:
            self.data.input_signal.tt, self.data.input_signal.st = isig.generate_triangular_signal(f0, N, dc/100)

        elif self.box_typeInputSignal.currentIndex() == 3 and dc != 0:
            self.data.input_signal.tt, self.data.input_signal.st = isig.generate_square_signal(f0, N, dc/100)

        elif self.box_typeInputSignal.currentIndex() == 4 and dc != 0:
            self.data.input_signal.tt, self.data.input_signal.st = isig.generate_triangular_signal(f0, N, dc/100)

        elif self.box_typeInputSignal.currentIndex() == 5 and dc != 0:
            self.data.input_signal.tt, self.data.input_signal.st = isig.generate_square_signal(f0, N, dc/100)

        elif self.box_typeInputSignal.currentIndex() == 6 and dc != 0:
            self.data.input_signal.tt, self.data.input_signal.st = isig.generate_triangular_signal( f0, N, dc/100)

        elif self.box_typeInputSignal.currentIndex() == 7:
            self.import_button.setEnabled(True)
            self.import_button.clicked.connect(lambda: import_file(self))

        elif ( self.box_typeInputSignal.currentIndex() != 7):
            self.import_button.setEnabled(False)



        #Make fft of the input signal
        self.data.input_signal.tf, self.data.input_signal.sf = fft_signal(self, self.data.input_signal.st, self.data.input_signal.tt, padding_length)
        self.data.input_signal.sf = self.data.input_signal.sf/N
        plot_signals(self, self.data.input_signal.tt, self.data.input_signal.st, self.data.input_signal.tf, self.data.input_signal.sf, Node.IN)


    elif self.box_typeInputSignal.currentIndex() != 3 and f0 == 0 and N == 0:
        print('Error: f0 or dc must be greater than 0')
        return None

    self.data.aaf_signal.st = self.data.input_signal.st
    if self.check_AAF.isChecked() and fp_AAF != 0:              # Hace falta chequear f=0 o ploteamos igual
        print('Applying AntiAliasFilter')
        self.data.aaf_signal.st = ft.AntiAliasFilter(fp_AAF, self.data.input_signal.st, self.data.input_signal.tt)
    self.data.aaf_signal.tf, self.data.aaf_signal.sf = fft_signal(self, self.data.aaf_signal.st, self.data.input_signal.tt, padding_length)
    self.data.aaf_signal.sf = self.data.aaf_signal.sf/N
    plot_signals(self, self.data.input_signal.tt, self.data.aaf_signal.st, self.data.aaf_signal.tf, self.data.aaf_signal.sf, Node.AAF)

    self.data.sh_signal.st = self.data.aaf_signal.st
    if self.check_sampleHold.isChecked() and fs != 0 and dsh != 0:
        print('Applying SampleAndHold')
        self.data.sh_signal.st = ft.SampleAndHold(self.data.input_signal.tt , self.data.aaf_signal.st, fs, dsh/100)
    self.data.sh_signal.tf, self.data.sh_signal.sf = fft_signal(self, self.data.sh_signal.st, self.data.input_signal.tt, padding_length)
    self.data.sh_signal.sf = self.data.sh_signal.sf/N    
    plot_signals(self, self.data.input_signal.tt, self.data.sh_signal.st, self.data.sh_signal.tf, self.data.sh_signal.sf, Node.SH)

    self.data.as_signal.st = self.data.sh_signal.st
    if self.check_analogSwitch.isChecked() and fs != 0 and das != 0:
        print('Applying AnalogSwitch')
        self.data.as_signal.st = ft.AnalogSwitch(self.data.input_signal.tt , self.data.sh_signal.st, fs, das/100)
    self.data.as_signal.tf, self.data.as_signal.sf = fft_signal(self, self.data.as_signal.st, self.data.input_signal.tt, padding_length)
    self.data.as_signal.sf = self.data.as_signal.sf/N
    plot_signals(self, self.data.input_signal.tt, self.data.as_signal.st, self.data.as_signal.tf, self.data.as_signal.sf, Node.AS)

    self.data.rf_signal.st = self.data.as_signal.st
    if self.check_RF.isChecked() and fp_RF != 0:    # and len(self.data.sample_signal.tt) != 0 and len(self.data.sample_signal.st) != 0:
        print('Applying RegenerativeFilter')            # Algo esta mal con el filtro recuperador
        self.data.rf_signal.st = ft.RegenerativeFilter(fp_RF, self.data.as_signal.st, self.data.input_signal.tt)
    self.data.rf_signal.tf, self.data.rf_signal.sf = fft_signal(self, self.data.rf_signal.st, self.data.input_signal.tt, padding_length)
    self.data.rf_signal.sf = self.data.rf_signal.sf/N
    plot_signals(self, self.data.input_signal.tt, self.data.rf_signal.st, self.data.rf_signal.tf, self.data.rf_signal.sf, Node.RF)

    if self.tab_plots.currentIndex() == 5: 
        if self.check_customInput.isChecked():
            plot_signals(self, self.data.input_signal.tt, self.data.rf_signal.st, self.data.rf_signal.tf, self.data.rf_signal.sf, Node.IN)
        if self.check_customAAF.isChecked():
            plot_signals(self, self.data.input_signal.tt, self.data.rf_signal.st, self.data.rf_signal.tf, self.data.rf_signal.sf, Node.AAF)
        if self.check_customSH.isChecked():
            plot_signals(self, self.data.input_signal.tt, self.data.rf_signal.st, self.data.rf_signal.tf, self.data.rf_signal.sf, Node.SH)
        if self.check_customAS.isChecked():
            plot_signals(self, self.data.input_signal.tt, self.data.rf_signal.st, self.data.rf_signal.tf, self.data.rf_signal.sf, Node.AS)
        if self.check_customRF.isChecked():
            plot_signals(self, self.data.input_signal.tt, self.data.rf_signal.st, self.data.rf_signal.tf, self.data.rf_signal.sf, Node.RF)
        
    if self.tab_plots.currentIndex() == 5:
        self.box_custom.setEnabled(True)
    else:
        self.box_custom.setEnabled(False)