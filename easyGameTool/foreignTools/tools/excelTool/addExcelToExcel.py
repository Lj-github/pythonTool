# -*- coding: utf-8 -*-
# @Time    : 18/4/12 上午11:04
# @Author  : myTool
# @File    : addExcelToExcel.py
# @Software: PyCharm

import xlrd
import xlwt
from xlwt import Workbook
#读取文件
import re
import ExcelTools as et
def isHaveEN(str):
    my_re = re.compile(r'[A-Za-z]', re.S)
    res = re.findall(my_re, str)
    if res.__len__() > 0:
        return True
    else:
        return False

#判断是否含有中文

def check_contain_chinese(check_str ):
    for ch in check_str.decode('utf-8'):
        if u'\u4e00' <= ch <= u'\u9fff':
            return True
    return False

def getExcelByFile(filepth,col):
    if filepth: ##是否需要判断为excel
        dataAll = []
        table_translate = xlrd.open_workbook(filepth)
        sheet_translate = table_translate.sheet_by_index(0)
        nrows_translate = sheet_translate.nrows
        ncols_translate = sheet_translate.ncols
        for j in range(nrows_translate):
            translate = sheet_translate.row_values(j, 0, ncols_translate)
            arrayitem = []
            for i in col:
                sstr = translate[i]
                if isinstance(translate[i], unicode):
                    sstr = str(translate[i].encode('utf8'))
                if str(sstr).__len__() != 0:

                    arrayitem.append(sstr)

                else:
                    print( "file =>" + filepth + "--------" + str(j) + " is empty !!!!  english is " + str(translate[3]))
            if arrayitem.__len__() > 0 :
                dataAll.append(arrayitem)
        return dataAll



def addExcel(oneArr,otherArr):
    allArr = oneArr
    if oneArr and otherArr:
        for arrItem in otherArr:
            isHave = False
            l = 0
            for oItem in oneArr:
                if oItem.__len__()>=3 and arrItem.__len__()>=2:
                    if oItem[2] == arrItem[1] :#如果内容相同 ccb不同 直接放在一个str里面
                        isHave = True
                        if oItem[1] == arrItem[0]:
                            print(" same item " + str(arrItem[0]))
                        else:

                            ccbArr = oItem[0].split(";")
                            if arrItem[0] in ccbArr:
                                print(" same item " + str(arrItem[0]))
                            else:
                                oItem[1] = oItem[1] + ";" + arrItem[0]
                                allArr[l] = oItem
                    l = l+1
            if (not isHave) and isHaveEN(arrItem[1]) and (not check_contain_chinese(arrItem[1])):

                allArr.append(arrItem)
            # if not (arrItem in allArr):
            #     allArr.append(arrItem)
            #     print( " add item " + str(arrItem[0]) )
        return allArr
    return []

def conpairList(lis,count):
    lis = lis
    if count>0:
        for l in range(0,count):
            if lis.__len__()<(l+1):
                lis.append("")
    return lis

# 0412 coffee  ccb 翻译和为一个excel
def addCoffeeExcelList0412(newList,resList):
    if not newList or not resList :return
    #:中文 4  yuenan 6

    for newItem in newList:
        for resItem in range(0,resList.__len__()) :
            if newItem[0] == resList[resItem][4]:
                print("add success =>  " + str(newItem[2])  )
                resList[resItem][6] = newItem[2]

    return resList

def addCcbExcelList0412(newList, resList):
    if not newList or not resList: return
    #:中文 4  yuenan 6
    for newItem in newList:
        for resItem in range(0,resList.__len__()) :
            if newItem[0] == resList[resItem][0]:
                print("add success =>  " + str(newItem[2]))
                resList[resItem][4] = newItem[2]

    return resList

def addCoffeeExcelList0509(newList,resList):
    if not newList or not resList :return
    #:中文 4  yuenan 6

    for newItem in newList:
        for resItem in range(0,resList.__len__()) :
            if newItem[0] == resList[resItem][4]:
                print("add success =>  " + str(newItem[2])  )
                resList[resItem][7] = newItem[2]

    return resList

def addCcbExcelList0509(newList, resList):
    if not newList or not resList: return
    #:中文 4  yuenan 6
    for newItem in newList:
        for resItem in range(0,resList.__len__()) :
            if newItem[0] == resList[resItem][0]:
                print("add success =>  " + str(newItem[2]))
                resList[resItem][5] = newItem[2]

    return resList






