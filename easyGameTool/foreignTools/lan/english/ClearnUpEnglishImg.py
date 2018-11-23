# -*- coding: utf-8 -*-


# 生成新的一份图片资源目录



import  easyGameTool.foreignTools.tools.excelTool.ExcelTools  as excelTools

import json
import os
import copy

svnPath = "/Users/admin/Documents/ljworkspace/local/cocos/assets/pikachu/sanguo/art_pikachu"


removeDir = ["翻译美术（法国）","翻译美术（越南）","翻译美术图","翻译美术图（俄文版）","绿洲","程天游","白路小游戏"]

img_english = "/Users/admin/Documents/ljworkspace/local/cocos/assets/pikachu/sanguo/aiweiyou_pokmon/EnglishResources/img_english"

projectFile = "/Users/admin/Documents/ljworkspace/local/cocos/project/pikachu_englishGit/pikachu_english/app/static/res"
projectToolFile = "/Users/admin/Documents/ljworkspace/local/cocos/project/pikachu_englishGit/pikachu_english/tools/pikachuFontAndPlist"
def GetFileList(dir, fileList):
    newDir = dir
    if os.path.isfile(dir):
        has = False
        for ii in removeDir:
            if dir.find(ii)>-1:
                has = True
        fpath, fname = os.path.split(dir)
        if not has and fname[0] != ".":
            fileList.append(dir.decode('utf-8'))
    elif os.path.isdir(dir):
        for s in os.listdir(dir):
            newDir=os.path.join(dir,s)
            GetFileList(newDir, fileList)
    return fileList

def GetFileListOnlyPng(dir, fileList):
    newDir = dir
    if os.path.isfile(dir):
        fpath, fname = os.path.split(dir)
        typ = fname.split(".").pop()
        if  typ == "png" or typ == "jpg":
            fileList.append(dir.decode('utf-8'))
    elif os.path.isdir(dir):
        for s in os.listdir(dir):
            newDir=os.path.join(dir,s)
            GetFileListOnlyPng(newDir, fileList)
    return fileList



if __name__ == '__main__':

    allObj  = GetFileList(svnPath,[])
    ## 创建table
    allImgFile = {}
    for fi in allObj:
        fpath, fname = os.path.split(fi)
        allImgFile[fname] = fi.replace(svnPath,img_english)

    allEnglishProjectImg = GetFileListOnlyPng(projectFile,[])
    allprojectToolFileList = GetFileListOnlyPng(projectToolFile,[])
    allCopyFile = copy.deepcopy(allEnglishProjectImg)
    for i in allprojectToolFileList :
        fpath, fname = os.path.split(i)
        isFind = False
        for j in allEnglishProjectImg:
            fpath1, fname1 = os.path.split(j)
            if fname == fname1:
                isFind = True
                break
        if not isFind:
            allCopyFile.append(i)

    for iii in allCopyFile:
        fpath, fname = os.path.split(iii)
        if allImgFile.has_key(fname) :
            excelTools.copyfile(iii,allImgFile[fname])
