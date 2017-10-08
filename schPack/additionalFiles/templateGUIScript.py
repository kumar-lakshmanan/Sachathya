#For Sachathya

from PyQt5 import QtCore, QtGui, Qsci, QtWidgets
from PyQt5.uic import loadUi
from schLib import schLookups as lookups
import os
import sip
import kmxQtCommonTools
import myClass

class myClassCls(QtWidgets.QMainWindow):
	
	def __init__(self,parent):
		self.tag=self.__class__.__name__.replace('Cls','').upper()
		
		self.sch=parent
		self.schGUIObj=self.sch.schGUIObj
		self.schQtApp=self.sch.schQtApp
		self.ttls=self.sch.ttls
		self.cmttls=kmxQtCommonTools.CommonTools()

		QtWidgets.QMainWindow.__init__(self)		
		self.uiFile=myClass.__file__.replace(".py",".ui")

		loadUi(self.uiFile, self)
		self.setWindowTitle(self.__class__.__name__.replace('Cls',''))

		self.pushButton.clicked.connect(self.doRun)
		
	def initialize(self):
		self.sch.display("myClassClsObj is working fine",self.tag)

	def doRun(self):
		input = self.textEdit.toPlainText()
		self.label.setText(input)
		self.sch.display("Sample: " + input, self.tag)

if (__name__=="__main__"):
	if(not hasattr(sch, 'myClassObj') or sch.devMode or sip.isdeleted(sch.myClassObj)):
		sch.myClassObj = myClassCls(sch)
	sch.myClassObj.show()
	sch.myClassObj.raise_()
