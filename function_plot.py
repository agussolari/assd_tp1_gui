import input_signals as isig

import numpy as np
from PyQt5.QtWidgets import QFileDialog
import filters as ft


def import_audio_file(self):
    if (self.box_typeInputSignal.currentIndex() == 2):
        print("Importing file")
        filename = QFileDialog.getOpenFileName(self, 'Open file', 'c:\\', "WAV files (*.wav)")
        isig.input_signal.tt, isig.input_signal.st = isig.generate_audio_signal(filename)
        plot_signals(self)
        
def plot_signals(self):
    # Define the padding length
    padding_length = self.spin_paddingLength.value()  # Adjust this value as needed

    print('test', len(isig.input_signal.tt), len(isig.input_signal.st), padding_length)
    
    if len(isig.input_signal.tt) != 0 and len(isig.input_signal.st) != 0 and padding_length != 0:
        print('plot_signals')
        # Add zero padding to the signals
        isig.input_signal_f.tt = np.pad(isig.input_signal.tt, (0, padding_length), 'constant')
        isig.input_signal_f.st = np.pad(isig.input_signal.st, (0, padding_length), 'constant')
                
        # compute fft
        isig.input_signal_f.tf = np.fft.fftfreq(len(isig.input_signal_f.tt), isig.input_signal_f.tt[1]-isig.input_signal_f.tt[0])
        isig.input_signal_f.sf = np.abs(np.fft.fft(isig.input_signal_f.st))
        
        #plot tt and st in "plot_a" QFrame with pyqtgraph
        self.plot_a_time.clear()
        self.plot_a_time.plot(isig.input_signal.tt, isig.input_signal.st, pen='r')
        self.plot_a_time.setTitle('Input Signal')
        self.plot_a_time.setLabel('left', 'Amplitude', units='V')
        self.plot_a_time.setLabel('bottom', 'Time', units='s')
        self.plot_a_time.showGrid(x=True, y=True)
        
        #plot espectro de la señal en "plot_a_frec" QFrame with pyqtgraph
        self.plot_a_freq.clear()
        self.plot_a_freq.plot(isig.input_signal_f.tf, isig.input_signal_f.sf, pen='r')
        self.plot_a_freq.setTitle('Input Signal Spectrum')
        self.plot_a_freq.setLabel('left', 'Amplitude', units='V')
        self.plot_a_freq.setLabel('bottom', 'Frequency', units='Hz')
        self.plot_a_freq.showGrid(x=True, y=True)
        



def generate_input_signal(self):

    f0 = self.spin_frecInputSignal.value()
    dc = self.spin_dutyInputSignal.value()
    N = self.spin_samplesInputSignal.value()
    fs = self.spin_frecControlSignal.value()
    ds = self.spin_dutyControlSignal.value()
    
    if f0 != 0 and N != 0:
        if self.box_typeInputSignal.currentIndex() == 0:
            isig.input_signal.tt, isig.input_signal.st = isig.generate_sinusoidal_signal(f0, N)
                                                                      
        elif self.box_typeInputSignal.currentIndex() == 1 and dc != 0:
            isig.input_signal.tt, isig.input_signal.st = isig.generate_triangular_signal( f0, N, dc/100)

    else:
        print('Error: f0 and dc must be greater than 0')
        return None
    
    if self.check_FAA.isChecked():
        print('Applying AntiAliasFilter')
        isig.input_signal.st = ft.AntiAliasFilter(50000, 40, 1, isig.input_signal.st, isig.input_signal.tt)
        
    if self.check_FR.isChecked():
        print('Applying RegenerativeFilter')
        isig.input_signal.st = ft.RegenerativeFilter(50000, 40, 1, isig.input_signal.st, isig.input_signal.tt)
        
    if self.check_sampleHold.isChecked():
        print('Applying SampleAndHold')
        isig.input_signal.st = ft.SampleAndHold(isig.input_signal.st, fs, ds, 0 , 0)
    
    plot_signals(self)
    
                

        



        
        
        
    