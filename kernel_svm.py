# -*- coding: utf-8 -*-
"""
Created on Sat Nov 23 14:49:07 2013

@author: sagar
"""

from sklearn import svm


try: # Import config params
   from dev_settings import *
except ImportError:
   print "Please create a dev_settings.py using dev_settings.py.example as\
          an example"
from os.path import join
from eegml import *

#From Bao Hong Tan's Thesis - p16
fs = 512.0
lowcut = 0.1
highcut = 5.0

#plot_butter(fs, lowcut, highcut, [1,2,3,4])
raw_dir = join(SAVE_URL,'raw')

file_in = join(raw_dir, "20101214163931.a.rawwave_label.csv")

with open(join(raw_dir,file_in)) as fi:
    fr=csv.reader(fi, delimiter='\t')
    next(fr)#header
    data=list(fr)

filtered_data = do_filter_signal(data, lowcut, highcut, fs, 3, None)

#==============================================================================
# SVM
#==============================================================================
l=20000
# SVM Fit
clf = svm.SVC(kernel='linear')
clf.fit([[i] for i in filtered_data[0:l]], [i[2] for i in data[0:l]])

# SVM Predict
idx_svm = clf.predict([i[1] for i in filtered_data[0:l]])
    