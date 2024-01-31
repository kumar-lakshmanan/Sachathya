'''
Created on Aug 27, 2017

@author: npn
'''
from schLib import schLookups as lookups
import configparser
import logging as log
import kmxTools

class core(object):
    '''
    classdocs
    '''

    def __init__(self,core=None, fileName=lookups.configFile):
        '''
        Constructor
        '''
        log.info('Config/Settings setup loading...')
        self.sch=core
        self.ttls = kmxTools.Tools()
        self.cfg=configparser.ConfigParser()
        self.fileName=fileName
        self.readConfig(self.fileName)
        log.info('Config/Settings setup done!')
    
    def saveDefaultSettings(self):
        log.info('Preparing config file with default settings')
        self.writeSetting('userName', 'Enter Your Name', 'General')
        self.writeSetting('userEmailId', 'Enter Your Name Email Id', 'General')
        self.writeSetting('disableStream', 0, 'GUI')        
        self.writeSetting('pyDesigner', 'C:\\Python34\\Lib\\site-packages\\PyQt6\\designer.exe', 'GUI')
        self.writeSetting('guiStartUpScript', 'None', 'GUI')
        self.storeConfig()
 
    def readAllSettings(self):
        log.info('Reading config file for settings')
        lookups.userName = self.readSetting('userName', 'General')
        lookups.userEmailId = self.readSetting('userEmailId', 'General')
        lookups.disableStream = self.readSetting('disableStream','GUI',0) 
        lookups.pyDesigner = self.readSetting('pyDesigner','GUI','C:\\Python34\\Lib\\site-packages\\PyQt6\\designer.exe')
        lookups.guiStartUpScript = self.readSetting('guiStartUpScript','GUI','None')
        log.info('Reading config file completd!')
        
    def readSetting(self, option, section='General', default=None):
        if (self.cfg.has_section(section) and self.cfg.has_option(section, option)):            
            return self.cfg.get(section, option)
        else:
            log.error('{0} missing or {0} has no option {1}'.format(section,option))
            return default
                    
    def writeSetting(self, option, value=None, section='General'):
        if (not self.cfg.has_section(section)):            
            self.cfg.add_section(section)
        self.cfg.set(section, option, str(value))
    
    def readConfig(self, fileName=lookups.configFile):
        fileName = fileName if fileName else self.fileName
        if not self.ttls.isPathOK(fileName): self.ttls.makeEmptyFile(fileName)
        log.info('{0} - Config settings read!'.format(fileName))
        fh = open(fileName,'r')
        self.cfg.read_file(fh)
        fh.close()
                
    def storeConfig(self, fileName=lookups.configFile):
        fileName = fileName if fileName else self.fileName        
        log.info('{0} - Config settings saved!'.format(fileName))
        fh = open(fileName,'w')
        self.cfg.write(fh)
        fh.close()
        