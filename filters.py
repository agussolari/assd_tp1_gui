import numpy as np
from scipy.signal import ellip, lsim, cheby1, cheb1ord
import scipy.signal as signal

def AntiAliasFilter(fp, signal, t): 
    N, wn = cheb1ord(2*np.pi*fp, 2*np.pi*fp*1.1, 1, 40, analog=True) #Calculate the order and wn of the filter

    

    a,b = cheby1(N, 1 , wn, btype='low', analog=True, output='ba')
    tout, yout, xout = lsim((a,b), signal, t) #Apply the filter to the signal
    return yout

def RegenerativeFilter(fp, signal, t):
   return AntiAliasFilter(fp, signal, t) #Apply the AntiAliasFilter

def SampleAndHold(t: np.ndarray, sig: np.ndarray, fs: float, ds: float) -> np.ndarray:
    """
    Samples the input signal `sig` with a clk of frequency `fs` and duty cycle `ds`.
    
    Holds the sampled value during the clk's low level.

    Returns the output signal array.
    """
    outSig = []
    sample_clock = signal.square(2*np.pi*fs*t, duty=ds)
    if sample_clock[0] == 0:
        sample_clock = -sample_clock
    for i in range(len(t)):
        if sample_clock[i] > 0:
            outSig.append(sig[i])
        else:
            outSig.append(outSig[i-1])

    return outSig

def AnalogSwitch(t: np.ndarray, sig: np.ndarray, fs: float, ds: float) -> np.ndarray:
    """"
    Samples the input signal `sig` with a clk of frequency `fs` and duty cycle `ds`.
    
    Sets to zero the sampled value during the clk's low level.
    
    Adds a delay of `delay` clk cycles to the output signal.
    """
    sample_clock = (signal.square(2*np.pi*fs*t, duty=ds)+1)/2
    if sample_clock[0] == 0:                                            # A veces signal.square no genera un clk que empieza en high
        sample_clock = 1-sample_clock

    return sig*sample_clock

def Delay(t: np.ndarray, sig: np.ndarray, fs: float, delay=0) -> np.ndarray:   
    """
    Adds a delay of `delay` clk cycles to the output signal `sig`.
    """
    outSig = []
    if delay > 0:                                                       # Se podría usar la fase también
        tstep = (t[-1]-t[0])/len(t)
        tdelay = (int(1/(tstep*fs)))*delay                              # No es exacto si el clk no es múltiplo del plot sampling
        outSig = [0]*tdelay + sig[:-tdelay]

    return outSig