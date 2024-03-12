# %%
from scipy import signal
from scipy.fft import rfft, rfftfreq, irfft
import matplotlib.pyplot as plt
import numpy as np


def timeSignal(t):
    return np.cos(2 * np.pi * 8e3 * t) + np.sin(2 * np.pi * 20e3 * t) + 0.8 * np.sin(
        2 * np.pi * 35e3 * t) + 0.5 * np.sin(2 * np.pi * 200e3 * t)


def FiltroAntiAlias(x, t):
    poles = [
        -9301.394085541 - 140211.376204937j,
        -9301.394085541 + 140211.376204937j,
        -26913.411651489 - 122396.327932432j,
        -26913.411651489 + 122396.327932432j,
        -42190.990306100 + 90265.322107311j,
        -42190.990306100 - 90265.322107311j,
        -52352.499344307 - 47970.9501448564j,
        -52352.499344307 + 47970.9501448564j,
        -55540.15182371682
    ]
    num = (-1) ** len(poles) * np.abs(np.prod(poles))
    den = np.poly(poles)

    time, xaa, algo = signal.lsim2((num, den), x, t)
    return xaa


def FiltroRecuperador(x, t):
    return FiltroAntiAlias(x, t)


def LlaveAnalogica(t, x, fs, dc):
    p = 0.5 * (signal.square(2 * np.pi * fs * t, dc) + 1)  # tren de pulsos
    return x * p


def SampleAndHold(t, x, fs, dc):
    y = []
    sh = 0.5 * (1 - signal.square(2 * np.pi * fs * t, dc)) * t

    for i in range(len(sh)):
        if sh[i] != 0:
            y.append(x[i])
        else:
            y.append(y[-1])
    return y


def testLlave():
    duracion = 1e-3
    N = 1000000  # cantidad de muestras
    fd = N / duracion
    t = np.linspace(0, duracion, N, endpoint=False)

    x = [timeSignal(i) for i in t]

    xaa = FiltroAntiAlias(x, t)
    t_steady = t[len(t) // 3: -1]
    x_steady = xaa[len(xaa) // 3: -1]

    plt.plot(t, x, linewidth=0.5)  # señal analógica
    plt.title('Señal analógica de entrada')
    plt.xlabel('t')
    plt.ylabel('x\u2090(t)')
    plt.plot(t, xaa)  # señal prefiltrada
    plt.show()

    # Espectro de la señal analógica
    plt.semilogy(rfftfreq(N, 1 / fd), 1 / N * np.abs(rfft(x)))
    plt.title('Espectro de la señal analógica')
    plt.xlim([0, 250e3])
    plt.show()

    plt.plot(t_steady, x_steady)
    plt.title('Señal analógica prefiltrada')
    plt.show()

    # S&H
    duty = 0.10
    fs = 50e3
    xsh = SampleAndHold(t_steady, x_steady, fs, duty)
    plt.plot(t_steady, xsh)
    plt.title('Señal tras el SH')
    plt.xlabel('t')
    plt.ylabel('x(t)')
    plt.show()

    # Espectro de la señal tras la llave
    plt.semilogy(rfftfreq(len(xsh), 1 / fd), 1 / len(xsh) * np.abs(rfft(xsh)))
    plt.title('Espectro de la señal tras el SH')
    plt.xlim([0, 250e3])
    plt.show()

    # Llave
    duty = 0.5
    fs = 50e3
    xllave = LlaveAnalogica(t_steady, xsh, fs, duty)
    plt.plot(t_steady, xllave)
    plt.title('Señal tras la llave')
    plt.xlabel('t')
    plt.ylabel('x(t)')
    plt.show()

    # Espectro de la señal tras la llave
    plt.semilogy(rfftfreq(len(xllave), 1 / fd), 1 / len(xllave) * np.abs(rfft(xllave)))
    plt.title('Espectro de la señal tras la llave')
    plt.xlim([0, 250e3])
    plt.show()

    # Filtro recuperador
    xr = FiltroAntiAlias(xllave, t_steady)
    plt.plot(t_steady, xr)
    plt.title('Señal de salida')
    plt.xlabel('t')
    plt.ylabel('xr(t)')
    plt.show()
    # t_steady2 = t[ len(t_steady)//3 : -1]
    # x_steady2 = xaa[ len(xllave)//3 : -1]

    # Espectro de la señal de salida
    plt.plot(rfftfreq(len(xr), 1 / fd), 1 / len(xr) * np.abs(rfft(xr)))
    plt.title('Espectro de la señal de salida')
    plt.xlim([0, 250e3])
    plt.show()
