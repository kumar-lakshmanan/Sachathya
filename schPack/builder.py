'''
Created on Oct 22, 2015

@author: MUKUND-update-yes
'''

import logging
from PyInstaller.building import build_main
from logging import getLogger

specFile = 'sachathya.spec'
workpath = 'temp'
distpath = '.'
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

