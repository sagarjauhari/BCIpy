"""
@author: sagar jauhari

General statistics of the EEG data
"""

import argparse, os, datetime, shutil, glob, pickle
from os.path import join, isfile
from slicer import Slicer
import process_series_files, kernel_svm, charts_for_paper, eegml, filters
import data_cleaning, stats
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt
import numpy as np
import re
import pylab

def plot_task_length(slicer, pdfpages):
    tasks = slicer.get_tasks()
    X = [slicer.get_time_duration_by_taskid(taskid) for taskid in tasks.index ]
    #fig, ax = plt.subplots()
    #ax.plot(X)
    n, bins, patches = plt.hist(X)
    plt.plot(bins)
    plt.grid(True)
    plt.xlabel("Task Duration (seconds)")
    plt.ylabel("Task count")
    plt.title("Histogram of task duration")
    pdfpages.savefig()

def plot_all(slicer, pdfpages):
    print "Generating statistics"
    plot_task_length(slicer, pdfpages)
    