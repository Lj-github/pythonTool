__author__ = 'lan'
"""
替换ccb语言 或者整个语言版本
包括备份 现在ccb的内容
3.需要替换完成后删除相应项目，或者添加已处理标记
俄文版替换错误例子：_DigGemRsps = ["DigBaoshiRsp", "DigHighBaoshiRsp", "DigTopLevelBaoshiRsp"] 替换了Dig

LayerSelectHero.coffee Grass
ChessStep.coffee Grass

"""

import pymysql
from collections import OrderedDict
import os
import shutil
import re
import xlrd
import datetime
import xlwt
import re

"警告⚠️ "
specialKeyWords = ['>type<','>value<','>name<','>string<','>children<']

svnPth = '/Users/lan/sanguo/'
coffee_path = '/Users/lan/clientprojects/pikachu_english/app/static/coffee'
json_path = '/Users/lan/clientprojects/pikachu_english/app/static/res'
ccb_path = '/Users/lan/clientprojects/pikachu_english/tools/pikachuCCB/ccb'

excelFiles=[
    '/Users/lan/sanguo/aiweiyou_pokmon/pika_foreign/ccbTranslate.xls'
]

'''origin pth translate sheetIdx'''
'''0中文 2英文 3俄文'''
"""这里origin translate 无效了"""
useIdx=[
    [0,2,2,0]
]

'''0.中文 2.英文 3.俄文 4.越南 5法语'''
"""第一列加了ID 所有列加一"""

'''当前外文版本'''
originIdx = 1
'''将要替换到外文版本'''
translateIdx = 6

LanguageTemp = ['','Chinese','','English','Russion','Vietnam',"French"]
translateTxt = ['','chinese','','english','russion','vietnam','french']
coffeeTranslateJson = ['','中文','','英文','俄文','越南','法语']
serverLink = {
    1:'http://test.easygametime.com:19090/webServer_pikachu/services/',
    3:'http://test.easygametime.com:19090/webServer_pikachu/services/',
    4:"https://pokemon-game01-dev.espritgames.ru:9443/webServer_pikachu/services/",
    5:'https://cert-test-hh5-server.pkc.easygametime.com:9443/webServer_pikachu/services/',
    6:'https://cert-test-hh5-server.pkc.easygametime.com:9443/webServer_pikachu/services/'
}
idx_language = {
    'id':0,
    'chinese':1,
    'english':3,
    'russion':4,
    'vietnam':5,
    'french':6,
}
svnPth = '/Users/lan/sanguo/'
jsonDataPthList = [
    '',
    'aiweiyou_pokmon/tools/exceltojson/json',
    '',
    'aiweiyou_pokmon/EnglishResources/tools/exceltojson/json',
    'aiweiyou_pokmon/RussionResources/tools/exceltojson/json',
    'aiweiyou_pokmon/VietnamResources/tools/exceltojson/json',
    'aiweiyou_pokmon/FrenchResources/tools/exceltojson/json',
]

resDataPthList = [
    [''],
    [
        'art_pikachu',
    ],
    [''],
    [
        'art_pikachu/翻译美术图',
        'art_pikachu/程天游',
        'art_pikachu/绿洲',
    ],
    ['art_pikachu/翻译美术图（俄文版）'],
    ['art_pikachu/翻译美术（越南）'],
    ['art_pikachu/翻译美术（法国）']
]

isOnlyTranslateCCB = True
"""备份cbb"""

'''只是翻译 true 以备份ccb为准 从备份ccb 生成翻译语言ccb
            false 以程序ccb为准 从程序ccb 备份ID索引ccb，并覆盖程序ccb为索引ccb'''
isNewTranslate = True

isUseIDCCB = False

notTranslateExlPth = '/Users/lan/Downloads/Language/法语/needTranslate/'

'''这个路径 本应该用作程序语言区分 但是实际上用作更新版本区分'''
backUpDir = "/Users/lan/Downloads/Language/法语/ccb/"
# backUpDir = '/Users/lan/Downloads/Language/英文/ccb/'
backUpDirList = [
    '',
    '',
    '',
    '/Users/lan/Downloads/Language/英语/ccb/',
    '/Users/lan/Downloads/Language/俄语/ccb/',
    '/Users/lan/Downloads/Language/越南/ccb/',
    '/Users/lan/Downloads/Language/法语/ccb/',
]

