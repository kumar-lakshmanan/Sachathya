'''
Created on Aug 26, 2017

@author: npn
'''
from PyQt5 import QtCore, QtGui, Qsci, QtWidgets
from PyQt5.uic import loadUi

print('\n')
from schLib import schLookups
from schLib import schLogging
from schLib import schStandardIO
from schLib import schArgParser
from schLib import schSettings
from schLib import schInterpreter
from schLib import schUtilities

import kmxTools
import sys
import os
import inspect

import logging as log
logger = log.getLogger()
log.basicConfig(format=schLookups.logFormt,level=log.DEBUG)
logger.disabled=True

import logging.config
logging.config.dictConfig({
    'version': 1,
    'disable_existing_loggers': True
})

class core(object):
    '''
    Sachathya Core
    '''

    def __init__(self):
        '''
        * All Sachathya Objects should start with sch and ends with Obj
        
        '''
        self.display("Starting Sachathya...")
        log.info('Loading internal modules...')
        self.schArgParserObj = schArgParser.core(self)
        logger.disabled = not self.schArgParserObj.schLogEnable         
        self.schStandardIOObj = schStandardIO.core(self)     
        self.schSettingsObj = schSettings.core(self)
        self.schInterpretersObj = schInterpreter.core(self)
        self.schUtilitiesObj = schUtilities.core(self)
        self.ttls = kmxTools.Tools()        
        self.display("Internal modules loaded!")        
        self.schDoStart()
                       
    def schDoStart(self):
        self.display("Starting initial setup...")

        #Security Setup
        key = self.schArgParserObj.schKey
        if (key):
            schLookups.ciperKey = str(self.schUtilitiesObj.getCodeForKey(key)) + str(self.ttls.getUUID())
            log.info('Key: {0}'.format(schLookups.ciperKey))   
            self.display('Ciper ready!')                     
        else:
            self.schDoExit('Secret key missing in argument.')
        
        #StdOutput Setup
        if(self.schArgParserObj.schStdRedirect=="file" and self.schArgParserObj.schMode != 'cli'):
            f = self.schArgParserObj.schStdRedirectLogFile
            self.schStandardIOObj.toFile(f)
            self.display('Stream redirect to file: {0}'.format(f))

        #Is it a first time?
        if self.schUtilitiesObj.isFirstTime():
            self.schSettingsObj.saveDefaultSettings()
            self.display('First time user default settings prepared')
        self.schSettingsObj.readAllSettings()
        self.display('Settings read!')

        #Ready Search Paths
        self.schDoAddSearchPaths()

    def schDoStartConsole(self):
        self.display('Running console...')
        sch.schInterpretersObj.simpleConsole()

    def schDoStartServer(self):
        script = self.schArgParserObj.schStartupScript
        self.display('Running server {0}...'.format(script))
        if(script and os.path.exists(script)):
            script = os.path.abspath(script)
            self.schInterpretersObj.runScript(script)
        else:
            self.schDoExit('Startup script not found')
    
    def schDoStartApp(self):        
        script = self.schArgParserObj.schStartupScript
        self.display('Running app {0}...'.format(script))
        if(script and os.path.exists(script)):
            script = os.path.abspath(script)
            self.schQtApp = QtWidgets.QApplication(sys.argv)
            self.schInterpretersObj.runScript(script)
            wins = self.schQtApp.topLevelWidgets()
            if len(wins): wins[0].closeEvent = self.schDoInstanceLastAction                
            sys.exit(self.schQtApp.exec_())
        else:
            self.schDoExit('App script not found')
                            
    def schDoAddSearchPaths(self):       
        folder = self.schArgParserObj.schScriptFolder
        self.display('Adding scriptfolder "{0}" to search path'.format(folder))        
        if(not folder):
            self.schDoExit('No script folder mentioned!')
        
        folder = os.path.abspath(folder)
        if(not os.path.exists(folder)):
            self.schDoExit('Script folder does not exists!')
    
        for root, subdirs, files in os.walk(folder):
            if(not '__' in root):
                self.schInterpretersObj.addToSysPath(root)

    def schDoExit(self, msg='Custom Exit'):
        self.display('Exit: ' + msg)
        log.warn(msg)
        sys.exit()
            
    def schDoInstanceFirstAction(self):
        log.debug('Sachathya custom startup...')        
        self.cleanUpDone = False        
        log.debug('Sachathya custom startup completed!')
                   
    def schDoInstanceLastAction(self, *arg):
        if(hasattr(self, 'cleanUpDone') and self.cleanUpDone):
            self.display('Sachathya custom cleanup already completed!')
        else:
            self.display('Sachathya custom cleanup starting...')
            
            #pass
            
            self.display('Sachathya custom cleanup completed!')
            self.cleanUpDone = True
        
        if len(arg) and arg[0].type() == 19:arg[0].accept()

    def display(self, msg):
        stack = inspect.stack()[1]
        stack2 = inspect.stack()[2]
        fileName = os.path.basename(stack[1])
        fn = stack[3]
        fn2 = stack2[3]
        print('[{0}()-{1}()] {2}'.format(fn,fn2,msg))
      
    def __enter__(self):        
        log.debug('SachathyaInstance startup...')
        self.schDoInstanceFirstAction()
        return self        

    def __exit__(self, exc_type, exc_value, traceback):
        log.debug('SachathyaInstance closing...')
        self.schDoInstanceLastAction()
        
    def __del__(self, *args, **kwargs):
        log.debug('Deleting SachathyaInstance...')        
        self.schDoInstanceLastAction()
        log.debug('SachathyaInstance deleted!')
        log.debug('Thank you for using sachathya!')
        
if __name__ == '__main__':
    with core() as sch:
        print('SachathyaInstance created!')

        #Mode Check and Start App
        if sch.schArgParserObj.schMode == 'cli':            
            sch.schDoStartConsole()
        elif(sch.schArgParserObj.schMode == 'server'):
            sch.schDoStartServer()        
        elif(sch.schArgParserObj.schMode == 'app'):
            sch.schDoStartApp()        
        