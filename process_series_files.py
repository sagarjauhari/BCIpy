import sys, os
from os.path import isfile, join
import re
import dateutil.tz
import pandas as pd
import numpy as np
from datetime import datetime

# Create dict of machine data
def create_dict_machine_data(raw_dir):
    onlyfiles_raw = [ f for f in os.listdir(raw_dir) if isfile(join(raw_dir,f)) ]
    pat_raw = re.compile("[0-9]*\.[a-z0-9]*\.rawwave\.csv")
    temp_dat_raw = [f.split('.')[0:2] for f in onlyfiles_raw if pat_raw.match(f)]
    mach_dict = {i[1]: i[0] for i in temp_dat_raw}
    return mach_dict

def create_raw_incremental(in_file, out_file, time_t, tzinfo=dateutil.tz.tzlocal()):
    "Create raw file with incremental miliseconds"
    raw = pd.read_csv(in_file, index_col=False) # avoid index to keep it from sorting

    day = time_t[0:4]+"-"+time_t[4:6]+"-"+time_t[6:8]

    # Incoming data has 512Hz samples with timestamps at resolution of one
    # second. For each second, convert the first timestamp to epoch time and
    # blank out the others so that we can do linear interpolation.
    # TODO estimate microseconds on first and last second, to avoid timestretch
    # TODO analyze clock skew, since some seconds have more or less samples
    # TODO consider a pandas.DatetimeIndex with just a start time and frequency
    prev_time = None
    for i,row in raw.iterrows():
        timestamp = row['%Time']
        if timestamp==prev_time:
            raw.set_value(i, '%Time', np.NaN)
        else:
            timestring = day + ' ' + timestamp + '.0'
            dt = datetime.strptime(timestring, '%Y-%m-%d %H:%M:%S.%f')\
                .replace(tzinfo=tzinfo) # set specified tz before conversion
            # time since UTC 1970-01-01 00:00:00, in seconds
            dt = float(dt.strftime('%s.%f'))
            raw.set_value(i, '%Time', dt)
        prev_time = timestamp

    # reindex with interpolated timestamps
    raw.index = pd.DatetimeIndex(
        pd.to_datetime(raw['%Time']\
            .convert_objects(convert_numeric=True)\
            .interpolate(), unit='s')
    ).tz_localize('UTC').tz_convert(tzinfo) # convert back to original tz
    raw.to_csv(out_file, index=True, cols=['Value'])
    return raw

def process_all_in_dir(indir, outdir):
    if not os.path.exists(outdir):
        os.makedirs(outdir)
    mach_dict = create_dict_machine_data(indir)
    for i in mach_dict:
        file_in = join(indir, mach_dict[i]+"."+i+".rawwave.csv")
        print "processing file %s" % file_in
        file_out =join(outdir, mach_dict[i]+"."+i+".rawwave_microsec.csv")
        create_raw_incremental(file_in,file_out, mach_dict[i])

if __name__ == '__main__':
    indir,outdir=sys.argv[1:3]
    process_all_in_dir(indir,outdir)