"警告⚠️ 程序内的艺术字备份会把备份路径内的东西覆盖，请确认程序语言类型 originIdx，一定要正确！"
isNeedBeifen = True

def search(path, word):
    for filename in os.listdir(path):
        fp = os.path.join(path, filename)
        if os.path.isfile(fp) and word in filename:
            return fp
        elif os.path.isdir(fp):
            fp = search(fp, word)
            if fp:
                return fp

def isSpecialKey(strOriginArray):
    for str in strOriginArray:
        for keyStr in specialKeyWords:
            if keyStr.find(str) >= 0:
                return True
        return False

def replaceOneFile(originText, newText, path):
    if not path:
        return
    strOriginArray = originText.split('\n')
    isSpecial = False
    with open(path,'r',32,'utf-8') as r:
        if isSpecialKey(strOriginArray):
            lines=r.readlines()
            isSpecial = True
        else:
            lines = r.read()
    print('path:',path)
    print('strOrigin:',strOriginArray,'isSpecial:',isSpecial," originText:",originText, " newText:",newText)
    lastLineTrue = False
    isLastLine = False

    with open(path,'w',32,'utf-8') as w:
        ismakeTranslateJs = False
        if not isSpecial:
            for i0 in range(len(strOriginArray)):
                _str = strOriginArray[i0]
                if (newText.find('ccbList_1089')>= 0):
                    print('_str:',_str)
                if i0 == 0:
                    lines = lines.replace(_str, newText)
                else:
                    lines = lines.replace(_str, '')
            w.write(lines)
            return
        if path.find("makeTranslate") >= 0 or path.find(".json") >= 0:
            isText = 3
            ismakeTranslateJs = True
        else:
            isText = 0
        for l in lines:
            if not ismakeTranslateJs:

                if l.find('<dict>') >= 0 or l.find('</dict>') >= 0:
                    isText = 0
                if l.find('<string>string</string>') > 0 and isText == 0:
                    isText = 1
                if l.find('<string>Text</string>') > 0 and isText == 1:
                    isText = 2
                if l.find('<key>value</key>') > 0 and isText == 2:
                    isText = 3
            isTranslate = True
            if isText != 3:
                isTranslate = False
            i = 0
            isfind = False
            if len(strOriginArray) > 1 and isTranslate:

                for i0 in range(len(strOriginArray)):
                    str = strOriginArray[i0]
                    if (newText.find('ccbList_1089')>= 0):
                        print('l:',l)
                    if l.find(str) >= 0 and str.strip() != '<':
                        isfind = True
                        if i0 == 0:
                            w.write(l.replace(str + '\n', newText))

                        elif str.find('<') < 0:
                            '''不是最后一段匹配'''
                            w.write(l.replace(str + '\n', ''))
                        elif str.strip() != '<':
                            '''规避只有< 的替换'''
                            w.write(l.replace(str, ''))
                        elif str.strip() == '<':
                            '''规避只有< 的替换'''
                            w.write(l.replace(str, ''))
                    elif l.find(str) >= 0 and str.strip() == '<' and lastLineTrue:
                        isfind = True
                        lastLineTrue = False
                        isLastLine = True
                        w.write(l.replace(str, ''))

            if not isfind:
                lastLineTrue = False
                w.write(l.replace(originText,newText))
            elif not isLastLine:
                lastLineTrue = True

def inputTempList(listroot,list1,temp):
    for i in list1:
        item = {}
        item['type'] = temp
        item['index'] = i
        listroot.append(item)
    return listroot
def sortTempList(a):
    return a['index']

