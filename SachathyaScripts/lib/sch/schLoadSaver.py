#For Sachathya
from schLib import schLookups as lookups
from PyQt5 import QtCore, QtGui, QtWidgets
import os
import kmxQtCommonTools
from PyQt5 import QtCore, QtGui, Qsci, QtWidgets

class schLoadSaverCls():
		
	"""
	import schLoadSaver
	
	self.ls = schLoadSaver.schLoadSaverCls()
	
	self.ls.systemName = 'MySystem'
	self.ls.systemNameShort = 'ms'
	self.ls.saveFolder = '.\\msSettings'
	self.ls.ext = 'ini'
	
	#Non - GUI Style - Save 
	self.ls.objToSave = ['item1','item2]
	self.ls.save('saveOne')
	
	#Non - GUI Style - Load
	self.ls.load('saveOne')
	data = self.ls.getObject()
	print(data)
	
	#-----
	
	#GUI Style - Save
	self.ls.objToSave = ['item1','item2]
	self.ls.showLoadSave()
	
	#GUI Style - load
	self.ls.objToSave = ['item1','item2]
	self.ls.showLoadSave()
	data = self.ls.getObject()
	print(data)
	
	
	"""
	
	def __init__(self,parent,winParent=None):
		self.tag=self.__class__.__name__.replace('Cls','').upper()
		self.sch=parent
		self.ttls=self.sch.ttls
		self.cmttls=kmxQtCommonTools.CommonTools()
		self.sch.display("schLoadSaver is ready!", self.tag)
		self.winParent=winParent
		
		self.systemName = 'SampleSystem'
		self.systemNameShort = 'sms'
		self.saveFolder = '.\\loadSaver'
		self.ext = '.ini'
		self.objToSave = None
		self.objLoaded = None

	def guiSetup(self):
		self.createWindowSetup()
		self.readyFileList()
			
	def getObject(self):
		return self.objLoaded
	
	def save(self, name='default'):
		if(not self.ttls.isPathOK(self.saveFolder)):
			self.ttls.makePath(self.saveFolder)
					
		if(name):
			fileName = os.path.join(self.saveFolder, '{0}{1}{2}'.format(self.systemNameShort,name,self.ext))		
			self.sch.ttls.pickleSaveObject(self.objToSave,fileName)
			print('Saving..{0}\n{1}'.format(self.objToSave,fileName))
			if(hasattr(self, 'win')):
				self.readyFileList()		
	
	def load(self, name='default'):
		if(name):
			if(not name.startswith(self.systemNameShort)):
				name = self.systemNameShort + name
			if(not name.endswith(self.ext)):
				name = name + self.ext
			
		fileName = os.path.join(self.saveFolder, name)
		print('Loading...' + fileName)
		self.objLoaded = None
		if(os.path.exists(fileName)):
			self.objLoaded = self.sch.ttls.pickleLoadObject(fileName)
			if(hasattr(self, 'win')):
				self.win.close()	
	
	def readyFileList(self):
		if(not self.ttls.isPathOK(self.saveFolder)):
			self.ttls.makePath(self.saveFolder)
				
		itms = []
		for eachFile in os.listdir(self.saveFolder):
			if (str(eachFile).endswith(self.ext) and str(eachFile).startswith(self.systemNameShort)):
				itms.append(str(eachFile))
				
		self.win.list.clear()	
		for eachItm in itms:
			listItm = QtWidgets.QListWidgetItem()
			listItm.setText(str(eachItm))
			self.win.list.addItem(listItm)
					
	def createWindowSetup(self):
		self.win, self.layout, lst = self.cmttls.createVerticalWindow(self.winParent, self.systemName, None)
		
		self.win.list = QtWidgets.QListWidget(self.win)
		self.win.list.itemDoubleClicked.connect(self.doLoad)
		self.layout.addWidget(self.win.list)

		self.win.saveBtn = QtWidgets.QPushButton('Save', self.win)
		self.win.saveBtn.clicked.connect(self.doSave)
		self.layout.addWidget(self.win.saveBtn)

	def showLoadSave(self):
		self.guiSetup()
		self.win.setModal(1)
		self.win.exec_()
		
	def doSave(self):
		name = self.cmttls.showInputBox(self.systemName ,'Save data to a file...')
		self.save(name)

	def doLoad(self, itm):
		self.load(itm.text())
		
if __name__ == '__main__':
	sch.devMode=1
	if(not hasattr(sch, 'schLoadSaverObj') or sch.devMode):	
		sch.schLoadSaverObj = schLoadSaverCls(sch)	
		
	self.ls = sch.schLoadSaverObj
	
	self.ls.systemName = 'MySystem'
	self.ls.systemNameShort = 'ms'
	self.ls.saveFolder = '.\\msSettings'
	self.ls.ext = '.ini'
	
	#Non - GUI Style - Save 
	self.ls.objToSave = ['item5','item4']
	self.ls.save('save3')
	
	#Non - GUI Style - Load
	self.ls.load('saveOne')
	data = self.ls.getObject()
	print(data)
	
	#-----
	
	#GUI Style - Save
	self.ls.objToSave = ['itemxxx1','itemccc2']
	#self.ls.showLoadSave()	

	
	#GUI Style - load
	self.ls.objToSave = ['itettrtretetm1','item2ccccccccccvvvvvv']
	self.ls.showLoadSave()
	data = self.ls.getObject()
	print(data)
