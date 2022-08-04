#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Auther: Godfrey Huang
# Email: godfrey.huang@udecg.com
#
# Created by Godfrey Huang on 2015-12-15.
# Copyright (c) 2015 udecg.com. All rights reserved.
import maya.cmds as cmds
import maya.mel as mel
import re
import sys,os,platform
import inspect
import logging
logger = logging.getLogger('dm2sc')

def currentFileDirectory():
	path = os.path.realpath(sys.path[0])
	if os.path.isfile(path):
		path = os.path.dirname(path)
		return os.path.abspath(path)
	else:
		caller_file = inspect.stack()[1][1]
		return os.path.abspath(os.path.dirname(caller_file))

def getParentPath(strPath):
    if not strPath:
        return None
    lsPath = os.path.split(strPath)
    if lsPath[1]:
        return lsPath[0]

    lsPath = os.path.split(lsPath[0])
    return lsPath[0]

def getModuleFolder():
    mayaAppDirTemp = os.getenv("MAYA_APP_DIR")
    modules = 'modules/'
    filePath = mayaAppDirTemp+'/'+modules
    if not os.path.exists(filePath):
        os.makedirs(filePath)
    return filePath

def createModFile():
    moduleDirPath = getParentPath(currentFileDirectory()).replace('\\','/')
    modFilePath = os.path.join(moduleDirPath, 'dm2sc.mod')
    with open(modFilePath, 'r') as mod:
        content = mod.read()
        content = re.sub('INSTALL_TARGET_DIR', moduleDirPath, content, flags=re.M)
        installModFilePath = getModuleFolder()+'/dm2sc.mod'
        if os.path.exists(installModFilePath): os.remove(installModFilePath)
        f = open(installModFilePath,'w')
        f.write(content)
        f.close()
        logger.info('The "{}" has been created'.format(installModFilePath))

def enableaPlugin():
    extDict = {'win64':'mll','mac':'bundle','linux':'so','linux64':'so'}
    os_arch = {'64bit': 'x64', '32bit':'x86'}.get(platform.architecture()[0],'x64')
    os_type = cmds.about(os=True)
    system = platform.system().lower()
    ext = extDict[os_type]
    version = cmds.about(v=True)[:4]
    moduleDirPath = getParentPath(currentFileDirectory()).replace('\\','/')
    pluginFileDirPath = os.path.join(moduleDirPath, 'plug-ins', version, system, os_arch).replace('\\','/')
    pluginFileName = 'deltaMushToSkinCluster'
    pluginFileFullName = '{}.{}'.format(pluginFileName,ext)
    pluginFilePath = os.path.join(pluginFileDirPath, pluginFileFullName).replace('\\','/')

    plugPaths = mel.eval('getenv "MAYA_PLUG_IN_PATH";').split(';')
    for p in plugPaths:
        if not pluginFileDirPath in plugPaths:
            plugPaths.append(pluginFileDirPath)
    pluginStr = ';'.join(plugPaths)
    mel.eval('putenv "MAYA_PLUG_IN_PATH" "{}";'.format(pluginStr))
    pluginsPrefsPath = os.path.join(cmds.internalVar(upd=True),'pluginPrefs.mel')
    with open(pluginsPrefsPath,'a+') as f:
        state = True
        for line in f.readlines():
            if re.findall(pluginFileFullName,line):
                state = False
        if state:
            f.write(r'evalDeferred("autoLoadPlugin(\"\", \"%s\", \"%s\")");' % (pluginFileFullName,pluginFileName))

    if not cmds.pluginInfo( pluginFilePath, query=True, autoload=True):
        cmds.pluginInfo( pluginFilePath, edit=True, autoload=True)

    if not cmds.pluginInfo(pluginFilePath,query=True,loaded=True):
        cmds.loadPlugin(pluginFilePath)

    logger.info('"{}" plugin loaded'.format(pluginFilePath))

def createShelfBtn():
    currentShelf = cmds.tabLayout("ShelfLayout",selectTab=True,query=True)
    cmds.shelfButton( annotation='Delta Mush To Skin Cluster',
                      command='import dm2sc.convert as convert\nconvert.main()',
                      label='DM2SC',
                      sourceType='python',
                      image1='pythonFamily.png',
                      imageOverlayLabel='DM2SC',
                      parent=currentShelf)
    logger.info('The shelf button created')

def main():
    createModFile()
    enableaPlugin()
    createShelfBtn()

if __name__=='__main__':
    main()