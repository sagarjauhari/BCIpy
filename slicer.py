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

import pandas as pd, numpy as np
import sys
import rolling_windows
import filters
import pytz
from os.path import join

ALL_RAW_URL='data'
try:
    from dev_settings import *
except ImportError:
    pass

class Slicer(object):
    """Loads data and metadata, extracts important features, and provides methods to retrieve subsets"""

    def __init__(self, taskfile=join(ALL_RAW_URL, 'task.xls')):
        self.load_tasks_from_tsv(taskfile)
        self.series = {}

    def get_tasks(self):
        return self.tasks

    def load_tasks_from_tsv(self, taskfile):
        """Reads task data from tab delimited file"""
        t = pd.read_table(taskfile, parse_dates=['start_time', 'end_time'], index_col=False)
        t['word_count'] = t.stim.apply(lambda x: len(x.split()))
        t['is_passage'] = t.word_count.apply(lambda x: x > 1)
        self.tasks = t

    def load_series_from_csv(self, seriesname, csvfilelist):
        """Reads a single series from a CSV file and merges it with the current data"""
        if csvfilelist==None or len(csvfilelist)==0:
            raise Exception("No files to process!")
       
        self.series[seriesname] = pd.concat([
            pd.read_csv(filename, parse_dates=[0], index_col=0,
                squeeze=True).tz_localize(pytz.UTC).tz_convert(pytz.timezone('US/Eastern'))
            for filename in csvfilelist
        ]).sort_index()

    def load_series_from_pickle(self, seriesname, picklefile):
        """For quick restore from previous Slicer state"""
        self.series[seriesname] = pd.read_pickle(picklefile)

    def get_passage_tasks_by_difficulty(self, difficulty, features=[]):
        """Gets data for only the tasks which have the specified difficulty, along with any features specified in the 'features' arg"""
        t = self.tasks
        taskids = t[t.difficulty==difficulty][t.is_passage].index
        return [self.get_by_task_id(taskid, features=features) for taskid in taskids]

    def get_by_task_id(self, taskid, features=[]):
        """Get just one task, by taskid, with the features specified in the 'features' arg"""
        task = self.tasks.loc[taskid]
        st, et = task['start_time':'end_time']
        st = st.tz_localize(pytz.timezone('US/Eastern'))
        et = et.tz_localize(pytz.timezone('US/Eastern'))

        task = task.to_dict()
        task.update({f:self.series[f][st:et] for f in features})
        return task
        
    def extract_first_n_raw(self, n=10):
        """
        Extract the first 'n' samples for each task's raw data
        and save in self.tasks
        """
        X = [
            self.get_n_samples_by_taskid(taskid, 'raw', n)
            for taskid in self.tasks.index
        ]
        self.tasks = self.tasks.combine_first(pd.DataFrame(X, index=self.tasks.index))

    def extract_first_n_median(self, n=10):
        """Extracts just the first n samples from the rolling median, 
        primarily to normalize sample vectors to the same length.
        To the existing dataframe, adds additional 'n' columns which are the 1st
        'n' values of the rolling median for each task. 
        """
        X = [
            self.get_n_samples_by_taskid(taskid, 'raw_rolling_median_128', n)
            for taskid in self.tasks.index
        ]
        self.tasks = self.tasks.combine_first(pd.DataFrame(X, index=self.tasks.index))

    def get_n_samples_by_taskid(self, taskid, feature, n=10):
        """For the specified taskid, return just the first n samples"""
        task = self.tasks.loc[taskid]
        st, et = task['start_time':'end_time']
        st = st.tz_localize(pytz.timezone('US/Eastern'))
        et = et.tz_localize(pytz.timezone('US/Eastern'))
        ret = np.array([0]*n)
        vals = self.series[feature][st:et][:n] # get up to n values
        ret[:len(vals)] = vals[:] # overwrite 0s where vals exist
        return ret
        
    def get_time_duration_by_taskid(self, taskid):
        """
        Returns task duration in seconds
        """
        task = self.tasks.loc[taskid]
        st, et = task['start_time':'end_time']
        st = st.tz_localize(pytz.timezone('US/Eastern'))
        et = et.tz_localize(pytz.timezone('US/Eastern'))
        return (et - st).microseconds/1000000.0
        

    def print_series_info(self):
        """Prints info about all series available, primarily for debugging purposes"""
        print ["%s: %s" % (k, type(s)) for k,s in self.series.iteritems()]

    def extract_rolling_median(self, seriesname='raw', window_size=128):
        """Extracts a rolling median for the specified series"""
        print "Extracting rolling median: name=%s window_size=%d" \
                                                 % (seriesname, window_size)

        new_feature_name = seriesname+'_rolling_median_'+str(window_size)
        self.series[new_feature_name]=rolling_windows.downsampled_rolling_median(
            self.series[seriesname],
            window_size=window_size
        )

    def extract_rolling_PSD(self, seriesname='raw', window_size=512):
        """Extracts power spectral density (PSD) for the specified series"""
        new_feature_name = seriesname+'_rolling_PSD_'+str(window_size)
        self.series[new_feature_name]=rolling_windows.rolling_power_ratio(
            self.series[seriesname],
            window_size=window_size
        )

    def extract_filtered_signal(self, seriesname='raw', fs=512.0, lowcut=0.1, highcut=20.0):
        """Applies a Butterworth bandpass filter to the specified series"""
        self.series[seriesname+'_butter_filtered'] = filters.butter_bandpass_filter(
            self.series[seriesname],
            lowcut=lowcut,
            highcut=highcut,
            fs=fs,
            order=4)

# If run from the command line, do some basic tests and ouput some debugging info
if __name__ == '__main__':
    print 'instantiating task slicer'
    s = Slicer()

    if len(sys.argv) > 2:
        print 'loading raw from list of csvfiles'
        s.load_series_from_csv('raw', sys.argv[1:])
    else:
        print 'loading raw from pickle'
        s.load_series_from_pickle('raw', sys.argv[1])

    print 'extracting filtered signal'
    s.extract_filtered_signal()
    print 'extracting rolling median'
    s.extract_rolling_median()
    print 'extracting rolling PSD'
    s.extract_rolling_PSD()
    print 'fetching task 1, with features'
    print s.get_by_task_id(1, features=['raw','raw_rolling_PSD_512', 'raw_rolling_median_128'])
    print s.get_passage_tasks_by_difficulty(2, features=['raw','raw_rolling_PSD_512', 'raw_rolling_median_128'])
    print [(d['SUBJECT'], len(d['raw'])) for d in s.get_passage_tasks_by_difficulty(1, features=['raw'])]
    s.print_series_info()