def replaceText(item,_isBackup):
    fileArr = item[1].split(";")
    for file in fileArr:
        if file.endswith(".ccb"):
            if _isBackup:
                path = backUpDir + file
            else:
                path = ccb_path + '/' + file

            if not os.path.exists(path):
                continue
            # if (item[2] == '' or item[2] == None) and not _isBackup:
            #     continue
            # print("item[0] items :", item[0].items())
            # itemString = "ccbList[" + item[0][0] + ']'
            itemString = "ccbList_" + item[0][0].split('.')[0]
            if _isBackup:
                for _originidx, _originTxt in item[0].items():

                    if (_originidx == 0 or _originTxt == '' or _originTxt == None):
                        continue
                    print('doTranslate_makeID:','>'+_originTxt+'<',';','>'+itemString+'<', path)
                    if _isBackup:
                        # print("item[0].get(_originidx):",item[0].get(_originidx))

                        replaceOneFile('>'+item[0].get(_originidx)+'<', '>'+itemString+'<', path)
            else:
                print("doTranslate: ",itemString," item[0].get(translateIdx):",item[0])
                if item[0].get(translateIdx) != '':
                    replaceOneFile('>'+itemString+'<','>'+item[0].get(translateIdx)+'<',  path)
                else:
                    replaceOneFile('>'+itemString+'<','>'+itemString+'<',  path)
                    _item = item[0]
                    notTranslateItem = {}
                    notTranslateItem[0] = _item[0]
                    notTranslateItem[1] = _item[1]
                    notTranslateItem[2] = _item[3]
                    notTranslatList[_item[0]] = notTranslateItem

                        # if _originidx == originIdx and item[0].get(originIdx) != '' and item[0].get(originIdx) != None:
                        #     replaceOneFile('>'+item[0].get(_originidx)+'<', '>'+item[2]+'<', path)
                        # elif (item[0].get(originIdx) == '' or item[0].get(originIdx) == None) and _originidx != originIdx:
                        #     replaceOneFile('>'+item[0].get(_originidx)+'<', '>'+item[2]+'<', path)

        elif file.endswith(".json"):
            path = search(json_path, file)
            if not path:
                continue
            originText = item[0].get(originIdx)
            if originText == '' or originText == None:
                continue

            if len(originText) >= 2:
                print('------originText:',originText)
                print('------item[2]:',item[2])
                replaceOneFile('\''+originText+'\'', '\''+item[2]+'\'', path)
            else:
                replaceOneFile('\"'+originText+'\"', '\"'+item[2]+'\"', path)

def sqlReplace():
    '''获取数据库连接'''
    conn=pymysql.connect(host='localhost',user='root',password='',db='russionFont',port=3306,charset='utf8')
    '''获取一个游标'''
    cur=conn.cursor()
    '''limit 10 #where isSpecial=0'''
    cur.execute('select * from english_0506 order by LENGTH(originText) DESC ')
    data=cur.fetchall()
    '''遍历输出'''
    arr = []
    for d in data:
        fields = (str(d[1]), str(d[originIdx]), str(d[translateIdx]))
        arr.append(fields)
    '''释放游标'''
    cur.close()

    for item in arr:
        print('item[0]:' + item[0] + ',item[1]:' + item[1] + ',item[2]:' + item[2] )
        if item[0] == '' or item[0] == None:
            continue
        else:
            replaceText(item,False)
    '''释放资源'''
    conn.close()

def excelReplace(filepth,indexMap,_isBackup):
    table_translate = xlrd.open_workbook(filepth)
    sheet_translate = table_translate.sheet_by_index(indexMap[3])
    nrows_translate = sheet_translate.nrows
    ncols_translate = sheet_translate.ncols
    dataArray = []
    for j in range(nrows_translate):
        print(sheet_translate.row(j))
        if j <= 3:
            continue
        translate = sheet_translate.row_values(j, 0, ncols_translate)
        print("excelReplace:",str(translate[translateIdx]))
        # if str(translate[translateIdx]) == '' and not _isBackup:
        #     continue

        arrayitem = []
        originParams = {}
        '''0.中文 2.英文 3.俄文'''
        for item in idx_language:
            index = idx_language[item]
            originParams[index] = str(translate[index])
        print("originParams:",originParams)
        # originParams[0] = str(translate[0])
        # originParams[2] = str(translate[2])
        # originParams[3] = str(translate[3])

        arrayitem.append(originParams)
        arrayitem.append(str(translate[indexMap[1]]))
        arrayitem.append(str(translate[translateIdx]))
        dataArray.append(arrayitem)
    # print("dataArray:",dataArray)
    for item in dataArray:
        if item[1] != '':
            replaceText(item,_isBackup)

