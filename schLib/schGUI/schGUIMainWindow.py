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


class core(QtWidgets.QMainWindow):

	def __init__(self, parent=None):
		self.sch = parent
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
		
		self.guiDoPrepareStatusBar()

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
		val = str(self.cline.text())
		self.appendDisplay(val+'\n')
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
		