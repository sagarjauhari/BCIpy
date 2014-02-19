# -*- coding: utf-8 -*-
"""
Created on Tue Feb 18 00:09:18 2014

@author: sagar
"""

import argparse, os, datetime, shutil, glob
from os.path import join, isfile

import process_series_files, kernel_svm

def arg_parse():
    parser = argparse.ArgumentParser(description='Process EEG Data.')

    parser.add_argument('-i', nargs=1 , required=True, dest='indir',
                        help='Directory containing raw EEG Files.')

    parser.add_argument('-o', nargs=1, required=True, dest='outdir',
                        help='Path of processed data and reports. New directory\
                        with timestamp will be created inside this folder.')

    parser.add_argument('--interpolate', action='store_true',
                        help='Interpolate 512Hz time stamps on 512Hz data\
                        having 1Hz time stamps (raw data available from CMU)')

    parser.add_argument('--kernelsvm', action='store_true',
                        help='Perform Kernelized SVC on interpolated raw data')
                        
    args = parser.parse_args()
    return args

def create_timestamp_dir(out_dir):
    mydir = join(out_dir,
                        datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S'))
    try:
        os.makedirs(mydir)
        os.makedirs(join(mydir,'data'))
    except OSError, e:
        if e.errno != 17:
            raise # This was not a "directory exist" error
    return mydir
    

if __name__=="__main__":
    args = arg_parse()
    out_dir = create_timestamp_dir(args.outdir[0])
    data_dir= join(out_dir,'data')

    if args.interpolate:
        process_series_files.process_all_in_dir(args.indir[0],
                                                join(out_dir,'data'))
    else: #just copy the files
        print "Copying data files to ", data_dir
        for csvf in glob.iglob(join(args.indir[0],"*.csv")):
            shutil.copyfile(csvf, join(data_dir, os.path.basename(csvf)))

    filelist=[join(data_dir,f) for f in os.listdir(data_dir)]
    if args.kernelsvm:
        kernel_svm.do_kernelsvm_slicer(filelist)
