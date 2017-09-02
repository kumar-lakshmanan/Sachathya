'''
Created on Aug 27, 2017

@author: npn
'''
import os
import sys

from schLib import schLookups as lookups
from code import InteractiveConsole

import logging as log

class core(object):
    '''
    classdocs
    '''

    def __init__(self,core=None):
        '''
        Constructor
        '''
        log.info('StdOut/Err setup loading...')
        self.sch = core
        self.originalStdOut = sys.stdout 
        self.originalStdErr = sys.stderr
        log.info('StdOut/Err setup done!')

    def toCustom(self, customClass):
        sys.stderr = sys.stdout = customClass
        log.info('StdOut/Err Redirected to custom class')
    
    def toFile(self, fileName = lookups.stdLogFile):
        sys.stderr = sys.stdout = open(fileName,'w')     
        log.info('StdOut/Err Redirected to file {0}'.format(fileName))   
    
    def reset(self):
        sys.stdout = self.originalStdOut
        sys.stderr = self.originalStdErr
        log.info('StdOut/Err Reverted back to original.')
        