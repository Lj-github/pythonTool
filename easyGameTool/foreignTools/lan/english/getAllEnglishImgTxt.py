# -*- coding: utf-8 -*-
# @Time    : 2018/7/20 下午8:54

''' 在英文版所有资源中放入txt 文件 '''
import  easyGameTool.foreignTools.tools.excelTool.ExcelTools as excelTools

import json
import os
import copy


img_english = "/Users/admin/Documents/ljworkspace/local/cocos/assets/pikachu/sanguo/aiweiyou_pokmon/EnglishResources/img_english"

lvzhouPath = "/Users/admin/Documents/ljworkspace/local/cocos/assets/pikachu/sanguo/art_pikachu/绿洲"

ctyPayh = "/Users/admin/Documents/ljworkspace/local/cocos/assets/pikachu/sanguo/art_pikachu/程天游"

joyfunPath = "/Users/admin/Documents/ljworkspace/local/cocos/assets/pikachu/sanguo/art_pikachu/翻译美术图"

''' 绿洲 程天佑 joyfun  '''
def GetFileListOnlyTxt(dir,fileList):
    newDir = dir
    if os.path.isfile(dir):
        fpath, fname = os.path.split(dir)
        typ = fname.split(".").pop()
        if typ == "txt" :
            fileList.append(dir.decode('utf-8'))
    elif os.path.isdir(dir):
        for s in os.listdir(dir):
            newDir = os.path.join(dir, s)
            GetFileListOnlyTxt(newDir, fileList)
    return fileList

if __name__ == '__main__':
    allImgFile = excelTools.GetFileList(img_english, [])
    allImgFileObj = {}
    for i in allImgFile:
        fpath, fname = os.path.split(i)
        allImgFileObj[fname] = i
    alllvzhouTxtFile = GetFileListOnlyTxt(lvzhouPath, [])
    allctyTxtFile = GetFileListOnlyTxt(ctyPayh, [])
    alljoyfunTxtFile = GetFileListOnlyTxt(joyfunPath, [])

    alllvzhouTxtFileObj = {}
    for i in alllvzhouTxtFile:
        fpath, fname = os.path.split(i)
        alllvzhouTxtFileObj[fname] = i
    allctyTxtFileObj = {}
    for i in allctyTxtFile:
        fpath, fname = os.path.split(i)
        allctyTxtFileObj[fname] = i
    alljoyfunTxtFileObj = {}
    for i in alljoyfunTxtFile:
        fpath, fname = os.path.split(i)
        alljoyfunTxtFileObj[fname] = i


    allObj = {}

    for i in alllvzhouTxtFileObj:
        allObj[i] = alllvzhouTxtFileObj[i]

    for i in allctyTxtFileObj:
        if not allObj.has_key(i):
            allObj[i] = allctyTxtFileObj[i]

    for i in alljoyfunTxtFileObj:
        if not allObj.has_key(i):
            allObj[i] = alljoyfunTxtFileObj[i]

    print("对比完成==>> 开始复制")

    for i in allObj:
        fpath, fname = os.path.split(i)
        if allImgFileObj.has_key(fname.replace("txt","png") )or allImgFileObj.has_key(fname.replace("txt","jpg")):
            if allImgFileObj.has_key(fname.replace("txt","png")):
                co = allObj[i]
                code = allImgFileObj[fname.replace("txt","png")].replace("png","txt")
                excelTools.copyfile(co,code )
            if allImgFileObj.has_key(fname.replace("txt", "jpg")):
                co = allObj[i]
                code = allImgFileObj[fname.replace("txt", "jpg")].replace("jpg", "txt")
                excelTools.copyfile(co, code)










