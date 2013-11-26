import pandas as pd, numpy as np
import rolling_windows

data = pd.read_table('preprocess/raw/20101214163931.a.rawwave_label.csv')
grouped = data.groupby(('taskid'))
taskids = grouped.size().keys()
ret = grouped.mean()
# add new columns, to populate below
ret['rolling_median'] = None
ret['rolling_PSD'] = None

for taskid in taskids:
    eeg_signal = grouped.get_group(taskid)[' Value'] # TODO remove space from name

    ret.set_value(taskid, 'rolling_median', rolling_windows.downsampled_rolling_median(eeg_signal, window_size=128))

    window_size = 512
    if len(eeg_signal) >= window_size:
        ret.set_value(taskid, 'rolling_PSD', rolling_windows.rolling_power_ratio(eeg_signal, window_size=512))

outfilename = 'features.pickle'
ret.save(outfilename)
print 'saved features as pickle in file "%s"' % outfilename
