# -*- coding: utf-8 -*-
# @Time    : 18/4/11 下午6:39
# @Author  : myTool
# @File    : index.py
# @Software: PyCharm


import os
import json
def GetFileList(dir, fileList):
    newDir = dir
    if os.path.isfile(dir):
        fileList.append(dir[auit.decode('utf-8').__len__():].decode('utf-8'))
    elif os.path.isdir(dir):
        for s in os.listdir(dir):
            newDir=os.path.join(dir,s)
            GetFileList(newDir, fileList)
    return fileList


auit = "/Users/admin/Documents/ljworkspace/local/cocos/project/pikachu_english/app/static/"

fileList = GetFileList( "/Users/admin/Documents/ljworkspace/local/cocos/project/pikachu_english/app/static/res/ccb/",[])

with open("allCcbien.json", 'w') as f:
    json.dump(fileList, f)

print("success")