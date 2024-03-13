import numpy as np
from scipy.signal import ellip, lsim
import scipy.signal as signal

def AntiAliasFilter(cut_frec, Aa, Ap, signal, t): 
    '''Apply a 4th Order low-pass Cauer filter with fc = cut_frec to the input signal. 
    
    Ap is the maximun attenuation in the passband and Aa is the minimun attenuation in the stopband 
    '''
    a,b = ellip(4, Ap, Aa, 2*np.pi*cut_frec, 'low', analog=True, output='ba') #Cauer Filter 4th order
    tout, yout, xout = lsim((a,b), signal, t) #Apply the filter to the signal
    return yout

def RegenerativeFilter(cut_frec, Aa, Ap, signal, t):
   return AntiAliasFilter(cut_frec, Aa, Ap, signal, t) #Apply the AntiAliasFilter
   

def SampleAndHold(t: np.ndarray, sig: np.ndarray, fs: float, ds: float, dh=0.0, delay=0) -> np.ndarray:
    ''' Samples the input signal `sig` with a clk of frequency `fs` and duty cycle `ds`.
    
    Holds the sampled value during the clk's low level.
    
    If (hold) duty cycle `dh` is specified, the output signal is set to zero during the hold time after ``dh/fs``.
    
    Adds a delay of `delay` clk cycles to the output signal.
    
    Returns the output signal array.
    '''
    # if 0<=ds<=0.9 and 0<=dh<=0.9 and ds+dh<=0.9:
    outSig = []
    sample_clock = signal.square(2*np.pi*fs*t, duty=ds)
    hold_clock = signal.square(2*np.pi*fs*t, duty=ds+dh)
    # hold_clock = signal.square(2*np.pi*fs*t, duty=ds+dh*(1-ds))       # Puede usarse si se quiere un duty relativo
    for i in range(len(t)):
        if sample_clock[i] > 0:
            outSig.append(sig[i])
        elif hold_clock[i] > 0:
            outSig.append(outSig[i-1])
        else:
            outSig.append(0)
    if delay > 0:
        tstep = (t[-1]-t[0])/len(t)
        tdelay = (int(1/(tstep*fs)))*delay                              # No es exacto si el clk no es múltiplo del plot sampling
        outSig = [0]*tdelay + outSig[:-tdelay]
    # else:
    #     print('Duty cycles ds and dh must be such that 0<=ds<1, 0<=dh<1 and 0<=ds+dh<1.')
    
    return outSig
