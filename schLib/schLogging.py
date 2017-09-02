'''
Created on Aug 27, 2017

@author: npn
'''
from schLib import schLookups as lookups
import logging as log
import sys
import inspect
import os

class core(object):
    '''
    classdocs
    '''

    def __init__(self,core=None, enableDebugger=False):
        '''
        Constructor
            
            Level    Numeric value
            
            CRITICAL    50    
            ERROR    40       
            WARNING    30     
            INFO    20        
            
            DEBUG    10       
            
            NOTSET    0
        '''
        log.info("Logger setup loading...")
        self.sch=core

        self._logFormat = log.Formatter(lookups.logFormt)
        handler = log.StreamHandler()
        handler.setFormatter(self._logFormat)
        
        self.schLogger = log.getLogger()        
        self.schLogger.addHandler(handler)
        log.basicConfig(format=lookups.logFormt,level=log.NOTSET)
        
        log.info("Logging setup done!")
                            
    def doSetLogLevel(self, level='NOTSET'):
        if (level == 'DEBUG'):            
            log.basicConfig(format=lookups.logFormt,level=log.DEBUG)
        elif (level == 'INFO'):            
            log.basicConfig(format=lookups.logFormt,level=log.INFO)
        elif (level == 'WARNING'):            
            log.basicConfig(format=lookups.logFormt,level=log.WARNING)
        elif (level == 'ERROR'):            
            log.basicConfig(format=lookups.logFormt,level=log.ERROR)
        else:       
            log.basicConfig(format=lookups.logFormt,level=log.NOTSET)
