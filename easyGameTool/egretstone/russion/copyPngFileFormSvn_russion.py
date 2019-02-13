# -*- coding: utf-8 -*-
# @Time    : 2018/9/7 下午7:27


#
'''
    从svn 上面 通过md5  对比图片文件  不同 则复制到project 文件里面   egret 项目 图片替换脚本
'''

svnPath = "/Users/admin/Desktop/石器俄服/img"
projectFile = "/Users/admin/Documents/ljworkspace/local/egret/ProStoneAge/ProStoneAge"

import os
import json
import shutil
import hashlib
import easyGameTool.foreignTools.cocosPikachuTools.ExcelTools as et


def createJsonFile(jsonObj):
    filee = os.path.realpath(__file__)
    fpath, fname = os.path.split(filee)
    sdkType = fname.split(".")[0].split("_").pop()

    with open("json_md5_" + sdkType + ".json", 'w') as f:
        json.dump(jsonObj, f)


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
        "".replace("png", "txt").replace("jpg", "txt")
        shutil.copyfile(srcfile, dstfile)
        # shutil.copyfile(dstfile, srcfile )
        # if  os.path.isfile(srcfile.replace("png","txt").replace("jpg","txt")):
        #     shutil.copyfile(srcfile.replace("png","txt").replace("jpg","txt"), dstfile.replace("png","txt").replace("jpg","txt"))
        #     print("TXT")
        #     print("copy %s -> %s" % (srcfile.replace("png","txt").replace("jpg","txt"), dstfile.replace("png","txt").replace("jpg","txt")))
        print("copy %s -> %s" % (srcfile, dstfile))


def get_file_md5(file_path):
    if not os.path.isfile(file_path):
        return
    myhash = hashlib.md5()
    f = open(file_path, 'rb')
    while True:
        b = f.read(8192)
        if not b:
            break
        myhash.update(b)
    f.close()
    return myhash.hexdigest()


def getJSonFile():
    filee = os.path.realpath(__file__)
    fpath, fname = os.path.split(filee)
    sdkType = fname.split(".")[0].split("_").pop()
    if not os.path.isfile("json_md5_" + sdkType + ".json"):
        return None
    with open("json_md5_" + sdkType + ".json", 'r') as f:
        return json.load(f)


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
        fp, fn = os.path.split(k)
        if fn == fName:
            return k
    return None


if __name__ == '__main__':
    allPng = et.getFileName(svnPath, ["png", "jpg"])
    sheetFile = '/Users/admin/Documents/ljworkspace/local/egret/ProStoneAge/ProStoneAge/tools/sheets'
    allSh = et.getFileName(sheetFile, ["sh"],[])

    allOldPng = et.getFileName(sheetFile, ["png", "jpg"],[])
    resource = '/Users/admin/Documents/ljworkspace/local/egret/ProStoneAge/ProStoneAge/StoneAppPro/resource'
    allProOldPng = et.getFileName(resource, ["png", "jpg"],[])

    #先复制 resource 里面的图片
    for png  in allPng:
        fp,fn = os.path.split(png)
        old = getLocalPathByName(allProOldPng,fn)
        if old:
            copyfile(png,old)
    for png  in allPng:
        fp, fn= os.path.split(png)
        old = getLocalPathByName(allOldPng,fn)
        if old:
            copyfile(png,old)
    for sh in allSh:
        shStr = "sh " + sh
        print( shStr)
        #os.system(shStr)