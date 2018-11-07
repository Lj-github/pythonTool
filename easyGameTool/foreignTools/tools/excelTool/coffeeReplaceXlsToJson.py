# -*- coding: utf-8 -*-
# @Time    : 18/4/21 下午2:47
# @Author  : myTool
# @File    : coffeeReplaceXlsToJson.py
# @Software: PyCharm

#将coffeereplace 表  导成 json


import xlrd
from xlwt import Workbook
import re
import json
import ExcelTools as et

def listToJson(list,fileName):
    if not list:return
    json.dumps(list)






if __name__ == '__main__':
    coffpath = "/Users/admin/Documents/ljworkspace/local/cocos/assets/pikachu/sanguo/aiweiyou_pokmon/pika_foreign/coffeeReplace_5.xls"
    ccbpath = "/Users/admin/Documents/ljworkspace/local/cocos/assets/pikachu/sanguo/aiweiyou_pokmon/pika_foreign/ccbTranslate.xls"
    allList = et.excelToList(ccbpath)

    index = allList["sheet0"][0]
    for i in range(0, index.__len__()):
        if i == 0:
            continue
        index[i] = index[i][0:1].lower() + index[i][1:]

    allList["sheet0"].remove(allList["sheet0"][0])

    # allList.insert(0,index)

    newList = []
    for lis in allList["sheet0"]:
        obj = {}
        #[str(lis[0]), int(lis[0])][int(lis[0]) == lis[0]]  #
        obj[index[0]] = [str(lis[0]), int(lis[0])][int(lis[0]) == lis[0]]# int(str().encode("utf-8"))
        obj[index[1]] = str(lis[1]).encode("utf-8")
        obj[index[2]] = str(lis[2]).encode("utf-8")
        obj[index[3]] = str(lis[3]).encode("utf-8")
        obj[index[4]] = str(lis[4]).encode("utf-8")
        obj[index[5]] = str(lis[5]).encode("utf-8")
        obj[index[6]] = str(lis[6]).encode("utf-8")
        newList.append(obj)

    allJson = json.dumps(newList)



    with open("/Users/admin/Documents/ljworkspace/local/cocos/test/foreignTools/tools/excelTool/jsonExport/ccbTranslate.json", "w") as f:
        f.write(allJson )
