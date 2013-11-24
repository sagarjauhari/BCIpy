# -*- coding: utf-8 -*-
"""
Created on Mon Nov 18 22:38:56 2013

@author: sagar
"""


from numpy import sin, linspace, pi
from pylab import plot, show, title, xlabel, ylabel, subplot
from scipy import fft, arange
import pandas as pd
from os.path import join

try:
    from dev_settings import *
except:
    pass


def plotSpectrum(y,Fs):
    """
    Plots a Single-Sided Amplitude Spectrum of y(t)
    """
    n = len(y) # length of the signal
    k = arange(n)
    T = n/Fs
    frq = k/T # two sides frequency range
    frq = frq[range(n/2)] # one side frequency range
    
    Y = fft(y)/n # fft computing and normalization
    Y = Y[range(n/2)]
     
    plot(frq,abs(Y),'r') # plotting the spectrum
    xlabel('Freq (Hz)')
    ylabel('|Y(freq)|')

# use filtered data
data=pd.read_csv(join(SAMPLE_URL,'20101214163931.a.rawwave.csv'))
plotSpectrum(list(data[' Value'])[0:1000000], 512)