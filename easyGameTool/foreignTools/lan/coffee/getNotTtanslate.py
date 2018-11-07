__author__ = 'lan'
#分离程序中文文本 把未翻译的 遍历翻译表 对应已经翻译项 添加对应coffee路径，对应未翻译项 后边追加。每次克隆excel备份。
'''
获取对应语言，coffee／ccb

'''
import os
from os.path import join
import re
import xlrd
import xlwt
# import sys
#
# reload(sys)
# sys.setdefaultencoding('utf8')
#
'''
英文版中文查找
'''

coffee_path = '/Users/lan/clientprojects/pikachu_english/app/static/coffee/'
# coffee_path = '/Users/lan/clientprojects/pikachu_russion/app/static/coffee/'
preKeywords = ['publish(', '@$id =', '@$init =', 'indexOf(', '@subscribe(', 'res: [', '@log', 'error(', 'log ', 'error ', '.log(']
afterKeywords = ['lbl', 'menu', 'undefined', '.png', '.ccb', '.plist', 'res/', '.fnt', 'hongdian', 'Msg', '#ff', '_', '.jpg', 'gongji', 'jiangli', 'Animation', '.mp3', 'test', 'true}'] #包含排除
startKeywords = ['layer', 'form', 'unknown', 'waixian', 'type', 'account/'] #开始字符排除
exclueWords = ['on', 'off', 'zh', 'en', 'Arial', 'item', 'ios', 'android', 'count', 'function', 'POST', 'GET', 'Helvetica', 'Content-Type', 'egret', 'joyfun', 'node', 'value', 'star', 'VIP', 'TRUE', 'length', 'result'] #整体排除
excludeFiles = ['Unit.coffee', 'GoUnitArmature.coffee', 'FormHeroTest.coffee', 'GameProtocol.coffee'] #待判定
resultWords = {}
replaceFile = '/Users/lan/Downloads/历次翻译整理/整理汇总翻译/coffeeReplace.xls'
# replaceFile = '/Users/lan/Downloads/历次翻译整理/russion/front_russionOnly_0420.xls'
# fileIdx = [4,1,3,5,0] #中文，路径，英文，俄文，ID
fileIdx = [4,1,3,0,0] #中文，路径，英文，俄文，ID
resultXlsWords = []
needTranslateMap = {}
splitedMap = {}
'''
isRussion:(1)俄文 (2)英文 (0)中文
isCharEnglish
'''
isRussion = 0


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

def checkStrCharUnuse(str):
    # print('str:',str)
    testIdx1 = str.find('\\\'')
    if testIdx1 >= 0:
        str = str.replace('\\\'','%**')
    testIdx2 = str.find('\\\"')
    if testIdx2 >= 0:
        str = str.replace('\\\"','$$$')

    return str

def checkStrCharuse(str):
    str = str.replace('%**','\\\'')
    str = str.replace('$$$','\\\"')
    return str

def isCharRussion(uchar):
    """判断一个unicode是否是汉字"""
    if uchar >= u'\u0400' and uchar<=u'\u052F':
        return True
    else:
        return False

def isStringRussion(str):
    for uchar in str:
        if isCharRussion(uchar):
            # print('Мегаэволюция:',str)
            return True
    return False

def isCharChinese(uchar):
    """判断一个unicode是否是汉字"""
    if uchar >= u'\u4e00' and uchar<=u'\u9fa5':
        return True
    else:
        return False

def isStringChinese(sText):
    if isRussion == 1:
        return isStringRussion(sText)
    elif isRussion == 2:
        return isStringEnglish(sText)

    if isinstance(sText, str):
        for uchar in sText:
            if isCharChinese(uchar):
                return True
        return False
    else:
        return False

def isStringWord(str):
    return re.match(r'.*[a-zA-Z]{2}.*', str)

def isStringMsgOrName(str):
    return re.match(r'.*[a-z][A-Z].*', str)

def isContainsKeyword(sText, keyWords):
    if isinstance(sText, str):
        for word in keyWords:
            if sText.find(word) != -1:
                return True
        return False
    else:
        return False

