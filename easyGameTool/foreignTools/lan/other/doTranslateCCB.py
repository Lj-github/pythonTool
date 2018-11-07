__author__ = 'lan'
"""
从数据库中读取前端翻译，并做前端代码和ccb的替换

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

coffee_path = '/Users/lan/clientprojects/pikachu_english/app/static/coffee'
json_path = '/Users/lan/clientprojects/pikachu_english/app/static/res'
ccb_path = '/Users/lan/clientprojects/pikachu_english/tools/pikachuCCB/ccb'

excelFiles=[
    '/Users/lan/Downloads/历次翻译整理/整理汇总翻译/CCBReplaceEnglish_最终.xls'
]

'''origin pth translate sheetIdx'''
'''0中文 2英文 3俄文'''
useIdx=[
    [0,1,2,0]
]

'''0.中文 2.英文 3.俄文'''
'''当前外文版本'''
originIdx = 0
'''将要替换到外文版本'''
translateIdx = 2

isOnlyTranslateCCB = True

"警告⚠️ 程序内的艺术字备份会把备份路径内的东西覆盖，请确认程序语言类型 originIdx，一定要正确！"
isNeedBeifen = True

translateTxt = ['chinese','chinese','english','russion']

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

            replaceOneFile('>'+item[0]+'<', '>'+item[2]+'<', path)
        elif file.endswith(".json"):
            path = search(json_path, file)
            if not path:
                continue
            originText = item[0]
            if originText == '' or originText == None:
                continue

            if len(originText) >= 2:
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
        arrayitem = []
        arrayitem.append(str(translate[indexMap[originIdx]]))
        arrayitem.append(str(translate[indexMap[1]]))
        arrayitem.append(str(translate[indexMap[translateIdx]]))
        dataArray.append(arrayitem)
    for item in dataArray:
        if item[1] != '':
            replaceText(item)

def resetProgectTag():
    fileName = 'makeTranslate.js'
    path = search('/Users/lan/clientprojects/pikachu_english/app/static/', fileName)

    if not path:
        return

    replaceOneFile('window.languageTs = \''+translateTxt[originIdx]+'\'', 'window.languageTs = \''+translateTxt[translateIdx]+'\'', path)

try:
    _fileCount = len(useIdx)
    for _idx in range(_fileCount):
        file = excelFiles[_idx]
        excelReplace(file,useIdx[_idx])
    '''生成ccbi'''
    os.system('sh /Users/lan/clientprojects/pikachu_english/tools/pikachuCCB/bin/openBin/copy_ccb.sh')
    print('ccb替换完毕')

    if not isOnlyTranslateCCB:
        resetProgectTag()
        print('程序语言标志替换完毕',translateIdx)

        if translateIdx == 2:
            os.system('sh /Users/lan/resBin/english/DataCopyPK_yuenan.sh')
            os.system('sh /Users/lan/resBin/english/updateAllSrc_english.sh')
        elif translateIdx == 3:
            os.system('sh /Users/lan/resBin/english/DataCopyPKen_Russion.sh')
            os.system('sh /Users/lan/resBin/english/updateAllSrc_yuenan.sh')
        elif translateIdx == 0:
            '''这里应该不会回退到中文版本，只是在前期测试使用'''
            os.system('sh /Users/lan/resBin/english/DataCopyPK_Chinese.sh')
            os.system('sh /Users/lan/resBin/english/updateAllSrc_chinese.sh')
        print('图片资源 数据替换完毕')

        '''备份程序使用中的字体文件'''
        desPth = '/Users/lan/clientprojects/pikachu_english/tools/pikachuFontAndPlist/Font'
        filePth1 = '/Users/lan/resBin/english/'
        fontPth = 'Font_english/'
        outPth = 'Out_english/'
        if originIdx == 3:
            fontPth = 'Font_russion/'
            outPth = 'Out_russion/'
        elif originIdx == 0:
            fontPth = 'Font_chinese/'
            outPth = 'Out_chinese/'
        pthSrc1 = filePth1 + fontPth
        '''先删除原文件夹才能拷贝'''
        if os.path.exists(pthSrc1):
            shutil.rmtree(pthSrc1)
        if isNeedBeifen:
            '''备份工具文件'''
            shutil.copytree(desPth, pthSrc1)
            filepth = '/Users/lan/clientprojects/pikachu_english/tools/pikachuFontAndPlist/Out/'
            '''备份 文件fnt png'''
            print(filepth + ' To ' + filePth1 + outPth)
            for filename in os.listdir(filepth):
                if filename.endswith(".fnt"):
                    path = filepth + filename
                    if not os.path.exists(path):
                        shutil.copyfile(path,filePth1 + outPth + filename)
                        fileRealNameArray = filename.split('.')
                        fileRealName = fileRealNameArray[0] + '.png'
                        shutil.copyfile(filepth + fileRealName,filePth1 + outPth + fileRealName)
        '''目的文件'''
        filepth2 = '/Users/lan/resBin/english/'
        fontPth2 = 'Font_english/'
        outPth2 = 'Out_english/'
        if translateIdx == 3:
            fontPth2 = 'Font_russion/'
            outPth2 = 'Out_russion/'
        elif translateIdx == 0:
            fontPth2 = 'Font_chinese/'
            outPth2 = 'Out_chinese/'
        pthSrc2 = filepth2+fontPth2

        if os.path.exists(desPth):
            shutil.rmtree(desPth)

        shutil.copytree(pthSrc2, desPth)
        pthOut = filepth2 + outPth2
        print(pthOut + ' To ' + filepth)
        for filename in os.listdir(pthOut):
            if filename.endswith(".fnt"):
                path = pthOut + filename
                shutil.copyfile(path,filepth + filename)
                fileRealNameArray = filename.split('.')
                fileRealName = fileRealNameArray[0] + '.png'
                if os.path.exists(pthOut + fileRealName):
                    shutil.copyfile(pthOut + fileRealName,filepth + fileRealName)
                print(filename,' ; ',fileRealName)

        os.system('sh /Users/lan/resBin/english/make_all_plist_en.sh')
        print('font资源替换完毕')

except Exception as e:
    print("异常"+e)