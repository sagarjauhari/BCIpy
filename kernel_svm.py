# -*- coding: utf-8 -*-
"""
Created on Sat Nov 23 14:49:07 2013

@author: sagar
"""

from sklearn import svm
import pickle
from sklearn.metrics import classification_report, accuracy_score
from sklearn import cross_validation
from sklearn.cross_validation import StratifiedKFold
from sklearn.grid_search import GridSearchCV

# example from Justis
from slicer import Slicer
import sys
slicer = Slicer()
print 'loading raw from list of csvfiles'
slicer.load_series_from_csv('raw', sys.argv[1:])
slicer.extract_rolling_median(seriesname='raw', window_size=128)
slicer.extract_first_n_median()
tasks = slicer.get_tasks()
passage_tasks = tasks[tasks.is_passage==True]
d1_tasks = passage_tasks[passage_tasks.difficulty==1]
d2_tasks = passage_tasks[passage_tasks.difficulty==2]
print d2_tasks
sys.exit()



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
# SVM - Linear
clf = svm.SVC(kernel='linear')
clf.fit(features, targets)
class_pred = list(clf.predict(features))
print classification_report(targets, class_pred)

# SVM - Radial Basis Function kernel
# Ref - http://scikit-learn.org/stable/modules/generated/sklearn.svm.SVC.html#sklearn.svm.SVC.predict_proba
clf = svm.SVC(kernel='rbf', probability=True)
clf.fit(features, targets)
class_pred = list(clf.predict_proba(features))
print classification_report(targets, [[1,2][int(i[0]*2)] for i in class_pred])

# SVM, radial basis function, cross validation
clf = svm.SVC(kernel='rbf', probability=True)
scores = cross_validation.cross_val_score(clf, array(features), array(targets),
                                          cv=10)
print "Using RBF kernel and 5 fold cross validation"
print("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))


#==============================================================================
# GridSearch CV
# http://scikit-learn.org/dev/auto_examples/grid_search_digits.html
#==============================================================================
# Hold out 20% for final scores
skf = StratifiedKFold(targets, 5)
for train, test in skf:
    break
X_train = [features[i] for i in train]
y_train = [targets[i] for i in train]
X_test = [features[i] for i in test]
y_test = [targets[i] for i in test]

# Set the parameters by cross-validation
tuned_parameters = [{'kernel': ['rbf'], 'gamma': [1e-3, 1e-4],
                     'C': [1, 10, 100]},
                    {'kernel': ['linear'], 'C': [1, 10, 100]}]
svr = svm.SVC()
clf = GridSearchCV(svr, tuned_parameters)
clf.fit(array(X_train), array(y_train))
y_pred = clf.predict(X_test)
print "Using RBF kernel, grid-search, holding out 20% data for reporting final scores"
print(classification_report(y_test, y_pred))
print 'Accuracy: ',accuracy_score(y_test, y_pred)
