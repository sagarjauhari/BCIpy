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

###
# creates boxplots to evaluate variance over the power spectrum
###

ps = read.csv('20101214163931.a.powerspec.csv') # import data
boxplot(ps[,2:150], outline=FALSE) # lower band dominates scale
boxplot(ps[,2:50], outline=FALSE) # so show it separately
boxplot(ps[,30:150], outline=FALSE) # and then the rest
