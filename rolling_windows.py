import pandas as pd
import numpy as np
import pylab
import matplotlib.pyplot as plt
import pyeeg
import sys

def plot_rolling_functions(series, window_size=128):
    pd.rolling_median(series,window_size).plot(label='median')
    pd.rolling_mean(series,window_size).plot(label='mean')
    pd.rolling_std(series,window_size).plot(label='std')
    pd.rolling_skew(series,window_size).plot(label='skew')
    pd.rolling_kurt(series,window_size).plot(label='kurt')
    pd.rolling_min(series,window_size).plot(label='min')
    pd.rolling_max(series,window_size).plot(label='max')
    plt.title('Various rolling window functions, window size %s' % (window_size))
    plt.legend()
    plt.show()

def compare_window_sizes(series, sizeList):
    plots = [pd.rolling_median(series, size).plot() for size in sizeList]
    plt.title('Comparison of rolling_median() with different window sizes')
    plt.legend(sizeList)
    plt.show()

    plots = [pd.rolling_mean(series, size).plot() for size in sizeList]
    plt.title('Comparison of rolling_mean() with different window sizes')
    plt.legend(sizeList)
    plt.show()

def downsampled_rolling_median(series, window_size=64, original_freq=512, freq=10):
    step = original_freq/freq
    return pd.rolling_median(series, window_size)[::step]

def plot_downsampled_rolling_median(series, window_size=64, original_freq=512, freq=10):
    median = pd.rolling_median(series, window_size)
    step = original_freq/freq
    downsampled = pd.rolling_median(series, window_size)[::step]
    pd.Series(series).plot()

    downsampled.plot()
    plt.title('rolling_median, window_size=%s, downsampled to %sHz' % (window_size, freq))
    annotations = [
        plt.annotate(int(val), (step*index, val))
        for index,val in enumerate(downsampled)
        if not np.isnan(val)
        ]
    plt.legend(('original', 'rolling_median'))
    plt.show()

def as_strided(series, window_size=512, step=64):
    assert len(series) >= window_size
    shape = ((len(series)-window_size)/step, window_size) # to find number of rows, discard one window_size and divide by step size
    strides = (series.strides[0]*step, series.strides[0]) # rearrange strides to move rows by step size and columns by indvidual value size
    return np.lib.stride_tricks.as_strided(series, shape=shape, strides=strides)

def rolling_power_ratio(series, bands=[0.5,4,7,12,30], sample_rate=512, window_size=512, step=64):
    return np.array([
        pyeeg.bin_power(window, bands, sample_rate)[1]
        for window in as_strided(series, window_size=window_size, step=step)
    ])

def rolling_power(series, bands=[0.5,4,7,12,30], sample_rate=512):
    return [ pyeeg.bin_power(window, bands, sample_rate)[0] for window in as_strided(series) ]

def plot_power_ratio(series):
    [pd.Series(freq_band).plot() for freq_band in np.transpose(rolling_power_ratio(series))]
    #plt.gca().add_patch(Rectangle((1,1),1,1))
    plt.show()

def print_help():
    print 'Usage: %s [csvfile] [cmd] ... [cmd]' % sys.argv[0]


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print_help()
        sys.exit()

    filename = sys.argv[1]
    f = pd.read_csv(filename)[' Value']
    #ts = pd.Series(d['Value'], index=d['Time'])
    shortseries = pd.Series(f[29000:30000]) # consider adding index

    mainfuncs = {
        'help': lambda: print_help(),
        'plotroll': lambda: plot_rolling_functions(shortseries),
        'compare_window_sizes': lambda: compare_window_sizes(shortseries, (32,64,128,256,512)),
        'plot_downsampled_rolling_median': lambda: plot_downsampled_rolling_median(f[0:9000], window_size=64),
        'plot_power_ratio': lambda: plot_power_ratio(f)
    }

    cmds = sys.argv[2:]
    for cmd in cmds:
        print 'running command %s' % cmd
        mainfuncs.get(cmd, print_help)()
        
    sys.exit()
