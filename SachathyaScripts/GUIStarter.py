#For Sachathya

from PyQt5 import QtCore, QtGui, Qsci, QtWidgets,  Qt
import sys,os

import kmxQtCommonTools
import kmxQtListWidget
import kmxQtMenuBuilder
import kmxQtTray
import kmxQtTreeWidget
import kmxTools

from schLib import schLookups as lookups

#Available Objects
#sch.ttls
#sch.schGUIObj
#sch.schQtApp
#sch.schGUIObj.QuickTools.setVisible

class SchGUIStarter():
    
    def __init__(self, parent):
        self.tag=self.__class__.__name__.replace('Cls','').upper()
        
        self.sch=parent
        self.schGUIObj=self.sch.schGUIObj
        self.schQtApp=self.sch.schQtApp
        self.ttls=self.sch.ttls
        self.cmttls=kmxQtCommonTools.CommonTools()
                
    def initialize(self):
        #Dev Mode
        self.sch.devMode = 0
        
        #Defaults
        self.toolButtonStyle = QtCore.Qt.ToolButtonTextBesideIcon
                       
        #Tray setup
        if hasattr(self.sch,'schTray'):
            self.sch.schTray.trayKiller()
        self.sch.schTray = kmxQtTray.Tray(self.sch.schGUIObj, self.doTrayClick, self.doTrayClick, 'user_samurai.png')
        self.sch.schTray.setupTray()        
        self.schActTglEditor = self.sch.schTray.trayMenuUpdate('Editor')
        self.schActTglEditor.setCheckable(True)
        self.schActTglEditor.setChecked(True)
        self.schActCleanOutput = self.sch.schTray.trayMenuUpdate('Clean Output')
        self.sch.schTray.trayMenuUpdate('|')
        self.schActQuit = self.sch.schTray.trayMenuUpdate('Quit')
                
        #Disable toolbar
        self.sch.schGUIObj.QuickTools.setVisible(0)
        self.sch.schGUIObj.QuickTools.setToolButtonStyle(self.toolButtonStyle)
        
        #Quick Toolbar
        self.sch.schGUIObj.QuickTools.addAction(self.schActTglEditor)
        self.sch.schGUIObj.QuickTools.addAction(self.schActCleanOutput)
        self.sch.schGUIObj.QuickTools.addSeparator()
        self.sch.schGUIObj.QuickTools.addAction(self.schActQuit)        
        
        #Custom Toolbar
        self.schCustomTools = self.sch.schGUIObj.addToolBar('Custom Tools')
        self.schCustomTools.setObjectName('customTools')
        self.schCustomTools.setToolButtonStyle(self.toolButtonStyle)      
        self.sch.schTray.trayMenuUpdate('|')
        self.customToolSetup()
        
        #Toggle Editor
        #self.toggleEditor()
        
        #setupIcons
        self.sch.schGUIObj.setWindowIcon(self.cmttls.getIcon('user_samurai.png'))
        self.cmttls.setIconForItem(self.sch.schGUIObj,'user_samurai.png')
        self.cmttls.setIconForItem(self.schActTglEditor, 'document_import.png')
        self.cmttls.setIconForItem(self.schActCleanOutput, 'broom.png')
        self.cmttls.setIconForItem(self.schActQuit, 'door_out.png')
        
        #CustomCleanup
        self.sch.customCleanUp = self.doCustomCleanup
        
        #Certificate
        os.environ["REQUESTS_CA_BUNDLE"] = os.path.join(os.getcwd(),'certifi', 'cacert.pem')
        print(os.environ["REQUESTS_CA_BUNDLE"])        
        
        #Ready!!!
        self.sch.schTray.trayMessage('Sachathya','Ready')
    
    def customToolSetup(self):

		#http://dev.vizuina.com/farmfresh/
        self.customToolsList = []
        self.addCustomTools('ObjBrowser','tablets.png','./SachathyaScripts/guiApp/objBrowser.py')
        self.addCustomTools('SysPaths','source_code.png','./SachathyaScripts/guiApp/sysPaths.py')
        self.addCustomTools('|')                
        self.addCustomTools('PathConv','document_valid.png','./SachathyaScripts/myCommands/pathslash.py')
        self.addCustomTools('RemoveSpace','buttonbar.png','./SachathyaScripts/myCommands/removespace.py')

        self.addCustomTools('Show\\Hide','cargo.png','./SachathyaScripts/myCommands/schShowHide.py')

        self.addCustomTools('DevMode','chess_horse.png','./SachathyaScripts/myCommands/devModeTgl.py')

		
        
    def doStartCustomTool(self, toolName):
        if(toolName==1):
            print('Tray right Click event is free')
        elif(toolName==2):
            print('Tray double Click event is free')
        elif(toolName==3):
            print('Tray click event is free')
        elif(toolName==4):
            print('Tray middle click event is free')
        else:
            for eachTools in self.customToolsList:
                if(toolName == eachTools[0]):
                    script = eachTools[2]
                    if(script):
                        self.doRunScript(script)
                    else:
                        print('No script linked to '+toolName)

    def doCustomCleanup(self):
        self.sch.schStandardIOObj.reset()
        self.sch.display('Output stream return back', self.tag)
        self.sch.schTray.trayKiller()
        
    def doTrayClick(self, *arg):
        menu = arg[0]
        if(menu=='Editor'):
            self.toggleEditor()
        elif(menu=='Clean Output'):
            self.sch.schGUIObj.qsciStreamOut.setText('')
        elif(menu=='Quit'):
            sys.exit(0)          
        else:
            self.doStartCustomTool(menu)
            
    def doRunScript(self, fileName):
        self.sch.display('Custom Script Run: ' + fileName, self.tag)
        self.sch.schInterpreterObj.runScript(fileName)
    
    def toggleEditor(self):
        n = self.sch.schGUIObj.mdiArea.isHidden()
        self.schActTglEditor.setChecked(n)
        self.sch.schGUIObj.mdiArea.parent().setVisible(n)
        self.sch.schGUIObj.mdiArea.setVisible(n)  

    def addCustomTools(self, toolName, icon=None, script=None):
        icon = icon if icon else 'draft.png'
        if toolName=='|':
            schActCustomTool = self.sch.schTray.trayMenuUpdate('|')
            self.schCustomTools.addSeparator()
        else:
            schActCustomTool = self.sch.schTray.trayMenuUpdate(toolName)
            schActCustomTool.setData(QtCore.QVariant(str(script)))
            self.cmttls.setIconForItem(schActCustomTool, icon)
            self.customToolsList.append((toolName,icon,script))
            self.schCustomTools.addAction(schActCustomTool)            
        return schActCustomTool          
                           
if (__name__=="__main__"):
    if(not hasattr(sch, 'schUserGUI') or sch.devMode):    
        sch.schUserGUI = SchGUIStarter(sch)
        sch.schUserGUI.initialize()