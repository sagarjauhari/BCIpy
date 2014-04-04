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

# -*- coding: utf-8 -*-
"""
Created on Mon Nov 25 02:02:10 2013

@author: sagar
"""

import sys
import re

def printModuleNames():
    pat = re.compile("matplotlib*|numpy*|scipy*|pylab*|pandas*")
    for name, module in sorted(sys.modules.items()):
        if hasattr(module, '__version__') and pat.match(name):
            print name, module.__version__ 
            
if __name__=='__main__':
    printModuleNames()
