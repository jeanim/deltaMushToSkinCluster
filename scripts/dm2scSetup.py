#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Auther: Godfrey Huang
# Email: huangqiu@cgenter.com
#
# Created by Godfrey Huang on 2015-12-15.
# Copyright (c) 2015 cgenter.com. All rights reserved.
import maya.cmds as cmds
import maya.mel as mel
import re
import sys,os
import inspect

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
    modulePath = getParentPath(currentFileDirectory()).replace('\\','/')
    modStr = '+ deltaMushToSkinCluster 1.0 %s\n' % modulePath
    modulePath = getModuleFolder()+'/deltaMushToSkinCluster.mod'
    if os.path.exists(modulePath):
        os.remove(modulePath)
    f = open(modulePath,'w')
    f.write(modStr)
    f.close()

def enableaPlugin(filename):
    extDict = {'win64':'mll','mac':'bundle','linux':'so','linux64':'so'}
    os = cmds.about(os=True)
    ext = extDict[os]
    version = cmds.about(v=True)[:4]
    pluginName = 'deltaMushToSkinCluster_%s' % version
    fileFullName = '%s.%s' % (pluginName,ext)
    rootPath = getParentPath(currentFileDirectory())
    pluginsPath = rootPath+'/plug-ins/'
    pluginFilePath = pluginsPath+fileFullName
    pluginStr = mel.eval('getenv "MAYA_PLUG_IN_PATH";')+';'+pluginsPath
    mel.eval('putenv "MAYA_PLUG_IN_PATH" "%s";' % pluginStr)
    with open(filename,'a+') as f:
        state = True
        for line in f.readlines():
            if re.findall(fileFullName,line):
                state = False
        if state:
            f.write(r'evalDeferred("autoLoadPlugin(\"\", \"%s\", \"%s\")");' % (fileFullName,pluginName))

    if not cmds.pluginInfo( pluginFilePath, query=True, autoload=True):
        cmds.pluginInfo( pluginFilePath, edit=True, autoload=True)

    if not cmds.pluginInfo(pluginFilePath,query=True,loaded=True):
        cmds.loadPlugin(pluginFilePath)

def createShelfBtn():
    currentShelf = cmds.tabLayout("ShelfLayout",selectTab=True,query=True)
    cmds.shelfButton( annotation='Delta Mush To Skin Cluster',
                      command='import dm2sc.convert as convert\nconvert.main()',
                      label='DM2SC',
                      sourceType='python',
                      image1='pythonFamily.png',
                      imageOverlayLabel='DM2SC',
                      parent=currentShelf)

def main():
    createModFile()
    pluginsPrefsPath = cmds.internalVar(upd=True)+'pluginPrefs.mel'
    enableaPlugin(filename=pluginsPrefsPath)
    createShelfBtn()

if __name__=='__main__':
    main()