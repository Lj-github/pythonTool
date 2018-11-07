__author__ = 'lan'
"""
3.需要替换完成后删除相应项目，或者添加已处理标记
俄文版替换错误例子：_DigGemRsps = ["DigBaoshiRsp", "DigHighBaoshiRsp", "DigTopLevelBaoshiRsp"] 替换了Dig

LayerSelectHero.coffee Grass
ChessStep.coffee Grass

"""
'''替换翻译 改成程序读json'''

import pymysql
from collections import OrderedDict
import os
import fileinput
import re
import xlrd

coffee_path = '/Users/lan/clientprojects/pikachu_english/app/static/coffee'

excelFiles=[
    '/Users/lan/Downloads/历次翻译整理/整理汇总翻译/coffeeReplace.xls'
]

'''Id filepth char originTxt(4.中文 3。英文 5。俄文)'''
'''originTxt 当前程序语言'''
useIdx=[
    [0,1,2,4,0]
]

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
    with open(path,'w') as w:
        for l in lines:
            if newText == 'text':
                newText = ''
            w.write(l.replace(originText,newText))

def replaceText(item):
    fileArr = item[1].split(";")

    for file in fileArr:
        print(file)
        if file.endswith(".ccb"):
            continue
        else:
            path = search(coffee_path, file)
            if not path:
                print('file not exist :' + file)
                continue
            originText = item[3]
            if originText == '' or originText == None:
                continue
            print('1.'+originText)
            print('2.'+originText)
            trans = 'coffeeTranslate['+str(item[0])+'][window.languageTs]'

            print('2.'+trans)
            if originText.find('\'') >= 0 :
                originText.replace('\'','\\\'')
            if originText.find('\"') >= 0 :
                originText.replace('\"','\\\"')


            replaceOneFile('\''+originText+'\'', trans, path)
            replaceOneFile('\"'+originText+'\"', trans, path)

def sqlReplace():
    '''获取数据库连接'''
    conn=pymysql.connect(host='localhost',user='root',password='',db='russionFont',port=3306,charset='utf8')
    '''获取一个游标'''
    cur=conn.cursor()
    '''limit 10 where isSpecial=0'''
    cur.execute('select * from english_0506 order by LENGTH(originText) DESC ')
    data=cur.fetchall()
    '''遍历输出'''
    arr = []
    for d in data:
        fields = (str(d[1]), str(d[2]), str(d[3]))
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
    sheet_translate = table_translate.sheet_by_index(indexMap[4] or 0)
    nrows_translate = sheet_translate.nrows
    ncols_translate = sheet_translate.ncols
    dataArray = []
    for j in range(nrows_translate):
        if j <= 3:
            continue
        translate = sheet_translate.row_values(j, 0, ncols_translate)
        print('translate:',translate)
        arrayitem = []
        arrayitem.append(str(int(translate[indexMap[0]])))
        arrayitem.append(str(translate[indexMap[1]]))
        arrayitem.append(str(translate[indexMap[2]]))
        arrayitem.append(str(translate[indexMap[3]]))
        dataArray.append(arrayitem)
    for item in dataArray:

        if item[1] != '':
            print('item[0]:' + item[0] + ',item[1]:' + item[1] + ',item[2]:' + item[2] + ',item[3]:' + item[3])
            replaceText(item)

try:
    _fileCount = len(useIdx)
    print('_fileCount:',_fileCount)
    for _idx in range(_fileCount):
        print('_idx:',_idx)
        file = excelFiles[_idx]
        print('file:',file)
        print(file,useIdx[_idx])
        excelReplace(file,useIdx[_idx])


except Exception as e:
    print("异常"+e)