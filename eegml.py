import csv
import time
import re
from datetime import datetime
from decimal import Decimal
from matplotlib import *
import matplotlib.pyplot as plt
import matplotlib.pylab as pylab
pylab.rcParams['figure.figsize'] = 15, 6

try: # Import config params
   import dev_settings as config
except ImportError:
   print "Please create a dev_settings.py using dev_settings.py.example as an example"

def format_time(ti):
    """
    Converts format '2010-12-14 16:56:36.996' to Decimal
    """
    to = datetime.strptime(ti, '%Y-%m-%d %H:%M:%S.%f')
    #Decimal not losing precision
    to = Decimal(to.strftime('%s.%f'))
    return str(to)
    
def format_task_xls():
    path_task_xls = config.DATA_URL + "/task.xls"
    path_task_xls_labels = config.SAVE_URL + "/task_xls_labels.csv"
    
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

# deprecated?
def compress_time_labels(file_name):
    """
    Combines contiguous time windows
    with same difficulty label
    """
    with open(file_name, 'rb') as fi,\
    open("./preprocess/task_xls_labels_compress.csv", 'w') as fo:
        fr = csv.reader(fi, delimiter='\t')
        fw = csv.writer(fo, delimiter='\t')
        fw.writerow(fr.next()) #header
        
        row1 = fr.next()
        t_id =row1[0]
        t_s = row1[1]
        t_e = row1[2]
        lab = row1[3]
        
        for row in fr: #row 2 onwards
            if row[3] == lab:
                t_e = row[2]
            else:
                fw.writerow([str(t_id),str(t_s), str(t_e), lab])
                t_id =row[0]
                t_s = row[1]
                t_e = row[2]
                lab = row[3]
        fw.writerow([str(t_id),str(t_s), str(t_e), lab]) #last row
