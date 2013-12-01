import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import butter, lfilter, freqz
import csv

def butter_bandpass(lowcut, highcut, fs, order=5):
    """
    http://wiki.scipy.org/Cookbook/ButterworthBandpass
    """
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return b, a

# Default lowcut and highcut are from Bao Hong Tan's Thesis - p16
def butter_bandpass_filter(data, lowcut=0.1, highcut=20.0, fs=512.0, order=5):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    return pd.TimeSeries(lfilter(b, a, data), index=data.index.copy())

def plot_butter(fs, lowcut, highcut, orders):
    """Plot the frequency response for a few different orders."""
    plt.figure()
    plt.clf()
    for order in orders:
        b, a = butter_bandpass(lowcut, highcut, fs, order=order)
        w, h = freqz(b, a, worN=2000)
        plt.plot((fs * 0.5 / np.pi) * w, abs(h), label="order = %d" % order)
        plt.title("Sample frequency responses of the band filter")
        plt.xlabel('Frequency (Hz)')
        plt.ylabel('Gain')
        plt.grid(True)
        plt.legend(loc='best')

def do_filter_signal(data, low_cut, high_cut, fs, order, out_file):
    data_np = data['Value']
    data_filtered = butter_bandpass_filter(data_np,
                                           low_cut,
                                           high_cut,
                                           fs,
                                           order)
    limit=2000

    fig, ax = plt.subplots()
    ax.plot(data[0:limit], label="Original Signal")
    ax.plot(data_filtered[0:limit], label="Filtered Signal")
    plt.grid(True)
    plt.legend(loc='best')
    plt.title("data[0:"+str(limit)+"]")

    if out_file is not None:
        with open(out_file,'w') as fo:
            fw = csv.writer(fo)
            fw.writerow(list(data_filtered))

    return data_filtered
