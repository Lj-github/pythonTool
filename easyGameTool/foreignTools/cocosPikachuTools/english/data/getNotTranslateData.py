__author__ = 'songbin'
'''
获取未翻译的数据文件（从收集的翻译表内）
'''

import pymysql
from collections import OrderedDict
import os
import fileinput
import re
import xlrd
import xlwt


'''表名'''
translateDir = '/Users/songbin/sanguo/aiweiyou_pokmon/pika_foreign/translateResource/translateDir'
'''Stong'''
# translateDir = '/Users/songbin/stone_age/stone_foreign/translateResource/translateDir'

translateTitleList = ['Id','colName','Chinese','English','Russion','French','Germany','TraditionalChinese','Vietnam']
'''                     0     1          2        3         4          5      6            7                  8'''
'''translateTitleList 的idx'''
translateIDx = 3
'''是否需要带上英语翻译'''
isNeedEnglish = False
isGetTranslate = False
isNeedAll = False

beTranslateDir = '/Users/songbin/sanguo/aiweiyou_pokmon/pika_foreign/translateResource/needBeTranslate'
beTranslateDir = '/Users/songbin/sanguo/aiweiyou_pokmon/pika_foreign/translateResource/sss'
# beTranslateDir = '/Users/songbin/Downloads/Language/越南/needBeTranslate-Russion-2018.11.01/needTranslateData'
# beTranslateDir = '/Users/songbin/Downloads/Language/俄文/allTranslate-pika-Russion-18.11.12/dataTranslate'

'''Stong'''
# beTranslateDir = '/Users/songbin/stone_age/stone_foreign/translateResource/needBeTranslate'

'''表名，sheet，ID，中文，英文，俄文，法文,德语，繁体，越南'''
beTranslateIdx = [0,1,2,3,4,5,6,7,8,9]

'''表列名，对应beTranslateIdx idx'''
chinese= ['chinese',3]
english= ['english',4]
russion= ['russion',5]
french= ['french',6]
germany= ['germany',7]
traditionalChinese= ['traditionalChinese',8]
vietnam= ['vietnam',9]

allSheetDataDic = {}
ignorOriginWords=['','预留','0.0',0.0,'{0}','...','......','……']

'''
0.英文 1。中文
'''
colLanguage = 1

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

'''获取对应表的待翻译内容'''
def makeSheepInfo(dataxlsName,filename):
    print('dataxlsName:',dataxlsName)
    table_data = xlrd.open_workbook(dataxlsName)
    sheetnames = table_data.sheet_names()
    sheetlen = len(sheetnames)
    translateData = {}
    for idx in range(sheetlen):
        sheetname = sheetnames[idx]
        print('sheetName:',sheetname)
        sheetnewTranslate = table_data.sheet_by_index(idx)
        rowNew = sheetnewTranslate.nrows
        colNew = sheetnewTranslate.ncols
        translateData[sheetname] = {}

        for i in range(rowNew):
            if i < 1:
                continue

            id = sheetnewTranslate.cell_value(i,0)
            if not translateData[sheetname].get(id):
                translateData[sheetname][id] = {}
            title = sheetnewTranslate.cell_value(i,1)
            if title == '' or title == None:
                print('title:',title)
                continue
            cell_value = sheetnewTranslate.cell_value(i,translateIDx)
            if(dataxlsName.find('chenghao') > 0):
                print('cell_value:',cell_value)
                print('sheetnewTranslate.cell_value(i,2):',sheetnewTranslate.cell_value(i,2))

            if not isNeedAll:
                if (isGetTranslate):
                    if (not cell_value or cell_value is ''):
                        continue
                elif (cell_value and cell_value is not ''):

                    continue

            '''过滤英语是否有翻译'''
            englishTranslate = sheetnewTranslate.cell_value(i,3)
            if (isNeedEnglish and (not englishTranslate or englishTranslate == '')):
                print('englishTranslate:',englishTranslate)
                continue
            chineseTranslate = sheetnewTranslate.cell_value(i,2)
            if (not chineseTranslate or chineseTranslate in ignorOriginWords):
                print('chineseTranslate:',chineseTranslate)
                continue
            translateData[sheetname][id][title] = {}
            translateData[sheetname][id][title][translateTitleList[2]] = sheetnewTranslate.cell_value(i,2)
            if (isNeedEnglish):
                translateData[sheetname][id][title][translateTitleList[3]] = sheetnewTranslate.cell_value(i,3)
            if (isGetTranslate or isNeedAll):
                translateData[sheetname][id][title][translateTitleList[translateIDx]] = cell_value

    writeExcelOld(translateData,filename)

def writeExcelOld(translateData,filename):
    xlsdir = beTranslateDir + '/' + filename

    print("translateData:",translateData)
    workbook = xlwt.Workbook()
    isNull = True
    for sheetname, idList in translateData.items():
        print('sheetname:',sheetname)
        newSheet = workbook.add_sheet(sheetname)
        '''ID，title，chinese，english'''
        for _idx in range(4):
            name = translateTitleList[_idx]
            print('titlename:',name)
            newSheet.write(0, _idx, name)
        '''如果查找待翻译语言是英文的话，则不需要再次写入表'''
        if (translateIDx is not 3):
            newSheet.write(0, 4, translateTitleList[translateIDx])

        row = 1
        for id, translateInfo in idList.items():
            if len(translateInfo)>0:
                isNull = False
            # print('translateInfo len:',len(translateInfo))
            # print('translateInfo:',translateInfo)
            for colname, translateStrInfo in translateInfo.items():
                isSetId = False
                index = 2
                for idx in range(len(translateTitleList)):
                    _name = translateTitleList[idx]
                    if idx != 0 and translateStrInfo.get(_name) and idx > 1:
                        newSheet.write(row, index, translateStrInfo.get(_name))
                        index = index + 1
                        if not isSetId:
                            isSetId = True
                            newSheet.write(row, 0, id)
                            newSheet.write(row, 1, colname)
                if (isSetId):
                    row = row + 1
    print('xlsdir:',xlsdir)
    fp = os.path.join(xlsdir)
    if not isNull:
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
    # for xlsname, itemTranslate in translateMap.items():
    #     fp = search(filwXlsOldPth,xlsname)
    #     if fp:


    for root, dirs, files in os.walk(translateDir):
        for OneFileName in files:
            if (OneFileName.find('.xls') > 0 or OneFileName.find('.xlsx') > 0):
                makeSheepInfo(os.path.join(root, OneFileName),OneFileName)

        for dir in dirs:
            for root2, dirs2, files2 in os.walk(os.path.join(root, dir)):
                for OneFileName2 in files2:
                    if OneFileName2.find('.xls') > 0 or OneFileName2.find('.xlsx') > 0:
                        makeSheepInfo(os.path.join(root2, OneFileName2),OneFileName)


    print('合并完毕')
except Exception as e:
    print("异常"+e)