#-*- coding: UTF-8 -*-
__author__ = 'lan'

"""
从数据库中读取前端翻译，并做前端代码和ccb的替换
3.需要替换完成后删除相应项目，或者添加已处理标记
俄文版替换错误例子：_DigGemRsps = ["DigBaoshiRsp", "DigHighBaoshiRsp", "DigTopLevelBaoshiRsp"] 替换了Dig
LayerSelectHero.coffee Grass
ChessStep.coffee Grass
"""

#import pymysql
from collections import OrderedDict
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import os
import shutil
import re
import xlrd

"警告⚠️ "
#项目路径
ROOTPATH = "/Users/admin/Documents/ljworkspace/local/cocos/project/pikachu_englishGit/"
#工具路径
TOOLSPATH = "/Users/admin/Documents/ljworkspace/local/cocos/test/foreignTools/lan/"


coffee_path = ROOTPATH + 'pikachu_english/app/static/coffee'
json_path = ROOTPATH + 'pikachu_english/app/static/res'
ccb_path = ROOTPATH + 'pikachu_english/tools/pikachuCCB/ccb'

svnPath = "/Users/admin/Documents/ljworkspace/local/cocos/assets/pikachu/sanguo/"

excelFiles=[
    #'/Users/lan/Downloads/历次翻译整理/整理汇总翻译/CCBReplaceEnglish_最终.xls'
    '/Users/admin/Documents/ljworkspace/local/cocos/assets/pikachu/sanguo/aiweiyou_pokmon/pika_foreign/CCBReplaceEnglish_6.xls'
]

'''origin pth translate sheetIdx'''
'''0中文 2英文 3俄文 4 越南'''
useIdx=[
    [0,1,2,3,4]
]

'''0.中文 2.英文 3.俄文 '''
'''当前外文版本'''
originIdx =  2 #0
'''将要替换到外文版本'''
translateIdx = 4 #  2

isOnlyTranslateCCB = False

"警告⚠️ 程序内的艺术字备份会把备份路径内的东西覆盖，请确认程序语言类型 originIdx，一定要正确！"
isNeedBeifen = True

translateTxt = ['chinese','chinese','english','russion',"vietnamese"]

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
            replaceOneFile('>' + item[0] + '<', '>' + item[2] + '<', path)
            #可能之前的语言
           # for index in range(len(item)):
            #    if index >= 2:
            #        if  replaceOneFile('>'+item[0]+'<', '>'+item[index]+'<', path):
            #            break

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

# def sqlReplace():
#     '''获取数据库连接'''
#     conn=pymysql.connect(host='localhost',user='root',password='',db='russionFont',port=3306,charset='utf8')
#     '''获取一个游标'''
#     cur=conn.cursor()
#     '''limit 10 #where isSpecial=0'''
#     cur.execute('select * from english_0506 order by LENGTH(originText) DESC ')
#     data=cur.fetchall()
#     '''遍历输出'''
#     arr = []
#     for d in data:
#         fields = (str(d[1]), str(d[originIdx]), str(d[translateIdx]))
#         arr.append(fields)
#     '''释放游标'''
#     cur.close()
#
#     for item in arr:
#         print('item[0]:' + item[0] + ',item[1]:' + item[1] + ',item[2]:' + item[2] )
#         if item[0] == '' or item[0] == None:
#             continue
#         else:
#             replaceText(item)
#     '''释放资源'''
#     conn.close()




def excelReplace(filepth,indexMap):
    table_translate = xlrd.open_workbook(filepth)
    sheet_translate = table_translate.sheet_by_index(indexMap[0])

    nrows_translate = sheet_translate.nrows
    ncols_translate = sheet_translate.ncols
    dataArray = []
    for j in range(nrows_translate):
        if j <= 3:
            continue
        translate = sheet_translate.row_values(j, 0, ncols_translate)
        arrayitem = []
        # index = 0 时 为当前语言 1 为当前ccb   2 为目标语言 剩下的是其他语言
        newndexMapI= indexMap

        instr = str(translate[newndexMapI[originIdx]])
        arrayitem.append(instr)
        if instr.__len__() == 0 :#基础语言为空 没的替换 直接跳过
            continue

        arrayitem.append(str(translate[newndexMapI[1]])) #ccb
        #判断是否存在  不存在则用原来的 不需要替换
        newStr = str(translate[newndexMapI[translateIdx]])
        if newStr.__len__() != 0 :
            # newStr = str(translate[newndexMapI[originIdx]])
            # print "cannot find word translate " + newStr + " to " + str(translateIdx)
            arrayitem.append(newStr)
            dataArray.append(arrayitem)

        #arrayitem.append(newStr)
        #
        # for ind  in newndexMapI :
        #     if ind != originIdx and ind != translateIdx and ind !=1 :
        #         arrayitem.append(str(translate[newndexMapI[ind]]))

    for item in dataArray:
        if item[1] != '':
            replaceText(item)

def resetProgectTag():
    fileName = 'makeTranslate.js'
    path = search(ROOTPATH+ 'pikachu_english/app/static/', fileName)

    if not path:
        return

    replaceOneFile('window.languageTs = \''+translateTxt[originIdx]+'\'', 'window.languageTs = \''+translateTxt[translateIdx]+'\'', path)



if __name__ == '__main__':

    '''执行脚本文件 plist fnt'''
    binPth = ROOTPATH + 'pikachu_english/tools/pikachuFontAndPlist/bin'
    for root, dirs, files in os.walk(binPth):
        for OneFileName in files:
            if OneFileName.find('.sh') > 0:
                os.system('sh ' + os.path.join(root, OneFileName))
                print("run "  + OneFileName)
    print('脚本文件执行完毕')
