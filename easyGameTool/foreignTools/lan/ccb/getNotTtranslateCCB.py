# -*- coding: utf-8 -*-

import codecs
import json
import os
import xlrd
import xlwt

'''抽取ccb内的中文 放在收集翻译的表内 并建待翻译表'''

try:
    import xml.etree.cElementTree as ElementTree
except ImportError:
    import xml.etree.ElementTree as ElementTree

# reload(sys)
# sys.setdefaultencoding("utf8")

ccb_path = '/Users/admin/Documents/ljworkspace/local/cocos/project/pikachu_englishGit/pikachu_english/tools/pikachuCCB/ccb'
keyWords = ['XXX', '00:00', 'x9', 'x1', 'Lv', '0k', 'Name', 'xxx', 'VIP', 'x2', 'X1', 'lv', 'Pipi', '90 k',
            'Next attributes', 'xz', 'X30', '皮皮']
pattens = ['：1000', 'LV 1', ':1']

# replaceFile = '/Users/songbin/Downloads/历次翻译整理/整理汇总翻译/CCBReplaceEnglish_最终.xls'
replaceFile = '/Users/admin/Desktop/ccbTranslate.xls'
idMapXlsPth = '/Users/admin/Desktop/tete/'
# idMapXlsPth='/Users/songbin/Downloads/Language/法语/ccbLbl/'

fileIdx = [1, 2, 3, 4]  # 中文，路径，英文，俄文
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
    if uchar >= u'\u0400' and uchar <= u'\u052F':
        return True
    else:
        return False


def isCharChinese(uchar):
    """判断一个unicode是否是汉字"""
    if uchar >= u'\u4e00' and uchar <= u'\u9fa5':
        return True
    else:
        return False


def isCharEnglish(uchar):
    if (uchar >= u'\u0061' and uchar <= u'\u007a') or (uchar >= u'\u0041' and uchar <= u'\u005a'):
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
    if isinstance(sText, str):
        for uchar in sText:
            if isCharChinese(uchar):
                return True
        return False
    else:
        return False


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
    # readfile(os.path.join(ccb_path, name))
    root = ElementTree.fromstring(readfile(os.path.join(ccb_path, name)))
    parse_node(root, name)
    # print('nodeIdMap:',nodeIdMap[name])


def parse_node(node, name):
    # if node.tag == 'array' and isText:
    #     self.parse_resource_arraynode(node)
    #     return
    isTypeKeyType = False
    isText = False

    isLabelName = 0
    lastLabelName = ''

    for child in node:
        if child.tag == 'key' and child.text == 'baseClass':
            isLabelName = 1
        elif isLabelName == 1 and child.tag == 'string' and (
                child.text == 'CCLabelTTF' or child.text == 'CCLabelBMFont'):
            isLabelName = 2
        elif isLabelName == 2 and child.tag == 'key' and child.text == 'displayName':
            isLabelName = 3
        elif isLabelName == 3 and child.tag == 'string':
            isLabelName = 0
            lastLabelName = str(child.text)
            nodeIdMap[name][lastLabelName] = {}
            nodeIdMap[name][lastLabelName]['str'] = '0'
            # print('nodeIdMap displayName:',lastLabelName)

        # print("child:",child.tag, 'text:',child.text)
        if child.tag == 'key' and child.text == 'type':
            isTypeKeyType = True
        elif isTypeKeyType and child.tag == 'string' and child.text == 'Text':
            isText = True
        elif isText and child.tag == 'string':
            # if (child.text == '踢出'):
            #     print('猴哥11111')
            #     print(isStringchinese(child.text))
            #     print(isContainsKeyword(child.text))
            if child.text and isStringchinese(child.text) and not isContainsKeyword(child.text):
                print(' %s\t%s' % (name, child.text))
                strText = str(child.text)
                pth = needTranslateMap.get(strText)
                if (pth):
                    needTranslateMap[strText] = pth + ';' + name
                else:
                    needTranslateMap[strText] = name

                # print('lastLabelName',lastLabelName)

            _len = len(nodeIdMap[name])
            index = 1
            for key, item in nodeIdMap[name].items():
                if (index == _len):
                    nodeIdMap[name][key]['str'] = str(child.text)
                index = index + 1

            break

        if child.tag == 'dict' or child.tag == 'array':
            parse_node(child, name)


