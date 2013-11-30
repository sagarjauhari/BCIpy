import csv
import time
import re
from datetime import datetime
from decimal import Decimal
from matplotlib import *
import matplotlib.pyplot as plt
import matplotlib.pylab as pylab
pylab.rcParams['figure.figsize'] = 15, 6
from os import listdir
from os.path import join, isfile
import numpy as np
import pandas as pd
import pickle
from scipy.stats.stats import pearsonr

import warnings
warnings.filterwarnings('ignore', 'DeprecationWarning')


try: # Import config params
    import dev_settings as config
except ImportError:
    print "Please create a dev_settings.py using dev_settings.py.example as an example"

def print_config():
    print config.DATA_URL
    print config.SAVE_URL

def format_time(ti):
    """
    Converts format '2010-12-14 16:56:36.996' to Decimal
    """
    to = datetime.strptime(ti, '%Y-%m-%d %H:%M:%S.%f')
    #Decimal not losing precision
    to = Decimal(to.strftime('%s.%f'))
    return str(to)

def format_task_xls(file):
    path_task_xls = join(config.DATA_URL, file + ".xls")
    path_task_xls_labels = join(config.SAVE_URL,  file + "_xls_labels.csv")

    with open(path_task_xls, 'rb') as fi,\
    open(path_task_xls_labels, 'w') as fo:
        fr = csv.reader(fi, delimiter='\t')
        fw = csv.writer(fo, delimiter='\t')

        h = fr.next()
        fw.writerow(['taskid',h[0], h[1], h[2], h[3], h[-1]]) #header

        for idx, row in enumerate(fr):
            row[2] = format_time(row[2])
            row[3] = format_time(row[3])
            fw.writerow([idx, row[0], row[1], row[2], row[3], row[-1]])

def label_data(in_file, out_file, compressed_label_file, subj_t, time_t, dbg=False):
    if dbg: print "#"+subj_t + "--------"

    with open(in_file, 'rb') as fi,\
    open(out_file, 'rb') as fi2,\
    open(compressed_label_file, 'w') as fo:

        day = time_t[0:4]+"-"+time_t[4:6]+"-"+time_t[6:8]
        fr1 = csv.reader(fi,  delimiter=',') # combined.csv
        fr2 = csv.reader(fi2, delimiter='\t')# xls_labels.csv
        fw  = csv.writer(fo,  delimiter='\t')# combined_label_uncompress.csv

        if dbg: print "day: " + day

        #headers
        fw.writerow(next(fr1, None) + ['Difficulty', 'taskid'] )
        next(fr2, None)

        #forward till subject data starts
        lab_row = fr2.next()
        while subj_t != lab_row[2]:
            lab_row = fr2.next()
        if dbg: print "start: " + str(lab_row[0])

        for idx, row in enumerate(fr1):
            row[0] = datetime.strptime(day+' '+row[0]+'.0',\
                            '%Y-%m-%d %H:%M:%S.%f').strftime('%s.%f')
            if Decimal(row[0]) < Decimal(lab_row[3]): # t < start_time
                if dbg: print str(idx)+": t<start_time"
                label = -1
                fw.writerow(row + [label, lab_row[0]])
                continue

            if Decimal(row[0]) <= Decimal(lab_row[4]): # t <= end_time
                if dbg: print str(idx)+": t <= end_time"
                label = lab_row[5]
                fw.writerow(row + [label, lab_row[0]])
                continue

            while Decimal(row[0] > lab_row[4]): # t > end_time
                try:
                    lab_row = next(fr2)
                    label = lab_row[5]
                    if lab_row[2] != subj_t:
                        raise Exception("Reached end of data for subject" + subj_t)
                except Exception as e: # reached end of file, or next subject
                    label = -1
                    if dbg: print e
                    break
            fw.writerow(row + [label,lab_row[0]])

        if dbg: print "end:   "+str(lab_row[0])
    return

