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
from os.path import join, isfile
from os import listdir
import re
from slicer import Slicer

# example from Justis
"""
from slicer import Slicer
import sys
slicer = Slicer()
print 'loading raw from list of csvfiles'
slicer.load_series_from_csv('raw', sys.argv[1:]) # load raw from args
slicer.extract_rolling_median(seriesname='raw', window_size=128) # extract rolling median for entire 'raw' series
slicer.extract_first_n_median() # for each task, extract first 10 and add to as columns to tasks DataFrame
tasks = slicer.get_tasks() # get the tasks DataFrame
passage_tasks = tasks[tasks.is_passage==True]
d1_tasks = passage_tasks[passage_tasks.difficulty==1]
d2_tasks = passage_tasks[passage_tasks.difficulty==2]
print d2_tasks
sys.exit()
"""


try: # Import config params
   from dev_settings import *
except ImportError:
   print "Please create a dev_settings.py using dev_settings.py.example as\
          an example"
from eegml import *

def get_values_single_subject():
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
    return features, targets


#==============================================================================
# SVM
#==============================================================================
# SVM - Linear
def do_SVM_linear():
    features, targets = get_values_single_subject()
    clf = svm.SVC(kernel='linear')
    clf.fit(features, targets)
    class_pred = list(clf.predict(features))
    print classification_report(targets, class_pred)
    
    # SVM - Radial Basis Function kernel
    # Ref - http://scikit-learn.org/stable/modules/generated/sklearn.svm.SVC.html
    #sklearn.svm.SVC.predict_proba
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
def create_train_test():
    skf = StratifiedKFold(targets, 5)
    for train, test in skf:
        break
    X_train = [features[i] for i in train]
    y_train = [targets[i] for i in train]
    X_test = [features[i] for i in test]
    y_test = [targets[i] for i in test]
    

def do_grid_cv_svc(X_train, y_train, X_test, y_test):
    # Set the parameters by cross-validation
    tuned_parameters = [{'kernel': ['rbf'], 'gamma': [1e-3, 1e-4],
                         'C': [1, 10, 100]},
                        {'kernel': ['linear'], 'C': [1, 10, 100]}]
    svr = svm.SVC()
    clf = GridSearchCV(svr, tuned_parameters)
    clf.fit(array(X_train), array(y_train))
    y_pred = clf.predict(X_test)
    print "Using RBF kernel, grid-search, holding out 20% data for reporting final\
             scores"
    print(classification_report(y_test, y_pred))
    print 'Accuracy: ',accuracy_score(y_test, y_pred)

def do_non_lin_svc(X_train, y_train, X_test, y_test):
    clf = svm.SVC()
    clf.fit(array(X_train), array(y_train))
    y_pred = clf.predict(X_test)
    print(classification_report(y_test, y_pred))
    print 'Accuracy: ',accuracy_score(y_test, y_pred)
    
#==============================================================================
# SVM with Slicer 
#==============================================================================
def get_raw_file_list():
    preproc_dir = join(ALL_RAW_URL,'preprocess')
    onlyfiles=[f for f in listdir(preproc_dir) if isfile(join(preproc_dir,f))]
    pat = re.compile("[0-9]*\.[0-9]*\.rawwave_microsec\.csv")
    return [f for f in onlyfiles if pat.match(f)]
    
def check_all_zeros(mat2d):
    """
    returns true if all values are zero
    """
    x_size = len(mat2d)
    y_size = len(mat2d[0])
    for i in range(y_size):
        for row in mat2d:
            if row[i] != 0:
                return False
    return True
    
    

def do_kernelsvm_slicer():
    n_vals = 10
    
    raw_files = get_raw_file_list()
    slicer = Slicer()
    print 'loading raw from list of csvfiles'
    slicer.load_series_from_csv('raw', 
            [join(ALL_RAW_URL,'preprocess', i) for i in raw_files])
    slicer.extract_rolling_median(seriesname='raw', window_size=128)
    slicer.extract_first_n_median(n=n_vals)
    tasks = slicer.get_tasks()
    
    #Remove rows in which all feature values are '0'
    tasks = tasks[[any(tasks.iloc[i,0:n_vals]!=0) for i in tasks.index]]
    print "Final # of rows: %d" % len(tasks)
    
    passage_tasks = tasks[tasks.is_passage==True]
    
    features = passage_tasks.loc[:, 0:(n_vals-1)]
    targets = list(passage_tasks.difficulty)
    
    assert not check_all_zeros(array(features)),"all values zero. halting!"
    
    skf = StratifiedKFold(targets, 5)
    for train, test in skf:
        break
    
    X_train = [features.iloc[i] for i in train]
    y_train = [targets[i] for i in train]
    X_test = [features.iloc[i] for i in test]
    y_test = [targets[i] for i in test]
    
    #do_grid_cv_svc(X_train, y_train, X_test, y_test)
    do_non_lin_svc(X_train, y_train, X_test, y_test)

do_kernelsvm_slicer()