def writeExcel():
    #     replaceFile = '/Users/songbin/Downloads/历次翻译整理/整理汇总翻译/cofeeTest.xls'
    # fileIdx = [4,1,3,5,0] #中文，路径，英文，俄文，ID

    table_translate = xlrd.open_workbook(replaceFile)
    table = table_translate.sheet_by_index(0)
    nrows = table.nrows  # 获取table工作表总行数
    ncols = table.ncols  # 获取table工作表总列数

    workbook = xlwt.Workbook()  # 创建一个excel文件
    newSheet = workbook.add_sheet('sheet0', cell_overwrite_ok=True)
    # print('translateCoffeeMap:',translateCoffeeMap)
    # 记录当前表的最大ID
    id = 0
    # 记录已经翻译过的文本 用来过滤出未翻译的文本
    findValues = {}
    trueRows = nrows
    for i in range(nrows):
        isFindTranslate = 0

        if table.cell_value(i, fileIdx[1]) == None or table.cell_value(i, fileIdx[1]) == '':
            trueRows = i
            break;

        _id = table.cell_value(i, 0)
        print("id:", _id)

        for j in range(ncols):
            cell_value = table.cell_value(i, j)
            if i == 0:
                newSheet.write(i, j, cell_value)
                continue
            objTranslatePth = needTranslateMap.get(str(cell_value))
            filepth = table.cell_value(i, fileIdx[1])
            if objTranslatePth != None and isFindTranslate != 1:
                isFindTranslate = 1
                # print('id',table.cell_value(i, 0),'chinese:',cell_value)
                newpthArray = objTranslatePth.split(';')
                for filename in newpthArray:
                    if filepth.find(filename) >= 0:
                        continue
                    filepth = filepth + ';' + filename
                findValues[str(cell_value)] = filepth

                newSheet.write(i, fileIdx[1], filepth)

            if (j != 0 and j != 2):
                newPtharray = makeXlsIdMap(filepth, str(cell_value), int(_id))
                if newPtharray:
                    isFindTranslate = 1
                    newSheet.write(i, fileIdx[1], newPtharray)

            if isFindTranslate == 1:
                if j == fileIdx[1]:
                    continue;
            newSheet.write(i, j, cell_value)

        if i > 0 and id < int(_id):
            id = int(_id)
    notTranslteMap = {}
    # print('findValues:',findValues)
    for key, item in needTranslateMap.items():
        # print('key:',key)
        if findValues.get(key) == None:
            notTranslteMap[key] = item

    needAddTanslteLen = len(notTranslteMap)
    if needAddTanslteLen > 0:
        k = 0
        # fileIdx = [4,1,3,5,0] #中文，路径，英文，俄文，ID
        for key1, item1 in notTranslteMap.items():
            newSheet.write(k + trueRows, 0, id + 1)
            newSheet.write(k + trueRows, fileIdx[0], key1)
            newSheet.write(k + trueRows, fileIdx[1], item1)
            newPtharray = makeXlsIdMap(item1, key1, id)
            if newPtharray:
                newSheet.write(k + trueRows, fileIdx[1], newPtharray)
            id = id + 1
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
    makeAnotherXls(notTranslteMap, pth)


def makeXlsIdMap(pthStr, originText, id):
    nodeIdMap
    # newpthArray = pthStr.split(';')
    # for filename in newpthArray:
    #     map = nodeIdMap.get(filename)
    #     if (map):
    #         for lblName, obj in map.items():
    #             str = obj.get('str')
    #             if (str == originText):
    #                 nodeIdMap[filename][lblName]['id'] = id
    findFileName = ''
    for fileName, fileMap in nodeIdMap.items():
        if (fileMap):
            for lblName, obj in fileMap.items():
                str = obj.get('str')
                if (str == originText):
                    nodeIdMap[fileName][lblName]['id'] = id
                    findFileName = fileName
                    break

    if findFileName != '' and pthStr.find(findFileName) < 0:
        print('findNew CCB Pth:', findFileName)
        pthStr = pthStr + ';' + findFileName
        return pthStr


