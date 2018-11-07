# -*- coding: utf-8 -*-
# @Time    : 2018/8/9 下午8:39
''' 充中文版本中 提权全部 中文  来作为数据 翻译   通过替换唯一键值对  id  '''

import os
import xlrd
from xlwt import Workbook
import sys
import foreignTools.tools.excelTool.ExcelTools  as et


rootPath = os.path.dirname(os.path.realpath(__file__))

svnPath = "/Users/admin/Documents/ljworkspace/local/cocos/assets/pikachu/sanguo/aiweiyou_pokmon/资源表"

def GetFileList(dir, fileList):
    newDir = dir
    if os.path.isfile(dir):
        fileList.append(dir.decode('utf-8'))
    elif os.path.isdir(dir):
        for s in os.listdir(dir):
            newDir=os.path.join(dir,s)
            GetFileList(newDir, fileList)
    return fileList

def getFileOnlyInclude(dir,fileType):
    all = []
    allFileList = GetFileList(dir,[])
    for fil in allFileList:
        fpath, fname = os.path.split(fil)
        if fname.split(".").pop() == fileType:
            all.append(fil)
    return all

#判断是否含有中文
def check_contain_chinese(check_str ):
    for ch in check_str.decode('utf-8'):
        if u'\u4e00' <= ch <= u'\u9fff':
            return True
    return False



def excelToList_Table(excelFile):
    print("生成代 ID 的 List list 内部是 table  带着名称")
    print(excelFile)
    fpath, fname = os.path.split(excelFile)
    xlsName = fname.split(".")[0]
    allTable = {}
    allList = []
    table_translate = xlrd.open_workbook(excelFile )
    allName = table_translate.sheet_names()
    xls = ""
    isIN = False
    if xlsName in allName:
        xls = xlsName
        isIN = True
    if xlsName.lower() in allName:
        xls = xlsName.lower()
        isIN = True
    if isIN:
        sheet_translate = table_translate.sheet_by_name(xls)
        if sheet_translate:
            nrows_translate = sheet_translate.nrows
            ncols_translate = sheet_translate.ncols
            for j in range(nrows_translate): # j 是行数  st 是列数
                if j<5 : continue
                firstRow = sheet_translate.row_values(0, 0, ncols_translate)
                translate = sheet_translate.row_values(j, 0, ncols_translate)

                for st in range(len(translate)) :
                    if check_contain_chinese(str(translate[st]) ):
                        if str(firstRow[st])  == ""  or translate[0] == "": continue
                        item = []
                        #item.append(str(int(translate[0])))
                        item.append(str(int(translate[0]))  + "=" + str(firstRow[st]))
                        item.append(translate[st])

                        # item[firstRow[st]] = translate[st]
                        # item["sub"] = str(translate[0])  + "_##_" + str(firstRow[st])
                        allList.append(item)
        allTable[xlsName] = allList
    return allTable

def meshSame(allList):
    resoultList = []
    for i in range(len(allList)) :
        item = allList[i]
        isContain = False
        for j in range(len(resoultList)):
            reItem = resoultList[j]
            if reItem[1] == item[1]:
                isContain = True
                resoultList[j][0] = resoultList[j][0]  + "&" + item[0]
        if not isContain:
            resoultList.append(item)
    return resoultList


exclude = ["lianaiqiecuo","xiaoguan","pingbizi"]


if __name__ == '__main__':
    print( "开始执行")
    allExcelFile = getFileOnlyInclude(svnPath, "xls")
    for fi in allExcelFile:
        fpath, fname = os.path.split(fi)
        xlsName = fname.split(".")[0]
        # if xlsName != "luotuomuLevel": continue
        if xlsName in exclude:
            continue
        thisFileList = excelToList_Table(fi)
        if thisFileList == {} : continue
        listt  = thisFileList[fname.split(".")[0]]
        if len(listt) >0:
            meshSamelistt = meshSame(listt)
            allObj = {}
            allObj[fname.split(".")[0]] = meshSamelistt
            et.makeExcel(allObj,"getAllChileseFromChineseDATASVN_Exprot/" + fname)









