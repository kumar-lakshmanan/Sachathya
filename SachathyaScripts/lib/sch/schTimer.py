#For Sachathya
from PyQt5 import QtCore, QtGui, Qsci, QtWidgets
from schLib import schLookups as lookups
import kmxQtCommonTools

class schTimerCls():
		
	def __init__(self,parent):
		self.tag=self.__class__.__name__.replace('Cls','').upper()
		self.sch=parent
		self.ttls=self.sch.ttls		
		self.cmttls=kmxQtCommonTools.CommonTools()
		self.sch.display("schTimerCls is ready!")
		self.fnTimerDone = {}

	def initialize(self):
		self.sch.qtime=QtCore.QTimer(self.sch.schQtApp)
		self.sch.qtime.timeout.connect(self.timeoutAction)   		
		self.sch.display("schTimerCls Initialized", self.tag)

	def addTimerExecFunctions(self, fn, argList = ()):
		self.fnTimerDone[fn.__name__]=(fn,argList)

	def startTimer(self,secs=5):
		self.sch.display("-Timer Started-", self.tag)
		self.sch.qtime.start(1000 * secs)

	def stopTimer(self):
		self.sch.display("-Timer Stopped-", self.tag)
		self.sch.qtime.stop()

	def timeoutAction(self):
		self.sch.display("---Timer Timed out--", self.tag)
		for eachFn in self.fnTimerDone:
			fns = self.fnTimerDone[eachFn]
			fnObj = fns[0]
			args = fns[1]
			fnObj(args)

if __name__ == '__main__':
	sch.schTimerClsObj = schTimerCls(sch)
	sch.schTimerClsObj.initialize()