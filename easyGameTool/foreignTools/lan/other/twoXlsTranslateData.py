__author__ = 'lan'
'''中英文翻译 与 其他语言翻译关联，修改待翻译数据'''

import pymysql
from collections import OrderedDict
import os
import fileinput
import re
import xlrd
import xlwt

'''英文版翻译'''
oldTranslatexls=[
    '/Users/lan/Downloads/历次翻译整理/绿洲/妖怪宝可萌-updated/0506/策划表部分_updated.xlsx',
    '/Users/lan/Downloads/历次翻译整理/绿洲/妖怪宝可萌-updated/0512/策划表0512新_updated.xlsx',
    '/Users/lan/Downloads/历次翻译整理/绿洲/妖怪宝可萌-updated/0605/策划表0605_updated.xlsx',
    '/Users/lan/Downloads/历次翻译整理/绿洲/妖怪宝可萌-updated/0613/策划表0612_updated.xlsx'
]
'''另一个语言的版本'''
newTranslatexls=[
    '/Users/lan/Downloads/历次翻译整理/绿洲/妖怪宝可萌-updated/0506/策划表部分_updated.xlsx',
    '/Users/lan/Downloads/历次翻译整理/绿洲/妖怪宝可萌-updated/0512/策划表0512新_updated.xlsx',
    '/Users/lan/Downloads/历次翻译整理/绿洲/妖怪宝可萌-updated/0605/策划表0605_updated.xlsx',
    '/Users/lan/Downloads/历次翻译整理/绿洲/妖怪宝可萌-updated/0613/策划表0612_updated.xlsx'
]

newFilePth = '/Users/lan/Downloads/历次翻译整理/绿洲/新翻译策划文本'
filwXlsOldPth = '/Users/admin/Documents/ljworkspace/local/cocos/assets/pikachu/sanguo/aiweiyou_pokmon/VietnamResources/资源表/'

def search(index):
    _len = len(oldTranslatexls)
    if index >= _len:
        return

    oldXls = oldTranslatexls[index]
    newXls = newTranslatexls[index]

    table_oldTranslate = xlrd.open_workbook(oldXls)
    table_newTranslate = xlrd.open_workbook(newXls)

    print(oldXls,'\n',newXls)
    makeSheepInfo(table_oldTranslate,table_newTranslate,index)

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
'''遍历两表对应sheet 以老翻译翻译为key，新翻译翻译为value建立dic'''
def makeSheepInfo(table_oldTranslate,table_newTranslate,index):
    sheetnames = table_oldTranslate.sheet_names()
    sheetlen = len(sheetnames)
    xlsSheetDic = {}
    for i in range(sheetlen):
        sheetnewTranslate = table_newTranslate.sheet_by_index(i)
        sheetoldTranslate = table_oldTranslate.sheet_by_index(i)
        rowNew = sheetnewTranslate.nrows
        rowOld = sheetoldTranslate.nrows
        dicNew = {}
        dicOld = {}
        for row in range(rowNew):
            rowvalues = sheetnewTranslate.row_values(row)
            dicNew[str(rowvalues[1])] = str(rowvalues[2])

        for rowold in range(rowOld):
            rowvalues = sheetoldTranslate.row_values(rowold)
            dicOld[str(rowvalues[1])] = str(rowvalues[2])

        sheetdic = {};
        for inew, valueNew in dicNew.items():
            for iold, valueOld in dicOld.items():
                if inew == iold and valueNew != valueOld:
                    sheetdic[valueOld] = valueNew
        xlsSheetDic[sheetnames[i]] = sheetdic
    writeExcelOld(xlsSheetDic,sheetnames,index)

def writeExcelOld(xlsSheetDic,sheetnames,xlsIdx):
    if len(xlsSheetDic) > 0:
        for name in sheetnames:
            sheetdic = xlsSheetDic.get(name)
            print('sheetName:',name)

            if len(sheetdic) > 0:
                print('sheetvalues:',sheetdic)
                xlsname = getOriginName(name)
                filePth = filwXlsOldPth + xlsname + '.xls'
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
                            if value != '' and value != None:
                                translateValue = sheetdic.get(value)
                                if translateValue != None:
                                    print('sheetrowKey:', value, 'sheetrowValue:', translateValue)
                                    value = translateValue
                            newSheet.write(row, col, value)

                fp = os.path.join(filwXlsOldPth + xlsname + '.xls')
                workbook.save(fp)
    search(xlsIdx+1)

try:
    isExists = os.path.exists(newFilePth)
    if not isExists:
        print('newFilePth:' + newFilePth)
        os.makedirs(newFilePth)
    search(0)

    print('合并完毕')
except Exception as e:
    print("异常"+e)