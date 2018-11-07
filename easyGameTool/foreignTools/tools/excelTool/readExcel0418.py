# -*- coding: utf-8 -*-
# @Time    : 18/4/18 下午2:11
# @Author  : myTool
# @File    : readExcel0418.py
# @Software: PyCharm


# 把发过来的excel 整理一下... 里面有ccb  也有coffee  合成一个ccb  excel   和 coffee excel


import os
import xlrd
from xlwt import Workbook
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

excelFiles=[
    ['/Users/lan/Downloads/历次翻译整理/绿洲/妖怪宝可萌-updated/1028/1128前端_updated.xlsx',[1,2,3,[0]]],
    ['/Users/lan/Downloads/历次翻译整理/绿洲/妖怪宝可萌-updated/1024/front1024_updated.xlsx',[1,2,3,[0]]],
    ['/Users/lan/Downloads/历次翻译整理/绿洲/妖怪宝可萌-updated/0605/前端0605_updated.xlsx',[1,2,4,[0]]],
    ['/Users/lan/Downloads/历次翻译整理/绿洲/妖怪宝可萌-updated/0512/前端0512_updated.xlsx',[1,2,4,[0]]],
    ['/Users/lan/Downloads/历次翻译整理/绿洲/妖怪宝可萌-updated/0506/前端-updated.xlsx',[1,2,5,[0]]],
    ['/Users/lan/sanguo/aiweiyou_pokmon/EnglishResources/绿洲翻译/1.8追加翻译（en）（done）/0105CCB.xls_Updated.xlsx',[1,0,2,[0]]],
    ['/Users/lan/sanguo/aiweiyou_pokmon/EnglishResources/绿洲翻译/1.8追加翻译（en）（done）/0105Coffee.xls_Updated.xlsx',[1,0,2,[0]]]
]

excelFiles=[
['/Users/admin/Desktop/CS-LC_PKM_Excel汇总_20180125/0506/前端.xls',[1,2,5,[0]]],
    ['/Users/admin/Desktop/CS-LC_PKM_Excel汇总_20180125/1128/1128前端（已审核）.xls',[1,2,3,[0]]],
    ['/Users/admin/Desktop/CS-LC_PKM_Excel汇总_20180125/1024/front1024.xls',[1,2,3,[0]]],
    ['/Users/admin/Desktop/CS-LC_PKM_Excel汇总_20180125/0605/前端0605.xls',[1,2,4,[0]]],
    ['/Users/admin/Desktop/CS-LC_PKM_Excel汇总_20180125/0512/前端0512.xls',[1,2,4,[0]]]

    #['/Users/lan/sanguo/aiweiyou_pokmon/EnglishResources/绿洲翻译/1.8追加翻译（en）（done）/0105CCB.xls_Updated.xlsx',[1,0,2,[0]]],
    #['/Users/lan/sanguo/aiweiyou_pokmon/EnglishResources/绿洲翻译/1.8追加翻译（en）（done）/0105Coffee.xls_Updated.xlsx',[1,0,2,[0]]]
]

CCBFILE = "/Users/admin/Documents/ljworkspace/local/cocos/assets/pikachu/sanguo/aiweiyou_pokmon/pika_foreign/CCBReplaceEnglish_2.xls"
COFFEEFILE = "/Users/admin/Documents/ljworkspace/local/cocos/assets/pikachu/sanguo/aiweiyou_pokmon/pika_foreign/coffeeReplace_2.xls"


#[文件路径，[中文列，路径列，翻译列，[需要的对应sheetIdx]]]

#return arrlist
#  [[ 中文  ccb文件  翻译文]  [中文  coffee文件  翻译文]]

