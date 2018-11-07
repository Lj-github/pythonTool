# -*- coding: utf-8 -*-
# @Time    : 18/5/3 下午5:02
# @Author  : myTool
# @File    : getForJsonExcel.py
# @Software: PyCharm

#  获得要转数据文件  json 的excel 文件



#两个相同的list  一个是旧的  一个是新的  旧的 是为了获取excel 中的对比  因为没有中文  先用中文做中介


import os
import xlrd
from xlwt import Workbook
import sys
import json
import ExcelTools as et

oldXlsList = [

    '/Users/admin/Documents/ljworkspace/local/cocos/assets/pikachu/sanguo/aiweiyou_pokmon/VietnamResources/CS-LC_PKM_Excel汇总_20180125/0506/策划表部分.xls',
    '/Users/admin/Documents/ljworkspace/local/cocos/assets/pikachu/sanguo/aiweiyou_pokmon/VietnamResources/CS-LC_PKM_Excel汇总_20180125/0512/策划表0512新.xls',
    '/Users/admin/Documents/ljworkspace/local/cocos/assets/pikachu/sanguo/aiweiyou_pokmon/VietnamResources/CS-LC_PKM_Excel汇总_20180125/0605/策划表0605.xls',
    # '/Users/admin/Documents/ljworkspace/local/cocos/assets/pikachu/sanguo/aiweiyou_pokmon/VietnamResources/CS-LC_PKM_Excel汇总_20180125/0613/策划表0612.xls'

    # '/Users/admin/Documents/ljworkspace/local/cocos/assets/pikachu/sanguo/aiweiyou_pokmon/EnglishResources/历次翻译整理/0506/策划表部分.xls',
    # '/Users/admin/Documents/ljworkspace/local/cocos/assets/pikachu/sanguo/aiweiyou_pokmon/EnglishResources/历次翻译整理/0512/策划表0512新.xls',
    # '/Users/admin/Documents/ljworkspace/local/cocos/assets/pikachu/sanguo/aiweiyou_pokmon/EnglishResources/历次翻译整理/0605/策划表0605.xls',
    #'/Users/admin/Documents/ljworkspace/local/cocos/assets/pikachu/sanguo/aiweiyou_pokmon/EnglishResources/历次翻译整理/0613/策划表0612.xls',
]
'''
此关系一一对应
'''

newXlsList = [
    #'/Users/admin/Documents/ljworkspace/local/cocos/assets/pikachu/sanguo/aiweiyou_pokmon/FrenchResources/策划表FR/策划表0512新.xlsx',
    # '/Users/admin/Documents/ljworkspace/local/cocos/assets/pikachu/sanguo/aiweiyou_pokmon/EnglishResources/历次翻译整理/0506/策划表部分.xls',
    # '/Users/admin/Documents/ljworkspace/local/cocos/assets/pikachu/sanguo/aiweiyou_pokmon/EnglishResources/历次翻译整理/0512/策划表0512新.xls',
    # '/Users/admin/Documents/ljworkspace/local/cocos/assets/pikachu/sanguo/aiweiyou_pokmon/EnglishResources/历次翻译整理/0605/策划表0605.xls',
    # '/Users/admin/Documents/ljworkspace/local/cocos/assets/pikachu/sanguo/aiweiyou_pokmon/EnglishResources/历次翻译整理/0613/策划表0612.xls',

    # '/Users/admin/Documents/ljworkspace/local/cocos/assets/pikachu/sanguo/aiweiyou_pokmon/VietnamResources/CS-LC_PKM_Excel汇总_20180125/0506/策划表部分.xls',
    # '/Users/admin/Documents/ljworkspace/local/cocos/assets/pikachu/sanguo/aiweiyou_pokmon/VietnamResources/CS-LC_PKM_Excel汇总_20180125/0512/策划表0512新.xls',
    # '/Users/admin/Documents/ljworkspace/local/cocos/assets/pikachu/sanguo/aiweiyou_pokmon/VietnamResources/CS-LC_PKM_Excel汇总_20180125/0605/策划表0605.xls',
    # '/Users/admin/Documents/ljworkspace/local/cocos/assets/pikachu/sanguo/aiweiyou_pokmon/VietnamResources/CS-LC_PKM_Excel汇总_20180125/0613/策划表0612.xls'

    "/Users/admin/Documents/ljworkspace/local/cocos/assets/pikachu/sanguo/aiweiyou_pokmon/FrenchResources/策划表FR/策划表部分.xlsx",
    "/Users/admin/Documents/ljworkspace/local/cocos/assets/pikachu/sanguo/aiweiyou_pokmon/FrenchResources/策划表FR/策划表0512新.xlsx",
    "/Users/admin/Documents/ljworkspace/local/cocos/assets/pikachu/sanguo/aiweiyou_pokmon/FrenchResources/pokemon_MEGA_fr2018/POKEMON_MEGA/2017/9月/美术资源/0605/0605/策划表0605.xls"



]

