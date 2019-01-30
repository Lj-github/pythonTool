# -*- coding: utf-8 -*-
# @Time    : 18/4/20 下午2:54

import xlrd
from xlwt import Workbook
'''
    excel 转list
'''
def excelToList(file):
    allTable = {}
    if file:
        print("<------  " + "file" + file + " begin search  " + " ------>")
        table_translate = xlrd.open_workbook(file)
        count = len(table_translate.sheets())
        allName= table_translate.sheet_names()
        for ins in range(0,count):
            allList = []
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
'''
    excel 里面的 sheet  转list
'''


def excelToListByFileAndSheetName(file,sheetName):
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
            for st in translate :
                arrayitem.append(st)
            allList.append(arrayitem)
    print("<------  " + "file" + file + "  search finesh " + " ------>")
    return allList

'''
    AllCCBTabel ： table   {"sheet":[]} 形式  
    xlsName ： excel name
'''



def makeExcel(AllCCBTabel,xlsName):
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
                    rstr = j
                    if isinstance(j, str):
                        rstr = j
                    # print("id = " + str(len) + " " + str(rstr) + "  is add success")
                    ws.write(len, ind, rstr)
                    ind = ind + 1
                    if ind == i.__len__():
                        len = len + 1
        print("save xls : " + xlsName)
        w.save(xlsName)


def listDeleteRepeatItem(list , index): #index: [] 需要作为判断的列数 arr
    if not list or not index: return
    news_List = []
    news_index = []
    for lis in range(0,index.__len__()):
        news_index.append([])
    for id in list:
        isHas = False
        for i in range(0,index.__len__()):
            if id[i] in news_index[i]:
                isHas = True
        if not isHas:
            news_List.append(id)

            for i in range(0, index.__len__()):
                news_index[i].append(id[i])
    return news_List

