# plot spectrograms from raw EEG wave
#rawwave = read.csv('20101214163931.a.rawwave.csv')
library(seewave)
rawwave = read.csv('preprocess/raw_incremental.csv')
spectro(rawwave$Value[0:3000], 512, wl=128)
spectro(rawwave$Value[0:30000], 512, wl=256)
