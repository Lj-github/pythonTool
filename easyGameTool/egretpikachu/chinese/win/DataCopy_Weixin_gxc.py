#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/11/29 16:19
# @Author  : Aries
# @Site    : 
# @File    : GameProtoCopy_Weixin.py
# @Software: PyCharm

# windows  可以只用 bat 文件

import os
import shutil
import easyGameTool.projectConfig as Config

msgFile = Config.WIN10_SVN_PATH + 'aiweiyou_pokmon\pokmon_weixin\\tools\微信\\gxc\\'
protocolOutPath= Config.WIN10_PROJECT_EGRET +  "SmartpikachuGame\libs\ezModules\gameProtocol\libs\\"
resourcePath=Config.WIN10_PROJECT_EGRET + "\SmartpikachuGame\\resource\data\\"

def copyfile(srcfile, dstfile):
    if not os.path.isfile(srcfile):
        print("%s not exist!" % (srcfile))
    else:
        fpath, fname = os.path.split(dstfile)
        if not os.path.exists(fpath):
            '''创建路径'''
            mkdir(fpath)
        '''复制文件'''
        "".replace("png", "txt").replace("jpg", "txt")
        shutil.copyfile(srcfile, dstfile)
        print("copy %s -> %s" % (srcfile, dstfile))


def mkdir(path):
    path = path.strip()
    path = path.rstrip("\\")
    isExists = os.path.exists(path)
    if not isExists:
        os.makedirs(path)
        return True
    else:
        return False

os.system("svn up " + msgFile)

copyfile(msgFile +'msgData.json' , resourcePath +'msgData.json')
copyfile(msgFile +'GameProtocoObjlDesc.d.ts' , protocolOutPath +'GameProtocoObjlDesc.d.ts')
copyfile(msgFile +'GameProtocolDesc.d.ts' , protocolOutPath +'GameProtocolDesc.d.ts')
