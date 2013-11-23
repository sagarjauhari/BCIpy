from eegml import *
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
compress_time_labels(join(SAVE_URL,"task_xls_labels.csv"))

from os import listdir
from os.path import isfile, join
import re

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
# Raw Data
#==============================================================================
raw_dir=join(DATA_URL,'raw')
mach_dict = create_dict_machine_data(raw_dir)

format_task_xls("task_for_raw")


if not os.path.exists(join(SAVE_URL,'raw')):
    os.makedirs(join(SAVE_URL,'raw'))

# Label each raw machine file
for i in mach_dict:
    file_in = join(raw_dir, mach_dict[i]+"."+i+".rawwave.csv")
    file_out =join(raw_dir, mach_dict[i]+"."+i+".rawwave_microsec.csv")
    create_raw_incremental(file_in,file_out)
    
    label_data_raw(file_out,
                 join(SAVE_URL,'raw', mach_dict[i]+"."+i+".rawwave_label.csv"),
                 join(SAVE_URL, "task_for_raw_xls_labels.csv"),
                 i, mach_dict[i])

#==============================================================================
# Plot raw signal
#==============================================================================
with open(join(SAVE_URL, "raw_incremental_label.csv"), 'r') as fi:
    fr = csv.reader(fi, delimiter='\t')
    next(fr)#header
    
    data = list(fr)
    time_x = [i[0] for i in data]
    signal_x = [i[1] for i in data]
    
    plot_signal(time_x, signal_x, 'Raw Signal - whole')
    plot_signal(time_x[0:1000], signal_x[0:1000], 'Raw Signal - 0-1000')
    plot_signal(time_x[315000:len(time_x)], signal_x[315000:len(signal_x)],\
                        'Raw Signal - 315000 - end')

#==============================================================================
# Filters and Power spectrum
#==============================================================================
#From Bao Hong Tan's Thesis - p16
fs = 512.0
lowcut = 0.1
highcut = 20.0

plot_butter(fs, lowcut, highcut, [1,2,3,4,5,6,7,8])
do_filter_signal(data, lowcut, highcut, fs, 4,
                 join(SAVE_URL,'raw_filtered.csv'))
                 
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
cln_data = clean_all(subj_list, subj_data)
pickle.dump(cln_data,open(join(SAVE_URL,"cln_data.pickle"),'wb'))

plot_cleaned_counts(subj_data, cln_data)
plot_subjects(subj_list, cln_data, 4)

#==============================================================================
# Random Forest Classifier
#    Bib: [Breiman, Leo. "Random forests." Machine learning 45.1 (2001): 5-32.]
#    Brief overview: http://blog.yhathq.com/posts/random-forests-in-python.html
# This classifier is often as the first technique to find out obvious and 
# sometimes not-so-obvious relationships
#==============================================================================
subj_id = 27

df = pd.DataFrame({'att':[int(i[2]) for i in cln_data[subj_id]],
                    'med':[int(i[3]) for i in cln_data[subj_id]],
                    'difficulty':[int(i[4]) for i in cln_data[subj_id]]})
df['is_train'] = np.random.uniform(0, 1, len(df)) <= .75
df.head()

from sklearn.metrics import classification_report

train, test = df[df['is_train']==True], df[df['is_train']==False]
features = df.columns[[0,2]]

clf = RandomForestClassifier(n_jobs=2)
clf.fit(train[features], train['difficulty'])

preds = clf.predict(test[features])

print classification_report(test['difficulty'], preds)
pd.crosstab(test['difficulty'], preds, rownames=['actual'], colnames=['preds'])

#==============================================================================
# Justis' idea of analysing the correlation between time taken to read a 
# sentence with the difficulty
# Correlation - Pearson's R value
# Header of task.xls
# ['machine', 'SUBJECT', 'start_time', 'end_time', 'stim', 'block', 'pool', 
#                                     'modality', 'TEXT', 'difficulty']
#==============================================================================
get_num_words(DATA_URL)