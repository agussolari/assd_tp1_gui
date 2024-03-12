from scipy import signal as sg
import matplotlib.pyplot as plt
import numpy as np
from scipy.io import wavfile


class signal:
    tt = []
    st = []
    
class signal_f:
    tf = []
    sf = []
    

    
input_signal = signal()
input_signal_f = signal_f()

# generear una señal senoidal de frecuencia, amplitud y fase configurables
def generate_sinusoidal_signal(f0, N, a0=1, p0=0):
    # fs: frecuencia de muestreo
    # f0: frecuencia de la señal
    # N: cantidad de muestras
    # a0: amplitud
    # p0: fase

    # calculo el periodo de la señal
    T0 = 1/f0

    #quiero que el vector de tiempos se ajuste a la frecuencia de la señal y tenga N muestras
    tt = np.linspace(0, 10*T0, N)    
    
    # genero la señal
    st = a0 * np.sin(2*np.pi*f0*tt + p0)

    return tt, st

# generear una señal cuadrada de frecuencia, amplitud, fase y duty cycle configurables
def generate_square_signal(f0, N, dc=1 ,a0=1, p0=0):
    # fs: frecuencia de muestreo
    # f0: frecuencia de la señal
    # N: cantidad de muestras
    # a0: amplitud
    # p0: fase
    # dc: duty cycle

    # calculo el periodo de la señal
    T0 = 1/f0
    # genero el vector de tiempos
    tt = np.linspace(0, 10*T0, N)
    # genero la señal
    st = a0 * sg.square(2*np.pi*f0*tt + p0, dc)

    return tt, st

# generear una señal triangular de frecuencia, amplitud, fase y duty cycle configurables
def generate_triangular_signal( f0, N, dc, a0=1, p0=0):
    # fs: frecuencia de muestreo
    # f0: frecuencia de la señal
    # N: cantidad de muestras
    # a0: amplitud
    # p0: fase
    # dc: duty cycle

    # calculo el periodo de la señal
    T0 = 1/f0

    # genero el vector de tiempos
    tt = np.linspace(0, 10*T0, N)
    # genero la señal
    st = a0 * sg.sawtooth(2*np.pi*f0*tt + p0, width=dc)

    return tt, st

# generear una señal exponencial de frecuencia, amplitud y fase configurables
def generate_exponential_signal(fs, f0, N, a0=1, p0=0, tau=1):
    # fs: frecuencia de muestreo
    # f0: frecuencia de la señal
    # N: cantidad de muestras
    # a0: amplitud
    # p0: fase
    # tau: constante de tiempo

    # calculo el periodo de la señal
    T0 = 1/f0
    # calculo el periodo de muestreo
    Ts = 1/fs
    # genero el vector de tiempos
    tt = np.linspace(0, 2*T0, N)
    # genero la señal
    st = a0 * np.exp(-tt/tau) * np.sin(2*np.pi*f0*tt + p0)

    return tt, st

# generar pulso de escalon unitario u(t) de amplitud configurable
def generate_step_signal(fs, N, a0=1):
    # fs: frecuencia de muestreo
    # N: cantidad de muestras
    # a0: amplitud

    # calculo el periodo de muestreo
    Ts = 1/fs
    # genero el vector de tiempos
    tt = np.linspace(0, 2*Ts, N)
    # genero la señal
    st = a0 * np.heaviside(tt, 1)

    return tt, st

# generar pulso de impulso unitario delta(t) de amplitud configurable
def generate_impulse_signal(fs, N, a0=1):
    # fs: frecuencia de muestreo
    # N: cantidad de muestras
    # a0: amplitud

    # calculo el periodo de muestreo
    Ts = 1/fs
    # genero el vector de tiempos
    tt = np.linspace(0, (N-1)*Ts, N)
    # genero la señal
    st = a0 * np.zeros(N)
    st[0] = 1

    return tt, st

#Sample wav audio file to tt and st
def generate_audio_signal(filename):

    # cargo el archivo .wav
    fs, data = wavfile.read(filename[0])
    # genero el vector de tiempos
    tt = np.linspace(0, len(data)/fs, len(data))
    # genero la señal
    if len(data.shape) > 1:
        st = np.mean(data, axis=1)
        print("Audio file has more than one channel, using the mean of all channels")
    else:
        st = data
        print("Audio file has only one channel")

    
    
    
    return list(tt), list(st)
    

#main
if __name__ == '__main__':
    tt, st = generate_sinusoidal_signal(1000, 10, 1000, 1, 0)
    plt.plot(tt, st)
    