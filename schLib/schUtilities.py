'''
Created on Aug 27, 2017

@author: npn
'''
import os
import sys

from schLib import schLookups as lookups

import logging as log
import logging.config

import kmxTools
from lxml.doctestcompare import strip

class core(object):
    '''
    classdocs
    '''

    def __init__(self,core=None):
        '''
        Constructor
        '''
        log.info('Utilities module loading...')
        self.sch = core
        self.ttls = kmxTools.Tools()
        log.info('Utilities module loading done!')

    def getWelcomeMessage(self):
        justify = 25        
        message = '\n'
        message += '\nSachathya {version}'.format(version = lookups.versionInfo)
        message += '\n{0}\n'.format(lookups.licInfo)
        
        message += '\nStart time:'.ljust(justify,'.') + self.ttls.getDateTime()
        message += '\nSystem name:'.ljust(justify,'.') + self.ttls.getSystemName()
        message += '\nWorking dir:'.ljust(justify,'.') + os.getcwd()        
        message += '\nFirst time user:'.ljust(justify,'.') + str(lookups.isFirstTime)
        message += '\nMode:'.ljust(justify,'.') + str(self.sch.schArgParserObj.schMode)
        message += '\nKey:'.ljust(justify,'.') + str(self.sch.schArgParserObj.schKey)
        message += '\nLog enabled:'.ljust(justify,'.') + str(self.sch.schArgParserObj.schLogEnable)
        message += '\nLog level:'.ljust(justify,'.') + str(self.sch.schArgParserObj.schLogLevel)
        message += '\nStream redirect:'.ljust(justify,'.') + str(self.sch.schArgParserObj.schStdRedirect)
        message += '\nStream redirect log:'.ljust(justify,'.') + str(self.sch.schArgParserObj.schStdRedirectLogFile)
        message += '\nScript dir:'.ljust(justify,'.') + self.sch.schArgParserObj.schScriptFolder
        message += '\nStartup script:'.ljust(justify,'.') + self.sch.schArgParserObj.schStartupScript
        message += '\nSachathya encryption:'.ljust(justify,'.') + self.sch.schUtilitiesObj.encrypt('sachathya')        
        message += '\nSachathya is ready!'
        message += '\n\n'
        return message

    def loggerSetup(self, level='', isEnable=1):
        logger = log.getLogger()
        log.basicConfig(format=lookups.logFormt,level=log.DEBUG)
        
        if level.lower() == 'info':
            logger.setLevel(log.INFO)
        elif level.lower() == 'debug':
            logger.setLevel(log.DEBUG)
        elif level.lower() == 'warn':
            logger.setLevel(log.WARN)
        elif level.lower() == 'error':
            logger.setLevel(log.ERROR)
        elif level.lower() == 'critical':
            logger.setLevel(log.CRITICAL)
        else:
            logger.setLevel(log.NOTSET)
                    
        logger.disabled = not isEnable
        logging.config.dictConfig({
            'version': 1,
            'disable_existing_loggers': not isEnable
        })

    def isFirstTime(self):
        if not lookups.isFirstTime:
            lookups.isFirstTime = not bool(self.ttls.fileContent(lookups.configFile))
        return lookups.isFirstTime
    
    def getCodeForKey(self,key):
        key = str(key).lower().strip()
        if not (len(key)>2 and len(key)<6):
            msg = 'Key should be of length between 4 to 8'
            log.error(msg)
            raise Exception(msg)
        
        if not (key.isalpha()):
            msg = 'Key should have only alphabets, No special characters or numbers'
            log.error(msg)
            raise Exception(msg)
        
        keyCode = ''
        for eachChr in key:
            val = str(ord(eachChr)).zfill(3)
            keyCode += val
            
        return int(keyCode)

    def encrypt(self, data):
        return self.ttls.encrypt(data, lookups.ciperKey)
    
    def decrypt(self, data):
        return self.ttls.decrypt(data, lookups.ciperKey)