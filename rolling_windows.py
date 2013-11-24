import pandas as pd
import numpy as np
import pylab
import matplotlib.pyplot as plt

"""
d = np.genfromtxt("preprocess/raw/20101214163931.a.rawwave_label.csv", dtype=None, names=True)
ts = pd.Series(d['Value'], index=d['Time'])
pd.rolling_mean(ts, 60).plot()
#pylab.plot([1,2,3])
"""

window_size = 512

f = np.genfromtxt("preprocess/raw_filtered.csv", dtype=None, delimiter=',')
pd.rolling_median(pd.Series(f[20000:30000]),window_size).plot()
pd.rolling_mean(pd.Series(f[20000:30000]),window_size).plot()
pd.rolling_std(pd.Series(f[20000:30000]),window_size).plot()
pd.rolling_skew(pd.Series(f[20000:30000]),window_size).plot()
pd.rolling_kurt(pd.Series(f[20000:30000]),window_size).plot()
pd.rolling_min(pd.Series(f[20000:30000]),window_size).plot()
pd.rolling_max(pd.Series(f[20000:30000]),window_size).plot()
plt.show()
