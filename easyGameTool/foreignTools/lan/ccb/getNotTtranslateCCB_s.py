# -*- coding: utf-8 -*-

import codecs
import json
import os
import xlrd
import xlwt
#from os.path import join


# encoding=utf8
import sys



try:
    import xml.etree.cElementTree as ElementTree
except ImportError:
    import xml.etree.ElementTree as ElementTree

# reload(sys)
# sys.setdefaultencoding("utf8")

ccb_path = '/Users/admin/Documents/ljworkspace/local/cocos/project/pikachu_englishGit/pikachu_english/tools/pikachuCCB/ccb/'
keyWords = ['XXX', '00:00', 'x9', 'x1', 'Lv', '0k', 'Name', 'xxx', 'VIP', 'x2', 'X1', 'lv', 'Pipi', '90 k', 'Next attributes', 'xz', 'X30', '皮皮']
pattens = ['：1000', 'LV 1', ':1']

replaceFile = '/Users/admin/Documents/ljworkspace/local/cocos/test/foreignTools/lan/ccb/ccb_0702.xls'
fileIdx = [0,1,2,3] #中文，路径，英文，俄文
needTranslateMap = {}

def isContainsKeyword(sText):
    if isinstance(sText, str):
        for word in keyWords:
            if sText.find(word) != -1:
                return True
        return False
    else:
        return False

def isCharRussion(uchar):
    """判断一个unicode是否是汉字"""
    if uchar >= u'\u0400' and uchar<=u'\u052F':
        return True
    else:
        return False

def isCharChinese(uchar):
    """判断一个unicode是否是汉字"""
    if uchar >= u'\u4e00' and uchar<=u'\u9fa5':
        return True
    else:
        return False

def isCharEnglish(uchar):
    if (uchar >= u'\u0061' and uchar<=u'\u007a') or (uchar >= u'\u0041' and uchar<=u'\u005a'):
        return True
    else:
        return False

'''
小写字母：[0x61,0x7a]（或十进制[97, 122]）
大写字母：[0x41,0x5a]（或十进制[65, 90]）
'''

def isStringEnglish(sText):
    if isinstance(sText, str):
        for uchar in sText:
            if isCharEnglish(uchar):
                return True
        return False
    else:
        return False

def isStringchinese(sText):
    #if isinstance(sText, str):
    for uchar in sText:
        if isCharChinese(uchar):
            return True
    return False
    #else:
       # return False

def readfile(file):
    """
    读取文本文件内容
    :param file:
    :return: string
    """
    fs = codecs.open(file, 'r', 'utf-8')
    try:
        return fs.read()
    except Exception as ex:
        print("read file %s with error.", file)
        print(ex)
    finally:
        fs.close()


def parse_resource(name):
    print(os.path.join(ccb_path, name))
    #readfile(os.path.join(ccb_path, name))

    #parse_node()
    strr = readfile(os.path.join(ccb_path, name))
    root = ElementTree.fromstring(strr)
    parse_node(root, name)

def parse_node(node, name):
    # if node.tag == 'array' and isText:
    #     self.parse_resource_arraynode(node)
    #     return
    isTypeKeyType = False
    isText = False

    for child in node:
        if child.tag == 'key' and child.text == 'type':
            isTypeKeyType = True
        elif isTypeKeyType and child.tag == 'string' and child.text == 'Text':
            isText = True
        elif isText and child.tag == 'string':
            if child.text and isStringchinese(child.text) and not isContainsKeyword(child.text):
                # print('%s\t%s' % (name, child.text))
                needTranslateMap[str(child.text)] = name
            break

        if child.tag == 'dict' or child.tag == 'array':
            parse_node(child, name)

def writeExcel():
#     replaceFile = '/Users/lan/Downloads/历次翻译整理/整理汇总翻译/cofeeTest.xls'
# fileIdx = [4,1,3,5,0] #中文，路径，英文，俄文，ID

    table_translate = xlrd.open_workbook(replaceFile)
    table = table_translate.sheet_by_index(0)
    nrows = table.nrows                         # 获取table工作表总行数
    ncols = table.ncols                         # 获取table工作表总列数

    workbook = xlwt.Workbook()  #创建一个excel文件
    newSheet = workbook.add_sheet('sheet0',cell_overwrite_ok=True)
    # print('translateCoffeeMap:',translateCoffeeMap)
#记录当前表的最大ID
    id = 0
