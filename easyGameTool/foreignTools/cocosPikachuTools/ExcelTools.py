# -*- coding: utf-8 -*-
# @Time    : 18/4/20 下午2:54
# @Author  : myTool
# @File    : ExcelTools.py
# @Software: PyCharm

# 库函数
import os
import xlrd
from xlwt import Workbook
import sys
import shutil


def excelToList(file):
    allTable = {}

    if file:
        print("<------  " + "file" + file + " begin search  " + " ------>")
        table_translate = xlrd.open_workbook(file)
        count = len(table_translate.sheets())
        allName = table_translate.sheet_names()

        for ins in range(0, count):
            allList = []
            # sheet_translate = table_translate.sheet_by_index(ins)
            sheet_translate = table_translate.sheet_by_name(allName[ins])
            nrows_translate = sheet_translate.nrows
            ncols_translate = sheet_translate.ncols

            for j in range(nrows_translate):

                translate = sheet_translate.row_values(j, 0, ncols_translate)
                arrayitem = []
                for st in translate:
                    arrayitem.append(st)
                allList.append(arrayitem)
            allTable[allName[ins]] = allList
    print("<------  " + "file" + file + "  search finesh " + " ------>")
    return allTable


def excelToListByFileAndSheetName(file, sheetName):
    allList = []
    if file and sheetName:
        print("<------  " + "file" + file + " begin search  " + " ------>")
        table_translate = xlrd.open_workbook(file)
        count = len(table_translate.sheets())

        # for ins in range(0,count):
        sheet_translate = table_translate.sheet_by_name(sheetName)

        nrows_translate = sheet_translate.nrows
        ncols_translate = sheet_translate.ncols

        for j in range(nrows_translate):

            translate = sheet_translate.row_values(j, 0, ncols_translate)
            arrayitem = []
            for st in translate:
                arrayitem.append(st)
            allList.append(arrayitem)
    print("<------  " + "file" + file + "  search finesh " + " ------>")
    return allList


# AllCCBLis  table { sheel :[list]}

def makeExcel(AllCCBTabel, AllCCBLisName):
    if AllCCBTabel:
        w = Workbook()
        for AllCCBName in AllCCBTabel:
            AllCCBLis = AllCCBTabel[AllCCBName]
            len = 0
            allArr = AllCCBLis
            ws = w.add_sheet(AllCCBName.decode('utf8'))
            for i in allArr:
                ind = 0
                for j in i:
                    # if i[0] == "":  # w为空 不执行
                    #     print("break at because null" + str(i[1]))
                    #     continue
                    # if i[0].isdigit():  # 为数字 不执行
                    #     print("break at because number" + str(i[1]))
                    #     continue
                    rstr = j
                    if isinstance(j, str):
                        rstr = j.decode('utf8')
                    # print("id = " + str(len) + " " + str(rstr) + "  is add success")
                    ws.write(len, ind, rstr)
                    ind = ind + 1
                    if ind == i.__len__():
                        len = len + 1
        print("save xls : " + AllCCBLisName)
        w.save(AllCCBLisName)


def makeExcel(AllCCBTabel, AllCCBLisName):
    if AllCCBTabel:
        w = Workbook()
        for AllCCBName in AllCCBTabel:
            AllCCBLis = AllCCBTabel[AllCCBName]
            len = 0
            allArr = AllCCBLis
            ws = w.add_sheet(AllCCBName)
            for i in allArr:
                ind = 0
                for j in i:
                    # if i[0] == "":  # w为空 不执行
                    #     print("break at because null" + str(i[1]))
                    #     continue
                    # if i[0].isdigit():  # 为数字 不执行
                    #     print("break at because number" + str(i[1]))
                    #     continue
                    rstr = j
                    if isinstance(j, str):
                        rstr = j
                    # print("id = " + str(len) + " " + str(rstr) + "  is add success")
                    ws.write(len, ind, rstr)
                    ind = ind + 1
                    if ind == i.__len__():
                        len = len + 1
        print("save xls : " + AllCCBLisName)
        w.save(AllCCBLisName)


def listDeleteRepeatItem(list, index):  # index: [] 需要作为判断的列数 arr
    if not list or not index: return
    news_List = []
    news_index = []
    for lis in range(0, index.__len__()):
        news_index.append([])
    for id in list:
        isHas = False
        for i in range(0, index.__len__()):
            if id[i] in news_index[i]:
                isHas = True
        if not isHas:
            news_List.append(id)

            for i in range(0, index.__len__()):
                news_index[i].append(id[i])
    return news_List


def GetFileList(dir, fileList):
    newDir = dir
    if os.path.isfile(dir):
        fileList.append(dir.decode('utf-8'))
    elif os.path.isdir(dir):
        for s in os.listdir(dir):
            newDir = os.path.join(dir, s)
            GetFileList(newDir, fileList)
    return fileList


def isNumber(str5):
    try:
        f = float(str5)
        True
    except ValueError:
        return False


def isInt(str5):
    try:
        f = int(str5)
        True
    except ValueError:
        return False


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


def isNotIntAndNotFloat(num):
    num = str(num)
    if num.replace(".", '').isdigit():
        if num.count(".") == 0:
            return False
        elif num.count(".") == 1:
            return False
    else:
        return True


def getFileOnlyName(dir, type=[], fileList=[]):
    newDir = dir
    if os.path.isfile(dir):
        fp, fn = os.path.split(dir)
        ft = fn.split(".").pop()
        if ft in type:
            fileList.append(fn)
    elif os.path.isdir(dir):
        for s in os.listdir(dir):
            newDir = os.path.join(dir, s)
            getFileOnlyName(newDir, type=type, fileList=fileList)
    return fileList


def getFileName(dir, type=[], fileList=[]):
    if os.path.isfile(dir):
        fp, fn = os.path.split(dir)
        ft = fn.split(".").pop()
        if ft in type:
            fileList.append(dir)
    elif os.path.isdir(dir):
        for s in os.listdir(dir):
            newDir = os.path.join(dir, s)
            getFileName(newDir, type=type, fileList=fileList)
    return fileList


"""判断一个unicode是否是汉字"""
def is_chinese(uchar):
    if uchar >= u'\u4e00' and uchar <= u'\u9fa5':
        return True
    else:
        return False

def isIncludeChinese(sText):
    if isinstance(sText, str):
        for uchar in sText:
            if is_chinese(uchar):
                return True
        return False
    else:
        return False