def resetProgectTag(isReplace):
    global frontLanguage

    fileName = 'makeTranslate.js'
    path = search('/Users/lan/clientprojects/pikachu_english/app/static/', fileName)

    if not path:
        return
    with open(path,'r',32,'utf-8') as r:
        lines=r.readlines()
    frontLanguage = ''
    for line in lines:
        if line.find('window.languageTs = ') >= 0:
            frontLanguage = line.split('\'')[1]
    global originIdx
    originIdx = idx_language.get(frontLanguage)
    if isReplace:
        print("originIdx:",originIdx,frontLanguage)
        replaceOneFile('window.languageTs = \''+translateTxt[originIdx]+'\'', 'window.languageTs = \''+translateTxt[translateIdx]+'\'', path)

def copyfile(srcfile,dstfile):
    if not os.path.isfile(srcfile):
        print("%s not exist!"%(srcfile))
    else:
        fpath,fname=os.path.split(dstfile)
        if not os.path.exists(fpath):
            '''创建路径'''
            os.makedirs(fpath)
        '''复制文件'''
        shutil.copyfile(srcfile,dstfile)
        print("copy %s -> %s"%( srcfile,dstfile))

def copyDir(srcDir, destDir, fileTypeList, isSingleDir,_isBackup=False):
    if isSingleDir:
        '''如果是全文件拷贝 比如json'''
        for root, dirs, files in os.walk(srcDir):
            for OneFileName in files:
                fileType = OneFileName.split('.')[-1:][0]
                if fileType in fileTypeList:
                    if isSingleDir:
                        src1 = os.path.join(root,OneFileName)
                        src2 = os.path.join(destDir,OneFileName)
                        copyfile(src1,src2)
                        if 'fnt' in fileTypeList:
                            fileName = OneFileName.split('.')[:-1][0]
                            src1 = os.path.join(root,fileName+'.png')
                            src2 = os.path.join(destDir,fileName+'.png')
                            if (_isBackup):
                                if not os.path.exists(src2):
                                    continue
                            copyfile(src1,src2)

    else:
        '''如果是散布文件拷贝 比如 png／jpg 等'''
        for root, dirs, files in os.walk(destDir):
            for OneFileName in files:
                fileType = OneFileName.split('.')[-1:][0]
                if fileType in fileTypeList:
                    for root2, dirs2, files2 in os.walk(srcDir):
                        isFindFile = False
                        for OneFileName2 in files2:
                            if OneFileName == OneFileName2:
                                src1 = os.path.join(root2,OneFileName2)
                                src2 = os.path.join(root,OneFileName)
                                copyfile(src1,src2)
                                isFindFile = True
                                break
                        if isFindFile:
                            break

def makeNotTranslateExl():

    dateStr = datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S')#现在

    filePth = notTranslateExlPth + dateStr+'.xls'

    # table = table_translate.sheet_by_index(0)
    # nrows = table.nrows                         # 获取table工作表总行数
    # ncols = table.ncols                         # 获取table工作表总列数
    # print('rows:',nrows)
    workbook = xlwt.Workbook()  #创建一个excel文件
    newSheet = workbook.add_sheet('sheet0',cell_overwrite_ok=True)

    isFindRestString = False
    i = 0
    for id, rowInfo in notTranslatList.items():
        for j in range(3):
            newSheet.write(i, j, rowInfo[j])
        i = i + 1

    workbook.save(filePth)
def resetProjectServer():
    fileName = 'debug.js'
    path = search('/Users/lan/clientprojects/pikachu_english/app/static/', fileName)

    if not path:
        return

    replaceOneFile('window.URL_HTTP_LOGIN = \''+serverLink[originIdx]+'\'', 'window.URL_HTTP_LOGIN = \''+serverLink[translateIdx]+'\'', path)


