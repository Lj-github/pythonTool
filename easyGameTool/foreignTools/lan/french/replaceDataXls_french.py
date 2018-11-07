
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
import sys
import foreignTools.tools.excelTool.ExcelTools as et

allXlsFile = "/Users/admin/Desktop/德语/10版数据翻译ccbcoffee"

filwXlsOldPth = '/Users/admin/Documents/ljworkspace/local/cocos/assets/pikachu/sanguo/aiweiyou_pokmon/GermanyResources/资源表0512/'
'''
为true时候 只用newTranslatexls内文件替换
'''
allObj = {}
# 无法 替换的
canNotDo= []
def GetFileList(dir,fType, fileList = [] ):
    newDir = dir
    if os.path.isfile(dir):
        fpath , fname = os.path.split(dir)
        if fname.split(".").pop() == fType and fname[0] != ".":
            fileList.append(dir)
    elif os.path.isdir(dir):
        for s in os.listdir(dir):
            newDir=os.path.join(dir,s)
            GetFileList(newDir, fType,fileList)
    return fileList

def search():
    allXls = GetFileList(allXlsFile,"xlsx")
    print("all xls log")
    for fi in allXls:
        makeSheepInfo(fi)
    print("all file searched")
    for ii in canNotDo:
        print( "无法 替换的文件"+ii)
    print("开始替换")
    writeExcelOld(allObj)
    print("替换完毕")

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
def makeSheepInfo(fillName):
    table_oldTranslate = xlrd.open_workbook(fillName)
    sheetnames = table_oldTranslate.sheet_names()
    sheetlen = len(sheetnames)
    for sheetName in sheetnames:
        if sheetName.find("Sheet") >-1:
            canNotDo.append(fillName)
            break
        sheetoldTranslate = table_oldTranslate.sheet_by_name(sheetName)
        #  直接 取 前 n-1 个  去匹配  数字 不管  能匹配的 直接 用最后一个  pop  替换
        rowOld = sheetoldTranslate.nrows
        for row in range(rowOld):
            if row < 1 :
                continue
            rowvalues = sheetoldTranslate.row_values(row)
            if not sheetName in allObj:
                allObj[sheetName] = []
            allObj[sheetName].append(rowvalues)

def writeExcelOld(xlsTable):

    for key in xlsTable:
        fil = getOriginName(key)
        print(key + "开始替换")
        keyFile = filwXlsOldPth+ fil+ ".xls"
        if not os.path.isfile(keyFile):
            print("不存在 file + " + keyFile)
            continue
        oldXls = xlrd.open_workbook(keyFile)
        workbook = xlwt.Workbook()
        xlsSheetNames = oldXls.sheet_names()
        for sheetname in xlsSheetNames:
            newSheet = workbook.add_sheet(sheetname)
            oldsheet = oldXls.sheet_by_name(sheetname)
            oldsheetrow = oldsheet.nrows
            oldSheetcol = oldsheet.ncols
            for row in range(oldsheetrow):

                for col in range(oldSheetcol):
                    value = oldsheet.cell_value(row, col)
                    ''' 取到数据表里面的值  '''
                    if value != '' and value != None and row >= 5 and et.isNotIntAndNotFloat(value) : #不是数字
                        for l in xlsTable[key]:
                            if value in l :
                                if value != l[len(l)-1]:
                                    if value != "" and l[len(l)-1] != "":
                                        if type(value) == type(l[len(l)-1]) : # 类型 要相同
                                            print("替换 文字 =>" + str(value)  + " => " +  str(l[len(l)-1]) )
                                            value = l[len(l)-1]
                    newSheet.write(row, col, value)

        fp = os.path.join(filwXlsOldPth + fil + '.xls')
        workbook.save(fp)


if __name__ == '__main__':
    search()
    print('合并完毕')