def preCheck(str):
    return isContainsKeyword(str, preKeywords)

def checkStart(str):
    for word in startKeywords:
        if str.startswith(word):
            return True
    return False


#匹配英文字符串
def scan(str):
    if preCheck(str):
        return
    if str.startswith("#"):
        return
    # p = re.compile('[\'\"]([\w\s\-,.?:;!\(\)\[\]\{\}+：$\\\\]+)[\'\"]')
    p = re.compile('[\'\"](.+)[\'\"]')
    allEle = p.findall(str)
    if allEle:
        for ele in allEle:
            recheckStr(ele)

def recheckStr(str):
    if isStringChinese(str):
        resultWords[str] = 1


def searchOneFile(path, OneFileName):
    if not path:
        return
    # print('path:' + path)
    global resultWords
    resultWords = {}
    with open(path, 'r') as r:
        lines = r.readlines()
        for l in lines:
            scan(l)
        # setWords = set(resultWords)
        for key, value in resultWords.items():
            # print(OneFileName + '\t' + key)
            _item = {}
            _item['filePth'] = OneFileName
            _item['keyOriginTxt'] = key
            resultXlsWords.append(_item)
            # print('filePth:',OneFileName)

def writeExcel(dataMap,notTranslteMap,isSplitMake):
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
    print('nrows:',nrows)
    for i in range(nrows):
        isFindTranslate = 0
        if (table.cell_value(i, fileIdx[1]) == None or table.cell_value(i, fileIdx[1]) == '') and (table.cell_value(i, fileIdx[4]) == None or table.cell_value(i, fileIdx[4]) == ''):
            trueRows = i
            break;
        for j in range(ncols):
            cell_value = table.cell_value(i, j)
            if j == 0:
                numArray = str(cell_value).split('.')
                num = numArray[0]
                if str(num).isdigit():
                    if id < int(num):
                        id = int(num);

            objTranslatePth = dataMap.get(str(cell_value))
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
    # print('dataMap:',dataMap)
    # print('findValues:',findValues)

    for key, item in dataMap.items():
        # print('key:',key)
        if findValues.get(key) == None and item != None:
            notTranslteMap[key] = item
            # print('notTtanslate:',key)
    # print(splitedMap)
    # print('notTranslteMap:',notTranslteMap)
    print(splitedMap,'isSplitMake:',isSplitMake)
    if len(splitedMap) > 0 and not isSplitMake:
        writeExcel(splitedMap,notTranslteMap,True)
        return

    needAddTanslteLen = len(notTranslteMap)
    print('notTranslteMap:',notTranslteMap)
    _id = id
    if needAddTanslteLen > 0:
        k = 0
        # fileIdx = [4,1,3,5,0] #中文，路径，英文，俄文，ID
        for key1, item1 in notTranslteMap.items():
            newSheet.write(k+trueRows, fileIdx[4], id+1)
            id = id + 1
            # print('key1:',key1,'colum:',fileIdx[1],' key1:',key1)
            originIdx = 0
            if isRussion == 1:
                originIdx = 3

            newSheet.write(k+trueRows, fileIdx[originIdx], key1)
            newSheet.write(k+trueRows, fileIdx[1], item1)
            # newSheet.write(k+trueRows, 2, str(_id))
            k = k + 1
            # print('oiginTxt:',key1)

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
    makeAnotherXls(notTranslteMap,id,pth)

