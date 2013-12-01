# edm_eeg
Code repository for our project in Educational Data Mining class with Dr. Tiffany Barnes, CSC 591-021 Fall 2013 at NCSU. We are analyzing EEG data collected by Mostow and Chang from Project LISTEN.

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