def getDirFromExcel(excelList):
    ccbList = []
    coffeeList = []
    if excelList:
        fileName = excelList[0]
        chineseCol = excelList[1][0]
        ccbcfeCol = excelList[1][1] #需要判断是否为ccb  还是 coffee
        translateCol = excelList[1][2]
        sheetIdxArr  = excelList[1][3]
        print("<------  " +  "file"   +  fileName + " begin search  " +   " ------>")
        table_translate = xlrd.open_workbook(fileName)

        for ins in range(sheetIdxArr.__len__()):

            sheet_translate = table_translate.sheet_by_index(sheetIdxArr[ins])
            nrows_translate = sheet_translate.nrows
            ncols_translate = sheet_translate.ncols

            for j in range(nrows_translate):

                translate = sheet_translate.row_values(j, 0, ncols_translate)
                arrayitem = []
                a = ""
                a.encode("utf8")
                chinese = str(translate[ chineseCol].encode("utf8"))
                arrayitem.append(chinese)
                fileN = str(translate[ccbcfeCol].encode("utf8"))
                arrayitem.append(fileN)  # ccb
                trsStr = None
                if isinstance(translate[translateCol],float) :
                    trsStr = str(translate[translateCol])
                else:
                    trsStr = str(translate[translateCol].encode("utf8"))
                arrayitem.append(trsStr)
                # 里面可能有ccb  可能有coffee
                ccbcoffolList = arrayitem[1].split(";")
                for cs in ccbcoffolList:
                    newItem = arrayitem
                    fileSp = cs.split(".").pop()
                    if fileSp == "ccb":
                        newItem[1] = cs
                        ccbList.append(arrayitem)
                    elif fileSp == "coffee":
                        newItem[1] = cs
                        coffeeList.append(arrayitem)
                    else:
                        print("---------file => " + arrayitem[1] + " is not ccb or coffee ")
    print("<------  " + "file" + fileName + "  search finesh " + " ------>")
    return [ccbList,coffeeList]


def excelToList(file):
    allList = []
    if file:
        print("<------  " + "file" + file + " begin search  " + " ------>")
        table_translate = xlrd.open_workbook(file)
        count = len(table_translate.sheets())


        for ins in range(0,count):
            sheet_translate = table_translate.sheet_by_index(ins)
            nrows_translate = sheet_translate.nrows
            ncols_translate = sheet_translate.ncols

            for j in range(nrows_translate):

                translate = sheet_translate.row_values(j, 0, ncols_translate)
                arrayitem = []
                for st in translate :
                    arrayitem.append(st)
                allList.append(arrayitem)
    print("<------  " + "file" + file + "  search finesh " + " ------>")
    return allList


def makeExcel(AllCCBLis,AllCCBLisName):

    if AllCCBLis:
        len = 0
        news_ids = []
        for id in AllCCBLis:
            if id not in news_ids:
                news_ids.append(id)
        print news_ids
        allArr = news_ids
        w = Workbook()
        ws = w.add_sheet('列表'.decode('utf8'))
        for i in allArr:
            ind = 0
            for j in i:
                # if i[0] == "":  # w为空 不执行
                #     print("break at because null" + str(i[1]))
                #     continue
                # if i[0].isdigit():  # 为数字 不执行
                #     print("break at because number" + str(i[1]))
                #     continue
                rstr = j
                if isinstance(j, str):
                    rstr = j.decode('utf8')
                # print("id = " + str(len) + " " + str(rstr) + "  is add success")
                ws.write(len, ind, rstr)
                ind = ind + 1
                if ind == i.__len__():
                    len = len + 1
        w.save(AllCCBLisName + ".xls")

def conpairList(lis,count):
    lis = lis
    if count>0:
        for l in range(0,count):
            if lis.__len__()<(l+1):
                lis.append("")
    return lis



