#-*- coding: UTF-8 -*-
__author__ = 'lan'
'''
两个版本数据表 中间语言链接     只作为
'''
import pymysql
from collections import OrderedDict
import os
import fileinput
import re
import xlrd
import xlwt
import sys
reload(sys)
sys.setdefaultencoding('utf8')

newTranslatexls= "/Users/admin/Documents/ljworkspace/local/cocos/assets/pikachu/sanguo/aiweiyou_pokmon/FrenchResources/策划表FR/策划表0512新.xlsx"


sheetCellIdxList = [[1,2]]

newFilePth = '/Users/admin/Desktop/res'
filwXlsOldPth = '/Users/admin/Downloads/molianfuben.xls'
'''
为true时候 只用newTranslatexls内文件替换
'''
isOnlyOnceReplace = False

def search(index):
    newXls = newTranslatexls



    table_newTranslate = xlrd.open_workbook(newXls)

    makeSheepInfo(table_newTranslate,index)

def getOriginName(fName):
    idx = fName.find('（')
    if idx >= 0:
        return fName[:idx]
    else:
        idx = fName.find('(')
        if idx >= 0:
            return fName[:idx]
        else:
            return fName


def getStrByKey(table,strr):
    for i in table:
        if i == strr:
            return table[i]

    return None


#遍历两表对应sheet 以老翻译翻译为key，新翻译翻译为value建立dic
def makeSheepInfo(table_oldTranslate,index):
    sheetnames = table_oldTranslate.sheet_names()
    sheetlen = len(sheetnames)
    print('sheetlen:',sheetlen)
    xlsSheetDic = {}
    sheetoldTranslate = table_oldTranslate.sheet_by_name("molianfuben")
    rowOld = sheetoldTranslate.nrows
    dicNew = {}
    dicOld = {}
    for rowold in range(rowOld):
        if rowold < 1:
            continue
        rowvalues = sheetoldTranslate.row_values(rowold)
        print(rowvalues)
        if rowvalues[sheetCellIdxList[index][0]] == None or rowvalues[sheetCellIdxList[index][0]] == '':
            continue
        dicOld[str(rowvalues[sheetCellIdxList[index][0]])] = str(rowvalues[sheetCellIdxList[index][1]])
    writeExcelOld(dicOld,sheetnames,index)

def writeExcelOld(sheetdic,sheetnames,xlsIdx):
    # print('xlsSheetDic:',xlsSheetDic)
    if len(sheetdic) > 0:
        # print('sheetvalues:',sheetdic)
        xlsname = "molianfuben"
        filePth = filwXlsOldPth
        oldXls = xlrd.open_workbook(filePth)
        workbook = xlwt.Workbook()
        xlsSheetNames = oldXls.sheet_names()
        print('fileName pth:', filePth)
        print('writefileSheet:',xlsSheetNames)
        for sheetname in xlsSheetNames:
            newSheet = workbook.add_sheet(sheetname)
            oldsheet = oldXls.sheet_by_name(sheetname)
            oldsheetrow = oldsheet.nrows
            oldSheetcol = oldsheet.ncols
            for row in range(oldsheetrow):
                for col in range(oldSheetcol):
                    value = oldsheet.cell_value(row, col)
                    if value != '' and value != None and row >= 5 and col > 20:

                        translateValue = getStrByKey(sheetdic,value) # sheetdic.get(value)
                        print "value = >> " + str(value)
                        if translateValue != None:
                            print('sheetrowKey:', value, 'sheetrowValue:', translateValue)
                            value = translateValue.decode("utf-8")
                    newSheet.write(row, col, value)

        fp = os.path.join(filwXlsOldPth )
        workbook.save(fp)
if __name__ == '__main__':

    search(0)

    print('合并完毕')

