'''
Created on Oct 22, 2015

@author: MUKUND-update-yes
'''

import logging
from PyInstaller.building import build_main
from logging import getLogger
import kmxTools

kttls = kmxTools.Tools()

specFile = 'sachathya.spec'
workpath = 'temp'
distpath = '.'

src = 'F:\\PythonWorkspace\\Sachathya\\schLib\\schGUI\\schGUIMainWindow.ui'
dst = 'F:\\PythonWorkspace\\Sachathya\\schPack\\additionalFiles\\schLib\\schGUI\\schGUIMainWindow.uic'
if(kttls.isPathOK(src)): kttls.copyFile(src, dst)

#logFormt = '%(relativeCreated)d %(levelname)s: %(message)s'
logFormt = '[%(asctime)s] %(module)s %(funcName)s [%(levelname)s] %(message)s' 
logLevel = logging.DEBUG
 
#Ready logger
logging.basicConfig(format=logFormt, level=logLevel)
logger=getLogger(__name__)

# Start Building
logger.debug("Starting build process...")
build_main.main(None, specFile, noconfirm=True, ascii=True, distpath=distpath, workpath=workpath, clean_build=True)
logger.debug("Completed!")

