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
import subprocess
import time

import kmxQtCommonTools
import kmxQtTreeWidget
from _operator import add


class core(QtWidgets.QMainWindow):

	def __init__(self, parent=None):
		log.info('Preparing GUI...')
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
		self.guiDoRunGUIStarterScript()
		self.guiDoLoadLayout()
		
		self.sch.display('Sachathya is ready!',self.tag)
	
	def guiDoSaveLayout(self):
		self.sch.display('Saving GUI layout... ', self.tag)
		self.cmttls.uiLayoutSave('layout.lyt')

	def guiDoLoadLayout(self):
		self.sch.display('Loading GUI layout... ', self.tag)
		self.cmttls.uiLayoutRestore('layout.lyt')

	def guiDoRunGUIStarterScript(self):
		self.sch.display('Running default startup script... ' + str(lookups.schStartupScript), self.tag)
		self._coreDoActions('Execute',lookups.schStartupScript)
				
		self.sch.display('Running GUI startup script... ' + str(lookups.guiStartUpScript), self.tag)
		self._coreDoActions('Execute',lookups.guiStartUpScript)
				
	def guiDoAlterAndUpdateUI(self):
		log.info('GUI alter and update...')
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
		self.appendDisplay(self.sch.schUtilitiesObj.getWelcomeGUIMessage())
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
			if(fileName and os.path.isfile(fileName) and os.path.exists(fileName)):
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
		menu = ['Create Folder...','Open Scripts Folder','','Refresh']
		self.itm = self.treeWidget.itemAt(point)
		if self.itm:
			label = str(self.itm.text(0))
			fileFolder = str(self.itm.data(0, QtCore.Qt.UserRole))
			typ = str(self.itm.data(0, QtCore.Qt.UserRole+1))
			
			if(typ=='file'):
				if (self.hasGUI(fileFolder)):
					menu = ['Execute','','Edit Script','Edit GUI','','Delete']
				else:
					menu = ['Execute','','Edit Script','|Edit GUI','','Delete']
			elif(typ=='dir'):
				menu = ['Create GUI Script...','Create Console Script...','','Create Folder...']

		self.cmttls.popUpMenu(self.treeWidget, point, menu, self.guiDoTreeOperations,self.itm)
	
	def hasGUI(self,nFileName=None):
		nFileName = nFileName.replace('py','ui')
		return os.path.isfile(nFileName) and os.path.exists(nFileName)

	def guiDoTreeOperations(self, arg):
		menuName = arg[0]
		menuId = arg[1]
		menuItem = arg[2]
		addItem = arg[3]

		if(addItem):
			label = str(addItem.text(0))
			fileName = str(addItem.data(0, QtCore.Qt.UserRole))
			typ = str(addItem.data(0, QtCore.Qt.UserRole+1))
		else:
			label = ''
			fileName = lookups.schScriptFolder
			typ = ''
		
		if(menuName == 'Execute'):
			self._coreDoActions('Execute', fileName)
		elif(menuName == 'Edit Script'):
			self.guiDoCreateEditor(fileName)
		elif(menuName == 'Edit GUI'):
			self.guiDoLaunchUIEditor(fileName)			
		elif(menuName == 'Create Console Script...'):
			self.guiDoCreateNewConsoleScript(fileName)
			self.scriptHandlerObj.loadScripts()	
		elif(menuName == 'Create GUI Script...'):
			self.guiDoCreateNewGUIScript(fileName)
			self.scriptHandlerObj.loadScripts()	
		elif(menuName == 'Create Folder...'):
			self.guiDoCreateNewFolder(fileName)
		elif(menuName == 'Delete'):
			self.guiDoDelete(typ,fileName)
			self.scriptHandlerObj.loadScripts()	
		elif(menuName == 'Refresh'):
			self.scriptHandlerObj.loadScripts()	
		elif(menuName == 'Open Scripts Folder'):
			self.guiDoOpenScriptsFolder()	
	
	def guiDoOpenScriptsFolder(self):
		command = 'explorer "{0}"'.format(lookups.schScriptFolder)
		self.sch.display('Executing Shell: ' + command)
		self.cmttls.shellExecute(command)  		
		
	def guiDoCreateNewFolder(self, loc):
		log.info('Create folder requested ' + str(loc))
		folder = os.path.abspath(loc)
		val = self.cmttls.showInputBox('New Folder','Enter folder name','mySplPack')
		if(val):
			folder = os.path.join(folder,val)
			log.info('Creating folder... ' + str(folder))
			os.mkdir(folder)
			log.info('Done')
		
	def guiDoDelete(self, typ, fileFolder):
		log.info('Delete item requested ' + str(fileFolder))
		if(typ=='file'):
			file1 = fileFolder
			file2 = fileFolder.replace('py','ui') if self.hasGUI(fileFolder) else None
			try:
				if(file1 and os.path.exists(file1)):
					print("Deleting..." + file1)
					os.remove(file1)
				if(file2 and os.path.exists(file2)):
					print("Deleting..." + file2)
					os.remove(file2)
			except:
				self.ttls.errorInfo()   
			
	def guiDoCreateNewGUIScript(self,loc):
		log.info('Create item requested ' + str(loc))
		folder = os.path.abspath(loc)
		val = self.cmttls.showInputBox('GUI Script','Enter module name','newGUIModule')
		if(val):
			newPYFile = os.path.join(folder,val+'.py')
			newUIFile = os.path.join(folder,val+'.ui')

			templateFile = os.path.abspath('templateGUIScript.py')			
			content = self.sch.ttls.fileContent(templateFile)
			content = content.replace('myClass',val)
			self.sch.ttls.writeFileContent(newPYFile, content)
			
			templateFile = os.path.abspath('templateGUIScript.ui')			
			content = self.sch.ttls.fileContent(templateFile)
			content = content.replace('myClass',val)
			self.sch.ttls.writeFileContent(newUIFile, content)
			
	def guiDoCreateNewConsoleScript(self,loc):
		log.info('Create item console script requested ' + str(loc))
		folder = os.path.abspath(loc)
		val = self.cmttls.showInputBox('Console Script','Enter module name','newModule')
		if(val):
			newFile = os.path.join(folder,val+'.py')
			templateFile = os.path.abspath('templateConsoleScript.py')			
			content = self.sch.ttls.fileContent(templateFile)
			content = content.replace('myClass',val)
			self.sch.ttls.writeFileContent(newFile, content)

	def guiDoLaunchUIEditor(self, fileName):
		log.info('Launch UI Editor requested ' + str(fileName))
		fileName = fileName.replace('py','ui')
		command = '"' + lookups.pyDesigner + '"' + " " + '"' + fileName + '"'
		self.cmttls.shellExecute(command)  

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
			fileName = self.cmttls.getFile('Select python script to open...', lookups.schScriptFolder, 'Python (*.py);;All Files(*)')
			if(fileName):self.guiDoCreateEditor(fileName)
		elif(menuName == 'Quit'):
			self.close()
			
	def guiDoInitializeScriptLister(self):
		log.info('Script initial loading starts ')
		self.scriptHandlerObj = scriptsHandler(self, self.sch)
		self.scriptHandlerObj.loadScripts()				

	def guiDoCreateEditor(self,fileName=None):
		log.info('Creating new editor ' + str(fileName))
		editor = schPythonEditor.core(self,self.sch)
		editor.initialize(fileName)
		self.mdiArea.addSubWindow(editor)
		editor.show()
		return editor		
					
	def guiDoExecuteCommandLine(self):
		log.info('Executing command line ')
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
		scriptsPath = lookups.schScriptFolder
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
						
		self.sch.display("Scripts Loaded!",self.tag)
												
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
		log.debug('Found script...' + str(plugFile))
		modName = os.path.basename(plugFile).replace(os.path.splitext(plugFile)[1], '')
		content = self.ttls.fileContent(plugFile)
		expecting = "for sachathya" 
		if(expecting.lower() in content.lower() and self._runFileFilter(plugFile)):
			item = self.qtTree.createItem(modName, plugFile)
			item.setData(0, QtCore.Qt.UserRole+1, QtCore.QVariant('file'))
			self.cmttls.setIconForItem(item,self.iconScript)
			log.debug('Adding script...' + str(plugFile))
			if(parentTreeItem is None):
				plugTreeItem = self.qtTree.addNewRoot(self.win.treeWidget, item)
			else:
				plugTreeItem = self.qtTree.addChild(item, parentTreeItem)
				
		else:
			plugTreeItem = None
		return plugTreeItem   		
		