# /usr/bin/env python
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

from slicer import Slicer
from matplotlib import pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import sys
import pandas as pd

def do_charts(slicer, pdfpages):
    print "\n***Generating Charts***"
    print "Extracting rolling medians"
    slicer.extract_rolling_median(seriesname='raw', window_size=32)
    slicer.extract_rolling_median(seriesname='raw', window_size=64)
    slicer.extract_rolling_median(seriesname='raw', window_size=128)
    
    start = pd.to_datetime('2009-12-14 16:56:55-05:00')
    end = pd.to_datetime('2011-12-14 16:56:58-05:00')
    
    raw = slicer.series['raw'][start:end]
    rm32 = slicer.series['raw_rolling_median_32'][start:end]
    rm64 = slicer.series['raw_rolling_median_64'][start:end]
    rm128 = slicer.series['raw_rolling_median_128'][start:end]
    
    print "Plotting"
    raw.plot()
    rm32.plot()
    rm64.plot()
    rm128.plot()
    plt.legend(('Raw 512Hz EEG', '32 samples per window', '64 samples per window',
    '128 samples per window'))
    plt.title('10 Hz rolling median, compared to 512Hz signal')
    pdfpages.savefig()
    
    #print raw, rm
    #slicer.extract_first_n_median() # for each task, extract first 10 and add to as columns to tasks DataFrame

if __name__=="__main__":
    slicer = Slicer()
    print 'loading raw from list of csvfiles'
    slicer.load_series_from_csv('raw', sys.argv[1:])
    pp = PdfPages('rolling_median.pdf')
    do_charts(slicer, pp)
    pp.close()
