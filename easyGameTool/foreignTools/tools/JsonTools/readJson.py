# -*- coding: utf-8 -*-
# @Time    : 2018/5/26 下午1:40
# @Author  : myTool
# @File    : readJson.py
# @Software: PyCharm

'''
    /Users/admin/Documents/ljworkspace/local/egret/SmartPikachu/SmartPikachuGit/SmartPikachu/SmartpikachuGame/resource/skill
    读取里面的json  没有mc 字段的json  名字 提取出来
'''


import os
import json
import shutil
def GetFileList(dir, fileList = []):
    newDir = dir
    if os.path.isfile(dir):
        fileList.append(dir.decode('utf-8'))
    elif os.path.isdir(dir):
        for s in os.listdir(dir):
            newDir=os.path.join(dir,s)
            GetFileList(newDir, fileList)
    return fileList

def copyfile(srcfile,dstfile):
    if not os.path.isfile(srcfile):
        print("%s not exist!"%(srcfile))
    else:
        fpath,fname=os.path.split(dstfile)
        if not os.path.exists(fpath):
            '''创建路径'''
            os.makedirs(fpath)
        '''复制文件'''
        shutil.copyfile(srcfile,dstfile)
        print("copy %s -> %s"%( srcfile,dstfile))

if __name__ == '__main__':
    readFil = "/Users/admin/Documents/ljworkspace/local/egret/SmartPikachu/SmartPikachuGit/SmartPikachu/SmartpikachuGame/resource/skill/"
    #readFil = "/Users/admin/Documents/ljworkspace/local/cocos/assets/pikachu/sanguo/art_pikachu/动画/"
    allFileList = GetFileList(readFil)
    noLis = []
    for fileName in allFileList:
        fpath, fname = os.path.split(fileName)
        last = fname.split(".").pop()
        if last == "json":
            with open(fileName, 'r') as load_f:
                load_dict = json.load(load_f)
                if "mc" in  load_dict:
                    print(fileName + "have mc key")
                else:
                    noLis.append(fname)
                    print(fname + "No ""mc"" key !!!!!")

    with open("SkilleffectDef2.json", 'w') as f:
        json.dump(noLis, f)
        print(noLis)
        print(noLis.__len__())
