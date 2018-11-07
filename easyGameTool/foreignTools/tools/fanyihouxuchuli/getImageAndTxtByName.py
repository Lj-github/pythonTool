# -*- coding: utf-8 -*-
# @Time    : 2018/5/18 下午3:29
# @Author  : myTool
# @File    : getImageAndTxtByName.py
# @Software: PyCharm


## 通过图片min



import sys



import os
import xlrd
from xlwt import Workbook
import shutil
import json

def excelToList(file):
    allTable = {}

    if file:
        print("<------  " + "file" + file + " begin search  " + " ------>")
        table_translate = xlrd.open_workbook(file)
        count = len(table_translate.sheets())
        allName= table_translate.sheet_names()

        for ins in range(0,count):
            allList = []
            #sheet_translate = table_translate.sheet_by_index(ins)
            sheet_translate = table_translate.sheet_by_name(allName[ins])
            nrows_translate = sheet_translate.nrows
            ncols_translate = sheet_translate.ncols

            for j in range(nrows_translate):

                translate = sheet_translate.row_values(j, 0, ncols_translate)
                arrayitem = []
                for st in translate :
                    arrayitem.append(st)
                allList.append(arrayitem)
            allTable[allName[ins]] = allList
    print("<------  " + "file" + file + "  search finesh " + " ------>")
    return allTable

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

def GetFileList(dir, fileList):
    newDir = dir
    if os.path.isfile(dir):
        fileList.append(dir.decode('utf-8'))
    elif os.path.isdir(dir):
        for s in os.listdir(dir):
            newDir = os.path.join(dir, s)
            GetFileList(newDir, fileList)
    return fileList

def getFileStaNameByfileName(name,allList):
    for na in allList:
        fpath, fname = os.path.split(na)
        if   fname == name:
            return na

    print("can not find name ------>> " + name)
    return ""

def createTxtByNameTxt(name,txt):
    f = file(name, "a+")
    if txt:
        f.write(txt)
    f.close()



if __name__ == '__main__':
    onFile = "getImageAndTxtByName.xlsx"
    searchFile = "/Users/admin/Documents/ljworkspace/local/cocos/assets/pikachu/sanguo/aiweiyou_pokmon/FrenchResources/"
    resFile = "/Users/admin/Desktop/cuowu/"

    allTable = excelToList(onFile)
    if allTable:
        allList = allTable["Sheet1"]
        allFileList =  GetFileList(searchFile,[])
        i = 0
        for item in   allList:
            i = i + 1
            if i == 1 :
                continue

            fileNam = getFileStaNameByfileName(item[0],allFileList)
            if fileNam != "":
                copyfile(fileNam,os.getcwd() + "/"+ item[0])
                createTxtByNameTxt(item[0].split(".")[0]+".txt",item[1].decode('utf-8'))








