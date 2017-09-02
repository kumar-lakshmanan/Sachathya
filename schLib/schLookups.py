import os

#Static lookups

__app__ = 'sachathya'
__appName__ = 'Sachathya'
__creater__ = 'Kumaresan Lakshmanan'
__version__ = 0.1
__date__ = '2017-08-27'
__updated__ = '2017-08-29'

versionStr = "v%s" % __version__
versionInfo ='%s (%s)' % (versionStr, __updated__)
licInfo="Sachathya is a Pre-compiled python framework for simple windows automation."
contactInfo = 'Contact kaymatrix@gmail.com for more info.'

logFormt = '[%(asctime)s] %(module)s %(funcName)s [%(levelname)s] %(message)s' 
loggerName = __app__
stdLogFile = __app__ + '_log.txt'

consoleBanner = "{0} {1} Commandline Console".format(__appName__,versionInfo)
configFile = 'config.ini'


#Default Arg lookups

defaultschKey = 'net'
defaultschLogEnable = 0
defaultschStdRedirect = 'std' #std, file
defaultschStdRedirectLogFile = 'schLog.log'
#defaultschMode = 'server'  #cli, app, server
#defaultschStartupScript = 'userScripts/firstScript.py'
defaultschMode = 'app'  #cli, app, server
defaultschStartupScript = 'userScripts/old/tools/youtubeDownloader.py'
defaultschScriptFolder = 'userScripts'

#Config settings lookups

userName = None
userEmailId = None

#Dynamic lookups

isFirstTime = None
ciperKey = None
cleanUpDone = False



