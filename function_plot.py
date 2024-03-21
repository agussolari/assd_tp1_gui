import input_signals as isig

import numpy as np
from PyQt5.QtWidgets import QFileDialog
import filters as ft

def fft_signal(self, signal, time, padding_length):
    if len(time) != 0 and len(signal) != 0 and padding_length != 0:
        tf, sf = [], []
        tf = np.fft.fftfreq(len(np.pad(time, (0, padding_length), 'constant')), np.pad(time, (0, padding_length), 'constant')[1]-np.pad(time, (0, padding_length), 'constant')[0])
        sf = np.abs(np.fft.fft(np.pad(signal, (0, padding_length), 'constant')))
    
        return tf, sf
        
    
def plot_signals(self, tt, st, tf, sf):
        print('Plotting signals')
        #plot tt and st in "plot_a" QFrame with pyqtgraph
        self.plot_a_time.clear()
        self.plot_a_time.plot(tt, st, pen='r')
        self.plot_a_time.setTitle('Input Signal')
        self.plot_a_time.setLabel('left', 'Amplitude', units='V')
        self.plot_a_time.setLabel('bottom', 'Time', units='s')
        self.plot_a_time.showGrid(x=True, y=True)
        
        #plot espectro de la señal en "plot_a_frec" QFrame with pyqtgraph
        self.plot_a_freq.clear()
        self.plot_a_freq.plot(tf, sf, pen='r')
        self.plot_a_freq.setTitle('Input Signal Spectrum')
        self.plot_a_freq.setLabel('left', 'Amplitude', units='V')
        self.plot_a_freq.setLabel('bottom', 'Frequency', units='Hz')
        self.plot_a_freq.showGrid(x=True, y=True)
        
def import_file(self):
    print("Importing file")
    filename = QFileDialog.getOpenFileName(self, 'Open file', 'c:\\', "WAV files (*.wav)")
    self.data.input_signal.tt, self.data.input_signal.st = isig.generate_audio_signal(filename)



def generate_input_signal(self):

    f0 = self.spin_frecInputSignal.value()
    dc = self.spin_dutyInputSignal.value()
    N = self.spin_samplesInputSignal.value()
    fs = self.spin_frecControlSignal.value()
    dsh = self.spin_dutyControlSignalSH.value()
    das = self.spin_dutyControlSignalAS.value()
    fp_FAA = self.spin_freqFAA.value()
    fp_FR = self.spin_freqFR.value()
    padding_length = self.spin_paddingLength.value()  # Adjust this value as needed

    
    if f0 != 0 and N != 0:
        if self.box_typeInputSignal.currentIndex() == 0:
            self.data.input_signal.tt, self.data.input_signal.st = isig.generate_sinusoidal_signal(f0, N)
            
        elif self.box_typeInputSignal.currentIndex() == 1 and dc != 0:
            self.data.input_signal.tt, self.data.input_signal.st = isig.generate_square_signal(f0, N, dc/100)
                                                                      
        elif self.box_typeInputSignal.currentIndex() == 2 and dc != 0:
            self.data.input_signal.tt, self.data.input_signal.st = isig.generate_triangular_signal( f0, N, dc/100)
        
        elif (self.box_typeInputSignal.currentIndex() == 3):
            self.import_button.setEnabled(True)
            self.import_button.clicked.connect(lambda: import_file(self))
            

        elif ( self.box_typeInputSignal.currentIndex() != 3):
            self.import_button.setEnabled(False)
            
            
         #Make fft of the input signal
        self.data.input_signal_f.tt, self.data.input_signal_f.st = fft_signal(self, self.data.input_signal.st, self.data.input_signal.tt, padding_length)
        plot_signals(self, self.data.input_signal.tt, self.data.input_signal.st, self.data.input_signal_f.tt, self.data.input_signal_f.st)


    elif self.box_typeInputSignal.currentIndex() != 2 and f0 == 0 and N == 0:
        print('Error: f0 or dc must be greater than 0')
        return None
    
    if self.check_FAA.isChecked() and fp_FAA != 0:
        print('Applying AntiAliasFilter')
        self.data.input_signal.st = ft.AntiAliasFilter(fp_FAA, self.data.input_signal.st, self.data.input_signal.tt)
        self.data.input_signal_f.tt, self.data.input_signal_f.st = fft_signal(self, self.data.input_signal.st, self.data.input_signal.tt, padding_length)
        
        plot_signals(self, self.data.input_signal.tt, self.data.input_signal.st, self.data.input_signal_f.tt, self.data.input_signal_f.st)
        
        
    if self.check_sampleHold.isChecked() and fs != 0 and dsh != 0 and not self.check_analogSwitch.isChecked():
        print('Applying SampleAndHold')
        self.data.sample_signal.st = ft.SampleAndHold(self.data.input_signal.tt , self.data.input_signal.st, fs, dsh/100)
        self.data.sample_signal.tt = self.data.input_signal.tt
        self.data.sample_signal_f.tt, self.data.sample_signal_f.st = fft_signal(self, self.data.sample_signal.st, self.data.input_signal.tt, padding_length)
        
        plot_signals(self, self.data.sample_signal.tt, self.data.sample_signal.st, self.data.sample_signal_f.tt, self.data.sample_signal_f.st)

    if self.check_analogSwitch.isChecked() and fs != 0 and das != 0:
        print('Applying AnalogSwitch')
        if self.check_sampleHold.isChecked():           # Hay que ver como guardamos etapas intermedias
            self.data.input_signal.st = ft.SampleAndHold(self.data.input_signal.tt , self.data.input_signal.st, fs, dsh/100)
        self.data.sample_signal.st = ft.AnalogSwitch(self.data.input_signal.tt , self.data.input_signal.st, fs, das/100)
        self.data.sample_signal.tt = self.data.input_signal.tt
        self.data.sample_signal_f.tt, self.data.sample_signal_f.st = fft_signal(self, self.data.sample_signal.st, self.data.input_signal.tt, padding_length)
        
        plot_signals(self, self.data.sample_signal.tt, self.data.sample_signal.st, self.data.sample_signal_f.tt, self.data.sample_signal_f.st)

    if self.check_FR.isChecked() and fp_FR != 0 and len(self.data.sample_signal.tt) != 0 and len(self.data.sample_signal.st) != 0:
        print('Applying RegenerativeFilter')            # Algo esta mal con el filtro recuperador
        self.data.sample_signal.st = ft.RegenerativeFilter(fp_FR, self.data.sample_signal.st, self.data.sample_signal.tt)
        self.data.sample_signal_f.tt, self.data.sample_signal_f.st = fft_signal(self, self.data.sample_signal.st, self.data.sample_signal.tt, padding_length)
        
        plot_signals(self, self.data.sample_signal.tt, self.data.sample_signal.st, self.data.sample_signal_f.tt, self.data.sample_signal_f.st)
        
    
    
    
                

        



        
        
        
    