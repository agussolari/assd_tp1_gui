from scipy import signal as sg
import matplotlib.pyplot as plt
import numpy as np
from scipy.io import wavfile



    



# generear una señal senoidal de frecuencia, amplitud y fase configurables
def generate_sinusoidal_signal(f0, per_ext, N, a0=1, p0=0):
    # fs: frecuencia de muestreo
    # f0: frecuencia de la señal
    # N: cantidad de muestras
    # a0: amplitud
    # p0: fase

    # calculo el periodo de la señal
    T0 = 1/f0

    #quiero que el vector de tiempos se ajuste a la frecuencia de la señal y tenga N muestras
    tt = np.linspace(0, per_ext*T0, int(N/10))
    # tt = np.linspace(0, 10*T0, N)
    
    # genero la señal
    st = a0 * np.sin(2*np.pi*f0*tt + p0)
    
    # Repeat the sine wave to make it periodic
    tt = np.linspace(0, 10*per_ext*T0, 10*int(N/10))
    st = np.tile(st, 10)
    
    return tt, st

# generear una señal cuadrada de frecuencia, amplitud, fase y duty cycle configurables
def generate_square_signal(f0, N, dc ,a0=1, p0=0):
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
def generate_exponential_signal( f0, N, a0=1, p0=0, tau=1):
    # fs: frecuencia de muestreo
    # f0: frecuencia de la señal
    # N: cantidad de muestras
    # a0: amplitud
    # p0: fase
    # tau: constante de tiempo

    # calculo el periodo de la señal
    T0 = 1/f0
    tau = T0
    # calculo el periodo de muestreo
    # genero el vector de tiempos
    tt = np.linspace(0, 10*T0, N)
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

# generear una señal AM de frecuencia, amplitud y fase configurables
def generate_am_signal(fc, fm, N, Ac=1, Am=1, phi_c=0, phi_m=0):
    # fc: frecuencia de la portadora
    # fm: frecuencia de la moduladora
    # N: cantidad de muestras
    # Ac: amplitud de la portadora
    # Am: amplitud de la moduladora
    # phi_c: fase de la portadora
    # phi_m: fase de la moduladora

    # calculo el periodo de la portadora y la moduladora
    Tc = 1/fc
    Tm = 1/fm

    # genero el vector de tiempos
    tt = np.linspace(0, 10*Tm, N)

    # genero la señal moduladora
    sm = Am * np.sin(2*np.pi*fm*tt + phi_m)

    # genero la señal portadora
    sc = Ac * np.sin(2*np.pi*fc*tt + phi_c)

    # genero la señal AM
    st = (1 + sm) * sc

    return tt, st

#Sample wav audio file to tt and st
def generate_audio_signal(filename):

    if filename[0] == '':
        print("No file selected")
        return [], []
    else:
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

    
        
        return np.array(tt), np.array(st)
    

#main
if __name__ == '__main__':
    tt, st = generate_sinusoidal_signal(1000, 10, 1000, 1, 0)
    plt.plot(tt, st)
    