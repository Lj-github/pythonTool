# -*- coding: utf-8 -*-
# @Time    : 2018/10/13 下午4:31

# 把中文版里面所有  越南没有的  都复制过来

chinesePro = "/Users/admin/Documents/ljworkspace/local/cocos/project/pikachu_english_180511/pikachu_english"

svnPath = [
    "/Users/admin/Documents/ljworkspace/local/cocos/project/pikachu_english_180511/pikachu_english/tools/pikachuFontAndPlist",
    "/Users/admin/Documents/ljworkspace/local/cocos/project/pikachu_english_180511/pikachu_english/tools/pikachuCCB",
    "/Users/admin/Documents/ljworkspace/local/cocos/project/pikachu_english_180511/pikachu_english/app/static/res",
    "/Users/admin/Documents/ljworkspace/local/cocos/project/pikachu_english_180511/pikachu_english/app/static/coffee"
]

englishPro = "/Users/admin/Documents/ljworkspace/local/cocos/project/pikachu_vietnam/pikachu_english"

projectFile = [
    "//Users/admin/Documents/ljworkspace/local/cocos/project/pikachu_vietnam/pikachu_english/tools/pikachuFontAndPlist",
    "/Users/admin/Documents/ljworkspace/local/cocos/project/pikachu_vietnam/pikachu_english/tools/pikachuCCB",
    "/Users/admin/Documents/ljworkspace/local/cocos/project/pikachu_vietnam/pikachu_english/app/static/res",
    "/Users/admin/Documents/ljworkspace/local/cocos/project/pikachu_vietnam/pikachu_english/app/static/coffee"
]

# 复制 全部 中文版的资源  当然是没有的

import os
import json
import shutil
import hashlib


def GetFileListOnlyImg(dir, fileList):
    newDir = dir
    if os.path.isfile(dir):
        fileList.append(dir)
    elif os.path.isdir(dir):
        for s in os.listdir(dir):
            newDir = os.path.join(dir, s)
            GetFileListOnlyImg(newDir, fileList)
    return fileList


def mkdir(path):
    path = path.strip()
    path = path.rstrip("\\")
    isExists = os.path.exists(path)
    if not isExists:
        os.makedirs(path)
        return True
    else:
        return False


def copyfile(srcfile, dstfile):
    if not os.path.isfile(srcfile):
        print("%s not exist!" % (srcfile))
    else:
        fpath, fname = os.path.split(dstfile)
        if not os.path.exists(fpath):
            '''创建路径'''
            mkdir(fpath)
        '''复制文件'''
        shutil.copyfile(srcfile, dstfile)

        print("copy %s -> %s" % (srcfile, dstfile))


# 只看 文件名就行
def get_file_md5(file_path):
    fpath, fname = os.path.split(file_path)
    return fname


def getFileListMd5Dir(fileList):
    obj = {}
    if fileList:
        for f in fileList:
            fpath, fname = os.path.split(f)
            key = fname.replace(".", "_")
            o = {}
            o["path"] = f
            o["md5"] = get_file_md5(f)
            obj[key] = o

    return obj


'''  由于 project 里面的图片 有两个路径 有的需要 都替换  o dir 需要加一个 字段  '''


def getProFileListMd5Dir(fileList):
    obj = {}
    if fileList:
        for f in fileList:
            fpath, fname = os.path.split(f)
            key = fname.replace(".", "_")
            o = {}
            if key in obj:
                o = obj[key]
                o["path2"] = f
                o["md52"] = get_file_md5(f)
            else:
                o["path"] = f
                o["md5"] = get_file_md5(f)
                obj[key] = o

    return obj


def getLocalPathByName(allFile, fName):
    for k in allFile:
        f = allFile[k]
        fp, fn = os.path.split(f["path"])
        if fn == fName:
            return f
    return None


def isEnglishHas(list, fileName):
    for ff in list:
        if ff == fileName:
            return True
    return False


if __name__ == '__main__':
    filee = os.path.realpath(__file__)
    fpath, fname = os.path.split(filee)
    for i in range(len(svnPath)):
        chineseproAllName = GetFileListOnlyImg(svnPath[i], [])
        englishroAllName = GetFileListOnlyImg(projectFile[i], [])

        for chineseFile in chineseproAllName:
            "chi".replace(chinesePro, "")
            comFi = chineseFile.replace(chinesePro, englishPro)
            if not isEnglishHas(englishroAllName, comFi):
                copyfile(chineseFile, comFi)
