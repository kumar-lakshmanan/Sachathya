'''
Created on Aug 27, 2017

@author: npn
'''
import os
import sys

from schLib import schLookups as lookups
from code import InteractiveConsole
import code

import logging as log
import kmxTools
import time

class core(object):
    '''
    classdocs
    '''

    def __init__(self,core=None):
        '''
        Constructor
        '''        
        self.sch = core
        log.debug('Python interpreter setup loading...')
        self.ttls = kmxTools.Tools()
        self.schConsole = code.InteractiveConsole(locals())
        log.debug('Python interpreter setup done!')

    def simpleCLI(self, callback=None):
        log.debug('Starting simple interactive interpreter!')
        for eachInput in sys.stdin:
            eachInput = str(eachInput).strip().lower()
            if(eachInput):
                if eachInput in ['quit','exit','stop']:                
                    self.sch.log.debug('Interactive interpreter closing!')
                    break;
                elif callback:
                    res = self.simpleEval(eachInput)
                    callback(res)
                else:
                    res = self.simpleEval(eachInput)
                    print(res)

    def simpleEval(self, code):
        try:
            return eval(code)
        except:
            self.ttls.errorInfo()
    
    def simpleConsole(self):
        log.info('Starting console...')
        try:
            self.schConsole.locals=locals()            
            self.schConsole.interact(lookups.consoleBanner)
        except:
            self.ttls.errorInfo()

    def runCommand(self, codeStr):
        log.info('Executing gui command...')
        codeStr = codeStr.strip()
        if(codeStr):
            try:
                self.schConsole.locals['dev'] = self.sch
                self.schConsole.runsource(codeStr, "<console>", "single")
                time.sleep(.01)             
            except:
                self.ttls.errorInfo()
    
    def runCode(self, codeStr='', fileName=None):
        log.info('Executing code...')
        codeStr = codeStr.strip()
        if(codeStr):
            try:
                self.schConsole.locals['dev'] = self.sch
                self.schConsole.runsource(codeStr, fileName, 'exec')
                time.sleep(.01)             
            except:
                self.ttls.errorInfo()
                
    def runScript(self, scriptFile=None):
        log.info('Trying to execute script file... %s' % scriptFile)
        if scriptFile and os.path.exists(scriptFile):
            basePath = os.path.dirname(scriptFile)
            fName = os.path.basename(scriptFile)
            data = self.ttls.fileContent(scriptFile)            
            self.addToSysPath(basePath)
            self.runCode(data,fName)
        else:
            log.info('Script file missing...' + scriptFile)          
                
    def getUpdatedLocals(self):
        try:
            raise None
        except:
            frame = sys.exc_info()[2].tb_frame.f_back
        namespace = frame.f_globals.copy()
        namespace.update(frame.f_locals)
        namespace['__name__'] = '__main__'
        return namespace          

    def addToSysPath(self, path):
        path = os.path.abspath(path)
        if('\.' in path): return None                
        if path not in sys.path and os.path.exists(path):
            log.info("Adding path to system... " + path)
            sys.path.append(path)   
    
    