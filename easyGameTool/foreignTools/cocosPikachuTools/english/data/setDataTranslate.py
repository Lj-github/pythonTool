__author__ = 'songbin'
'''
更新数据文件对应翻译
初始 从对应英文表内可翻译列 取出文字，找出对应中文表内中文，建立表

后： 从英文表内取出对应中文 追缴在中文列，并收集导出对应待翻译的表。
默认 只覆盖非空表格内容，不添加空格，
     可以根据配置表 加行 减行 （但是不会主动删除收集到的文件表，如需删除 需手动删掉）
（因为策划会根据UI需求手动修改翻译资源表，资源数据表---》收集翻译表 仅仅是同步修改的东西）
'''

import pymysql
from collections import OrderedDict
import os
import fileinput
import re
import xlrd
import xlwt

# rootDataDir = '/Users/songbin/sanguo/aiweiyou_pokmon/EnglishResources/资源表0512'
# rootDataDir = '/Users/songbin/sanguo/aiweiyou_pokmon/RussionResources/资源表0512'
# rootDataDir = '/Users/songbin/sanguo/aiweiyou_pokmon/FrenchResources/资源表0512'
rootDataDirList = {
    2:"/Users/admin/Documents/ljworkspace/local/cocos/assets/pikachu/sanguo/aiweiyou_pokmon/资源表",
    3:'/Users/admin/Documents/ljworkspace/local/cocos/assets/pikachu/sanguo/aiweiyou_pokmon/EnglishResources/资源表0512',
    4:'/Users/admin/Documents/ljworkspace/local/cocos/assets/pikachu/sanguo/aiweiyou_pokmon/RussionResources/资源表0512',
    5:'/Users/admin/Documents/ljworkspace/local/cocos/assets/pikachu/sanguo/aiweiyou_pokmon/FrenchResources/资源表0512',
    6:'/Users/admin/Documents/ljworkspace/local/cocos/assets/pikachu/sanguo/aiweiyou_pokmon/GermanyResources/资源表0512',
    7:'',
    8:'/Users/admin/Documents/ljworkspace/local/cocos/assets/pikachu/sanguo/aiweiyou_pokmon/VietnamResources/资源表0512',
}
'''Stone'''
# rootDataDirList = {
#     2:"/Users/songbin/stone_age/石器时代数值配置",
#     3:'/Users/songbin/sanguo/aiweiyou_pokmon/EnglishResources/资源表0512',
#     4:'/Users/songbin/stone_age/Russian stone/外文版配置文件',
#     5:'/Users/songbin/sanguo/aiweiyou_pokmon/FrenchResources/资源表0512',
#     6:'/Users/songbin/sanguo/aiweiyou_pokmon/GermanyResources/资源表0512',
#     7:'',
#     8:'/Users/songbin/sanguo/aiweiyou_pokmon/VietnamResources/资源表0512',
# }


'''表名 所收集的翻译表目录'''
translateDir = '/Users/admin/Documents/ljworkspace/local/cocos/assets/pikachu/sanguo/aiweiyou_pokmon/pika_foreign/translateResource/translateDir'
'''Stone'''
# translateDir = '/Users/songbin/stone_age/stone_foreign/translateResource/translateDir'


translateTitleList = ['Id','colName','Chinese','English','Russion','French','Germany','TraditionalChinese','Vietnam']
'''                  【0     1          2        3         4         5        6         7                     8】'''
'''isReplaceNull 是否会连同空的表格一起填充（全覆盖式 true ；只覆盖有内容的 false）'''
isReplaceNull = True####

'''translateIDx=2(从中文表内抽取对应中文填充在翻译收集表) 应该最后在执行，中文只是填充，不会增加行'''
translateIDxList = [3,4,5,6,7,8,2]
translateIDxList = [3,2]

# beTranslateDir = '/Users/songbin/sanguo/aiweiyou_pokmon/pika_foreign/translateResource/needBeTranslate'
'''表名，sheet，ID，中文，英文，俄文，法文, 德文，繁文，越南'''
# beTranslateIdx = [0,1,2,3,4,5,6,7,8,9]