def doCCBTranslate(_isBackup = False):
    if (_isBackup):
        print("copyDir(ccb_path, backUpDir, ['ccb'],True)")
        copyDir(ccb_path, backUpDir, ['ccb'],True, _isBackup)
    else:
        print("copyDir(backUpDir, ccb_path, ['ccb'],True)")
        copyDir(backUpDir, ccb_path, ['ccb'],True,_isBackup)


    if (_isBackup or (not isUseIDCCB and not _isBackup)):
        _fileCount = len(useIdx)
        for _idx in range(_fileCount):
            file = excelFiles[_idx]
            excelReplace(file,useIdx[_idx], _isBackup)

    if (_isBackup):
        doCCBTranslate(False)
        makeNotTranslateExl()

try:
    '''从程序里 获取当前语言版本 参数表示是否切换版本'''
    resetProgectTag(not isOnlyTranslateCCB)
    print('程序语言标志替换完毕',translateIdx)
    resetProjectServer()

    global notTranslatList
    notTranslatList = {}

    if isNewTranslate:
        doCCBTranslate(False)
        makeNotTranslateExl()
    else:
        doCCBTranslate(True)

    '''生成ccbi'''
    _localPth='/'.join(os.path.realpath(__file__).split('/')[:-1])
    '''程序根目录 应该都是pikachu_english吧 如果不是 自己改'''
    programPth = ccb_path.split('pikachu_english/')[0] + 'pikachu_english/'

    # os.system('sh ' + programPth + 'tools/pikachuCCB/bin/openBin/copy_ccb.sh')
    print('ccb替换完毕')

    if not isOnlyTranslateCCB:

        print('替换版本对应测试服完毕')

        coffeeJsonDir = coffeeTranslateJson[originIdx]
        coffeeJsonDirPth = '/Users/lan/Downloads/Language/' + coffeeJsonDir + '/copyTranslateJson.sh'
        os.system('sh ' + coffeeJsonDirPth)
        print('翻译数据替换完毕')

        copyDir(svnPth + jsonDataPthList[translateIdx], programPth + 'app/static/res/data', ['json'], True)
        print('数据替换完毕')

        resPthlist = resDataPthList[translateIdx]
        for pth in resPthlist:
            copyDir(svnPth + pth, programPth, ['png','jpg'], False)
        print('图片替换完毕')

        '''对应svn上艺术字资源路径'''
        fontResSvnPth = svnPth + 'aiweiyou_pokmon/pika_foreign/Font/' + LanguageTemp[translateIdx]
        fontPth = fontResSvnPth + '/Font/'
        pngPth = fontResSvnPth + '/Out/'

        '''切换艺术字之前 需要备份到svn目录上'''
        copy_FontResSvnPth = svnPth + 'aiweiyou_pokmon/pika_foreign/Font/' + LanguageTemp[originIdx]
        copy_fontPth = copy_FontResSvnPth + '/Font/'
        copy_pngPth = copy_FontResSvnPth + '/Out/'

        copyDir(programPth + 'tools/pikachuFontAndPlist/Font', copy_fontPth, ['GlyphProject'], True)
        copyDir(programPth + 'tools/pikachuFontAndPlist/Out', copy_pngPth, ['fnt'], True)
        print('艺术字文件备份完毕')

        copyDir(fontPth, programPth + 'tools/pikachuFontAndPlist/Font', ['GlyphProject'], True)
        copyDir(pngPth, programPth + 'tools/pikachuFontAndPlist/Out', ['fnt'], True)
        copyDir(pngPth, programPth + 'app/static/res/ui', ['fnt'], True)
        print('艺术字文件更改完毕')

        '''执行脚本文件 plist fnt'''
        binPth = programPth + 'tools/pikachuFontAndPlist/bin'
        for root, dirs, files in os.walk(binPth):
            for OneFileName in files:
                if OneFileName.find('.sh') > 0:
                    ptn = os.path.join(binPth,OneFileName)
                    os.system('sh ' + ptn)

except Exception as e:
    print("异常"+e)