#记录已经翻译过的文本 用来过滤出未翻译的文本
    findValues = {}
    trueRows = nrows
    for i in range(nrows):
        isFindTranslate = 0
        if table.cell_value(i, fileIdx[1]) == None or table.cell_value(i, fileIdx[1]) == '':
            trueRows = i
            break;
        for j in range(ncols):
            cell_value = table.cell_value(i, j)
            objTranslatePth = needTranslateMap.get(str(cell_value))
            if objTranslatePth != None and isFindTranslate != 1:
                isFindTranslate = 1
                # print('id',table.cell_value(i, 0),'chinese:',cell_value)
                newpthArray = objTranslatePth.split(';')
                filepth = table.cell_value(i, fileIdx[1])
                for filename in newpthArray:
                    if filepth.find(filename) >= 0:
                        continue
                    filepth = filepth + ';' + filename
                findValues[str(cell_value)] = filepth
                newSheet.write(i, fileIdx[1], filepth)
            if isFindTranslate == 1:
                if j == fileIdx[1]:
                    continue;
            newSheet.write(i, j, cell_value)
    notTranslteMap = {}
    print('findValues:',findValues)
    for key, item in needTranslateMap.items():
        print('key:',key)
        if findValues.get(key) == None:
            notTranslteMap[key] = item

    needAddTanslteLen = len(notTranslteMap)
    if needAddTanslteLen > 0:
        k = 0
        # fileIdx = [4,1,3,5,0] #中文，路径，英文，俄文，ID
        for key1, item1 in notTranslteMap.items():
            newSheet.write(k+trueRows, fileIdx[0], key1.encode("utf-8"))
            newSheet.write(k+trueRows, fileIdx[1], item1)
            k = k + 1

    newfilearray = replaceFile.split('/')
    pth = ''
    fileName = ''
    for dir in newfilearray:
        if dir.find('.') <= 0:
            pth = pth + dir + '/'
        else:
            namearray = dir.split('.')
            fileName = namearray[0] + '.xls'
    print('fileName pth:', pth + fileName)
    fp = os.path.join(pth + fileName)
    workbook.save(fp)
    makeAnotherXls(notTranslteMap,pth)

#抽取待翻译文本
def makeAnotherXls(notTranslteMap,pth):
    needAddTanslteLen = len(notTranslteMap)
    workbook2 = xlwt.Workbook()  #创建一个excel文件
    newSheet2 = workbook2.add_sheet('sheet0',cell_overwrite_ok=True)
    if needAddTanslteLen > 0:
        k = 1
        # fileIdx = [4,1,3,5,0] #中文，路径，英文，俄文，ID
        newSheet2.write(0, fileIdx[0], 'Chinese')
        newSheet2.write(0, fileIdx[1], 'FilePth')
        newSheet2.write(0, fileIdx[2], 'English')
        newSheet2.write(0, fileIdx[3], 'Russion')
        for key1, item1 in notTranslteMap.items():
            newSheet2.write(k, fileIdx[0], key1)
            newSheet2.write(k, fileIdx[1], item1)
            k = k + 1

    fp = os.path.join(pth + '待翻译文本CCB.xls')
    print(fp)
    workbook2.save(fp)



def gerFileList():
    filList = [  "FormConfirmDaoGuanRoleInfo.ccb",
    "FormDaoGuanHistory.ccb",
    "FormGongHuiXianZhiYouJian.ccb",
    "LayerDaoGuan.ccb",
    "LayerGongHuiDaoGuan.ccb",
    "LayerGongHuiDaoGuanFirstHead.ccb",
    "DaoGuanFirstHeadCell.ccb",
    "LayerGongHuiDaoGuanGongXian.ccb",
    "LayerGongHuiDaoGuanRank.ccb",
    "DaoGuanRankCell.ccb",
    "LayerGongHuiDaoGuanScene.ccb",
    "LayerDaoGuanRole.ccb",
    "LayerGongHuiXianZhiZhanli.ccb",
    "FormGongHuiXianZhiYouJian.ccb",]
    neL = []
    for i in filList:
        neL.append(ccb_path + "/"+ i)
        print(i)
    print(neL)
    return  filList


if __name__ == "__main__" :
    # parse_resource('ArtifactNodeInList')
    # try:
    needTranslateMap = {}
    # for root, dirs, files in os.walk(ccb_path):
    #     for OneFileName in files:
    #         if OneFileName.find('.ccb') == -1:
    #
    #
    #       continue
    allList = gerFileList()

    for OneFileName in allList:
        parse_resource(OneFileName)
    writeExcel()
    print('处理完毕！')

    # except Exception as e:
    #     print("异常"+e)