def writeIdMap():
    nodeIdMap
    for fileName, fileMap in nodeIdMap.items():
        ccbLblXlsPth = idMapXlsPth + fileName.split('.')[0] + '.xls'
        if os.path.exists(ccbLblXlsPth):
            table_translate = xlrd.open_workbook(ccbLblXlsPth)
            table = table_translate.sheet_by_index(0)
            """获取table工作表总行数"""
            nrows = table.nrows
            """获取table工作表总列数"""
            ncols = table.ncols
        else:
            nrows = 0

        workbook2 = xlwt.Workbook()  # 创建一个excel文件
        newSheet2 = workbook2.add_sheet('sheet0', cell_overwrite_ok=True)

        newSheet2.write(0, 0, 'lblName')
        newSheet2.write(0, 1, 'lblId')
        findNameList = []
        if nrows > 0:
            for i in range(nrows):
                cellValue = table.row_values(i, 0, ncols)
                if i == 0:
                    continue
                lblInfo = fileMap.get(cellValue[0])
                if not lblInfo:
                    newSheet2.write(i, 0, cellValue[0])
                    newSheet2.write(i, 1, cellValue[1])
                else:
                    findNameList.append(cellValue[0])
                    lblId = lblInfo.get('id')
                    lblText = lblInfo.get('str')
                    if lblId:
                        lblId = lblInfo.get('id')
                        isWrit = True
                    elif lblText.find('ccbList_') >= 0:
                        lblId = int(lblText.split('_')[1])
                        isWrit = True
                    newSheet2.write(i, 0, cellValue[0])
                    newSheet2.write(i, 1, str(lblId))
        row = nrows
        if row == 0:
            row = row + 1
        for lblNode, nodeInfo in fileMap.items():
            lblname = lblNode
            if lblname in findNameList:
                continue
            print('nodeInfo: lblNode:', lblNode, nodeInfo)
            lblId = nodeInfo.get('id')
            lblText = nodeInfo.get('str')
            isWrit = False
            if lblId:
                lblId = nodeInfo.get('id')
                isWrit = True
            elif lblText.find('ccbList_') >= 0:
                lblId = int(lblText.split('_')[1])
                isWrit = True

            if (isWrit):
                newSheet2.write(row, 0, lblname)
                newSheet2.write(row, 1, lblId)
                row = row + 1

        print("ccbLblXlsPth:", ccbLblXlsPth)
        newfilearray = ccbLblXlsPth.split('/')
        pth = ''
        for dir in newfilearray:
            if dir.find('.') <= 0:
                pth = pth + dir + '/'

        if not os.path.exists(pth):
            '''创建路径'''
            os.makedirs(pth)

        workbook2.save(ccbLblXlsPth)


# 抽取待翻译文本
def makeAnotherXls(notTranslteMap, pth):
    needAddTanslteLen = len(notTranslteMap)
    workbook2 = xlwt.Workbook()  # 创建一个excel文件
    newSheet2 = workbook2.add_sheet('sheet0', cell_overwrite_ok=True)
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
    print("newFilePth:", fp)
    workbook2.save(fp)


if __name__ == "__main__":
    # parse_resource('ArtifactNodeInList')
    try:
        global nodeIdMap
        nodeIdMap = {}
        needTranslateMap = {}
        for root, dirs, files in os.walk(ccb_path):
            for OneFileName in files:
                if OneFileName.find('.ccb') == -1:
                    continue
                nodeIdMap[OneFileName] = {}
                parse_resource(OneFileName)
        writeExcel()
        print('nodeIdMap:', nodeIdMap)
        writeIdMap()

        print('处理完毕！')

    except Exception as e:
        print("异常" + e)
