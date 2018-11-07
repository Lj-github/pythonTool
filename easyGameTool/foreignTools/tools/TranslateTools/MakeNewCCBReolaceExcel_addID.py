# -*- coding: utf-8 -*-
# @Time    : 2018/5/19 下午5:06
# @Author  : myTool
# @File    : MakeNewCCBReolaceExcel_addID.py
# @Software: PyCharm
import sys
import os
import xlrd
from xlwt import Workbook



excelFile =   '/Users/admin/Documents/ljworkspace/local/cocos/assets/pikachu/sanguo/aiweiyou_pokmon/pika_foreign/CCBReplaceEnglish_7.xls'

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


def makeExcel(AllCCBTabel,AllCCBLisName):

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


if __name__ == '__main__':
    allLis = excelToList(excelFile)

    for i in allLis:
        for j in range(0,allLis[i].__len__()):
            allLis[i][j].insert(0, j )


    makeExcel(allLis,"tass.xls")