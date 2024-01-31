#For Sachathya


import sys
import inspect
from schLib import schLookups as lookups
import os
import sqlite3
os.environ["REQUESTS_CA_BUNDLE"] = os.path.join(os.getcwd(),'certifi', 'cacert.pem')
print(os.environ["REQUESTS_CA_BUNDLE"])
print('Hello every one. This is from Common Starter')


win = sch.schGUIObj.mdiArea.activeSubWindow()

print(win)

chl = win.children()

sci = chl[len(chl)-1]

print(sci)


#sci.setEolMode(Qsci.QsciScintilla.EolWindows)


sci.setEolVisibility(1)

sci.setIndentationGuides(1)



sci.setEolMode(Qsci.QsciScintilla.EolUnix)
data = sci.text()

sch.ttls.writeFileContent('ok.txt',data)
