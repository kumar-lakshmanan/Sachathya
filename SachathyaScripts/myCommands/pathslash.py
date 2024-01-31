#For Sachathya

from PyQt5 import QtCore, QtGui, Qsci, QtWidgets
from PyQt5.uic import loadUi
from schLib import schLookups as lookups
import os
import sip
import pathslash

class pathslashCls():
	
	def __init__(self,parent):
		self.tag=self.__class__.__name__.replace('Cls','').upper()
		
		self.sch=parent
		self.schGUIObj=self.sch.schGUIObj
		self.schQtApp=self.sch.schQtApp
		self.ttls=self.sch.ttls
		
	def initialize(self):
		self.path = self.doGetClipboard()
		if self.path.find('\\\\')==-1:
			self.path = self.path.replace('\\','\\\\')
		print(self.path)
		self.doSetClipboard(self.path)

	def doSetClipboard(self, text):
		cb = self.sch.schQtApp.clipboard()
		cb.clear(mode=cb.Clipboard)
		cb.setText(text, mode=cb.Clipboard)	
	
	def doGetClipboard(self):
		cb = self.sch.schQtApp.clipboard()
		return str(cb.text(mode=cb.Clipboard))
	
if (__name__=="__main__"):
	if(not hasattr(sch, 'pathslashObj') or sch.devMode):
		sch.pathslashObj = pathslashCls(sch)
	sch.pathslashObj.initialize()