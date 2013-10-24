# edm_eeg
Code repository for our project in Educational Data Mining class with Dr. Tiffany Barnes, CSC 591-021 Fall 2013 at NCSU. We are analyzing EEG data collected by Mostow and Chang from Project LISTEN.

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
R --vanilla < /path/to/sketchpad.R
</pre>

It will produce a PDF called Rplots.pdf with a page for each chart produced by the script.


