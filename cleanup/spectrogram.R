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
