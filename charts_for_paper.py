from slicer import Slicer
from matplotlib import pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import sys
import pandas as pd

slicer = Slicer()
print 'loading raw from list of csvfiles'
slicer.load_series_from_csv('raw', sys.argv[1:])
slicer.extract_rolling_median(seriesname='raw', window_size=32)
slicer.extract_rolling_median(seriesname='raw', window_size=64)
slicer.extract_rolling_median(seriesname='raw', window_size=128)

start = pd.to_datetime('2010-12-14 16:56:55-05:00')
end = pd.to_datetime('2010-12-14 16:56:58-05:00')

raw = slicer.series['raw'][start:end]
rm32 = slicer.series['raw_rolling_median_32'][start:end]
rm64 = slicer.series['raw_rolling_median_64'][start:end]
rm128 = slicer.series['raw_rolling_median_128'][start:end]

raw.plot()
rm32.plot()
rm64.plot()
rm128.plot()
plt.legend(('Raw 512Hz EEG', '32 samples per window', '64 samples per window',
'128 samples per window'))
plt.title('10 Hz rolling median, compared to 512Hz signal')
pp = PdfPages('rolling_median.pdf')
pp.savefig()
pp.close()
#print raw, rm
#slicer.extract_first_n_median() # for each task, extract first 10 and add to as columns to tasks DataFrame
