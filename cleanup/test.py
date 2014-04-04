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

from eegml import *
import filters
import data_cleaning
from os.path import join
import pickle
from sklearn.ensemble import RandomForestClassifier
import pandas as pd

try: # Import config params
   from dev_settings import *
except ImportError:
   print "Please create a dev_settings.py using dev_settings.py.example as\
          an example"

format_task_xls("task")

from os import listdir
from os.path import isfile, join
import re

# Plot the values of different orders of Butterworth filter
# Lowcut and highcut values are from Bao Hong Tan's Thesis - p16
filters.plot_butter(512.0, 0.1, 20.0, [1,2,3,4,5,6,7,8])

#==============================================================================
# 1Hz Data
#==============================================================================
# Create dict of subject data
onlyfiles = [ f for f in listdir(DATA_URL) if isfile(join(DATA_URL,f)) ]
pat = re.compile("[0-9]*\.[0-9]*\.combined\.csv")
temp_dat = [f.split('.')[0:2] for f in onlyfiles if pat.match(f)]
sub_dict = {i[1]: i[0] for i in temp_dat}

# Label each subject file
for i in sub_dict:
    label_data(DATA_URL + "/"+sub_dict[i] + "." +i+".combined.csv",
            SAVE_URL + "/task_xls_labels.csv",
            SAVE_URL + "/"+sub_dict[i] + "." +i+".labelled.csv",
            i, sub_dict[i])

#==============================================================================
# Individual 1hz data of subjects
#==============================================================================
subj_list = get_subject_list(SAVE_URL)
subj_data = get_data(subj_list, SAVE_URL)
plot_subjects(subj_list, subj_data, 4)

# Data Cleaning
"""
Looks like some of the subjects like 24 have all '0' attention and meditation 
values. Also, at several places, the quality value of signals is 'non-zero'. 
In Tan's thesis, they have discarded the entire trial if the quality was non 
zero:

A trial was considered good if the quality signal indicated a value of 0 for 
the duration of the entire trial, that is, the level of noise present in the 
trial was acceptable; otherwise, the trial was excluded from analyses in this 
thesis.

However, initial plan is to remove just the data for the time slots 
corresponding to non-zero quality
"""
cln_data = data_cleaning.clean_all(subj_list, subj_data)
pickle.dump(cln_data,open(join(SAVE_URL,"cln_data.pickle"),'wb'))

data_cleaning.plot_cleaned_counts(subj_data, cln_data)
plot_subjects(subj_list, cln_data, 4)

#==============================================================================
# Justis' idea of analysing the correlation between time taken to read a 
# sentence with the difficulty
# Correlation - Pearson's R value
# Header of task.xls
# ['machine', 'SUBJECT', 'start_time', 'end_time', 'stim', 'block', 'pool', 
#                                     'modality', 'TEXT', 'difficulty']
#==============================================================================
get_num_words(DATA_URL)