if __name__ == '__main__':
    AllCCBLis = []
    AllCOFLis = []
    for filLis in excelFiles:
        listIt = getDirFromExcel(filLis)
        for i in listIt[0]:
            AllCCBLis.append(i)
        for i in listIt[1]:
            AllCOFLis.append(i)
    print("<-------- get Success --------->")

    # #
    # if AllCCBLis:
    #     len = 0
    #     news_ids = []
    #     for id in AllCCBLis:
    #         if id not in news_ids:
    #             news_ids.append(id)
    #     print news_ids
    #
    #     allArr = news_ids
    #     w = Workbook()
    #     ws = w.add_sheet('列表'.decode('utf8'))
    #     for i in allArr:
    #         ind = 0
    #         for j in i:
    #             if i[0] == "":  # w为空 不执行
    #                 print("break at because null" + str(i[1]))
    #                 continue
    #             if i[0].isdigit():  # 为数字 不执行
    #                 print("break at because number" + str(i[1]))
    #                 continue
    #             rstr = j
    #             if isinstance(j, str):
    #                 rstr = j.decode('utf8')
    #             # print("id = " + str(len) + " " + str(rstr) + "  is add success")
    #             ws.write(len, ind, rstr)
    #             ind = ind + 1
    #             if ind == i.__len__():
    #                 len = len + 1
    #     w.save("AllCCBLis.xls")
    #
    # if AllCOFLis:
    #     len = 0
    #     news_ids = []
    #     for id in AllCOFLis:
    #         if id not in news_ids:
    #             news_ids.append(id)
    #     print news_ids
    #     allArr = news_ids
    #     w = Workbook()
    #     ws = w.add_sheet('列表'.decode('utf8'))
    #     for i in allArr:
    #         ind = 0
    #         for j in i:
    #             if i[0] == "":  # w为空 不执行
    #                 print("break at because null" + str(i[1]))
    #                 continue
    #             if i[0].isdigit():  # 为数字 不执行
    #                 print("break at because number" + str(i[1]))
    #                 continue
    #             rstr = j
    #             if isinstance(j, str):
    #                 rstr = j.decode('utf8')
    #             # print("id = " + str(len) + " " + str(rstr) + "  is add success")
    #             ws.write(len, ind, rstr)
    #             ind = ind + 1
    #             if ind == i.__len__():
    #                 len = len + 1
    #
    #     w.save("AllCOFLis.xls")


    #对比文件  重新排版LIST
    CCBFILELLIST= excelToList(CCBFILE)
    print("get ccb excel arr success ")
    COFFEEFILELIST = excelToList(COFFEEFILE)

    print("get coffee excel arr success ")

    #对比
    # for lis in AllCCBLis:
    #     newAr = conpairList([],5)
    #     ishas = False
    #     for i in range(CCBFILELLIST.__len__()) :
    #         pd =  conpairList(CCBFILELLIST[i],5)
    #         lis = conpairList(lis,3)
    #         ss = pd[0]
    #
    #         if str(ss)  == str(lis[0]) :# 中文相同
    #             #判断文件
    #             ccbLis1 = pd[1].split(";")
    #             if lis[1].encode("utf8") in ccbLis1:
    #                 pd = conpairList(pd,5)
    #                 pd[4] = lis[2]
    #                 CCBFILELLIST[i] = pd  #补全
    #                 ishas = True
    #
    #
    #     if not ishas:
    #         newAr = conpairList([],5)
    #         newAr[0] = lis[0]
    #         newAr[1] = lis[1]
    #         newAr[4] = lis[2]
    #         CCBFILELLIST.append(newAr)
    #
    # makeExcel(CCBFILELLIST, "CCBFILELLIST")

    # 对比
    for lis in AllCOFLis:
        newAr = conpairList([], 7)
        ishas = False
        for i in range(COFFEEFILELIST.__len__()):
            pd = conpairList(COFFEEFILELIST[i], 7)
            lis = conpairList(lis, 3)
            ss = pd[4]

            if str(ss) == str(lis[0]):  # 中文相同
                # 判断文件
                ccbLis1 = pd[1].split(";")
                if lis[1].encode("utf8") in ccbLis1:
                    pd = conpairList(pd, 7)
                    pd[6] = lis[2]
                    COFFEEFILELIST[i] = pd  # 补全
                    ishas = True

        if not ishas:
            newAr = conpairList([], 7)
            newAr[6] = lis[2]
            newAr[1] = lis[1]
            newAr[4] = lis[0]
            COFFEEFILELIST.append(newAr)

    makeExcel(COFFEEFILELIST, "COFFEEFILELLIST")
