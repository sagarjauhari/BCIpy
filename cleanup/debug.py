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