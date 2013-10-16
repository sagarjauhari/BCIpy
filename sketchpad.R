###
# sketchpad.R: a place to store things we did in R that might be useful for this project
###

# import data
sigqual = read.csv('20101214163931.a.sigqual.csv')
meditation = read.csv('20101214163931.a.meditation.csv')
combined = read.csv('20101214163931.a.combined.csv')
ps = read.csv('20101214163931.a.powerspec.csv')
tasks = read.delim('task.xls')
rawwave = read.csv('20101214163931.a.rawwave.csv')

# examine some distributions
hist(sigqual$Value)
hist(meditation$Value)

# scatterplot of attention and meditation
plot(combined$Attention, combined$Meditation)

# mean across power spectrum
colMeans(ps[,2:512])

# use barplots to visualize mean spectral distribution
barplot(colMeans(ps[,2:512])) # note that barely anything above ~30Hz was registered
barplot(colMeans(ps[,2:128])) # there's a huge spike around 29-30Hz
barplot(colMeans(ps[,2:100])) # this clips before the ~29Hz spike, for better inspection of lower spectra
barplot(colMeans(ps[,24:64])) # ~5-15hz
barplot(colMeans(ps[,2:24])) # delta
barplot(colMeans(ps[,2:32]))
barplot(colMeans(ps[,16:64])) # exclude delta
barplot(colMeans(ps[,16:100])) # exclude delta and gamma

# working toward summarizing variance across spectra, but haven't gotten anywhere yet
var(ps[,2:128])
var(ps[,2:3])
cov(ps[,2:3])

# grabbing sets of raw 512Hz samples
rawwave[0:4,] # just the first few
rawwave[339:(339+519),]$Value # Why are there 519 samples in a second? Clock skew? Recording latency?

plot(rawwave[339:(339+519),]$Value) # I think this scatterplot is roughly the waveform. Need line chart instead

# attempting to make line chart of waveform, not yet successful
x = rawwave[339:(339+519),]$Value
plot(x,x,type='n')
slice = rawwave[339:(339+519),]
lines(slice$X.Time, slice$Value)
