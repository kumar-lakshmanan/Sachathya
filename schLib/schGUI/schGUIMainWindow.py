#For DevConsole
import inspect
import os

from PyQt5.QtCore import (QFile, QFileInfo, QPoint, QSettings, QSignalMapper, QSize, QTextStream, Qt, )
from PyQt5.QtWidgets import (QAction, QApplication, QFileDialog, QMainWindow, QMdiArea, QMessageBox, QTextEdit, QWidget, )
from PyQt5.QtGui import (QIcon, QKeySequence, QFont, QColor)
from PyQt5.Qsci import (QsciScintilla, QsciLexerPython)
from PyQt5 import QtCore, QtGui, Qsci, QtWidgets
from PyQt5.uic import loadUi
import os
import sys
import logging as log
from PyQt5.Qt import QLineEdit
from schLib import schLookups as lookups
from schLib import fatcow_rc

import kmxQtCommonTools
import kmxQtTreeWidget


class core(QtWidgets.QMainWindow):

	def __init__(self, parent=None):
		self.sch = parent
		self.ttls = self.sch.ttls
		QtWidgets.QMainWindow.__init__(self)		
		self.uiFile = sys.modules[__name__].__file__
		self.uiFile = self.uiFile.replace(".py",".ui")
		loadUi(self.uiFile, self)		
		self.tag = 'SchGUI'

	def guiInitialize(self):
		self.sch.display('Sachathya GUI Initializing...',self.tag)
		
		self.sch.display('Output streaming redirected to gui...',self.tag)
		self.sch.schStandardIOObj.toCustom(self)
		self.guiDoPrepareOutput()
		self.appendDisplay(self.sch.schUtilitiesObj.getWelcomeMessage())
		self.guiDoPrepareStatusBar()
		self.scriptHandlerObj = scriptsHandler(self, self.sch)
		self.scriptHandlerObj.loadScripts()

	def guiDoPrepareStatusBar(self):
		self.sch.display('Preparing the statusbar commandline input...',self.tag)
		self.cline= QLineEdit()
		self.cline.setPlaceholderText('>>>')
		self.cline.setFrame(False)
		self.cline.returnPressed.connect(self.guiDoExecuteCommandLine)
		self.sb = self.statusBar
		self.sb.addWidget(self.cline,1)
		self.sb.setSizeGripEnabled(0)
		self.cline.setFocus()
		
	def guiDoExecuteCommandLine(self):
		val = str(self.cline.text()).strip()
		self.appendDisplay('>>> ' + val + '\n')
		self.sch.schInterpreterObj.runCommand(val)
		self.cline.setText('')
		self.cline.setFocus()
		
	def guiDoPrepareOutput(self):
		self.qsciStreamOut.setEolMode(Qsci.QsciScintilla.EolWindows)
		#self.qsciStreamOut.setIndentationsUseTabs(True)
		#self.qsciStreamOut.setTabWidth(4)
		self.qsciStreamOut.setMarginWidth(1, 0)        
		self.qsciStreamOut.setUtf8(True)
		self.qsciStreamOut.setEolVisibility(False)      
		self.qsciStreamOut.setReadOnly(True)
		self.qsciStreamOut.setFont(QFont("Courier", 8))
		self.qsciStreamOut.setColor(QColor('#ffffff'))
		self.qsciStreamOut.setPaper(QColor('#000000'))		
		self.qsciStreamOut.setSelectionForegroundColor(QColor('#000000'))
		self.qsciStreamOut.setSelectionBackgroundColor(QColor('#ffffff'))
		
	def write(self, data):
		self.appendDisplay(data)
	
	def appendDisplay(self, data):
		self.qsciStreamOut.setCursorPosition(self.qsciStreamOut.lines(), 0)
		self.qsciStreamOut.insertAt(data, self.qsciStreamOut.lines(), 0)
		vsb = self.qsciStreamOut.verticalScrollBar()
		vsb.setValue(vsb.maximum())    
		hsb = self.qsciStreamOut.horizontalScrollBar()
		hsb.setValue(0)    		

class scriptsHandler():

	def __init__(self, win=None, parent=None):
		self.win = win
		self.sch = parent
		self.ttls = self.sch.ttls
		self.cmttls = kmxQtCommonTools.CommonTools(self.win)
		self.qtTree = kmxQtTreeWidget.TreeWidget()
		
		self.iconApp = 'roadworks.png'
		self.iconFolder = 'folder.png'
		self.iconScript = 'code.png'
		
		self.disallowedFolder = ['__','.git']
		self.allowedFiles = ['.py']
		
		self.win.setWindowIcon(self.cmttls.getIcon(self.iconApp))
	
	def _runFolderFilter(self, folderpath):		
		for eachFilter in self.disallowedFolder:
			if (eachFilter.lower() in folderpath.lower()):
				return False
		return True

	def _runFileFilter(self, filepath):
		ext = os.path.splitext(filepath)
		return ext[1] in self.allowedFiles
	
	def loadScripts(self):
		self.win.treeWidget.clear()	
		scriptsPath = self.sch.schArgParserObj.schScriptFolder
		print("Populating scripts... ")
		for eachItem in os.listdir(scriptsPath):
			currentDirName = eachItem
			currentDirPath = os.path.join(scriptsPath,currentDirName)	
			if self._runFolderFilter(currentDirPath):		
				if os.path.isdir(currentDirPath):			  
					rItem = self.qtTree.createItem(currentDirName, currentDirPath)
					self.qtTree.addNewRoot(self.win.treeWidget, rItem)
					self.cmttls.setIconForItem(rItem,self.iconFolder)
					self.populateCore(rItem, currentDirPath)
				else:
					self.createScriptItem(currentDirPath)	
						
		print("Scripts Loaded!")
												
	def populateCore(self, parentItem, searchPath):					  
		
		for eachItem in os.listdir(searchPath):
			currentDirName = eachItem
			currentDirPath = os.path.join(searchPath,currentDirName)	
			if self._runFolderFilter(currentDirPath):
				if os.path.isdir(currentDirPath):
					rItem = self.qtTree.createItem(currentDirName,currentDirPath)
					self.cmttls.setIconForItem(rItem,self.iconFolder)
					self.qtTree.addChild(rItem, parentItem)
					self.populateCore(rItem, currentDirPath)
				else:
					self.createScriptItem(currentDirPath, parentItem)   

	def createScriptItem(self, plugFile, parentTreeItem=None):
		modName = os.path.basename(plugFile).replace(os.path.splitext(plugFile)[1], '')
		content = self.ttls.fileContent(plugFile)
		expecting = "d" 
		if(expecting in content and self._runFileFilter(plugFile)):
			item = self.qtTree.createItem(modName, plugFile)
			self.cmttls.setIconForItem(item,self.iconScript)
			if(parentTreeItem is None):
				plugTreeItem = self.qtTree.addNewRoot(self.win.treeWidget, item)
			else:
				plugTreeItem = self.qtTree.addChild(item, parentTreeItem)
				
		else:
			plugTreeItem = None
		return plugTreeItem   		
		