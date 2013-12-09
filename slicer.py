import pandas as pd, numpy as np
import sys
import rolling_windows
import filters
from dateutil.tz import tzlocal, tzutc
from os.path import join

ALL_RAW_URL='data'
try:
    from dev_settings import *
except ImportError:
    pass

class Slicer(object):
    def __init__(self, taskfile=join(ALL_RAW_URL, 'task.xls')):
        self.load_tasks_from_tsv(taskfile)
        self.series = {}

    def get_tasks(self):
        return self.tasks

    def load_tasks_from_tsv(self, taskfile):
        "reads task data from tab delimited file"
        t = pd.read_table(taskfile, parse_dates=['start_time', 'end_time'], index_col=False)
        t['word_count'] = t.stim.apply(lambda x: len(x.split()))
        t['is_passage'] = t.word_count.apply(lambda x: x > 1)
        self.tasks = t

    def load_series_from_csv(self, seriesname, csvfilelist):
        self.series[seriesname] = pd.concat([
            pd.read_csv(filename, parse_dates=[0], index_col=0,
                squeeze=True).tz_localize(tzutc()).tz_convert(tzlocal())
            for filename in csvfilelist
        ]).sort_index()

    def load_series_from_pickle(self, seriesname, picklefile):
        self.series[seriesname] = pd.read_pickle(picklefile)

    def get_passage_tasks_by_difficulty(self, difficulty, features=[]):
        t = self.tasks
        taskids = t[t.difficulty==difficulty][t.is_passage].index
        return [self.get_by_task_id(taskid, features=features) for taskid in taskids]

    def get_by_task_id(self, taskid, features=[]):
        task = self.tasks.loc[taskid]
        st, et = task['start_time':'end_time']
        st = st.tz_localize(tzlocal())
        et = et.tz_localize(tzlocal())

        task = task.to_dict()
        task.update({f:self.series[f][st:et] for f in features})
        return task

    def extract_first_n_median(self, n=10):
        X = [
            self.get_n_samples_by_taskid(taskid, 'raw_rolling_median_128')
            for taskid in self.tasks.index
        ]
        self.tasks = self.tasks.combine_first(pd.DataFrame(X, index=self.tasks.index))

    def get_n_samples_by_taskid(self, taskid, feature, n=10):
        task = self.tasks.loc[taskid]
        st, et = task['start_time':'end_time']
        st = st.tz_localize(tzlocal())
        et = et.tz_localize(tzlocal())
        ret = np.array([0,0,0,0,0,0,0,0,0,0])
        vals = self.series[feature][st:et][:10] # get up to 10 values
        ret[:len(vals)] = vals[:] # overwrite 0s where vals exist
        return ret

    def print_series_info(self):
        print ["%s: %s" % (k, type(s)) for k,s in self.series.iteritems()]

    def extract_rolling_median(self, seriesname='raw', window_size=128):
        new_feature_name = seriesname+'_rolling_median_'+str(window_size)
        self.series[new_feature_name]=rolling_windows.downsampled_rolling_median(
            self.series[seriesname],
            window_size=window_size
        )

    def extract_rolling_PSD(self, seriesname='raw', window_size=512):
        new_feature_name = seriesname+'_rolling_PSD_'+str(window_size)
        self.series[new_feature_name]=rolling_windows.rolling_power_ratio(
            self.series[seriesname],
            window_size=window_size
        )

    def extract_filtered_signal(self, seriesname='raw', fs=512.0, lowcut=0.1, highcut=20.0):
        self.series[seriesname+'_butter_filtered'] = filters.butter_bandpass_filter(
            self.series[seriesname],
            lowcut=lowcut,
            highcut=highcut,
            fs=fs,
            order=4)

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
