schAppName = 'Sachathya'
schSourceCodeHome = 'G:/pyworkspace/Sachathya'
schMainEntryCode = f'{schSourceCodeHome}/sachathya.py'
schPublishPath = f'{schSourceCodeHome}/distribute/{schAppName}.zip'
schPackerHome = f'{schSourceCodeHome}/schPack'
schVersionFile = f'{schSourceCodeHome}/schLib/schLookups.py'
schVersionHistoryFile = f'{schPackerHome}/build_support/addons/VersionHistory.txt'
kmxPyLibSourceCodeHome = 'G:/pyworkspace/KmaxPyLib'
specTemplate = f'{schPackerHome}/build_support/pyInstallerSpecTemplate.txt'
schAppIcon = f'{schPackerHome}/build_support/appicon.ico'
builderUI = f'{schPackerHome}/build_support/builder.ui'
buildPath = f'{schPackerHome}/dist'
distPath = f'{schPackerHome}/dist'
buildSpecFile = f'{schPackerHome}/_tmp.spec'
outputPath = f'{distPath}/{schAppName}'

#Will be placed nxt to Sachathya exe
addOnFiles = []
addOnFiles.append('G:\\pyworkspace\\Sachathya\\README.md')
addOnFiles.append('G:\\pyworkspace\\Sachathya\\templateConsoleScript.py')
addOnFiles.append('G:\\pyworkspace\\Sachathya\\templateGUIScript.py')
addOnFiles.append('G:\\pyworkspace\\Sachathya\\templateGUIScript.ui')
addOnFiles.append('G:\\pyworkspace\\Sachathya\\config.ini')
addOnFiles.append('G:\\pyworkspace\\Sachathya\\layout.lyt')
addOnFiles.append('G:\\pyworkspace\\Sachathya\\docs\\PyOne Presentation.pdf')

#Contents will be placed nxt to Sachathya exe
addOnFolders = []
addOnFolders.append('G:\\pyworkspace\\Sachathya\\schPack\\build_support\\addons')

#Special File Copy
splAddOnFiles = []
splAddOnFiles.append(('G:\\pyworkspace\\Sachathya\\schLib\\schGUI\\schGUIMainWindow.uic', f'{outputPath}\_internal\schLib\schGUI\schGUIMainWindow.uic'))

#Special Folder Copy
splAddOnFolders = []
splAddOnFolders.append(('G:\\pyworkspace\\Sachathya\\SachathyaScripts', f'{outputPath}\\SachathyaScripts'))

#-----------------------------------

import sys,os
import shutil

#os.chdir(schSourceCodeHome)
sys.path.append('.')
sys.path.append(schSourceCodeHome)
sys.path.append(kmxPyLibSourceCodeHome)
sys.path.append(schPackerHome)

import kmxTools
ttls = kmxTools.Tools()

def doPreProcessing():
    print(f'\n\nClean any existing files... {buildPath}')
    ttls.cleanFolder(buildPath)

def doPostProcessing():
    
    print(f'\n\nCopying addOn files...')
    for cnt, eachFile in enumerate(addOnFiles):
        print(f'Copying {cnt+1}/{len(addOnFiles)}... {eachFile}')
        ttls.copyFile(eachFile,outputPath)

    print(f'\n\nCopying addOn folders...')
    for cnt, eachFolder in enumerate(addOnFolders):
        print(f'Copying {cnt+1}/{len(addOnFolders)}... {eachFolder}')
        ttls.copyFolder(eachFolder,outputPath)

    print(f'\n\nCopying spl addOn files...')
    for cnt, eachFile in enumerate(splAddOnFiles):
        src = eachFile[0]
        dst = eachFile[1]
        print(f'Spl Copying {cnt+1}/{len(splAddOnFiles)} - {src} to {dst}')
        ttls.makePathForFile(dst)
        ttls.copyFile(src,dst)     

    print(f'\n\nCopying spl addOn folders...')
    for cnt, eachFolder in enumerate(splAddOnFolders):
        src = eachFolder[0]
        dst = eachFolder[1]
        print(f'Spl Copying {cnt+1}/{len(splAddOnFolders)}... {src} to {dst}')
        ttls.copyFolderSpl(src,dst)

    print(f'\n\nCompressing to zip file...{outputPath}.zip')
    shutil.make_archive(outputPath, 'zip', outputPath)        
 
    print(f'\n\n\n--------Build Completed!--------')
    print('\n\n')
    print(f'Please Check: {outputPath}')
    print('\n\n')
    print('--------Done-------')

    sys.exit(0)

def prepareSpecFile():
    templateData = ttls.fileContent(specTemplate)
    specData = templateData
    specData = specData.replace('[APPNAME]', schAppName)
    specData = specData.replace('[ENTRYSCRIPT]', schMainEntryCode)
    specData = specData.replace('[APPICON]', schAppIcon)
    ttls.writeFileContent(buildSpecFile,specData)
    print(f'Spec file ready: {buildSpecFile}')

#-----------------------------------
if __name__ == '__main__':
    import corebuilderlib
    from PyInstaller.building import build_main    

    prepareSpecFile()    
    corebuilderlib.startUI()
    #build_main.main(None, buildSpecFile, noconfirm=True, ascii=True, distpath=distPath, workpath=buildPath, clean_build=True)       
    #doPostProcessing() 