#抽取待翻译文本
def makeAnotherXls(notTranslteMap,id,pth):
    needAddTanslteLen = len(notTranslteMap)
    workbook2 = xlwt.Workbook()  #创建一个excel文件
    newSheet2 = workbook2.add_sheet('sheet0',cell_overwrite_ok=True)
    if needAddTanslteLen > 0:
        k = 1
        # fileIdx = [4,1,3,5,0] #中文，路径，英文，俄文，ID
        newSheet2.write(0, fileIdx[4], 'id')
        newSheet2.write(0, fileIdx[0], 'Chinese')
        newSheet2.write(0, fileIdx[1], 'FilePth')
        newSheet2.write(0, fileIdx[2], 'English')
        newSheet2.write(0, fileIdx[3], 'Russion')
        for key1, item1 in notTranslteMap.items():
            newSheet2.write(k, fileIdx[4], id+1)
            id = id + 1
            newSheet2.write(k, fileIdx[0], key1)
            newSheet2.write(k, fileIdx[1], item1)
            k = k + 1

    fp = os.path.join(pth + '待翻译文本.xls')
    workbook2.save(fp)

if __name__ == "__main__":
    try:
        for root, dirs, files in os.walk(coffee_path):
            for OneFileName in files:
                if OneFileName.find('.coffee') == -1:
                    continue
                if (OneFileName in excludeFiles):
                    continue
                searchOneFile(os.path.join(root, OneFileName), OneFileName)

        print('resultXlsWords:',resultXlsWords)
        needTranslateMap = {}
        for value in resultXlsWords:
            # print(value)
            pth = needTranslateMap.get(str(value.get('keyOriginTxt')))
            if pth != None:
                if pth.find(str(value.get('filePth'))) < 0:
                    pth = pth + ';' + str(value.get('filePth'))
            else:
                pth = str(value.get('filePth'))
            needTranslateMap[str(value.get('keyOriginTxt'))] = pth;
            # print(str(value.get('keyOriginTxt')) + '\t' + pth)
        print("needTranslateMap:",needTranslateMap)
        #过滤中文时候用
        needSpliteMapList = {}
        # print('needTranslateMap:',needTranslateMap)
        splitedMap = {}
        for key, item in needTranslateMap.items():
            # print('key:',key,'item:',item)
            checkStr = checkStrCharUnuse(str(key))
            if checkStr.find('\'') >= 0 or checkStr.find('\"') >= 0:
                needSpliteMapList[str(key)] = item
                _list = []
                if checkStr.find('\'') >= 0:
                    _list = checkStr.split('\'')
                elif checkStr.find('\"') >= 0:
                    _list = checkStr.split('\"')
                for item1 in _list:
                    _list2 = []
                    if item1.find('\'') >= 0:
                        _list2 = item1.split('\'')
                    elif item1.find('\"') >= 0:
                        _list2 = item1.split('\"')
                    else:
                        _list2.append(item1)

                    for item2 in _list2:
                        if isStringChinese(item2):
                            originTxt1 = checkStrCharuse(str(item2))
                            pth = splitedMap.get(originTxt1)
                            if pth == None:
                                splitedMap[originTxt1] = item
                                pth = item
                            else:
                                pthArray = item.split(';')
                                for addPth in pthArray:
                                    if pth.find(addPth) < 0:
                                        pth = pth + ';' + addPth
                            splitedMap[originTxt1] = pth
                            print(originTxt1,'pth:',pth)
        print('needSpliteMapList:',needSpliteMapList)
        for _nk, _nitem in needSpliteMapList.items():
            if needTranslateMap.get(_nk) != None:
                needTranslateMap[_nk] = None;
        print('needTranslateMap:',needTranslateMap)
        writeExcel(needTranslateMap,{},None)


            # if str(value.get('StringChare')) == '\"':
            #     print(str(value.get('filePth')) + '\t' + '双引号' + '\t' + key)
            # else:
            #     print(str(value.get('filePth')) + '\t' + str(value.get('StringChare')) + '\t' + key)
        # print('ignorResourts:',ignorResourts)
        #上边的idList和ccbList通过这里打印获取到的
        # print("idList:",idList)
        # print("ccbList:",ccbList)
        print('处理完毕！')
        # str = "\"c\"d'e'f"
        # print(str.split('\"'))
        # p = re.compile('[\'\"](.+)[\'\"]')
        # allEle = p.findall(str)
        # print(allEle)
        # print(str.find('\"'))
        # print(str.find('\''))

    except Exception as e:
        print("异常" + e)