#要改的excel 最终转为json
newXlsAllXls_witchForJSONPATH =  "/Users/admin/Documents/ljworkspace/local/cocos/assets/pikachu/sanguo/aiweiyou_pokmon/VietnamResources/资源表0512/"

#最终导出目录
outPath = "/Users/admin/Desktop/out1/"
newXlsAllXls_witchForJSONPATH = outPath
"""
按需求重写
"""

def anylistToOneList(oldlist,newList):
    resL = []
    for i in range(0,oldlist.__len__()):
        resL.append(oldlist[i])
        for j in range(0,newList.__len__()):
            if oldlist[i][1] == newList[j][1]:
                resL[i].append(newList[j][2])

    return resL

def getAllSheetNameByFile(file):
    if not file: return []
    table_translate = xlrd.open_workbook(file)
    return table_translate.sheet_names()



def excelToListByFileAndSheetName2(file, sheetName,cols):
    allList = []
    if "daoju" in sheetName:
        print("ads")

    if file and sheetName:
        print("<------  " + "file" + file + " begin search  " + " ------>")
        table_translate = xlrd.open_workbook(file)
        count = len(table_translate.sheets())

        # for ins in range(0,count):
        sheet_translate = table_translate.sheet_by_name(sheetName)
        print(sheet_translate.name )

        nrows_translate = sheet_translate.nrows
        co = sheet_translate.ncols
        if cols:
            co = cols
        ncols_translate = co

        for j in range(nrows_translate):

            translate = sheet_translate.row_values(j, 0, ncols_translate)
            arrayitem = []
            for st in translate:
                arrayitem.append(st)
            allList.append(arrayitem)
    print("<------  " + "file" + file + "  search finesh " + " ------>")
    return allList


def getFileByCompireName(fileName,Name):
    allFileList = et.GetFileList(fileName,[])
    for i in allFileList:
        fpath, fname = os.path.split(i)
        if fname[0] == "." :continue
        Name = Name.split("（")[0].split("(")[0]
        fnameL = fname.split(".")[0]
        if fnameL == Name:
            return i
    print("can not fond "+ Name + " form  " + fileName)
    return ""

def addListToList(oldList,resList):

    for s in oldList:
        if isNumber(s[2]) :
            continue
        if str(s[2]).__len__()==0:
            continue
        if s.__len__() >= 4:
            if s[2] != s[3]:
                for i in range(0, resList.__len__()):
                    if i > 4:
                        for j in range(0, resList[i].__len__()):
                            if s[2] == resList[i][j]:
                                if s[3] != "":
                                    resList[i][j] = str(s[3])

                                    # print( "ok => " + str(s[2])  + " to " + str(s[3]) )
        # for i in range(0, resList.__len__()):
        #     for j in range(0, resList[i].__len__()):
        #         resList[i][j] = str(resList[i][j])
        #
    return resList

def isNumber(str5):
    try:
        f = float(str5)
        True
    except ValueError:
        return False


def runStr(obj):
    for ke in obj:
        for i in range(0, obj[ke].__len__()):
            for j in range(0, obj[ke][i].__len__()):
                num2 = str(obj[ke][i][j])
                nu  = str(num2)[-2:] == '.0' and str(num2)[:-2] or str(num2)
                obj[ke][i][j] = nu
    return obj

if __name__ == '__main__':
    # resTable = {}
    # resTable["test1"] = [[1,2,3]]
    # resTable["test2"]= [[1,2,3]]
    #
    #
    # et.makeExcel(resTable, outPath + "aaaaaa.xls")

    #存储所有list
    allTable = {}
    if newXlsList.__len__() == oldXlsList.__len__():
        for i in range(0,newXlsList.__len__()):
            newFile = newXlsList[i]
            oldFile = oldXlsList[i]
            allSheetName = getAllSheetNameByFile(newFile)
            for j in range(0,allSheetName.__len__()):
                newList = excelToListByFileAndSheetName2(newFile,allSheetName[j],3)
                oldList = excelToListByFileAndSheetName2(oldFile,allSheetName[j],3)
                #生成新的list
                resList = anylistToOneList(oldList,newList)
                #获取列表
                #因为有括号  要去掉
                onName = allSheetName[j].split("（")[0].split("(")[0]
                needPath = getFileByCompireName(newXlsAllXls_witchForJSONPATH,allSheetName[j])
                if "baoshifuben" == onName:
                    print("error")
                lis = et.excelToList(needPath)
                if not (onName  in lis):
                    print("can not found ind = > " + allSheetName[j])
                    continue
                foraddlis = lis[onName]

                fpath, fname = os.path.split(needPath)
                #if not("daoju" in fname): continue
                resl = addListToList(resList,foraddlis)

                lis[onName] = resl

                et.makeExcel(lis,outPath+fname)


