from eegml import *
from os.path import join

try: # Import config params
   from dev_settings import *
except ImportError:
   print "Please create a dev_settings.py using dev_settings.py.example as an example"

format_task_xls()
compress_time_labels(join(SAVE_URL,"task_xls_labels.csv"))

from os import listdir
from os.path import isfile, join
import re

onlyfiles = [ f for f in listdir(DATA_URL) if isfile(join(DATA_URL,f)) ]
pat = re.compile("[0-9]*\.[0-9]*\.combined\.csv")
temp_dat = [f.split('.')[0:2] for f in onlyfiles if pat.match(f)]
sub_dict = {i[1]: i[0] for i in temp_dat}

for i in sub_dict:
    label_data(DATA_URL + "/"+sub_dict[i] + "." +i+".combined.csv",
            SAVE_URL + "/task_xls_labels.csv",
            SAVE_URL + "/"+sub_dict[i] + "." +i+".labelled.csv",
            i, sub_dict[i])

create_raw_incremental(join(DATA_URL, "20101214163931.a.rawwave.csv"),
                       join(SAVE_URL,"raw_incremental.csv"))
label_data_raw_signal(join(SAVE_URL,"raw_incremental.csv"),
            join(SAVE_URL,"task_xls_labels.csv"),
            join(SAVE_URL,"raw_incremental_label.csv"))
