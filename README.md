<!--
# Copyright 2013, 2014 Justis Grant Peters and Sagar Jauhari

# This file is part of BCIpy.
# 
# BCIpy is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# BCIpy is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with BCIpy.  If not, see <http://www.gnu.org/licenses/>.
-->
&copy; 2013, 2014 Justis Grant Peters and Sagar Jauhari

# BCIpy
#### Python toolkit to analyse EEG data
Code repository for our project in Educational Data Mining class with Dr. Tiffany Barnes, CSC 591-021 Fall 2013 at NCSU. We are analyzing EEG data collected by Mostow and Chang from Project LISTEN.

## Using the data processing pipeline
	$ python process_eeg.py --help
	usage: process_eeg.py [-h] -i INDIR -o OUTDIR --type {raw,pam1hz}
	                      [--interpolate] [--kernelsvm] [--chartsforpaper]
	                      [--plotsubjects] [--plotavgrolmed NSAMP]
	                      [--plotavgraw NSAMPRAW] [--plotraw NRAW] [--filter]
	                      [--stats] [--clean]
	
	Process EEG Data.
	
	optional arguments:
	  -h, --help            show this help message and exit
	  -i INDIR              Directory containing EEG Files.
	  -o OUTDIR             Path of processed data and reports. New directory with
	                        timestamp will be created inside this folder.
	  --type {raw,pam1hz}   Select type of input data: Raw 512 Hz data or Neurosky
	                        output data of 1Hz having proprietary fields:
	                        PoorSignal, Attention and Meditation.
	  --interpolate         Interpolate 512Hz time stamps on 512Hz data having 1Hz
	                        time stamps (raw data available from CMU). [raw]
	  --kernelsvm           Perform Kernelized SVC on interpolated raw data. [raw]
	  --chartsforpaper      Create charts in single page PDF files. [raw]
	  --plotsubjects        Create charts for 1Hz data of subjects. [pam1hz]
	  --plotavgrolmed NSAMP
	                        Plot average rolling median of first NSAMP samples.
	                        Note: Rolling median is usually downsampled to 10Hz,
	                        so 1st second = 10 samples. [raw]
	  --plotavgraw NSAMPRAW
	                        Plot raw signal averaged over all subjects for 1st
	                        NSAMPRAW samples. [raw]
	  --plotraw NRAW        Plot raw signal of all subjects for 1st NRAW samples.
	                        [raw]
	  --filter              Use Butteworth filter and plot charts for 1Hz subject
	                        data. [pam1hz]
	  --stats               General statistics of data [raw]
	  --clean               Remove data with 0 attention or meditation values;
	                        Remove data with > 0 poor signal value. [pam1hz]



## Processing timeseries data from CMU
The 512Hz data from CMU has timestamp information, but only at 1Hz resolution. To interpolate these:
<pre>
python process_series_files.py data/raw/ preprocess/raw/
</pre>

## Using slicer
The Slicer class manages timeseries and extracted features as they relate to tasks from task.xls.

	# instantiating task slicer
	s = Slicer()

	if len(sys.argv) > 2:
			print 'loading raw from list of csvfiles'
			s.load_series_from_csv('raw', sys.argv[1:])
	else:
			print 'loading raw from pickle'
			s.load_series_from_pickle('raw', sys.argv[1])

	# extract features from 'raw'
	s.extract_filtered_signal()
	s.extract_rolling_median()
	s.extract_rolling_PSD()

	# fetch task 1, with features
	# Return type is a dict, with task-level features, plus the requested timeseries features
	print s.get_by_task_id(1, features=['raw','raw_rolling_PSD_512', 'raw_rolling_median_128'])

## Using Python notebooks
<pre>
sudo apt-get install ipython
git clone git@github.com:sagarjauhari/edm_eeg.git edm_eeg.git
cd edm_eeg.git
ipython notebook --pylab-inline
</pre>

## Running R scripts
To run an R script, for example sketchpad.R:
<pre>
cd dir-with-eeg-data/
R --vanilla &lt; /path/to/sketchpad.R
</pre>

It will produce a PDF called Rplots.pdf with a page for each chart produced by the script.

## Patching the data
If you're using eeg_data_set2.zip_, you will want to fix the first line in 20101214171219.1.rawwave.csv to look like this:
<pre>
%Time,Value
</pre>

# License and Copyright
&copy; 2013, 2014 Justis Grant Peters and Sagar Jauhari

This file is part of BCIpy.

BCIpy is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

BCIpy is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with BCIpy.  If not, see <http://www.gnu.org/licenses/>.

# Dependencies
- [PyEEG](https://code.google.com/p/pyeeg/) - Licenced under GPL V3

