import pandas as pd, numpy as np
import sys
import rolling_windows

class Slicer(object):
    def __init__(self, taskfile='data/task.xls'):
        self.load_tasks_from_tsv(taskfile)
        self.series = {}

    def load_tasks_from_tsv(self, taskfile):
        "reads task data from tab delimited file"
        self.tasks = pd.read_table(taskfile,
            parse_dates=['start_time', 'end_time'], index_col=False)

    def load_series_from_csv(self, seriesname, csvfile):
        try: # assume a list of files
            self.series[seriesname] = pd.concat([pd.read_csv(filename, parse_dates=[0], index_col=0,
                squeeze=True) for filename in csvfile]).sort_index()
        except TypeError:
            self.series[seriesname] = pd.read_csv(csvfile, parse_dates=[0], index_col=0, squeeze=True)

    def load_series_from_pickle(self, seriesname, picklefile):
        self.series[seriesname] = pd.read_pickle(picklefile)

    def get_by_task_id(self, taskid, features=[]):
        task = self.tasks.loc[taskid]
        st, et = task['start_time':'end_time']

        task = task.to_dict()
        task.update({f:self.series[f].between_time(st,et) for f in features})
        return task

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

if __name__ == '__main__':
    print 'instantiating task slicer'
    s = Slicer()

    if len(sys.argv) > 2:
        print 'loading raw from list of csvfiles'
        s.load_series_from_csv('raw', sys.argv[1:])
    else:
        print 'loading raw from pickle'
        s.load_series_from_pickle('raw', sys.argv[1])

    s.print_series_info()
    print 'extracting rolling median'
    s.extract_rolling_median()
    print 'extracting rolling PSD'
    s.extract_rolling_PSD()
    print 'fetching task 1, with features'
    print s.get_by_task_id(1, features=['raw','raw_rolling_PSD_512', 'raw_rolling_median_128'])
