#-*- coding: UTF-8 -*-
__author__ = 'lan'
'''
两个版本数据表 中间语言链接
'''

import pymysql
from collections import OrderedDict
import os
import fileinput
import re
import xlrd
import xlwt

'''
绿洲
'''
# oldTranslatexls=[
#     '/Users/lan/Downloads/历次翻译整理/绿洲/妖怪宝可萌-updated/0506/策划表部分_updated.xlsx',
#     '/Users/lan/Downloads/历次翻译整理/绿洲/妖怪宝可萌-updated/0512/策划表0512新_updated.xlsx',
#     '/Users/lan/Downloads/历次翻译整理/绿洲/妖怪宝可萌-updated/0605/策划表0605_updated.xlsx',
#     '/Users/lan/Downloads/历次翻译整理/绿洲/妖怪宝可萌-updated/0613/策划表0612_updated.xlsx',
# ]
# '''
# joyfun
# '''
oldTranslatexls=[
    '/Users/admin/Documents/ljworkspace/local/cocos/assets/pikachu/sanguo/aiweiyou_pokmon/VietnamResources/CS-LC_PKM_Excel汇总_20180125/0512/策划表0512新.xls'
    # '/Users/lan/sanguo/aiweiyou_pokmon/EnglishResources/历次翻译整理/0506/策划表部分.xls',
    # '/Users/lan/sanguo/aiweiyou_pokmon/EnglishResources/历次翻译整理/0512/策划表0512新.xls',
    # '/Users/lan/sanguo/aiweiyou_pokmon/EnglishResources/历次翻译整理/0605/策划表0605.xls',
    # '/Users/lan/sanguo/aiweiyou_pokmon/EnglishResources/历次翻译整理/0613/策划表0612.xls',
]
'''
程天游
'''
# oldTranslatexls=[
#     '/Users/lan/sanguo/aiweiyou_pokmon/EnglishResources/程天游修改版/本地化内容1218/0506/策划表部分.xls',
#     '/Users/lan/sanguo/aiweiyou_pokmon/EnglishResources/程天游修改版/本地化内容1218/0512/策划表0512新.xls',
#     # '/Users/lan/sanguo/aiweiyou_pokmon/EnglishResources/程天游修改版/本地化内容1218/0605/策划表0605.xls',
#     '/Users/lan/sanguo/aiweiyou_pokmon/EnglishResources/程天游修改版/本地化内容1218/0613/策划表0612.xls',
# ]
newTranslatexls=[
    '/Users/admin/Documents/ljworkspace/local/cocos/assets/pikachu/sanguo/aiweiyou_pokmon/FrenchResources/策划表FR/策划表0512新.xlsx'
    # '/Users/lan/Downloads/历次翻译整理/越南/CS-LC_PKM_Excel汇总_20180125/0506/策划表部分.xls',
    # '/Users/lan/Downloads/历次翻译整理/越南/CS-LC_PKM_Excel汇总_20180125/0512/策划表0512新.xls',
    # '/Users/lan/Downloads/历次翻译整理/越南/CS-LC_PKM_Excel汇总_20180125/0605/策划表0605.xls',
    # '/Users/lan/Downloads/历次翻译整理/越南/CS-LC_PKM_Excel汇总_20180125/0613/策划表0612.xls'
]
sheetCellIdxList = [
    [0,1]
    # [1,2]
]

newFilePth = '/Users/lan/Downloads/历次翻译整理/绿洲/新翻译策划文本'
# filwXlsOldPth = '/Users/lan/sanguo/aiweiyou_pokmon/VietnamResources/资源表0512/'
# filwXlsOldPth = '/Users/lan/sanguo/aiweiyou_pokmon/EnglishResources/资源表0512/'
filwXlsOldPth = '/Users/lan/sanguo/aiweiyou_pokmon/EnglishResources/资源表0512-绿洲/'
'''
为true时候 只用newTranslatexls内文件替换
'''
isOnlyOnceReplace = True

def search(index):
    _len = len(oldTranslatexls)
    print(_len)
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
#遍历两表对应sheet 以老翻译翻译为key，新翻译翻译为value建立dic
def makeSheepInfo(table_oldTranslate,table_newTranslate,index):
    sheetnames = table_oldTranslate.sheet_names()
    sheetlen = len(sheetnames)
    print('sheetlen:',sheetlen)
    xlsSheetDic = {}
    for i in range(sheetlen):
        sheetnewTranslate = table_newTranslate.sheet_by_index(i)
        print(sheetnames[i])
        sheetoldTranslate = table_oldTranslate.sheet_by_index(i)
        rowNew = sheetnewTranslate.nrows
        rowOld = sheetoldTranslate.nrows
        dicNew = {}
        dicOld = {}
        for row in range(rowNew):
            rowvalues = sheetnewTranslate.row_values(row)
            print(rowvalues)
            if rowvalues[sheetCellIdxList[index][0]] == None or rowvalues[sheetCellIdxList[index][0]] == '':
                continue
            print(rowvalues[sheetCellIdxList[index][0]])
            print(rowvalues[sheetCellIdxList[index][1]])
            dicNew[str(rowvalues[sheetCellIdxList[index][0]])] = str(rowvalues[sheetCellIdxList[index][1]])

        for rowold in range(rowOld):

            rowvalues = sheetoldTranslate.row_values(rowold)
            print(rowvalues)
            if rowvalues[sheetCellIdxList[index][0]] == None or rowvalues[sheetCellIdxList[index][0]] == '':
                continue
            dicOld[str(rowvalues[sheetCellIdxList[index][0]])] = str(rowvalues[sheetCellIdxList[index][1]])
        sheetdic = {}

        if not isOnlyOnceReplace:
            for inew, valueNew in dicNew.items():
                for iold, valueOld in dicOld.items():
                    if inew == iold and valueNew != valueOld:
                        sheetdic[valueOld] = valueNew
        else:
            for inew, valueNew in dicNew.items():
                sheetdic[inew] = valueNew

        xlsSheetDic[sheetnames[i]] = sheetdic
    writeExcelOld(xlsSheetDic,sheetnames,index)

def writeExcelOld(xlsSheetDic,sheetnames,xlsIdx):
    # print('xlsSheetDic:',xlsSheetDic)
    if len(xlsSheetDic) > 0:
        for name in sheetnames:
            sheetdic = xlsSheetDic.get(name)
            print('sheetName:',name)

            if len(sheetdic) > 0:
                # print('sheetvalues:',sheetdic)
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


if __name__ == '__main__':
    # _localPth='/'.join(os.path.realpath(__file__).split('/')[:-1])
    # _localPth = _localPth.split('englishTranslate')[:-1][0]
    # print('_localPth:',_localPth)
    # isExists = os.path.exists(newFilePth)
    # if not isExists:
    #     print('newFilePth:' + newFilePth)
    #     os.makedirs(newFilePth)
    search(0)

    print('合并完毕')