def getDiffArr(oneArr,otherArr):
    allArr = []
    if oneArr and otherArr:
        for arrItem in otherArr:
            isHave = False
            l = 0
            for oItem in oneArr:
                if oItem[1] == arrItem[1]:#如果内容相同 ccb不同 直接放在一个str里面
                    isHave = True
                    if oItem[0] == arrItem[0]:
                        print(" same item " + str(arrItem[0]))
                    else:
                        ccbArr = oItem[0].split(";")
                        if arrItem[0] in ccbArr:
                            print(" same item " + str(arrItem[0]))
                        else:
                            oItem[0] = oItem[0] + ";" + arrItem[0]
                            allArr.append(oItem)
                l = l+1
            if not isHave:
                allArr.append(arrItem)
            # if not (arrItem in allArr):
            #     allArr.append(arrItem)
            #     print( " add item " + str(arrItem[0]) )
        return allArr
    return []

import ExcelTools as et




#def makeExcel(sheetName,)
if __name__ == '__main__':
    coffpath = "/Users/admin/Documents/ljworkspace/local/cocos/assets/pikachu/sanguo/aiweiyou_pokmon/pika_foreign/coffeeReplace_6.xls"
    ccbpath = "/Users/admin/Documents/ljworkspace/local/cocos/assets/pikachu/sanguo/aiweiyou_pokmon/pika_foreign/CCBReplaceEnglish_6.xls"
    #try:


    '''' # 注释 
        len = 0
        ccbre = getExcelByFile("CCBReplaceEnglish_2.xls", [0,1, 2,3])
        fulccbre = getExcelByFile("maxd8.xls", [1, 0])
    
        allArr = addExcel(ccbre, fulccbre)
        #allArr = getDiffArr(ccbre, fulccbre)
    
        w = Workbook()
        ws = w.add_sheet('列表'.decode('utf8'))
        news_ids = []
        for id in allArr:
            if id not in news_ids:
                news_ids.append(id)
        print news_ids
    
        allArr = news_ids
    
    '''
    #coffee
    # allList = et.excelToList(coffpath)
    # allList = allList["sheet0"]
    # newPath = "/Users/admin/Desktop/法语翻译/PIKA_180423-1/front_180423/待翻译_coffeeFrench.xls"
    # newList = et.excelToList(newPath)
    # newList = newList["sheet0"]
    # resList = addCoffeeExcelList0509(newList,allList)
    # res = {}
    # res["sheet0"] = resList
    # et.makeExcel(res,"coffee.xls")

    #ccb

    allList = et.excelToList(ccbpath)
    allList = allList["sheet0"]
    newPath = "/Users/admin/Desktop/法语翻译/PIKA_180423-1/front_180423/待翻译_ccbFrench.xls"
    newList = et.excelToList(newPath)
    newList = newList["sheet0"]
    resList = addCcbExcelList0509(newList, allList)
    res = {}
    res["sheet0"] = resList
    et.makeExcel(res, "ccb4.xls")



    # for i in allArr:
    #     len = len + 1
    #     ind = 0
    #     for j in i:
    #         if i[0].encode('utf8') == "":  # w为空 不执行
    #             print("break at because null" + str(i[1]))
    #             continue
    #         if i[0].isdigit():  # 为数字 不执行
    #             print("break at because number" + str(i[1]))
    #             continue
    #
    #         rstr = j
    #         if isinstance(j, str):
    #             rstr = j.decode('utf8')
    #         # print("id = " + str(len) + " " + str(rstr) + "  is add success")
    #         ws.write(len, ind, rstr)
    #
    #         ind = ind + 1
    # for i in allArr:
    #     len = len + 1
    #     ind = 0
    #     for j in i:
    #         # if i[2].encode('utf8') == "":  # w为空 不执行
    #         #     print("break at because null" + str(i[1]))
    #         #     continue
    #         # if i[2].isdigit():  # 为数字 不执行
    #         #     print("break at because number" + str(i[1]))
    #         #     continue
    #
    #         rstr = j
    #         if isinstance(j, str):
    #             rstr = j.decode('utf8')
    #         # print("id = " + str(len) + " " + str(rstr) + "  is add success")
    #         ws.write(len, ind, rstr)
    #
    #         ind = ind + 1
    # w.save("CCBReplaceEnglish_3.xls")


    #
    # except Exception as e:
    #     print("异常"+e)