def create_raw_incremental(in_file, out_file):
    "Create raw file with incremental miliseconds"
    raw = pd.read_csv(in_file)

    c=0.0
    prev_time = None
    for i,row in raw.iterrows():
        timestamp = row['%Time']
        if timestamp==prev_time:
            c = c + 0.001
        else:
            c = 0.0
            prev_time = timestamp
        raw.set_value(i, '%Time', timestamp + '.' + str(c).split('.')[1])

    # FIXME something is sorting timestamp alphabetically
    raw.to_csv(out_file, index=False)

def label_data_raw(in_file, out_file, task_xls_label_file, mach_t, time_t, dbg=False):
    if dbg: print "#"+mach_t + "--------"

    with open(in_file, 'rb') as fi,\
    open(task_xls_label_file, 'rb') as fi2,\
    open(out_file, 'w') as fo:

        day = time_t[0:4]+"-"+time_t[4:6]+"-"+time_t[6:8]
        fr1 = csv.reader(fi,  delimiter=',') #microsec file
        fr2 = csv.reader(fi2, delimiter='\t')# xls_labels.csv
        fw  = csv.writer(fo,  delimiter='\t')

        #headers
        fw.writerow(next(fr1, None) + ['Difficulty', 'taskid'] )
        next(fr2, None)

        #forward till subject mach starts
        lab_row = fr2.next()
        while mach_t != lab_row[0]:
            lab_row = fr2.next()
        if dbg: print "start: " + str(lab_row[0])

        for idx, row in enumerate(fr1):
            row[0] = datetime.strptime(day+' '+row[0],\
                            '%Y-%m-%d %H:%M:%S.%f').strftime('%s.%f')
            if Decimal(row[0]) < Decimal(lab_row[3]): # t < start_time
                label = -1
                taskid= -1
                fw.writerow(row + [label, taskid])
                continue

            if Decimal(row[0]) < Decimal(lab_row[4]): # t < end_time
                label = lab_row[5]
                taskid= lab_row[0]
                fw.writerow(row + [label, taskid])
                continue

            while Decimal(row[0] > lab_row[4]): # t > end_time
                try:
                    lab_row = next(fr2)
                    label = lab_row[5]
                    taskid=lab_row[0]
                except: # reached end of file
                    label = -1
                    taskid= -1
                    break
            fw.writerow(row + [label, taskid])

        if dbg: print "end:   "+str(lab_row[0])
    return

def plot_signal(x_ax, y_ax, label, ax=None):
    if ax==None:
        fig, ax = plt.subplots()
    ax.plot(x_ax, y_ax, label=label)
    ax.grid(True)
    fig.tight_layout()
    plt.legend(loc='upper left')
    plt.show()
    return ax

def get_subject_list(dir_url):
    onlyfiles = [ f for f in listdir(dir_url) if isfile(join(dir_url,f)) ]
    pat = re.compile("[0-9]*\.[0-9]*\.labelled\.csv")
    temp_dat = [f.split('.')[0:2] for f in onlyfiles if pat.match(f)]
    sub_dict = {i[1]: i[0] for i in temp_dat}
    return sub_dict

def get_data(subj_list, dir_url):
    subj_data = {}
    for s_id in subj_list.keys():
        s_time = subj_list[s_id]
        s_file = s_time + "." + s_id + ".labelled.csv"
        with open(join(dir_url,s_file), 'rb') as fi:
            fr = csv.reader(fi,delimiter="\t")
            next(fr) #header
            s_data = list(fr)
            subj_data[int(s_id)] = s_data
    return subj_data

