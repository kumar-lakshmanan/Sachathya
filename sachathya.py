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
from schLib.schGUI import schGUIMainWindow

import kmxTools
import sys
import os
import inspect

import logging as log
import logging.config
       
logger = log.getLogger()
log.basicConfig(format=schLookups.logFormt,level=log.DEBUG)
logger.disabled = 1
logging.config.dictConfig({
    'version': 1,
    'disable_existing_loggers': 1
})
               
class core(object):
    '''
    Sachathya Core
    '''

    def __init__(self):
        '''
        * All Sachathya Objects should start with sch and ends with Obj
        
        '''
        self.ttls = kmxTools.Tools()     
        
        self.display("Starting Sachathya...")
        log.info('Loading internal modules...')
        self.schUtilitiesObj = schUtilities.core(self)
        self.schArgParserObj = schArgParser.core(self)
        self.schUtilitiesObj.loggerSetup(self.schArgParserObj.schLogLevel,self.schArgParserObj.schLogEnable)
        self.schStandardIOObj = schStandardIO.core(self)     
        self.schSettingsObj = schSettings.core(self)
        self.schInterpreterObj = schInterpreter.core(self)        
           
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
        if(self.schArgParserObj.schStdRedirect=="file" and self.schArgParserObj.schMode != 'console'):
            f = self.schArgParserObj.schStdRedirectLogFile
            self.schStandardIOObj.toFile(f)
            self.display('Stream redirect to file: {0}'.format(f))

        #Is it a first time?
        if self.schUtilitiesObj.isFirstTime():            
            self.display('First time user default settings prepared')
            self.schSettingsObj.saveDefaultSettings()
        self.schSettingsObj.readAllSettings()
        self.display('Settings read!')

        #Ready Search Paths
        self.schDoAddSearchPaths()

    def schDoStartGUI(self):
        self.display('Running sachathya GUI...')
        self.schQtApp = QtWidgets.QApplication(sys.argv)
        self.schGUIObj = schGUIMainWindow.core(self)
        self.schGUIObj.closeEvent = self.schDoInstanceLastAction      
        self.schGUIObj.show()
        self.schGUIObj.guiInitialize()
        sys.exit(self.schQtApp.exec_())        

    def schDoStartConsole(self):
        self.display('Running sachathya console...')
        sch.schInterpreterObj.simpleConsole()

    def schDoStartConsoleApp(self):
        script = self.schArgParserObj.schStartupScript
        self.display('Running server {0}...'.format(script))
        if(script and os.path.exists(script)):
            script = os.path.abspath(script)
            self.schInterpreterObj.runScript(script)
        else:
            self.schDoExit('Startup script not found')
    
    def schDoStartGUIApp(self):        
        script = self.schArgParserObj.schStartupScript
        self.display('Running app {0}...'.format(script))
        if(script and os.path.exists(script)):
            script = os.path.abspath(script)
            self.schQtApp = QtWidgets.QApplication(sys.argv)
            self.schInterpreterObj.runScript(script)
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
                self.schInterpreterObj.addToSysPath(root)

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

    def display(self, msg, tag='DISPLAY'):
        stack = inspect.stack()[1]
        stack2 = inspect.stack()[2]
        fileName = os.path.basename(stack[1])
        fn = stack[3]
        fn2 = stack2[3]
        ti = self.ttls.getDateTime('%Y-%m-%d %H:%M:%S,000')
        print('[{0}] {1}() - {2}() [{3}] {4}'.format(ti,fn,fn2,tag,msg))
      
    def __enter__(self):        
        log.warn('SachathyaInstance startup actions initiated...')
        self.schDoInstanceFirstAction()
        return self        

    def __exit__(self, exc_type, exc_value, traceback):
        log.warn('SachathyaInstance closing actions initiated...')
        self.schDoInstanceLastAction()
        
    def __del__(self, *args, **kwargs):
        log.warn('SachathyaInstance destroying actions initiated...')        
        self.schDoInstanceLastAction()
        log.warn('SachathyaInstance deleted!')
        log.warn('Thank you for using sachathya!')
        
if __name__ == '__main__':
    with core() as sch:
        print('SachathyaInstance created!')

        #Mode Check and Start App
        if sch.schArgParserObj.schMode == 'console':            
            sch.schDoStartConsole()
        elif(sch.schArgParserObj.schMode == 'gui'):
            sch.schDoStartGUI()             
        elif(sch.schArgParserObj.schMode == 'consoleApp'):
            sch.schDoStartConsoleApp()        
        elif(sch.schArgParserObj.schMode == 'guiApp'):
            sch.schDoStartGUIApp()        
        