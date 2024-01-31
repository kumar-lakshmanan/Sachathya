'''
#For Sachathya
'''
from schLib import schLookups as lookups
from PyQt5 import QtCore, QtWidgets
import sip
import os

class schProcessExecuteCls():
	
	def __init__(self,parent):
		self.tag=self.__class__.__name__.replace('Cls','').upper()
		self.sch=parent
		self.ttls=self.sch.ttls
		self.sch.display("schProcessExecuteCls is ready!", self.tag)

	def initialize(self):
		self.qprocess=QtCore.QProcess()
		self.qprocessEnv=QtCore.QProcessEnvironment.systemEnvironment()
		
		self.displayErrors = True

		self.qprocess.started.connect(self.processStarted)   		
		self.qprocess.readyReadStandardOutput.connect(self.processOutput)
		self.qprocess.readyReadStandardError.connect(self.processErrorOutput)
		self.qprocess.finished.connect(self.processCompleted) # gives args
		self.qprocess.error.connect(self.processErrorOccurred)  # gives args		
		#self.qprocess.errorOccurred.connect(self.processErrorOccurred)
		self.qprocess.stateChanged.connect(self.processChanged)  # gives args		

		self.processDisplay(self.sch.ttls.getCurrentPath())
		self.sch.display("schProcessExecuteCls initialized!", self.tag)
		
	def setupExecution(self, application, workingDir='', args='', envVariableTupleList=[]):
		self.application=application
		self.workingDir=workingDir
		self.args=args
		for eachEnv in envVariableTupleList:
			if(len(eachEnv)==2):
				self.qprocessEnv.insert(eachEnv[0],eachEnv[1])

		self.qprocess.setProgram(self.application)
		self.qprocess.setArguments([self.args])
		self.qprocess.setWorkingDirectory(self.workingDir)
		self.qprocess.setProcessEnvironment(self.qprocessEnv)	

	def executionDoStart(self):
		if self.qprocess.state() != QtCore.QProcess.Running:
			command = str(self.application +  ' ' + self.args)
			self.processDisplay('Execution starting...')
			self.processDisplay('Command: ')
			self.processDisplay(command)
			self.processDisplay('Working Dir: ' + str(self.workingDir))
			#print('Custom Env: ' + ';'.join(self.parent.qprocessEnv.toStringList()))
			self.qprocess.setProcessChannelMode(QtCore.QProcess.SeparateChannels)
			#self.qprocess.setProcessChannelMode(QtCore.QProcess.ForwardedChannels)
			self.qprocess.setOpenMode(QtCore.QIODevice.Text)
			self.qprocess.start(command)
			if not self.qprocess.waitForStarted():
				self.processErrorOutput()
				self.processDisplay('Unable to start the process')

	def executionDoTerminate(self):
		if (not sip.isdeleted(self.qprocess)):		
			if self.qprocess.state() == QtCore.QProcess.Running:	
				self.processDisplay('Execution terminating...')			
				self.qprocess.kill()
				sip.delete(self.qprocess)
				self.processDisplay('Execution Terminated!')	

	def executionShowStatus(self):
		print(self._procesStatus(self.qprocess.state()))

	def processStarted(self):
		self.processDisplay('ProcessStarted...')

	def processOutput(self):
		if (not sip.isdeleted(self.qprocess)):
			if self.qprocess.canReadLine():
				QtWidgets.QApplication.processEvents()
				self.processDisplay(str(self.qprocess.readAllStandardOutput().data().decode("utf-8")))			
			
	def processErrorOutput(self):
		QtWidgets.QApplication.processEvents()
		#print('Err:'+str(self.qprocess.errorString()))
		if (not sip.isdeleted(self.qprocess)):
			data = str(self.qprocess.readAllStandardError().data().decode("utf-8"))
			#if data: self.processDisplay('\nError: '+data)
			if data and self.displayErrors: self.processDisplay(data)

	def processCompleted(self, exitCode, processStatus):
		if processStatus==0:
			self.processDisplay('--ProcessCompleted-ExitCode:--' + str(exitCode))
			self.processCompletedExternal(str(exitCode))
		if processStatus==1:
			self.processErrorOutput()
			self.processDisplay('--ProcessCrashCompleted-ExitCode:--' + str(exitCode))
			self.processCompletedExternal(str(exitCode))

	def processErrorOccurred(self, errorCode):
		self.processErrorOutput()
		if(errorCode==0):
			self.processDisplay("Process Error Occurred: FailedToStart")
		elif(errorCode==1):
			self.processDisplay("Process Error Occurred: Crashed")
		elif(errorCode==2):
			print("Process Error Occurred: Timedout")
		elif(errorCode==3):
			self.processDisplay("Process Error Occurred: ReadError")
		elif(errorCode==4):
			self.processDisplay("Process Error Occurred: WriteError")
		elif(errorCode==5):
			self.processDisplay("Process Error Occurred: UnknownError")
		
	def processChanged(self, status):
		self.processDisplay(self._procesStatus(status))

	def processCompletedExternal(self, code):
		print('Completed: ' + code)
		
	def _procesStatus(self, status):
		if status == QtCore.QProcess.Running:
			return "Process Status: Running"
		elif status == QtCore.QProcess.Starting:
			return "Process Status: Starting"
		elif status == QtCore.QProcess.NotRunning:
			self.processErrorOutput()
			return "Process Status: NotRunning (Could be completed/Crashed/Stopped/Not yet Started)"
			
	def processDisplay(self, content):
		print(content)

		
if __name__ == '__main__':
	sch.schProcessExecuteClsObj = schProcessExecuteCls(sch)
	sch.schProcessExecuteClsObj.initialize()
	
	inputFile = 'D:\\Youtubes\\Audio\\ChoRamasamy\\010_Track_Cho ramaswamy - on Hinduism.mp3'
	outputFile = 'D:\\Youtubes\\Audio\\ChoRamasamy\\010_Track_Cho ramaswamy - on Hinduism.amr'	

	app = 'ffmpeg'
	cwd = '.'
	args = '-i "{0}" -nostdin -y -ar 8000 -ab 12.2k -ac 1 "{1}"'.format(inputFile,outputFile)
	

	sch.schProcessExecuteClsObj.displayErrors = True
	sch.schProcessExecuteClsObj.setupExecution(app,cwd,args)
	sch.schProcessExecuteClsObj.executionDoStart()
		