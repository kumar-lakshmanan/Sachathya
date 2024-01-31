'''
Created on Oct 22, 2015

@author: MUKUND-update-yes
'''

import logging
from PyInstaller.building import build_main
from logging import getLogger
from PyQt5 import QtWidgets, QtGui
from PyQt5.uic import loadUi
import sys
import importlib

import SchPacker
import kmxTools
from schLib import schLookups

#logFormt = '%(relativeCreated)d %(levelname)s: %(message)s'
logFormt = '[%(asctime)s] %(module)s %(funcName)s [%(levelname)s] %(message)s' 
logLevel = logging.DEBUG
 
#Ready logger
logging.basicConfig(format=logFormt, level=logLevel)
logger=getLogger(__name__)

class ReleaseBuilder(QtWidgets.QDialog):

    def __init__(self):
        self.tag = self.__class__.__name__
        QtWidgets.QDialog.__init__(self)        
        loadUi(SchPacker.builderUI, self)

        self.ttls = kmxTools.Tools()
        self.doUpdatedVersionValues()

    def display(self):
        info = ''
        info += 'Current Version: ' + self.cVersion
        info += '\nLast Update: ' + self.cUpdateDate
        info += '\nLast Release Type : ' + self.cReleaseType

        info += '\n\nNew Version: ' + self.newVersion
        info += '\nNew Update: ' + self.releaseDate
        info += '\nNew Release Type: ' + self.releaseType
                
        self.textBrowser.setPlainText(info)
        
        info = 'Version History:\n\n'
        info += self.cVersionHistoryContent
        self.textBrowser_2.setPlainText(info)

    def doUpdatedVersionValues(self):
        importlib.reload(schLookups)
        self.cVersion = schLookups.__version__
        self.cUpdateDate = schLookups.__updated__
        self.cReleaseType = schLookups.__release__
        self.cVersionHistoryContent = self.ttls.fileContent(SchPacker.schVersionHistoryFile)
        
        self.releaseType = 'Test'
        if self.radioButton.isChecked():
            self.releaseType = 'Major'
        if self.radioButton_2.isChecked():
            self.releaseType = 'Minor'
        if self.radioButton_3.isChecked():
            self.releaseType = 'Fix'                    
        if self.radioButton_4.isChecked():
            self.releaseType = 'Test'
            
        self.releaseDate = self.ttls.getDateTime('%Y-%m-%d')
        
        versionNo = self.cVersion.split('.')
        major = versionNo[0]
        minor = versionNo[1]
        fix = versionNo[2]

        newMajor = int(major)
        newMinor = int(minor)
        newFix = int(fix)
        
        self.newVersion = ''
        
        if(self.releaseType == 'Major'):
            newMajor = newMajor+1
            newMinor = 0
            newFix = 0
        if(self.releaseType == 'Minor'):
            newMinor = newMinor+1
            newFix = 0
        if(self.releaseType == 'Fix'):
            newFix = newFix+1
                                                
        self.newVersion = '{major}.{minor}.{fix}'.format(major=newMajor,minor=newMinor,fix=newFix)
        self.display()
        
    def doFileUpdates(self):
        
        self.cVersion = schLookups.__version__
        self.cUpdateDate = schLookups.__updated__
        self.cReleaseType = schLookups.__release__        
        self.cVersionFileContent = self.ttls.fileContent(SchPacker.schVersionFile)
        self.cVersionHistoryContent = self.ttls.fileContent(SchPacker.schVersionHistoryFile)
        
        self.doUpdatedVersionValues()
        
        versionFileContent = self.cVersionFileContent
        old = "__version__ = '{0}'".format(self.cVersion)
        new = "__version__ = '{0}'".format(self.newVersion)
        versionFileContent = versionFileContent.replace(old, new)
        
        old = "__updated__ = '{0}'".format(self.cUpdateDate)
        new = "__updated__ = '{0}'".format(self.releaseDate)
        versionFileContent = versionFileContent.replace(old, new)

        old = "__release__ = '{0}'".format(self.cReleaseType)
        new = "__release__ = '{0}'".format(self.releaseType)
        versionFileContent = versionFileContent.replace(old, new)
        
        self.ttls.writeFileContent(SchPacker.schVersionFile, versionFileContent)
        
        changeContent = str(self.textEdit.toPlainText())
        versionHistoryHeader = '{date} - {type} - {version}'.format(date=self.releaseDate,type=self.releaseType,version=self.newVersion)
        newVersionHistory = '{old}\n\n{header}\n{content}'.format(old=self.cVersionHistoryContent,header=versionHistoryHeader,content=changeContent)
        
        self.ttls.writeFileContent(SchPacker.schVersionHistoryFile, newVersionHistory)
        
            
    def doPlainBuild(self):
        logger.debug('Requested plain build process...')
        self.pushButton.setEnabled(0)
        self.pushButton_3.setEnabled(0)
        self.startBuilder()
        
    def doStart(self):
        logger.debug('Start build process...')
        self.pushButton.setEnabled(0)
        self.pushButton_3.setEnabled(0)
        
        self.doFileUpdates()
        self.startBuilder()
        self.doUpdatedVersionValues()

    def doCancel(self):
        logger.debug('Closing the build system')
        sys.exit()
        
    def startBuilder(self):
        logger.debug("Build process starting...")
        SchPacker.doPreProcessing()
        build_main.main(None, SchPacker.buildSpecFile, noconfirm=True, ascii=True, distpath=SchPacker.distPath, workpath=SchPacker.buildPath, clean_build=True)
        #build_main.main(self.cfg, None, noconfirm=True, ascii=True, distpath=distpath, workpath=workpath, clean_build=True)        
        logger.debug("Build Completed!")        

def startUI():
    app = QtWidgets.QApplication(sys.argv)
    r = ReleaseBuilder()
    r.show()
    app.exec_()