__author__ = 'songbin'
'''
翻译回来
把对应翻译放在收集翻译表内 和 对应数据表内

新的 翻译  回来时候   可以 直接替换  


 这个是 从一堆文件里面  直接 替换的  文件夹里面 有  beizhu.xls  daoju.xls 等 
支持语言校准（表内同时存在新旧两列翻译，但新翻译无表头，且可为空）
'''

import pymysql
from collections import OrderedDict
import os
import fileinput
import re
import xlrd
import xlwt


'''表名'''
translateDir = '/Users/admin/Documents/ljworkspace/local/cocos/assets/pikachu/sanguo/aiweiyou_pokmon/pika_foreign/translateResource/translateDir'
translateTitleList = ['Id','colName','Chinese','English','Russion','French','Germany','TraditionalChinese','Vietnam']
'''                     0      1         2          3         4        5        6          7                   8'''
translateIDx = 8

beTranslateDir = '/Users/admin/Documents/ljworkspace/local/cocos/assets/pikachu/sanguo/aiweiyou_pokmon/pika_foreign/translateResource/needBeTranslate'
beTranslateDir = '/Users/admin/Desktop/pikachu越南版/越南翻译1226fankui/越南翻译1226/data'
# beTranslateDir = '/Users/songbin/Downloads/needBeTranslate/needBeTranslate'
# beTranslateDir = '/Users/songbin/Downloads/Language/德语/joyfun/beTranslateGermany_0921/dataTranslated'
'''表名，sheet，ID，中文，英文，俄文，法文,德文，繁文,越南'''
beTranslateIdx = [0,1,2,3,4,5,6,7,8,9]

'''表列名，对应beTranslateIdx idx'''
chinese= ['chinese',3]
english= ['english',4]
russion= ['russion',5]
french= ['french',6]
Germany= ['Germany',7]
traditionalChinese= ['traditionalChinese',8]
vietnam= ['vietnam',9]

'''ID 与translateTitleList对应'''
dataPthList = {
    # 3:[
    #     '/Users/songbin/sanguo/aiweiyou_pokmon/EnglishResources/资源表0512',
    #     '/Users/songbin/sanguo/aiweiyou_pokmon/EnglishResources/资源表0512-绿洲'
    # ],
    3:['/Users/admin/Documents/ljworkspace/local/cocos/assets/pikachu/sanguo/aiweiyou_pokmon/EnglishResources/资源表0512'],
    4:['/Users/admin/Documents/ljworkspace/local/cocos/assets/pikachu/sanguo/aiweiyou_pokmon/RussionResources/资源表0512'],
    5:['/Users/admin/Documents/ljworkspace/local/cocos/assets/pikachu/sanguo/aiweiyou_pokmon/FrenchResources/资源表0512'],
    # 5:['/Users/admin/Documents/ljworkspace/local/cocos/assets/pikachu/sanguo/aiweiyou_pokmon/GermanyResources/资源表0512'],
    6:['/Users/admin/Documents/ljworkspace/local/cocos/assets/pikachu/sanguo/aiweiyou_pokmon/GermanyResources/资源表0512'],
    7:[],
    8:['/Users/admin/Documents/ljworkspace/local/cocos/assets/pikachu/sanguo/aiweiyou_pokmon/VietnamResources/资源表0512'],
}


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
    # print('dataxlsName:',dataxlsName)
    table_data = xlrd.open_workbook(dataxlsName)
    sheetnames = table_data.sheet_names()
    sheetlen = len(sheetnames)
    translateData = {}
    for idx in range(sheetlen):
        sheetname = sheetnames[idx]
        # print('sheetName:',sheetname)
        sheetnewTranslate = table_data.sheet_by_index(idx)
        rowNew = sheetnewTranslate.nrows
        colNew = sheetnewTranslate.ncols
        translateData[sheetname] = {}
        if colNew <= 1:
            continue

        for i in range(rowNew):
            if i < 1:
                continue

            id = str(sheetnewTranslate.cell_value(i,0)).split('.')[0]
            if (not translateData[sheetname].get(id)):
                translateData[sheetname][id] = {}
            title = sheetnewTranslate.cell_value(i,1)
            # print('title:',title)
            if title == '' or title == None:
                continue

            for j in range(colNew):
                if j >= 2:
                    cell_value = sheetnewTranslate.cell_value(i,j)
                    # print('cell_value:',cell_value)
                    if (not cell_value or cell_value is ''):
                        continue
                    if not translateData.get(sheetname).get(id).get(title):
                        translateData[sheetname][id][title] = {}
                    languageName = sheetnewTranslate.cell_value(0,j)
                    '''有语言校对时候，可能会出现同一语言两列，而校对后的一列可能没有列名'''
                    if not languageName:
                        languageName = translateTitleList[translateIDx]

                    # print('languageName:',languageName)
                    translateData[sheetname][id][title][languageName] = cell_value

    writeExcelOld(translateData,filename)


