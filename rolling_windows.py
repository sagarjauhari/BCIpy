import pandas as pd
import numpy as np
import pylab
import matplotlib.pyplot as plt

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

    median.plot()
    plt.title('rolling_median, window_size=%s, downsampled to %sHz' % (window_size, freq))
    annotations = [
        plt.annotate(int(val), (step*index, val))
        for index,val in enumerate(downsampled)
        if not np.isnan(val)
        ]
    plt.show()


if __name__ == "__main__":
    f = np.genfromtxt("preprocess/raw_filtered.csv", dtype=None, delimiter=',')
    #ts = pd.Series(d['Value'], index=d['Time'])
    series = pd.Series(f[29000:30000]) # consider adding index
    plot_rolling_functions(series)
    compare_window_sizes(series, (32,64,128,256,512))
    plot_downsampled_rolling_median(series)
