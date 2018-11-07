# -*- coding: utf-8 -*-
# @Time    : 18/4/11 下午8:40
# @Author  : myTool
# @File    : makeExcel.py
# @Software: PyCharm

'''
    通过json 转 excel
'''

import os
import xlrd
from xlwt import Workbook
import sys
import json
import foreignTools.tools.excelTool.ExcelTools as et

if __name__ == '__main__':
    allArr = []
    with open("json/tran.json", 'r') as f:
        allArr = json.loads(f.read().decode('utf8'))


    allccbList = et.excelToList("/Users/admin/Documents/ljworkspace/local/cocos/assets/pikachu/sanguo/aiweiyou_pokmon/pika_foreign/CCBReplaceEnglish_6.xls")
    #第三个为英文  2 为俄文
    for i in range(0,allArr.__len__()) :
        has = False
        for j in range(0,allccbList.__len__()) :
            if allArr[i].__len__()>=4 and allccbList[j].__len__()>=5:
                if allArr[i][3] == allccbList[j][2]:
                    print(i)
                    print(allArr[i])
                    allccbList[j][3] = allArr[i][2]
                    print("replace success => " + allArr[i][2] )
                    has = True
                if allArr[i][3] == allccbList[j][4]:
                    print(i)
                    print(allArr[i])
                    allccbList[j][3] = allArr[i][2]
                    print("replace success => " + allArr[i][2])
                    has = True
        if not has :
            print("no")
            print(allArr[i])
            #去掉包括数字的
            if allArr[i].__len__()>=4:
                if allArr[i][2]!=allArr[i][3]:
                    #去掉没有节点名称的
                    #去掉文字相同的
                    #

                    allccbList.append(allArr[i])


    et.makeExcel(allccbList,"test.xls")
    print("over")