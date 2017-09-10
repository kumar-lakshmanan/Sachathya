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
from schLib.schGUI import schPythonEditor


import kmxQtCommonTools
import kmxQtTreeWidget


class core(QtWidgets.QMainWindow):

	def __init__(self, parent=None):
		self.sch = parent
		self.ttls = self.sch.ttls
		self.tag = 'SchGUI'
		QtWidgets.QMainWindow.__init__(self)		
		self.uiFile = sys.modules[__name__].__file__
		self.uiFile = self.uiFile.replace(".py",".ui")
		loadUi(self.uiFile, self)
		self.cmttls = kmxQtCommonTools.CommonTools(self)		

	def guiInitialize(self):
		self.sch.display('Sachathya GUI Initializing...',self.tag)
		if not int(lookups.disableStream):
			self.sch.display('Output streaming redirected to gui...',self.tag)
			self.sch.schStandardIOObj.toCustom(self)
		else:
			info = 'Stream redirect to gui stopped as per config setting...'
			info += '\nContinue watching in default stream handler.'
			self.sch.display(info,self.tag)
			self.appendDisplay(info)
			
		self.guiDoAlterAndUpdateUI()
		self.guiDoInitializeScriptLister()

	def guiDoAlterAndUpdateUI(self):
		
		# Output window tweak
		self.qsciStreamOut.setEolMode(Qsci.QsciScintilla.EolWindows)
		self.qsciStreamOut.setMarginWidth(1, 0)        
		self.qsciStreamOut.setUtf8(True)
		self.qsciStreamOut.setEolVisibility(False)      
		self.qsciStreamOut.setReadOnly(True)
		self.qsciStreamOut.setFont(QFont("Courier", 8))
		self.qsciStreamOut.setColor(QColor('#ffffff'))
		self.qsciStreamOut.setPaper(QColor('#000000'))		
		self.qsciStreamOut.setSelectionForegroundColor(QColor('#000000'))
		self.qsciStreamOut.setSelectionBackgroundColor(QColor('#ffffff'))
		
		#Display basic info
		self.appendDisplay(self.sch.schUtilitiesObj.getWelcomeMessage())
		self.sch.display('GUI Update is in progress...',self.tag)
		
		#Prepare the status bar
		self.sch.display('Preparing the statusbar commandline input...',self.tag)
		self.cline= QLineEdit()
		self.cline.setPlaceholderText('>>>')
		self.cline.setFrame(False)
		self.cline.returnPressed.connect(self.guiDoExecuteCommandLine)
		self.sb = self.statusBar
		self.sb.addWidget(self.cline,1)
		self.sb.setSizeGripEnabled(0)
		self.cline.setFocus()	
		
		#MDI Updates
		self.sch.display('Updating the MDI GUI...',self.tag)
		self.cmttls.enableRightClick(self.mdiArea)
		self.cmttls.connectToRightClick(self.mdiArea, self.guiDoMDIRightClick)
		
		#ScriptLister Updates
		self.sch.display('Updating the Script lister GUI...',self.tag)
		self.cmttls.enableRightClick(self.treeWidget)
		self.cmttls.connectToRightClick(self.treeWidget, self.guiDoScriptListerRightClick)
		self.treeWidget.itemDoubleClicked.connect(self.guiDoScriptListerDoubleClick)
		
	def _coreDoActions(self, todo, arg1=''):
		if(todo=='Execute'):
			fileName = arg1
			data = self.ttls.fileContent(fileName)
			self.sch.display('Executing script... ' + fileName, self.tag)
			self.sch.schInterpreterObj.runScript(fileName)

	def guiDoScriptListerDoubleClick(self, itm):
		label = str(itm.text(0))
		fileFolderName = str(itm.data(0, QtCore.Qt.UserRole))
		typ = str(itm.data(0, QtCore.Qt.UserRole+1))		
		
		moddies = QtWidgets.QApplication.keyboardModifiers()
		if moddies & Qt.ControlModifier:
			if(typ=='file'):
				self.guiDoCreateEditor(fileFolderName)
		else:
			if(typ=='file'):
				self._coreDoActions('Execute',fileFolderName)
		
	def guiDoScriptListerRightClick(self, point):
		menu = ['Create folder','Open script folder','','Refresh']
		self.itm = self.treeWidget.itemAt(point)
		if self.itm:
			label = str(self.itm.text(0))
			data = str(self.itm.data(0, QtCore.Qt.UserRole))
			typ = str(self.itm.data(0, QtCore.Qt.UserRole+1))
			if(typ=='file'):
				menu = ['Execute','Edit','','|Delete']
			elif(typ=='dir'):
				menu = ['Create GUI Script...','Create Console Script...','','Create Folder...','','|Delete']

		self.cmttls.popUpMenu(self.treeWidget, point, menu, self.guiDoTreeOperations,self.itm)

	def guiDoTreeOperations(self, arg):
		menuName = arg[0]
		menuId = arg[1]
		menuItem = arg[2]
		addItem = arg[3]

		label = str(addItem.text(0))
		fileName = str(addItem.data(0, QtCore.Qt.UserRole))
		typ = str(addItem.data(0, QtCore.Qt.UserRole+1))
		
		if(menuName == 'Execute'):
			self._coreDoActions('Execute', fileName)
		elif(menuName == 'Edit'):
			self.guiDoCreateEditor(fileName)
			
						

	def guiDoMDIRightClick(self, point):
		self.mdiMenu = ['New','Open...','','Quit']
		self.cmttls.popUpMenu(self.mdiArea, point, self.mdiMenu, self.guiDoMDIOperations)

	def guiDoMDIOperations(self, arg):
		menuName = arg[0]
		menuId = arg[1]
		menuItem = arg[2]
		addItem = arg[3]
		
		if(menuName == 'New'):
			self.guiDoCreateEditor()
		elif(menuName == 'Open...'):
			fileName = self.cmttls.getFile('Select python script to open...', self.sch.schArgParserObj.schScriptFolder, 'Python (*.py);;All Files(*)')
			self.guiDoCreateEditor(fileName)
		elif(menuName == 'Quit'):
			self.close()
			
	def guiDoInitializeScriptLister(self):
		self.scriptHandlerObj = scriptsHandler(self, self.sch)
		self.scriptHandlerObj.loadScripts()				

	def guiDoCreateEditor(self,fileName=None):
		editor = schPythonEditor.core(self,self.sch)
		editor.initialize(fileName)
		self.mdiArea.addSubWindow(editor)
		editor.show()
		return editor		
					
	def guiDoExecuteCommandLine(self):
		val = str(self.cline.text()).strip()
		self.appendDisplay('>>> ' + val + '\n')
		self.sch.schInterpreterObj.runCommand(val)
		self.cline.setText('')
		self.cline.setFocus()
		
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
		self.tag = self.win.tag
		
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
		self.sch.display('Loading Scripts...',self.tag)
		for eachItem in os.listdir(scriptsPath):
			currentDirName = eachItem
			currentDirPath = os.path.join(scriptsPath,currentDirName)	
			if self._runFolderFilter(currentDirPath):		
				if os.path.isdir(currentDirPath):			  
					rItem = self.qtTree.createItem(currentDirName, currentDirPath)
					rItem.setData(0, QtCore.Qt.UserRole+1,  QtCore.QVariant('dir'))
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
					rItem.setData(0, QtCore.Qt.UserRole+1,  QtCore.QVariant('dir'))
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
			item.setData(0, QtCore.Qt.UserRole+1, QtCore.QVariant('file'))
			self.cmttls.setIconForItem(item,self.iconScript)
			if(parentTreeItem is None):
				plugTreeItem = self.qtTree.addNewRoot(self.win.treeWidget, item)
			else:
				plugTreeItem = self.qtTree.addChild(item, parentTreeItem)
				
		else:
			plugTreeItem = None
		return plugTreeItem   		
		