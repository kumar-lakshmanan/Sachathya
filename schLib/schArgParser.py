'''
Created on Aug 27, 2017

@author: npn
'''
import argparse
import schLib.schLookups as lookups
import logging as log

class core(object):
    '''
    schArgParser Core activity
    '''

    def __init__(self,core=None):
        '''
        schArgParser Core Constructor
        '''        
        self.tag ='ARGPARSER'
        self.sch=core
        log.debug('Commandline parser setup loading...')
        self.parser = argparse.ArgumentParser(description=lookups.licInfo , epilog=lookups.contactInfo, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
        self.addArguments()
        self.readArguments()
        log.debug('Commandline parser setup done!')        
    
    def readArguments(self):
        log.info('Reading argumnets...')
        self.args = self.parser.parse_args()
        lookups.schKey = self._getValue('schKey')        
        lookups.schMode = self._getValue('schMode')
        lookups.schLogEnable = self._getValue('schLogEnable')
        lookups.schLogLevel = self._getValue('schLogLevel')
        lookups.schStdRedirect = self._getValue('schStdRedirect')
        lookups.schStdRedirectLogFile = self._getValue('schStdRedirectLogFile')
        lookups.schStartupScript = self._getValue('schStartupScript')
        lookups.schScriptFolder = self._getValue('schScriptFolder')
            
    def addArguments(self):
        log.info('Preparing argumnets...')
        self.validSchModes = ['console','gui','consoleApp','guiApp']
        self.validSchStdRedirect = ['std','file']
        self.validSchLogLevel = ['debug','info','warn','error','critical']
        self.parser.add_argument('--schKey', metavar='', type=self.argValidate_schKey, default=lookups.schKey, help='secret key code, should be less then 6 character')
        self.parser.add_argument('--schMode', metavar='', type=self.argValidate_schMode, default=lookups.schMode, help='sachathya engine mode')
        self.parser.add_argument('--schLogEnable', metavar='',  type=bool, default=lookups.schLogEnable, help='sachathya engine log enable')
        self.parser.add_argument('--schLogLevel', metavar='',  type=self.argValidate_schLogLevel, default=lookups.schLogLevel, help='sachathya engine log enable')        
        self.parser.add_argument('--schStdRedirect', metavar='',  type=self.argValidate_schStdRedirect, default=lookups.schStdRedirect, help='sachathya engine std output redirection')
        self.parser.add_argument('--schStdRedirectLogFile', metavar='',  type=str, default=lookups.schStdRedirectLogFile, help='sachathya engine std output redirection')        
        self.parser.add_argument('--schStartupScript', metavar='',  type=str, default=lookups.schStartupScript, help='sachathya engine std output redirection')
        self.parser.add_argument('--schScriptFolder', metavar='',  type=str, default=lookups.schScriptFolder, help='sachathya engine std output redirection')

    def argValidate_schLogLevel(self, val):
        if(val in self.validSchLogLevel):
            return val
        else:
            msg = "{0} is not a valid log level among schLogLevel: {1}".format(val,self.validSchLogLevel)
            raise argparse.ArgumentTypeError(msg)

    def argValidate_schStdRedirect(self, val):
        if(val in self.validSchStdRedirect):
            return val
        else:
            msg = "{0} is not a valid string among redirect option: {1}".format(val,self.validSchStdRedirect)
            raise argparse.ArgumentTypeError(msg)

    def argValidate_schMode(self, val):        
        if(val in self.validSchModes):
            return val
        else:
            msg = "{0} is not a valid string among schModes: {1}".format(val,self.validSchModes)
            raise argparse.ArgumentTypeError(msg)

    def argValidate_schKey(self, val):
        if(len(val)<6):
            return val
        else:
            msg = "{0} is not less then six character schKey".format(val)
            raise argparse.ArgumentTypeError(msg)
   
    def _getValue(self,objName):
        return getattr(self.args, objName) if hasattr(self.args, objName) else None