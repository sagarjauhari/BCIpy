# -*- coding: utf-8 -*-
"""
Created on Sat Nov 23 14:49:07 2013

@author: sagar
"""

from sklearn import svm
import pickle
from sklearn.metrics import classification_report



try: # Import config params
   from dev_settings import *
except ImportError:
   print "Please create a dev_settings.py using dev_settings.py.example as\
          an example"
from os.path import join
from eegml import *

with open('features.pickle','r') as fi:
    rol_feat = pickle.load(fi)

# find task IDs where atleast 10 values are present
features=[]
targets=[]
for i in range(135):
    g1 = [f for f in rol_feat['rolling_median'][i][3:13]]
    g2 = rol_feat['Difficulty'][i]
    if len(g1) >= 10 and 1<=g2<=2:
        features.append(g1)
        targets.append(g2)


#==============================================================================
# SVM
#==============================================================================
# SVM Fit
clf = svm.SVC(kernel='linear')
clf.fit(features, targets)

# SVM Predict
class_pred = list(clf.predict(features))

# Report
print classification_report(targets, class_pred)