def writeExcelOld(translateData,filename):
    _filename = filename.replace('xlsx','xls')
    _filename = _filename.replace(' (1)','')

    xlsdir = translateDir + '/' + _filename
    resourceDataBeReplace = {}
    workbook = xlwt.Workbook()
    if (isFileExists(xlsdir)):
        table_data = xlrd.open_workbook(xlsdir)
        sheetnames = table_data.sheet_names()
        sheetlen = len(sheetnames)

        for idx in range(sheetlen):
            sheetname = sheetnames[idx]

            if (not translateData.get(sheetname)):
                translateData[sheetname] = {}

            sheetnewTranslate = table_data.sheet_by_index(idx)
            rowNew = sheetnewTranslate.nrows
            colNew = sheetnewTranslate.ncols

            newSheet = workbook.add_sheet(sheetname)
            colTitleList = []
            for i in range(rowNew):

                id = str(sheetnewTranslate.cell_value(i,0)).split('.')[0]

                '''策划数据表的列名'''
                keyColname = sheetnewTranslate.cell_value(i,1)
                translateInfo = {}
                isNeedTranslate = False
                if i != 0:
                    translateInfo1 = translateData.get(sheetname).get(id)
                    '''translateInfo1 为 策划数据表待翻译列项'''
                    if (translateInfo1 and translateInfo1.get(keyColname)):
                        translateInfo = translateInfo1.get(keyColname)
                        isNeedTranslate = True
                        resourceDataBeReplace[keyColname] = True

                for j in range(colNew):
                    cellContent = sheetnewTranslate.cell_value(i,j)
                    if i == 0:
                        colTitleList.append(cellContent)
                    else:
                        if isNeedTranslate:
                            if (translateInfo.get(colTitleList[j])):
                                '''为了清空翻译'''
                                # if j == translateIDx:
                                #     cellContent = ''
                                # else:
                                cellContent = translateInfo.get(colTitleList[j])

                    newSheet.write(i, j, cellContent)

    print('xlsdir:',xlsdir)
    fp = os.path.join(xlsdir)
    workbook.save(xlsdir)
    # if (xlsdir.find('huodongpaixu')>=0):
    #     print('translateData:',translateData)
    writeResourceData(translateData,filename,resourceDataBeReplace)

def writeResourceData(translateData,filename,resourceDataBeReplace):
    if filename.find('NewActivity') >= 0:
        return
    datalist = dataPthList.get(translateIDx)
    # if (filename.find('wujiang')>=0):
    #     print('translateData:',translateData)
    # if filename == 'wujiang.xlsx':
    #     print("translateData:",translateData)
    # print("writeResourceData:",translateData)
    for datapth in datalist:
        xlsdir = datapth + '/' + filename.replace('xlsx','xls').replace(" (1)","")

        # print("writeResourceData:",xlsdir)
        workbook = xlwt.Workbook()
        if (isFileExists(xlsdir)):
            table_data = xlrd.open_workbook(xlsdir)
            sheetnames = table_data.sheet_names()
            sheetlen = len(sheetnames)

            for idx in range(sheetlen):
                sheetname = sheetnames[idx]

                if (not translateData.get(sheetname)):
                    translateData[sheetname] = {}

                sheetnewTranslate = table_data.sheet_by_index(idx)

                rowNew = sheetnewTranslate.nrows
                colNew = sheetnewTranslate.ncols

                newSheet = workbook.add_sheet(sheetname)
                colTitleList = []
                print('rol:',str(rowNew),' col:',str(colNew))
                for i in range(rowNew):

                    id = str(sheetnewTranslate.cell_value(i,0)).split('.')[0]
                    translateInfo = {}
                    isNeedTranslate = False
                    if i > 4:
                        translateInfo = translateData.get(sheetname).get(id)
                        # if (filename.find('wujiang')>=0):
                        #     print('sheetname',sheetname,'id',id,'translateInfo:',translateInfo)
                        # print('resource translate data:translateInfo:',translateInfo, 'id:',str(id))
                        if (translateInfo):
                            isNeedTranslate = True

                    for j in range(colNew):
                        cellContent = sheetnewTranslate.cell_value(i,j)
                        if i == 0:
                            colTitleList.append(cellContent)
                        elif i > 4:
                            if isNeedTranslate:
                                '''策划数据列名'''
                                resourceDatacolName = colTitleList[j]
                                if (filename.find('huodongpaixu')>=0):
                                    print('resourceDatacolName:',translateInfo.get(resourceDatacolName))
                                if (translateInfo.get(resourceDatacolName) and resourceDataBeReplace.get(resourceDatacolName)):
                                    valueLanguages = translateInfo.get(resourceDatacolName)
                                    value = valueLanguages.get(translateTitleList[translateIDx])
                                    '''为了覆盖 为中文'''
                                    # value = valueLanguages.get(translateTitleList[2])
                                    # if (filename == 'wujiang.xlsx'):
                                    #     print('resourceDatacolName:',resourceDatacolName)
                                    # if filename == 'wujiang.xlsx' and resourceDatacolName == "Type":
                                    #     print()
                                    #     value = valueLanguages.get(translateTitleList[3])

                                    if (value):
                                        # print('replace value ' + str(id) + ';' + resourceDatacolName+';'+value)
                                        cellContent = value

                        newSheet.write(i, j, cellContent)

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
    # for xlsname, itemTranslate in translateMap.items():
    #     fp = search(filwXlsOldPth,xlsname)
    #     if fp:

    print('beTranslateDir')
    for root, dirs, files in os.walk(beTranslateDir):
        for OneFileName in files:
            if (OneFileName.find('.xls') > 0 or OneFileName.find('.xlsx') > 0):
                OneFileName = OneFileName.replace(" done", '')
                makeSheepInfo(os.path.join(root, OneFileName),OneFileName)
                print('OneFileName:',OneFileName)

        for dir in dirs:
            for root2, dirs2, files2 in os.walk(os.path.join(root, dir)):
                for OneFileName2 in files2:
                    if OneFileName2.find('.xls') > 0 or OneFileName2.find('.xlsx') > 0:
                        makeSheepInfo(os.path.join(root2, OneFileName2),OneFileName)
                        print('OneFileName:',OneFileName)


    print('合并完毕')
except Exception as e:
    print("异常"+e)