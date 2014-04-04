# Copyright 2013, 2014 Justis Grant Peters and Sagar Jauhari

# This file is part of BCIpy.
# 
# BCIpy is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# BCIpy is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with BCIpy.  If not, see <http://www.gnu.org/licenses/>.

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
    show()

# use filtered data
data=pd.read_csv(join(SAMPLE_URL,'20101214163931.a.rawwave.csv'))
plotSpectrum(list(data[' Value'])[0:90000], 512)
