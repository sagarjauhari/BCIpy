###
# creates boxplots to evaluate variance over the power spectrum
###

ps = read.csv('20101214163931.a.powerspec.csv') # import data
boxplot(ps[,2:150], outline=FALSE) # lower band dominates scale
boxplot(ps[,2:50], outline=FALSE) # so show it separately
boxplot(ps[,30:150], outline=FALSE) # and then the rest
