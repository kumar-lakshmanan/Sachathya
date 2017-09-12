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
        log.debug('Preparing welcome message...')
        justify = 25        
        message = '\n'
        message += '\nSachathya {version}'.format(version = lookups.versionInfo)
        message += '\n{0}\n'.format(lookups.licInfo)
        
        message += '\nStart time:'.ljust(justify,'.') + self.ttls.getDateTime()
        message += '\nSystem name:'.ljust(justify,'.') + self.ttls.getSystemName()
        message += '\nWorking dir:'.ljust(justify,'.') + os.getcwd()        
        message += '\nFirst time user:'.ljust(justify,'.') + str(lookups.isFirstTime)
        message += '\nMode:'.ljust(justify,'.') + str(lookups.schMode)
        message += '\nKey:'.ljust(justify,'.') + str(lookups.schKey)
        message += '\nLog enabled:'.ljust(justify,'.') + str(lookups.schLogEnable)
        message += '\nLog level:'.ljust(justify,'.') + str(lookups.schLogLevel)
        message += '\nStream redirect:'.ljust(justify,'.') + str(lookups.schStdRedirect)
        message += '\nStream redirect log:'.ljust(justify,'.') + str(lookups.schStdRedirectLogFile)
        message += '\nScript dir:'.ljust(justify,'.') + lookups.schScriptFolder
        message += '\nStartup script:'.ljust(justify,'.') + lookups.schStartupScript
        message += '\nSachathya encryption:'.ljust(justify,'.') + self.sch.schUtilitiesObj.encrypt('sachathya')        
        message += '\n\n'
        return message
    
    def getWelcomeGUIMessage(self):
        log.debug('Preparing GUI Welcome message...')
        justify = 25        
        message = self.getWelcomeMessage()
        message += 'GUI Settings'
        message += '\n'
        message += '\nuserName:'.ljust(justify,'.') + str(lookups.userName)
        message += '\nuserEmailId:'.ljust(justify,'.') + str(lookups.userEmailId)
        message += '\ndisableStream:'.ljust(justify,'.') + str(lookups.disableStream)        
        message += '\npyDesigner:'.ljust(justify,'.') + str(lookups.pyDesigner)
        message += '\nguiStartUpScript:'.ljust(justify,'.') + str(lookups.guiStartUpScript)
        message += '\n\n'
        return message    
        
    def loggerSetup(self, level='', isEnable=1):
        log.debug('Logger level modifier...')
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
        log.debug('Is first time check...')
        if not lookups.isFirstTime:
            lookups.isFirstTime = not bool(self.ttls.fileContent(lookups.configFile))
        return lookups.isFirstTime
    
    def getCodeForKey(self,key):
        log.debug('Keycode prepare...')
        key = str(key).lower().strip()
        if not (len(key)>2 and len(key)<7):
            msg = 'Key should be of length between 3 to 8'
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
        log.debug('Encrypt data...')
        return self.ttls.encrypt(data, lookups.ciperKey)
    
    def decrypt(self, data):
        log.debug('Decrypt data...')
        return self.ttls.decrypt(data, lookups.ciperKey)