'''表列名，对应beTranslateIdx idx'''
chinese= ['chinese',3]
english= ['english',4]
russion= ['russion',5]
french= ['french',6]
germany= ['germany',7]
traditionalChinese= ['traditionalChinese',8]
vietnam= ['vietnam',9]

'''策划翻译配置表'''
translateConfigFile = '/Users/admin/Documents/ljworkspace/local/cocos/assets/pikachu/sanguo/aiweiyou_pokmon/pika_foreign/文本替换.xls'
'''Stong'''
# translateConfigFile = '/Users/songbin/stone_age/stone_foreign/文本替换.xls'
'''表名，sheet，列名（；；；）'''
ignorOriginWords=['','预留','0.0',0.0,'{0}','...','......','……']

# ignorXlsname = ['xiaoguan','lianaiqiecuo','baoshishan','caishendianteshu','canhun','daojulibao','dhbs','dhwj']




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
def makeSheepInfo(dataxlsName,configData,filename):
    print('dataxlsName:',dataxlsName)
    table_data = xlrd.open_workbook(dataxlsName)
    sheetnames = table_data.sheet_names()
    sheetlen = len(sheetnames)
    translateData = {}
    for idx in range(sheetlen):
        sheetname = sheetnames[idx]
        print('sheetName:',sheetname)
        if (not configData.get(sheetname)):
            continue
        coltitleList = configData.get(sheetname)
        sheetnewTranslate = table_data.sheet_by_index(idx)
        rowNew = sheetnewTranslate.nrows
        colNew = sheetnewTranslate.ncols
        translateData[sheetname] = {}

        for i in range(rowNew):
            if i < 5:
                continue
            # id = sheetnewTranslate.cell_value(i,0)
            id = str(sheetnewTranslate.cell_value(i,0)).split('.')[0]
            translateData[sheetname][id] = {}

            for j in range(colNew):
                title = sheetnewTranslate.cell_value(0,j)
                if title == '' or title == None:
                    continue
                if (not title in coltitleList):
                    continue
                translateData[sheetname][id][title] = {}
                cell_value = sheetnewTranslate.cell_value(i,j)

                '''收集所有版本数据表对应的内容'''
                if cell_value in ignorOriginWords or not cell_value:
                # if cell_value == '' or cell_value == '预留' or cell_value == '0.0' or cell_value == 0.0:
                    continue

                if isStringChinese(cell_value) and not (cell_value.find('.mp3') > 0 or cell_value.find('.json') > 0 or cell_value.find('.png') > 0 or cell_value.find('.jpg') > 0 or cell_value.find('.plist') > 0):
                    translateData[sheetname][id][title][translateTitleList[2]] = cell_value
                else:
                    # value = makeCellValueRichText(cell_value)
                    translateData[sheetname][id][title][translateTitleList[translateIDx]] = cell_value

    writeExcelOld(translateData,filename)

def makeCellValueRichText(cellValue):
    isRichText = False
    if cellValue.find('\"color\"') > 0 and cellValue.find('\"text\"') > 0:
        isRichText = True

    if not isRichText:
        return cellValue
    else:
        for key in cellValue:
            print('key:',key)
            'TODO 校准富文本格式'


