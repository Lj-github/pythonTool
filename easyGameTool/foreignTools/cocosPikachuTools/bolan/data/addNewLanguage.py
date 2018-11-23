__author__ = 'songbin'
'''
添加新语言 列
'''

import pymysql
from collections import OrderedDict
import os
import sys
import re
import xlrd
import xlwt

# printtranslateIDx = sys.argv[1]

'''表名'''
translateDir = '/Users/songbin/sanguo/aiweiyou_pokmon/pika_foreign/translateResource/translateDir'
translateTitleList = ['Id','colName','Chinese','English','Russion','French','Germany','TraditionalChinese','Vietnam']
translateIDx = 5

'''表名，sheet，ID，中文，英文，俄文，法文, 德文，繁文'''
beTranslateIdx = [0,1,2,3,4,5,6,7,8]


"""判断一个unicode是否是汉字"""
def is_chinese(uchar):
    if uchar >= u'\u4e00' and uchar <= u'\u9fa5':
        return True
    else:
        return False

"""判断一个unicode是否是数字"""
def is_number(uchar):
    if uchar >= u'\u0030' and uchar <= u'\u0039':
        return True
    else:
        return False

"""判断一个unicode是否是英文字母"""
def is_alphabet(uchar):
    if (uchar >= u'\u0041' and uchar <= u'\u005a') or (uchar >= u'\u0061' and uchar <= u'\u007a'):
        return True
    else:
        return False

def isStringChinese(sText):
    if isinstance(sText, str):
        for uchar in sText:
            if is_chinese(uchar):
                return True
        return False
    else:
        return False

def isStringNumber(sText):
    if isinstance(sText, str):
        for uchar in sText:
            if is_number(uchar):
                return True
        return False
    else:
        return False

def isStringEnglish(sText):
    if isinstance(sText, str):
        for uchar in sText:
            if is_alphabet(uchar):
                return True
        return False
    else:
        return False

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

def writeExcelOld(filenamePth):
    xlsdir = filenamePth
    # print("translateData:",translateData)
    if (isFileExists(xlsdir)):
        table_data = xlrd.open_workbook(xlsdir)
        sheetnames = table_data.sheet_names()
        sheetlen = len(sheetnames)

        for idx in range(sheetlen):
            sheetname = sheetnames[idx]

            sheetnewTranslate = table_data.sheet_by_index(idx)
            rowNew = sheetnewTranslate.nrows
            colNew = sheetnewTranslate.ncols

            workbook = xlwt.Workbook()
            newSheet = workbook.add_sheet(sheetname)
            for i in range(rowNew):
                for j in range(len(translateTitleList)):
                    cellValue = ''
                    if j < colNew:
                        cellValue = sheetnewTranslate.cell_value(i,j)
                    else:
                        if i == 0:
                            cellValue = translateTitleList[j]
                    newSheet.write(i, j, cellValue)

        print('xlsdir:',xlsdir)
        fp = os.path.join(xlsdir)
        workbook.save(xlsdir)

def isFileExists(filePth):
    if not os.path.isfile(filePth):
        print("%s not exist!"%(filePth))
        return False
    else:
        fpath,fname=os.path.split(filePth)
        if not os.path.exists(fpath):
            '''创建路径'''
            os.makedirs(fpath)
            return False
        return True

def search(path, word):
    for filename in os.listdir(path):
        fp = os.path.join(path, filename)
        if os.path.isfile(fp) and word in filename:
            return fp
        elif os.path.isdir(fp):
            fp = search(fp, word)
            if fp:
                return fp


try:
    for root, dirs, files in os.walk(translateDir):
        for OneFileName in files:
            if (OneFileName.find('.xls') > 0 or OneFileName.find('.xlsx') > 0):
                writeExcelOld(os.path.join(root, OneFileName))

        for dir in dirs:
            for root2, dirs2, files2 in os.walk(os.path.join(root, dir)):
                for OneFileName2 in files2:
                    if OneFileName2.find('.xls') > 0 or OneFileName2.find('.xlsx') > 0:
                        writeExcelOld(os.path.join(root2, OneFileName2))

    print('合并完毕')
except Exception as e:
    print("异常"+e)