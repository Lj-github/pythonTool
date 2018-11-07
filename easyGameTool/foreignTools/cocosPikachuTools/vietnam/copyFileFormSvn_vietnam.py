# -*- coding: utf-8 -*-
# @Time    : 2018/9/7 下午7:27


#
'''
    从svn 上面 通过md5  对比图片文件  不同 则复制到project 文件里面  并生成 plist 文件

'''


svnPath = "/Users/admin/Documents/ljworkspace/local/cocos/assets/pikachu/sanguo/art_pikachu/翻译美术（越南）/越南_0423"
svnPath = "/Users/admin/Documents/ljworkspace/local/cocos/assets/pikachu/sanguo/art_pikachu/翻译美术（越南）/越南合作方翻译图"
projectFile = "/Users/admin/Documents/ljworkspace/local/cocos/project/pikachu_vietnam/pikachu_english"

import os
import json
import shutil
import hashlib

def GetFileListOnlyImg(dir, fileList):
    newDir = dir
    if os.path.isfile(dir):
        fPath,fName = os.path.split(dir)
        fType = fName.split(".").pop()
        if fType in ["png","jpg"]:
            fileList.append(dir)
    elif os.path.isdir(dir):
        for s in os.listdir(dir):
            newDir=os.path.join(dir,s)
            GetFileListOnlyImg(newDir, fileList)
    return fileList

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
        "".replace("png","txt").replace("jpg","txt")
        shutil.copyfile(srcfile, dstfile)
        #shutil.copyfile(dstfile, srcfile )
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
            key = fname.replace(".","_")
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
            key = fname.replace(".","_")
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
def getLocalPathByName(allFile,fName):
    for k in allFile:
        f = allFile[k]
        fp,fn = os.path.split(f["path"])
        if fn == fName:
            return f
    return None


if __name__ == '__main__':
    filee = os.path.realpath(__file__)
    fpath, fname = os.path.split(filee)
    sdkType = fname.split(".")[0].split("_").pop()
    isFirst = False
    if not os.path.isfile("json_md5_" + sdkType + ".json"):
        isFirst = True

    if isFirst:
        print("第一次 执行 先生成 md5 json  并且会更具md5 全部对比 比较耗时")
    print("svn 更新 => " + svnPath)
    #os.system("svn up " + svnPath)
    print("svn 更新 完成 ")


    svnImgFile = GetFileListOnlyImg(svnPath,[])
    projectImgFilr = GetFileListOnlyImg(projectFile,[])
    allSvnImgMd5Dir = getFileListMd5Dir(svnImgFile)
    allProImgMd5Dir = getProFileListMd5Dir(projectImgFilr)
    ''' svn 资源为准 '''
    res = getJSonFile()
    allNeedRunShellFileList = []
    #if not res:
    print("开始 全部对比 ")  # 直接全部比 完事
    ''' 只考虑SVN 里面的  因为有的图片文件不需要翻译  '''
    for k in allSvnImgMd5Dir:
        svnimg = allSvnImgMd5Dir[k]
        fp, fn = os.path.split(svnimg["path"])
        proFile = getLocalPathByName(allProImgMd5Dir,fn)
        if proFile:
            if proFile["md5"] != svnimg["md5"]:
                copyfile(svnimg["path"], proFile["path"])
                if proFile["path"].find("pikachuFontAndPlist") > -1:
                    # 是需要shell 脚本 打包
                    lPath = proFile["path"]
                    index = lPath.find("pikachuFontAndPlist")

                    if index > -1:
                        frmName = lPath[index:].replace("pikachuFontAndPlist", "").split("/")[
                            1]  # fil.split("/")[index:index+1]
                        print("plistFileName = >" + frmName)
                        shellFile = lPath[:index] + "pikachuFontAndPlist/bin/" + frmName + ".sh"
                        print("plistFileShellName = >" + shellFile)
                        if not shellFile in allNeedRunShellFileList:
                            allNeedRunShellFileList.append(shellFile)

                    ''' 需要打包图片 '''
            if "path2" in proFile:
                if proFile["md52"] != svnimg["md5"]:
                    copyfile(svnimg["path"], proFile["path2"])
                    if proFile["path"].find("pikachuFontAndPlist") > -1:
                        # 是需要shell 脚本 打包
                        lPath = proFile["path"]
                        index = lPath.find("pikachuFontAndPlist")
                        if index > -1:
                            frmName = lPath[index:].replace("pikachuFontAndPlist", "").split("/")[
                                1]  # fil.split("/")[index:index+1]
                            print("plistFileName = >" + frmName)
                            shellFile = lPath[:index] + "pikachuFontAndPlist/bin/" + frmName + ".sh"
                            print("plistFileShellName = >" + shellFile)
                            if not shellFile in allNeedRunShellFileList:
                                allNeedRunShellFileList.append(shellFile)


    for sh in allNeedRunShellFileList:
        os.system("sh " + sh)
    print("生成新的json 文件")
    createJsonFile(allSvnImgMd5Dir)

