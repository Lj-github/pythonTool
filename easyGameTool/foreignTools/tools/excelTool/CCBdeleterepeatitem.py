# -*- coding: utf-8 -*-
# @Time    : 18/4/20 下午2:26
# @Author  : myTool
# @File    : CCBdeleterepeatitem.py
# @Software: PyCharm

##去除ccb 里面的 重复数据  将ccb文件字符串 放在一块

import os
import xlrd
from xlwt import Workbook
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
rootPath = os.path.dirname(os.path.realpath(__file__))

import  ExcelTools as et


ccbexcelpath ="/Users/admin/Documents/ljworkspace/local/cocos/assets/pikachu/sanguo/aiweiyou_pokmon/pika_foreign/CCBReplaceEnglish_3.xls"


def if_ChineseEqual_add_csbFile_to_ccbCol(list):
    if not list : return
    news_List = []
    for item in list:
        isHas = False
        for added in news_List:
            if item[0] == added[0]:
                isHas = True
                csbList = added[1].split(";")
                itemccbList = item[1].split(";")
                for id in itemccbList:
                    if not( id  in csbList):
                        csbList.append(id)
                #sbList.append(item[1])
                added[1] = ";".join(csbList)
                print("add ccbfile from item " + item[0] + item[1])

        if not isHas:
            news_List.append(item)

    return news_List

## 通过文件名字 获取到文件的绝对路径


def getFileFullNameByLastName(allList, name):

    for fil in allList:
        fpath, fname = os.path.split(fil)
        if fname == name:
            return fil
    return ""

def getLineByStr_File(Str,path):
    if not Str or not path:return
    with open(path, 'r') as r:
        lines = r.readlines()
    print('path:', path)
    print('Str:', Str)
    lineNum = -1

    #with open(path, 'w') as w:
    for l in range(0,lines.__len__()):
        lstr = lines[l]
        if lstr.find(Str) >= 0:
            lineNum = l
            break
    print(lineNum == -1 and "can not find str " + Str +"from " + path or "find str => " + Str + " from " + path + " line : " + str(int(lineNum) ) )
    return int(lineNum)

def getStrByLine_file(line,path):
    if not line or not path:return
    with open(path, 'r') as r:
        lines = r.readlines()
    print('path:', path)
    print('line:', line)

    if lines.__len__()>= line:
        return lines[line]
    return ""

if __name__ == '__main__':
    #ccbList = et.excelToList(ccbexcelpath)
    coffeebexcelpath = "/Users/admin/Documents/ljworkspace/local/cocos/assets/pikachu/sanguo/aiweiyou_pokmon/pika_foreign/coffeeReplace_5.xls"
    ccbList = et.excelToList(coffeebexcelpath)
    l = 0
    needChangeList = []
    #到底有多少要改
    for idx in ccbList:
        if idx[5] == "":
            l = l +1
            cofLis = idx[1].split(";")
            idx[1] = cofLis[0]
            needChangeList.append(idx)
            print("有 " + str(l) +"  需要改" )
            print("中文为 " + str(idx[4]) + "  需要改")
    #去英文中找位置

    #获取中文所有文件
    cp = "/Users/admin/Documents/ljworkspace/local/cocos/project/pikachu_english/app/static/coffee/"
    allChineseFileList = et.GetFileList(cp,[])

    ccp = "/Users/admin/Documents/ljworkspace/local/cocos/project/pikachu_russion/app/static/coffee/"
    allRussionFileList = et.GetFileList(ccp,[])

    #从中文文件中查找字符串  coffeeTranslate[id].language  返回所在行数  再去俄文版的行数里面   拿出字符串  字符串前面加一个 a  后面 加一个a  直
    #直接对字符串进行split（'"'） 拿到中间的 就 应该是  所匹配的俄文版字符！！！！！
    #needChangeList
    for needIdx in needChangeList:
        fileName = needIdx[1]
        absoluteFileName = getFileFullNameByLastName(allChineseFileList,fileName)
        neStr =  "coffeeTranslate[" + str(int(needIdx[0]) ) + "][window.languageTs]"
        lineNum = getLineByStr_File(neStr,absoluteFileName)
        if lineNum:
            absoluteRussionFilePath = getFileFullNameByLastName(allRussionFileList,fileName)
            rstr = getStrByLine_file(lineNum,absoluteRussionFilePath)
            if rstr != "":
                rstr = "a" + rstr + "a"
                rstrList = rstr.split('"')
                if rstrList.__len__() == 3 :
                    print("can success get str "  + rstrList[0])
                    print("russion str " + rstrList[1] )
                else:

                    print('\033[1;35m error str \033[0m!')

##答应出了 58个

    #newLis = if_ChineseEqual_add_csbFile_to_ccbCol(ccbList)

    ##添加表头
    # titleArr = ["Chinese","FilePth","English","Russion","Vietnam"]
    # newLis.insert(0,titleArr)
    #
    #
    # et.makeExcel(newLis,"CCBReplaglish_3")
    print("success")




