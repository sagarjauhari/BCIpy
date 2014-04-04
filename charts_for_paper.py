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
import matplotlib
from matplotlib import pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import sys
import pandas as pd

def do_charts(slicer, pdfpages):
    print "\n***Generating Charts***"
    
    fig, ax = plt.subplots(figsize=(7, 6), dpi=80)    

    start = pd.to_datetime('2010-12-13 13:54:10.5-05:00')
    end = pd.to_datetime('2010-12-13 13:54:11.5-05:00')
    
    window_sizes = [32, 64, 128]
    raw = slicer.series['raw'][start:end]
    raw.plot()
    
    for ws in window_sizes:
        slicer.extract_rolling_median(seriesname = 'raw', window_size = ws)
        rm = slicer.series['raw_rolling_median_' + str(ws)][start:end]
        rm.plot(xticks=[i for i in rm.index])
    
    plt.legend(['512Hz EEG']+[ 'Rolling Median %d window size' % ws \
                                for ws in window_sizes]
                                ,loc='best')
    plt.ylabel(r"Potential ($\mu$V)")
    plt.xlabel(r"Time ($\mu$Sec)")
    #plt.title('10 Hz rolling median, compared to 512Hz signal')
    ax.xaxis.set_major_formatter(matplotlib.dates.DateFormatter('%S.%f'))
    ax.set_ylim(ax.get_ylim()[::-1])
    pdfpages.savefig()
    #plt.show()
   
if __name__=="__main__":
    slicer = Slicer()
    print 'loading raw from list of csvfiles'
    slicer.load_series_from_csv('raw', sys.argv[1:])
    pp = PdfPages('rolling_median.pdf')
    do_charts(slicer, pp)
    pp.close()