def writeExcelOld(translateData,filename):
    xlsdir = translateDir + '/' + filename
    if filename.find('beizhu') >= 0:
        print("translateData:",translateData)

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
            colList = configTranslateData.get(filename).get(sheetname)
            for i in range(rowNew):
                id = str(sheetnewTranslate.cell_value(i,0)).split('.')[0]
                if (not translateData.get(sheetname).get(id)):
                    translateData[sheetname][id] = {}

                for j in range(colNew):
                    colname = sheetnewTranslate.cell_value(i,1)
                    cell = sheetnewTranslate.cell_value(i,j)
                    if (colname in colList) and j is not translateIDx:
                        if (not translateData.get(sheetname).get(id).get(colname)):
                            translateData[sheetname][id][colname] = {}

                        translateData[sheetname][id][colname][translateTitleList[j]] = cell
                        translateData[sheetname][id][colname]['isExistInFile'] = True
                    elif not isReplaceNull and j is translateIDx:
                        '''默认不覆盖原来为空的表格'''
                        if cell == '' or not cell:
                            translateData[sheetname][id][colname][translateTitleList[j]] = ''


    # print("translateData:",translateData)
    workbook = xlwt.Workbook()
    for sheetname, idList in translateData.items():
        print('sheetname:',sheetname)

        newSheet = workbook.add_sheet(sheetname)
        for idx in range(len(translateTitleList)):
            name = translateTitleList[idx]
            newSheet.write(0, idx, name)
        row = 1
        for id, translateInfo in idList.items():
            # print('translateInfo len:',len(translateInfo))
            # print('translateInfo:',translateInfo)
            for colname, translateStrInfo in translateInfo.items():
                if id == '612' and filename.find('beizhu')>=0:
                    print("beizhu text:",translateStrInfo)
                # if sheetname.find('beizhu') >= 0 and colname.find("Text") >= 0:
                #     print("beizhu text:",translateStrInfo)

                if (len(translateStrInfo) <= 0):
                    continue
                if ((not translateStrInfo.get('isExistInFile')) and translateIDx == 2):
                    continue
                if row == 436 and filename.find('beizhu')>=0:
                    print('row:',row)
                for idx in range(len(translateTitleList)):
                    _name = translateTitleList[idx]
                    if id == '612' and filename.find('beizhu')>=0:
                        print("beizhu text: _name:",_name,'colname:',colname, 'row:',row,'translate:',translateStrInfo.get(_name))
                    if (idx == 0):
                        # print('translateStrInfo:',translateStrInfo)
                        newSheet.write(row, idx, id)
                        newSheet.write(row, 1, colname)
                    elif translateStrInfo.get(_name) and idx > 1:
                        newSheet.write(row, idx, translateStrInfo.get(_name))

                row = row + 1
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

def makeTranslateData():
    print('dataxlsName:',translateConfigFile)
    global configTranslateData;
    configTranslateData = {}

    table_data = xlrd.open_workbook(translateConfigFile)

    sheetnewTranslate = table_data.sheet_by_index(0)
    rowNew = sheetnewTranslate.nrows
    colNew = sheetnewTranslate.ncols
    for i in range(rowNew):
        if i == 0:
            continue
        sheetname = sheetnewTranslate.cell_value(i,1)
        colTitle = sheetnewTranslate.cell_value(i,2)
        if (not colTitle or colTitle == ''):
            continue
        tabname = sheetnewTranslate.cell_value(i,0)+'.xls'
        if (not configTranslateData.get(tabname)):
            configTranslateData[tabname] ={}


        colTitlelist = colTitle.split(';')
        configTranslateData[tabname][sheetname] = colTitlelist



try:
    # for xlsname, itemTranslate in translateMap.items():
    #     fp = search(filwXlsOldPth,xlsname)
    #     if fp:
    makeTranslateData()
    print('configData:',configTranslateData)
    global rootDataDir
    global translateIDx
    for idx in translateIDxList:
        translateIDx = idx
        rootDataDir = rootDataDirList[translateIDx]
        if (rootDataDir or rootDataDir is not ''):
            for root, dirs, files in os.walk(rootDataDir):
                for OneFileName in files:
                    if (OneFileName.find('.xls') > 0 or OneFileName.find('.xlsx') > 0):
                        configData = configTranslateData.get(OneFileName)
                        if (configData):
                            makeSheepInfo(os.path.join(root, OneFileName),configData,OneFileName)

                for dir in dirs:
                    for root2, dirs2, files2 in os.walk(os.path.join(root, dir)):
                        for OneFileName2 in files2:
                            if OneFileName2.find('.xls') > 0 or OneFileName2.find('.xlsx') > 0:
                                if (configTranslateData.get(OneFileName)):
                                    makeSheepInfo(os.path.join(root2, OneFileName2),configData,OneFileName)


    print('合并完毕')
except Exception as e:
    print("异常"+e)