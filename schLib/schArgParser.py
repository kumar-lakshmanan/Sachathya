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
        self.sch=core
        log.debug('Commandline parser setup loading...')
        self.parser = argparse.ArgumentParser(description=lookups.licInfo , epilog=lookups.contactInfo, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
        self.addArguments()
        self.readArguments()
        log.debug('Commandline parser setup done!')        
    
    def readArguments(self):
        self.args = self.parser.parse_args()
        self.schKey = self._getValue('schKey')        
        self.schMode = self._getValue('schMode')
        self.schLogEnable = self._getValue('schLogEnable')
        self.schLogLevel = self._getValue('schLogLevel')
        self.schStdRedirect = self._getValue('schStdRedirect')
        self.schStdRedirectLogFile = self._getValue('schStdRedirectLogFile')
        self.schStartupScript = self._getValue('schStartupScript')
        self.schScriptFolder = self._getValue('schScriptFolder')
            
    def addArguments(self):
        self.validSchModes = ['console','gui','consoleApp','guiApp']
        self.validSchStdRedirect = ['std','file']
        self.validSchLogLevel = ['debug','info','warn','error','critical']
        self.parser.add_argument('--schKey', metavar='', type=self.argValidate_schKey, default=lookups.defaultschKey, help='secret key code, should be less then 6 character')
        self.parser.add_argument('--schMode', metavar='', type=self.argValidate_schMode, default=lookups.defaultschMode, help='sachathya engine mode')
        self.parser.add_argument('--schLogEnable', metavar='',  type=bool, default=lookups.defaultschLogEnable, help='sachathya engine log enable')
        self.parser.add_argument('--schLogLevel', metavar='',  type=self.argValidate_schLogLevel, default=lookups.defaultschLogLevel, help='sachathya engine log enable')        
        self.parser.add_argument('--schStdRedirect', metavar='',  type=self.argValidate_schStdRedirect, default=lookups.defaultschStdRedirect, help='sachathya engine std output redirection')
        self.parser.add_argument('--schStdRedirectLogFile', metavar='',  type=str, default=lookups.defaultschStdRedirectLogFile, help='sachathya engine std output redirection')        
        self.parser.add_argument('--schStartupScript', metavar='',  type=str, default=lookups.defaultschStartupScript, help='sachathya engine std output redirection')
        self.parser.add_argument('--schScriptFolder', metavar='',  type=str, default=lookups.defaultschScriptFolder, help='sachathya engine std output redirection')

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