def plot_subject(s_comb, title=None):
    fig, ax = plt.subplots()
    x_ax = [int(i[0].split('.')[0]) for i in s_comb]

    sig_q = [int(i[1]) for i in s_comb]
    atten = [int(i[2]) for i in s_comb]
    medit = [int(i[3]) for i in s_comb]
    diffi = [int(i[4])*50 for i in s_comb]
    taskid= [int(i[5]) for i in s_comb]
    taskid_set = list(set(taskid))
    taskid_norm = [taskid_set.index(i) for i in taskid]

    ax.plot(x_ax,sig_q, label='Quality')
    ax.plot(x_ax, atten, label='Attention')
    ax.plot(x_ax, medit, label='Meditation')
    ax.plot(x_ax, diffi, label='Difficulty')
    #ax.plot(x_ax, taskid_norm, label='taskid')

    ax.grid(True)
    fig.tight_layout()
    plt.legend(loc='upper left')
    plt.title(title)
    plt.show()
    return

def plot_subjects(subj_list, data, count):
    for i in range(count):
        s1 = subj_list.keys()[i]
        plot_subject(data[int(s1)], "Subject: "+s1)
    return

def get_num_words(DATA_URL):
    path_task_xls = DATA_URL + "/task.xls"

    with open(path_task_xls, 'rb') as fi:
        fr = csv.reader(fi, delimiter='\t')
        next(fr)#header

        data = list(fr)
        data_cols = zip(*data)

        l=len(data_cols[0])
        num_words_stim = [float(len(i.split())) for i in data_cols[4]]
        num_chars_stim = [float(len(i)) for i in data_cols[4]]
        difficulty = [float(i) for i in data_cols[-1]]
        time_diff = [float(Decimal(format_time(data_cols[3][i]))-\
                    Decimal(format_time(data_cols[2][i])))\
                    for i in xrange(l)]

        time_per_word = [time_diff[i]/num_words_stim[i] for i in range(l)]
        time_per_char = [time_diff[i]/num_chars_stim[i] for i in range(l)]

        sentence_idx=[i for i in xrange(l) if num_words_stim[i] > 1]

        print pearsonr(time_per_word, difficulty)
        print pearsonr(time_per_char, difficulty)

        print pearsonr([time_per_word[i] for i in sentence_idx],
                       [difficulty[i] for i in sentence_idx])
        print pearsonr([time_per_char[i] for i in sentence_idx],
                       [difficulty[i] for i in sentence_idx])

        tpa = [difficulty[i] for i in sentence_idx]
        plt.hist(tpa)

# Create dict of machine data
def create_dict_machine_data(raw_dir):
    onlyfiles_raw = [ f for f in listdir(raw_dir) if isfile(join(raw_dir,f)) ]
    pat_raw = re.compile("[0-9]*\.[a-z0-9]*\.rawwave\.csv")
    temp_dat_raw = [f.split('.')[0:2] for f in onlyfiles_raw if pat_raw.match(f)]
    mach_dict = {i[1]: i[0] for i in temp_dat_raw}
    return mach_dict

def get_performance(x,y):
    """ Measures the performance metrics for x(actual)
        and y (experimental).
    """
    if len(x) != len(y):
        print "Error: Lengths not same"
        return
    TP = FN = FP = TN = 0.0

    for i in range(0,len(x)):
        for j in range(0, len(x)):
            if i == j:
                continue

            if x[i]==x[j] and y[i]==y[j]:
                TP = TP + 1
            elif x[i]!=x[j] and y[i]!=y[j]:
                TN = TN + 1
            elif x[i]==x[j] and y[i]!=y[j]:
                FN = FN + 1
            elif x[i]!=x[j] and y[i]==y[j]:
                FP = FP + 1
    TP = TP/2
    TN = TN/2
    FN = FN/2
    FP = FP/2

    accuracy = (TP + TN) / (TP + TN + FP + FN)
    precision = TP/(TP + FP)
    recall = TP/(TP + FN)
    fscore = 2*precision*recall/(precision + recall)

    print "  Accuracy: \t" + str(round(accuracy, 3))
    print "  Precision: \t" + str(round(precision, 3))
    print "  Recall: \t" + str(round(recall, 3))
    print "  F-Score: \t" + str(round(fscore, 3))
