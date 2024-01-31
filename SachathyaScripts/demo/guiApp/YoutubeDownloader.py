#For Sachathya

from schLib import schLookups as lookups
import schProcessExecute
import schLoadSaver
import kmxQtCommonTools
from PyQt5 import QtCore, QtGui, Qsci, QtWidgets

class YoutubeDownloaderCls():
    

    def __init__(self,parent):
        self.tag=self.__class__.__name__.replace('Cls','').upper()
        self.sch=parent
        self.ttls=self.sch.ttls
        self.cmttls=kmxQtCommonTools.CommonTools()
        self.sch.display("YoutubeDownloader is ready!", self.tag)

    def initialize(self):
        self.sch.display("YoutubeDownloader initialized more info added!", self.tag)
        self.doReadyWindow()

    def doReadyWindow(self):        
        self.window, layout, lst = self.cmttls.createVerticalWindow(None,'YoutubeDownloader',None)
        self.window.setWindowTitle('Youtube Downloader')
        self.inputTxt = QtWidgets.QTextEdit(self.window)
        self.inputTxt2 = QtWidgets.QLineEdit(self.window)
        self.btnDownAudio = QtWidgets.QPushButton('Download Audio', self.window)
        self.btnDownVideo = QtWidgets.QPushButton('Download Video', self.window)
        self.btnStop = QtWidgets.QPushButton('Stop', self.window)    

        self.btnLoadSave = QtWidgets.QPushButton('Load/Save', self.window)
        
        layout.addWidget(self.inputTxt)
        layout.addWidget(self.inputTxt2)
        layout.addWidget(self.btnDownAudio)
        layout.addWidget(self.btnDownVideo)
        layout.addWidget(self.btnStop)
        layout.addStretch()
        layout.addWidget(self.btnLoadSave)
        
        self.btnDownAudio.clicked.connect(self.doStart)
        self.btnDownVideo.clicked.connect(self.doStart)
        self.btnLoadSave.clicked.connect(self.doLoadSave)

        self.btnStop.clicked.connect(self.doStop)
        self.inputTxt2.setText('D:\\Audio\\NonMusic\\TracksByVelkudis')    
        self.inputTxt.setText('https://www.youtube.com/watch?v=o9lIS5X069A&list=PLmePPSf6_0Svpgo0rzYgmwORlPKJ4P982')    
        self.window.show()        

    def getCommandAudio(self):
        #Download youtube playlist as mp3
        ret = '''        
        --extract-audio
        --audio-format "mp3"
        --audio-quality 0
        --retries 5
        --ignore-errors 
        --continue
        --output "{0}\\%(autonumber)03d_Track_%(title)s.%(ext)s"
        {1}
        '''
        return ret

    def getCommandVideo(self):
        #Download youtube playlist as mp3
        ret = '''        
        --retries 5
        --ignore-errors 
        --continue
        --output "{0}\\%(autonumber)03d_Track_%(title)s.%(ext)s"
        {1}
        '''
        return ret

    def doLoadSave(self):
        
        self.ls = schLoadSaver.schLoadSaverCls(self.sch,self.window)    
        
        self.ls.systemName = 'LoadSave'
        self.ls.systemNameShort = 'yt'
        self.ls.saveFolder = '.\\ytSettings'
        self.ls.ext = '.ini'        

        input1 = self.inputTxt.toPlainText()
        input2 = self.inputTxt2.text()        
        self.ls.objToSave = [input1,input2]
        
        self.ls.showLoadSave()
        
        data = self.ls.getObject()
        if(data):
            self.inputTxt.setText(data[0])
            self.inputTxt2.setText(data[1])            
        
        
    def doStart(self):        
        req = self.window.sender().text()
        
        input1 = self.inputTxt.toPlainText()
        input2 = self.inputTxt2.text()

        self.app = 'E:\\YoutubeDownloader\\bin\\youtube-dl.exe'
        self.cwd = 'E:\\YoutubeDownloader\\bin'
        
        if(req == 'Download Audio'):
            self.args = self.getCommandAudio().format(input2,input1)
        elif(req == 'Download Video'):
            self.args = self.getCommandVideo().format(input2,input1)
            
        self.sch.schProcessExecuteObj = schProcessExecute.schProcessExecuteCls(sch)
        self.sch.schProcessExecuteObj.initialize()

        self.sch.schProcessExecuteObj.displayErrors = True 
        self.sch.schProcessExecuteObj.processCompletedExternal = self.pyExCompleted    
        self.sch.schProcessExecuteObj.setupExecution(self.app,self.cwd,self.args)
        self.sch.schProcessExecuteObj.executionDoStart()

    def doStop(self):        
        self.sch.schProcessExecuteObj.executionDoTerminate()

    def pyExCompleted(self, code):
        print('Youtube Download Completed!')

if __name__ == '__main__':
    if(not hasattr(sch, 'YoutubeDownloaderObj') or sch.devMode):
        sch.YoutubeDownloaderObj = YoutubeDownloaderCls(sch)
    sch.YoutubeDownloaderObj.initialize()