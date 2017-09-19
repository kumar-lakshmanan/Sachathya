'''
Created on Aug 26, 2017

@author: npn
'''
from PyQt5.QtCore import (QFile, QFileInfo, QPoint, QSettings, QSignalMapper, QSize, QTextStream, Qt, )
from PyQt5.QtWidgets import (QAction, QApplication, QFileDialog, QMainWindow, QMdiArea, QMessageBox, QTextEdit, QWidget, QSizePolicy)
from PyQt5.QtGui import (QIcon, QKeySequence, QFont, QColor)
from PyQt5.Qsci import (QsciScintilla, QsciLexerPython, QsciAPIs)
from PyQt5 import QtCore, QtGui, Qsci, QtWidgets
from PyQt5.uic import loadUi

from schLib import schLookups as lookups
from schLib import schStandardIO
from schLib import schArgParser
from schLib import schSettings
from schLib import schInterpreter
from schLib import schUtilities
from schLib.schGUI import schGUIMainWindow
from schLib import fatcow_rc

import kmxINIConfigReadWrite
import kmxQtCommonTools
import kmxQtListWidget
import kmxQtMenuBuilder
import kmxQtTray
import kmxQtTreeWidget
import kmxTools

import sys
import os
import inspect
import atexit
import traceback

import logging as log
import logging.config
       
logger = log.getLogger()
log.basicConfig(format=lookups.logFormt,level=log.DEBUG)
logger.disabled = 1
logging.config.dictConfig({
    'version': 1,
    'disable_existing_loggers': 1
})
    
sys.excepthook = kmxTools.errorHandler

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
        self.schUtilitiesObj.loggerSetup(lookups.schLogLevel,lookups.schLogEnable)
        self.schStandardIOObj = schStandardIO.core(self)     
        self.schSettingsObj = schSettings.core(self)
        self.schInterpreterObj = schInterpreter.core(self)        
           
        self.display("Internal modules loaded!")        
        self.schDoStart()

    def schDoStart(self):
        self.display("Starting initial setup...")
        
        #Security Setup
        self.display("Ciper check...")
        if (lookups.schKey):
            lookups.ciperKey = str(self.schUtilitiesObj.getCodeForKey(lookups.schKey)) + str(self.ttls.getUUID())
            log.info('Key: {0}'.format(lookups.ciperKey))   
            self.display('Ciper ready!')                     
        else:
            self.schDoExit('Secret key missing in argument.')
        
        #StdOutput Setup
        self.display("Stream redirect check...")
        if(lookups.schStdRedirect=="file" and lookups.schMode != 'console'):
            f = lookups.schStdRedirectLogFile
            self.display('Stream redirect to file: {0}'.format(f))
            self.schStandardIOObj.toFile(f)

        #Is it a first time?
        self.display("Settings file check...")
        if self.schUtilitiesObj.isFirstTime():            
            self.display('First time user default settings prepared')
            self.schSettingsObj.saveDefaultSettings()
        self.schSettingsObj.readAllSettings()
        self.display('Settings read!')

        #Ready Search Paths
        self.display("Search paths check...")
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
        print(self.schUtilitiesObj.getWelcomeMessage())
        sch.schInterpreterObj.simpleConsole()
        
    def schDoStartConsoleApp(self):
        script = lookups.schStartupScript
        print(self.schUtilitiesObj.getWelcomeMessage())
        self.display('Running console app {0}...'.format(script))
        if(script and os.path.exists(script)):
            script = os.path.abspath(script)
            self.schInterpreterObj.runScript(script)
        else:
            self.schDoExit('Console app not found: {0}'.format(script))
    
    def schDoStartGUIApp(self):        
        script = lookups.schStartupScript
        print(self.schUtilitiesObj.getWelcomeMessage())
        self.display('Running gui app {0}...'.format(script))
        if(script and os.path.exists(script)):
            script = os.path.abspath(script)
            self.schQtApp = QtWidgets.QApplication(sys.argv)
            self.schInterpreterObj.runScript(script)
            wins = self.schQtApp.topLevelWidgets()
            if len(wins): wins[0].closeEvent = self.schDoInstanceLastAction                
            sys.exit(self.schQtApp.exec_())
        else:
            self.schDoExit('GUI app not found')
                            
    def schDoAddSearchPaths(self):       
        folder = lookups.schScriptFolder
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
        self.display('Exit Triggered: ' + msg)
        log.warn(msg)
        sys.exit()
            
    def schDoInstanceFirstAction(self):
        log.debug('Sachathya custom startup...')        
        self.cleanUpDone = False        
        
        #pass
        
        log.debug('Sachathya custom startup completed!')
                   
    def schDoInstanceLastAction(self, *arg):
        if(hasattr(self, 'cleanUpDone') and self.cleanUpDone):
            self.display('Sachathya cleanup already completed!')
        else:
            self.display('Sachathya cleanup starting...')
            if (hasattr(self, 'customCleanUp')):
                self.display('Sachathya custom cleanup running...')
                self.customCleanUp()
            
            if(hasattr(self, 'schGUIObj')):
                self.schGUIObj.guiDoSaveLayout()
            
            self.display('Sachathya cleanup completed!')
            self.cleanUpDone = True
        
        if len(arg) and arg[0].type() == 19:arg[0].accept()

    def display(self, msg, tag='MAIN'):
        stack = inspect.stack()[1] if len(inspect.stack())>=2 else ''
        stack2 = inspect.stack()[2] if len(inspect.stack())>=3 else '' 
        fileName = os.path.basename(stack[1]) if len(stack)>=2 else ''
        fn = stack[3] if len(stack)>=4 else ''
        fn2 = stack2[3] if len(stack2)>=4 else ''
        ti = self.ttls.getDateTime('%Y-%m-%d %H:%M:%S,000')
        print('[{0}] {1}() - {2}() [{3}] {4}'.format(ti,fn,fn2,tag,msg))
      
    def __enter__(self):        
        log.warn('SachathyaInstance startup actions initiated...')
        self.schDoInstanceFirstAction()
        return self        

    def __exit__(self, exc_type, exc_value, traceback):
        log.warn('SachathyaInstance exit actions initiated...')
        self.schDoInstanceLastAction()
        log.warn('Thank you for using sachathya!')
        
if __name__ == '__main__':
    
    print ('Sachathya {version}'.format(version = lookups.versionInfo))    
    with core() as sch:
        print('SachathyaInstance created!')
        atexit.register(sch.schDoInstanceLastAction)
        
        #Mode Check and Start App
        if lookups.schMode == 'console':            
            sch.schDoStartConsole()
        elif(lookups.schMode == 'gui'):
            sch.schDoStartGUI()             
        elif(lookups.schMode == 'consoleApp'):
            sch.schDoStartConsoleApp()        
        elif(lookups.schMode == 'guiApp'):
            sch.schDoStartGUIApp()        
        
        