#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author: Godfrey Huang
# Email: godfreyhuang@cgenter.com
# Website: www.cgenter.com
#
# Created by Godfrey Huang on 2015-11-02.
# Copyright (c) 2015 CGENTER.COM. All rights reserved.

import pymel.core as pm

def batchCovert():
	sels = pm.selected()
	if sels:
		for sel in sels:
			if sel.getShape().type() == 'mesh':
				originNode = sel
				originShapeNodes = originNode.getShapes()
				pm.select(cl=True)
				if originShapeNodes:
					originShapeNode = originShapeNodes[0]
					historyNodes = originShapeNode.listHistory()
					if historyNodes:
						influenceJoints = []
						for node in historyNodes:
							if node.type() == 'joint':
								influenceJoints.append(node)
						tempNode = pm.duplicate(originNode,name=originNode+'_temp')[0]
						pm.setAttr(tempNode+'.visibility',0)
						pm.select(influenceJoints,r=True)
						pm.select(tempNode,add=True)
						pm.skinCluster(name=tempNode.name()+'_skinCluster',toSelectedBones=True,maximumInfluences=5,dropoffRate=4)
						pm.copySkinWeights(originNode,tempNode,noMirror=True,surfaceAssociation='closestPoint',influenceAssociation='closestJoint',normalize=True)
						pm.deltaMushToSkinCluster(source=originShapeNode.name(),target=tempNode.getShape().name())
						pm.copySkinWeights(tempNode,originNode,noMirror=True,surfaceAssociation='closestPoint',influenceAssociation='closestJoint')
						pm.delete(tempNode)
	else:
		pm.displayWarning('Please select polygon object!')

def main():
	batchCovert()

if __name__ == '__main__':
	main()