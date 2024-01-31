# -*- mode: python -*-

appName = 'Sachathya'
appScript = 'G:/pythoncodes/Sachathya/sachathya.py'
appIcon = 'G:/pythoncodes/Sachathya/schPack/build_support/appicon.ico'
block_cipher = None

a = Analysis([appScript],
             pathex=[
                     'C:\\python3',
                     'C:\\python3\\DLLs', 
                     'C:\\python3\\lib', 
                     'C:\\python3\\lib\\site-packages', 
                     'C:\\python3\\Lib\\site-packages\\PyQt5'
                     'C:\\python3\\lib\\site-packages\\pip-8.1.2-py3.4.egg', 
                     'C:\\python3\\lib\\site-packages\\youtube_dl-2016.12.1-py3.4.egg', 
                     'C:\\python3\\lib\\site-packages\\defusedxml-0.5.0-py3.4.egg', 
                     'C:\\python3\\lib\\site-packages\\wstools-0.4.5-py3.4.egg', 
                     'C:\\python3\\lib\\site-packages\\six-1.10.0-py3.4.egg', 
                     'C:\\python3\\lib\\site-packages\\setuptools-28.8.0-py3.4.egg', 
                     'C:\\python3\\lib\\site-packages\\osa-0.2-py3.4.egg', 
                     'C:\\python3\\lib\\site-packages\\lxml-3.7.3-py3.4-win32.egg', 
                     'C:\\python3\\lib\\site-packages\\pysimplesoap-1.16-py3.4.egg',
                     'C:\\python3\\lib\\site-packages\\zuora_client-1.0-py3.4.egg', 
                     'C:\\python3\\lib\\site-packages\\httplib2-0.10.3-py3.4.egg', 
                     'C:\\python3\\lib\\site-packages\\rinse-0.4.0-py3.4.egg', 
                     'C:\\python3\\lib\\site-packages\\soap2py-1.16-py3.4.egg', 
                     'C:\\python3\\lib\\site-packages\\xmljson-0.1.7-py3.4.egg', 
                     'C:\\python3\\lib\\site-packages\\suds_py3-1.3.3.0-py3.4.egg',
                     'C:\\python3\\lib\\site-packages\\win32', 
                     'C:\\python3\\lib\\site-packages\\win32\\lib', 
                     'C:\\python3\\lib\\site-packages\\Pythonwin',
                     'C:\\python3\\lib\\site-packages\\flask',
                     '.'],
             hiddenimports=[
                            'sip', 
                            'PyQt5', 
                            'PyQt5.Qsci',
                            'PyQt5.QtWebEngineWidgets',
                            'PyQt5.uic', 
                            'beautifulsoup4',
                            'requests',
                            'flask' 
                            'logging', 
                            'sqlite3', 
                            'xmljson', 
                            'version'
                            ],
             binaries=[],
             datas=[],                          
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(pyz, a.scripts, exclude_binaries=True, name=appName, debug=False, strip=False, upx=True, icon=appIcon, console=False)

coll = COLLECT(exe, a.binaries, a.zipfiles, a.datas, strip=False, upx=True, name=appName)

import SchPacker
SchPacker.doPostProcessing()