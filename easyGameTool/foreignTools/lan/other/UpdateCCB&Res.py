__author__ = 'lan'
"""
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

"警告⚠️ "

svnPth = '/Users/lan/sanguo/'
json_path = '/Users/lan/clientprojects/pikachu_english/app/static/res'
ccb_path = '/Users/lan/clientprojects/pikachu_english/tools/pikachuCCB/ccb'

'''ccb翻译收集文件'''
excelFiles=[
    '/Users/lan/sanguo/aiweiyou_pokmon/pika_foreign/CCBReplaceEnglish_6.xls'
]

'''origin pth translate sheetIdx'''
'''0中文 2英文 3俄文 4.越南 5.法语'''
useIdx=[
    [3,1,2,0]
]

'''0.中文 2.英文 3.俄文 4.越南 5法语'''
'''当前外文版本'''
originIdx = 3
'''将要替换到外文版本'''
translateIdx = 2

LanguageTemp = ['Chinese','','English','Russion','Vietnam']
translateTxt = ['chinese','chinese','english','russion','vietnamese']
idx_language = {
    'chinese':0,
    'english':2,
    'russion':3,
    'vietnamese':4,
}
svnPth = '/Users/lan/sanguo/'
jsonDataPthList = [
    'aiweiyou_pokmon/tools/exceltojson/json',
    '',
    'aiweiyou_pokmon/EnglishResources/tools/exceltojson/json',
    'aiweiyou_pokmon/RussionResources/tools/exceltojson/json',
    'aiweiyou_pokmon/VietnamResources/tools/exceltojson/json'
]

resDataPthList = [
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

isOnlyTranslateCCB = False

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

def replaceOneFile(originText, newText, path):
    if not path:
        return
    with open(path,'r') as r:
        lines=r.readlines()
    strOriginArray = originText.split('\n')
    print('path:',path)
    print('strOrigin:',strOriginArray)
    lastLineTrue = False
    isLastLine = False

    with open(path,'w') as w:
        for l in lines:
            i = 0
            isfind = False

            if len(strOriginArray) > 1:
                for i0 in range(len(strOriginArray)):
                    str = strOriginArray[i0]
                    if not str or str == None or  str == '':
                        continue
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
                        print('str:',str)
                        w.write(l.replace(str, ''))

            if not isfind:
                lastLineTrue = False
                w.write(l.replace(originText,newText))
            elif not isLastLine:
                lastLineTrue = True


def replaceText(item):
    fileArr = item[1].split(";")

    for file in fileArr:
        print(file)
        if file.endswith(".ccb"):
            path = ccb_path + '/' + file
            if not os.path.exists(path):
                continue
            if item[2] == '' or item[2] == None:
                continue

            for _originidx, _originTxt in item[0].items():
                if _originidx != useIdx[0][2]:
                    '''循环遍历各种语言 非被替换的文字所在列'''
                    if _originTxt.strip() == '':
                        continue
                    replaceOneFile('>'+_originTxt+'<', '>'+item[2]+'<', path)

        elif file.endswith(".json"):
            path = search(json_path, file)
            if not path:
                continue
            originText = item[0].get(useIdx[0][0])
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
            replaceText(item)
    '''释放资源'''
    conn.close()

def excelReplace(filepth,indexMap):
    table_translate = xlrd.open_workbook(filepth)
    sheet_translate = table_translate.sheet_by_index(indexMap[3])
    nrows_translate = sheet_translate.nrows
    ncols_translate = sheet_translate.ncols
    dataArray = []
    for j in range(nrows_translate):
        if j <= 3:
            continue
        translate = sheet_translate.row_values(j, 0, ncols_translate)
        if str(translate[translateIdx]) == '':
            continue

        arrayitem = []
        originParams = {}
        '''0.中文 2.英文 3.俄文'''
        originParams[0] = str(translate[0])
        originParams[2] = str(translate[2])
        originParams[3] = str(translate[3])
        originParams[4] = str(translate[4])
        originParams[5] = str(translate[5])

        arrayitem.append(originParams)
        '''路径'''
        arrayitem.append(str(translate[indexMap[1]]))
        '''目的翻译'''
        arrayitem.append(str(translate[translateIdx]))
        dataArray.append(arrayitem)

    for item in dataArray:
        if item[1] != '':
            replaceText(item)

def resetProgectTag(isReplace):
    global frontLanguage

    fileName = 'makeTranslate.js'
    path = search('/Users/lan/clientprojects/pikachu_english/app/static/', fileName)

    if not path:
        return
    with open(path,'r') as r:
        lines=r.readlines()
    for line in lines:
        if line.find('window.languageTs = ') >= 0:
            frontLanguage = line.split('\'')[1]
    global originIdx
    originIdx = idx_language.get(frontLanguage)
    if isReplace:
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

def copyDir(srcDir, destDir, fileTypeList, isSingleDir):
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

try:

    """
    a = True
    if a:
        copy_FontResSvnPth = svnPth + 'aiweiyou_pokmon/pika_foreign/Font/' + LanguageTemp[3]
        copy_fontPth = copy_FontResSvnPth + '/Font/'
        copy_pngPth = copy_FontResSvnPth + '/Out/'

        '''生成ccbi'''
        _localPth='/'.join(os.path.realpath(__file__).split('/')[:-1])
        '''程序根目录 应该都是pikachu_english吧 如果不是 自己改'''
        programPth = _localPth.split('pikachu_english/')[0] + 'pikachu_russion/'
        copyDir(programPth + 'tools/pikachuFontAndPlist/Font', copy_fontPth, ['GlyphProject'], True)
        copyDir(programPth + 'tools/pikachuFontAndPlist/Out', copy_pngPth, ['fnt'], True)
        print('艺术字文件备份完毕')
    """


    '''从程序里 获取当前语言版本 参数表示是否切换版本'''
    if not isOnlyTranslateCCB:
        resetProgectTag(not isOnlyTranslateCCB)
        print('程序语言标志替换完毕',translateIdx)

    _fileCount = len(useIdx)
    for _idx in range(_fileCount):
        file = excelFiles[_idx]
        excelReplace(file,useIdx[_idx])

    '''生成ccbi'''
    _localPth='/'.join(os.path.realpath(__file__).split('/')[:-1])
    '''程序根目录 应该都是pikachu_english吧 如果不是 自己改'''
    programPth = _localPth.split('pikachu_english/')[0] + 'pikachu_english/'

    os.system('sh ' + programPth + 'tools/pikachuCCB/bin/openBin/copy_ccb.sh')
    print('ccb替换完毕')

    if not isOnlyTranslateCCB:
        copyDir(svnPth + jsonDataPthList[translateIdx], programPth + 'app/static/res/data', ['json'], True)
        print('数据替换完毕')

        resPthlist = resDataPthList[translateIdx]
        for pth in resPthlist:
            print('------resPth:',svnPth + pth)
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
                    os.system('sh ' + os.path.join(root,OneFileName))
        print('脚本文件执行完毕')

except Exception as e:
    print("异常"+e)