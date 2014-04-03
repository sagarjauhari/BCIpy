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
import rolling_windows
from os.path import join

try: # Import config params
   from dev_settings import *
except ImportError:
   print "Please create a dev_settings.py. Example: dev_settings.py.example"

data = pd.read_table(join(SAVE_URL,'raw','20101214163931.a.rawwave_label.csv'))
grouped = data.groupby(('taskid'))
taskids = grouped.size().keys()
ret = grouped.mean()
# add new columns, to populate below
ret['rolling_median'] = None
ret['rolling_PSD'] = None

for taskid in taskids:
    eeg_signal = grouped.get_group(taskid)[' Value']
    # TODO remove space from name

    ret.set_value(taskid, 'rolling_median',
                  rolling_windows.downsampled_rolling_median(eeg_signal,
                                                             window_size=128))

    window_size = 512
    if len(eeg_signal) >= window_size:
        ret.set_value(taskid, 'rolling_PSD',
                      rolling_windows.rolling_power_ratio(eeg_signal,
                                                          window_size=512))

outfilename = 'features.pickle'
ret.save(outfilename)
print 'saved features as pickle in file "%s"' % outfilename
