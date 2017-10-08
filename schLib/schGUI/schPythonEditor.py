'''
Created on Sep 7, 2017

@author: npn
'''
from PyQt5.QtCore import (QFile, QFileInfo, QPoint, QSettings, QSignalMapper, QSize, QTextStream, Qt, )
from PyQt5.QtWidgets import (QAction, QApplication, QFileDialog, QMainWindow, QMdiArea, QMessageBox, QTextEdit, QWidget, QSizePolicy)
from PyQt5.QtGui import (QIcon, QKeySequence, QFont, QColor)
from PyQt5.Qsci import (QsciScintilla, QsciLexerPython, QsciAPIs)
from PyQt5 import QtCore, QtGui, Qsci, QtWidgets
from PyQt5.uic import loadUi
from schLib import schLookups as lookups

import os,sys

class core(QsciScintilla):
    '''
    classdocs
    '''

    def __init__(self, win, parent):
        '''
        Constructor

        '''

        super(core, self).__init__()
        self.tag ='PYEDIT'
        self.sch = parent
        self.win = win
        self.ttls = self.sch.ttls
        self.cmttls = self.win.cmttls
                       
        self.setMarginWidth(1, 25)
        self.setMarginLineNumbers(1, 1)
        self.setReadOnly(False)
        self.setUtf8(True)
        self.setCaretWidth(10)
        self.setCaretLineBackgroundColor(QColor("#e6fff0"))
        self.setCaretLineVisible(True)
        self.setMatchedBraceBackgroundColor(Qt.yellow)
        self.setBraceMatching(QsciScintilla.SloppyBraceMatch)
        self.setIndentationsUseTabs(False)
        self.setEolMode(Qsci.QsciScintilla.EolUnix)
        self.setTabWidth(4)
        self.setAutoIndent(True)
        
        sp = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        sp.setHorizontalStretch(1)
        sp.setVerticalStretch(0)
        self.setSizePolicy(sp)
        
        self.setAutoCompletionThreshold(1)
        self.setAutoCompletionSource(QsciScintilla.AcsAll)
        self.setAutoCompletionFillupsEnabled(True)
        self.setLexer(QsciLexerPython(self))
        
        font = QFont()
        font.setFamily('Courier')
        font.setFixedPitch(True)
        font.setPointSize(9)        
        self.lexer().setFont(font)
        self.apis = QsciAPIs(self.lexer())  
            
        for list in locals():
            self.apis.add(list)
        for list in globals():
            self.apis.add(list)

        self.apis.prepare()    
        
    def initialize(self, scriptFileName=''):
        self.sch.display('Preparing new python editor...',self.tag)
        self.cmttls.enableRightClick(self)
        self.cmttls.connectToRightClick(self, self.guiDoRightClick)
        self.isSaved=False
        self.isEdited = 0
        self.scriptFileName = scriptFileName
        if not self.scriptFileName:
            self.isNew = 1
            self.setWindowTitle('New Script')
            self.scriptName = "New Script"
            self.sch.display('Blank',self.tag)
        else:
            self.isNew = 0
            content = self.ttls.fileContent(self.scriptFileName)
            self.setText(content)
            self.scriptName = os.path.basename(self.scriptFileName)
            self.setWindowTitle(self.scriptName)
            self.sch.display(self.scriptFileName,self.tag)

    def guiDoRightClick(self, point):
        self.menu = ['Execute','','Save','Save As...']
        self.cmttls.popUpMenu(self, point, self.menu, self.guiDoOperations)
        
    def guiDoOperations(self, arg):
        if(arg[0]=='Execute'):
            self._coreDoOperations('Execute')        
        if(arg[0]=='Save'):
            self._coreDoOperations('Save')
        if(arg[0]=='Save As...'):
            self._coreDoOperations('Save As...')            
        if(arg[0]=='Close'):
            self._coreDoOperations('Close')    
                        
    def _coreDoOperations(self, todo=None):
        
        if(todo == 'Execute'):
            data = str(self.text()).strip()
            if(self.scriptFileName):
                self._coreSave(self.scriptFileName)
                self.sch.display('Executing script... ' + self.scriptFileName, self.tag)
                self.sch.schInterpreterObj.runScript(self.scriptFileName)
            else:
                self.sch.display('Executing code... ' + self.scriptName, self.tag)
                self.sch.schInterpreterObj.runCode(data, self.scriptName)
            
        elif(todo == 'Close'):
            if self.isEdited: self._confirmAndSave()
            self.close()
            self.win.mdiArea.removeSubWindow(self)
            
        elif(todo == 'Save' and not self.isSaved):
            if (self.isNew):
                fileName = self.cmttls.getFileToSave('Save python script file...', lookups.schScriptFolder, 'Python (*.py);;All Files(*)')
                if(fileName):self._coreSave(fileName)
            else:
                self._coreSave(self.scriptFileName)
                
        elif(todo == 'Save As...'):
            fileName = self.cmttls.getFileToSave('Save python script file...', lookups.schScriptFolder, 'Python (*.py);;All Files(*)')
            if(fileName): self._coreSave(fileName)

    def _confirmAndSave(self):
        res = self.cmttls.showYesNoBox('File not saved', 'Script file not yet saved. Do you want to save the file?')
        if(res and self.isNew):
            fileName = self.cmttls.getFileToSave('Save python script file...', lookups.schScriptFolder, 'Python (*.py);;All Files(*)')
            if(fileName): self._coreSave(fileName)
        elif(res and not self.isNew):    
                self._coreSave(self.scriptFileName)

    def _coreSave(self, fileName):
        self.sch.display('Saving the script file... ' + fileName, self.tag)
        data = str(self.text()).strip()
        self.ttls.writeFileContent(fileName, data)
        self.isSaved=True
        self.isEdited=False
        self.scriptFileName=fileName
        title = self.windowTitle()
        if(title[0]=='*'):
            newtitle = title[1:]
            self.setWindowTitle(newtitle)
                
    def closeEvent(self, event):
        if self.isEdited: self._confirmAndSave()
        event.accept()
                    
    def keyPressEvent(self, event):
        if(not self.isEdited):
            title = self.windowTitle()
            self.setWindowTitle('*'+title)
            self.isEdited=True
            self.isSaved=False        
        
        moddies = QtWidgets.QApplication.keyboardModifiers()
        if moddies & Qt.ControlModifier:
            if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
                self._coreDoOperations('Execute')
            if event.key() == Qt.Key_S:
                self._coreDoOperations('Save')
            if event.key() == Qt.Key_Q:
                self._coreDoOperations('Close')                
            else:
                QsciScintilla.keyPressEvent(self, event)
        else:
            QsciScintilla.keyPressEvent(self, event)

            