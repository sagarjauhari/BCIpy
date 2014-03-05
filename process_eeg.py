# -*- coding: utf-8 -*-
"""
Created on Tue Feb 18 00:09:18 2014

@author: sagar
"""

import argparse, os, datetime, shutil, glob, pickle
from os.path import join, isfile
from slicer import Slicer
import process_series_files, kernel_svm, charts_for_paper, eegml, filters
import data_cleaning
from matplotlib.backends.backend_pdf import PdfPages

def arg_parse():
    parser = argparse.ArgumentParser(description='Process EEG Data.')

    parser.add_argument('-i', nargs=1 , required=True, dest='indir',
                        help='Directory containing EEG Files.')

    parser.add_argument('-o', nargs=1, required=True, dest='outdir',
                        help='Path of processed data and reports. New \
                        directory with timestamp will be created inside this\
                        folder.')
                        
    parser.add_argument('--type', nargs=1, required=True, dest='intype',
                        choices = ['raw', 'pam1hz'], help='Select type of\
                        input data: Raw 512 Hz data or Neurosky\
                        output data of 1Hz having proprietary fields: \
                        PoorSignal, Attention and Meditation. ')

    parser.add_argument('--interpolate', action='store_true',
                        help='Interpolate 512Hz time stamps on 512Hz data\
                        having 1Hz time stamps (raw data available from CMU). \
                        [raw]')

    parser.add_argument('--kernelsvm', action='store_true',
                        help='Perform Kernelized SVC on interpolated raw data.\
                         [raw]')
                        
    parser.add_argument('--chartsforpaper', action='store_true',
                        help='Create charts in single page PDF files. [raw]')
                        
    parser.add_argument('--plotsubjects', action='store_true',
                        help='Create charts for 1Hz data of subjects. \
                        [pam1hz]')

    parser.add_argument('--filter', action='store_true',
                        help='Use Butteworth filter and plot charts for 1Hz\
                         subject data. [pam1hz]')
                         
    parser.add_argument('--clean', action='store_true',
                        help='Remove data with 0 attention or meditation\
                        values; Remove data with > 0 poor signal value.\
                        [pam1hz]')

    args = parser.parse_args()
    return args

def create_timestamp_dir(out_dir):
    mydir = join(out_dir,
                        datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S'))
    try:
        os.makedirs(mydir)
        os.makedirs(join(mydir,'data'))
        os.makedirs(join(mydir,'reports'))
    except OSError, e:
        if e.errno != 17:
            raise # This was not a "directory exist" error
    return mydir
    

if __name__=="__main__":
    args = arg_parse()
    out_dir = create_timestamp_dir(args.outdir[0])
    data_dir= args.indir[0]
    report_dir = join(out_dir, 'reports')
    temp_dir = join(out_dir, 'data')
    
#==============================================================================
#     Process Raw Data
#==============================================================================
    if args.intype[0]=='raw':
        if args.interpolate:
            process_series_files.process_all_in_dir(args.indir[0],
                                                    join(out_dir,'data'))
            data_dir = join(out_dir,'data')
            
        """
        else: #just copy the files
            print "Copying data files to ", data_dir
            for csvf in glob.iglob(join(args.indir[0],"*.csv")):
                shutil.copyfile(csvf, join(data_dir, os.path.basename(csvf)))
        """
        print "Instantiating Slicer and loading series"
        slicer = Slicer()
        filelist=[join(data_dir,f) for f in os.listdir(data_dir)]
        slicer.load_series_from_csv('raw', filelist)
        
        if args.kernelsvm:
            kernel_svm.do_kernelsvm_slicer(slicer)
        
        if args.chartsforpaper:
            pp = PdfPages(join(report_dir, 'rolling_median.pdf'))
            charts_for_paper.do_charts(slicer, pp)
            pp.close()
#==============================================================================
#      Process neurosky proprietary data
#==============================================================================
    elif args.intype[0] == 'pam1hz':
        eegml.format_task_xls(data_dir, temp_dir)
        eegml.label_sub_files(data_dir, temp_dir)        
        subj_list = eegml.get_subject_list(temp_dir)
        subj_data = eegml.get_data(subj_list, temp_dir)
        
        if args.plotsubjects:
            pp = PdfPages(join(report_dir, 'subjects_combined.pdf'))
            eegml.plot_subjects(subj_list, subj_data, pp)
            pp.close()

        if args.filter:
            pp = PdfPages(join(report_dir, 'subjects_filtered.pdf'))
            filters.plot_butter(512.0, 0.1, 20.0, [1,2,3,4,5,6,7,8], pp)
            pp.close()
            
        if args.clean:
            pp = PdfPages(join(report_dir, 'subjects_cleaned.pdf'))
            clean_data = data_cleaning.clean_all(subj_list, subj_data)
            pickle.dump(clean_data, open(join(temp_dir, 
                                            "clean_data_1hz.pickle"),'wb'))
            
            data_cleaning.plot_cleaned_counts(subj_data, clean_data, pp)
            eegml.plot_subjects(subj_list, clean_data, pp)
            pp.close()