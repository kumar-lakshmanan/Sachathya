import os

#Static lookups

__app__ = 'sachathya'
__appName__ = 'Sachathya'
__creater__ = 'Kumaresan Lakshmanan'
__date__ = '2017-08-27'
__version__ = '0.5.8'
__updated__ = '2017-10-08'
__release__ = 'Test'

versionStr = "v%s" % __version__
versionInfo ='%s (%s)' % (versionStr, __updated__)
licInfo="Customized standalone python framework for windows automation."
contactInfo = 'Contact kaymatrix@gmail.com for more info.'

logFormt = '[%(asctime)s] %(module)s - %(funcName)s() [%(levelname)s] %(message)s' 
loggerName = __app__
stdLogFile = __app__ + '_log.txt'

consoleBanner = "{0} {1} Commandline console".format(__appName__,versionInfo)
configFile = 'config.ini'


#Default Arg lookups

schKey = 'net'
schLogEnable = 1
schLogLevel = 'warn' #debug, info, warn, error, critical
schStdRedirect = 'std' #std, file
schStdRedirectLogFile = 'schLog.log'
schMode = 'gui'  #console, consoleApp, guiApp, gui
schStartupScript = 'None'
schScriptFolder = 'SachathyaScripts'

#Config settings lookups

userName = None
userEmailId = None
disableStream = 0
pyDesigner = 'C:\\Python34\\Lib\\site-packages\\PyQt5\\designer.exe'
guiStartUpScript = 'F:\\PythonWorkspace\\SachathyaScripts\\Starter.py'

#Dynamic lookups

isFirstTime = None
ciperKey = None
cleanUpDone = False



