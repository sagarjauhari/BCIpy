# plot spectrograms from raw EEG wave
#rawwave = read.csv('20101214163931.a.rawwave.csv')
library(seewave)
rawwave = read.delim('preprocess/raw_incremental_label.csv')
tasks = read.delim('preprocess/task.xls')
taskIds = unique(rawwave$TaskId)
print(taskIds)
for (id in taskIds) {
	title = cat('Task ID #', id, ', difficulty: ', 'TBD')
	spectro(rawwave[rawwave$TaskId == id,]$Value, 512, wl=64, main=id)
	print(title)
}
#spectro(rawwave$Value[0:3000], 512, wl=128)
#spectro(rawwave$Value[0:30000], 512, wl=256)
