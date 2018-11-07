#-*- coding: UTF-8 -*-
import os
import shutil


#中文版  ui 路径
PATH_CH  = "/Users/admin/Documents/ljworkspace/local/cocos/assets/pikachu/sanguo/art_pikachu/"
#PATH_CH  = "/Users/admin/Desktop/pytest/art_pikachu/"

#英文版  ui 路径
PATH_EN =  "/Users/admin/Documents/ljworkspace/local/cocos/assets/pikachu/sanguo/art_pikachu/翻译美术图/"
#PATH_EN =  "/Users/admin/Desktop/pytest/art_pikachu/翻译美术图/"

# 俄文版  ui 路径
PATH_EW = "/Users/admin/Documents/ljworkspace/local/cocos/assets/pikachu/sanguo/art_pikachu/翻译美术图（俄文版）/"
PATH_EW = "/Users/admin/Desktop/pytest/art_pikachu/翻译美术图（俄文版）/"
PATH_EW = "/Users/admin/Documents/ljworkspace/local/cocos/assets/pikachu/sanguo/art_pikachu/翻译美术（越南）/越语版/"

#存放的最终路径

PATH_SAVR = "/Users/admin/Desktop/pika越狱版/越语版2/"

# 以英文版为基础 查询俄文版文件  如果俄文版的文件  不存在  则从中文版中找到文件 放到英文版本中



def copyfile(srcfile,dstfile):
    if not os.path.isfile(srcfile):
        print "%s not exist!"%(srcfile)
    else:
        fpath,fname=os.path.split(dstfile)
        if not os.path.exists(fpath):
            os.makedirs(fpath)
        shutil.copyfile(srcfile,dstfile)
        print "copy %s -> %s"%( srcfile,dstfile)


def GetFileList(dir, fileList):
    newDir = dir
    if os.path.isfile(dir):
        fileList.append(dir.decode('utf-8'))
    elif os.path.isdir(dir):
        for s in os.listdir(dir):
            newDir=os.path.join(dir,s)
            GetFileList(newDir, fileList)
    return fileList


def getFileStrLen(path):
    if path :
        return  path.decode('utf-8').__len__()


"""
    rootPath 需要替换的路 --俄文
    benPath 参照路径 --英文
    homePath 基础路径 -- 中文
"""

def compairLan(rootPath,benPath,homePath  ,savePath):
    allToCheckList = GetFileList(benPath, [])
    if allToCheckList :
        for file in allToCheckList:
            fileSP = file[getFileStrLen(benPath):]
            cheFile = rootPath + fileSP.encode('utf8')
            fpath, fname = os.path.split(cheFile)
            if fname[0] == ".":#忽略. 隐藏文件
                continue
            if  os.path.isfile(cheFile):
                print( "------" +cheFile + "is  " + "-  existed")
            else:
                rPath = homePath + fileSP.encode('utf8')
                sPath = savePath + fileSP.encode('utf8')
                if  os.path.isfile(rPath):
                    #只需要复制png  jpg
                    fpath, fname = os.path.split(rPath)
                    endi = fname.split(".").pop()
                    if  endi == "png" or  endi == "jpg" :
                        copyfile(rPath,sPath)

try:
    compairLan(PATH_EW,PATH_EN,PATH_CH,PATH_SAVR)
except NameError:
    pass
