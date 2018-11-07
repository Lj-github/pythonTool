# -*- coding: utf-8 -*-
# @Time    : 18/4/10 下午8:08
# @Author  : myTool
# @File    : MakeLanExcel2do.py
# @Software: PyCharm

#   提去指定excel 列数 生成新的文件

import xlrd
import xlwt
from xlwt import Workbook
import os
import sys

reload(sys)

sys.setdefaultencoding('utf-8')
#基础文件
READ_PATH = "/Users/admin/Documents/ljworkspace/local/cocos/assets/pikachu/sanguo/aiweiyou_pokmon/pika_foreign/CCBReplaceEnglish_1.xls"
READ_PATH = "/Users/admin/Documents/ljworkspace/local/cocos/assets/pikachu/sanguo/aiweiyou_pokmon/pika_foreign/coffeeReplace_2.xls"

##生成目录
RESULT_PATH = "/Users/admin/Desktop/pikachu/"
#生成的文件名
RESULT_NAME = "CCBReplaceVietnamese.xls"


RESULT_NAME = "coffeeReplaceVietnamese.xls"
## 列
COL = 4

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
            sstr = translate[col]
            if isinstance(translate[col], unicode):
                sstr = str(translate[col].encode('utf8'))
            if str(sstr).__len__() != 0:
                arrayitem.append(sstr)
                dataAll.append(arrayitem)
            else:
                print("--------" + str(j) + " is empty !!!!  english is " + str(translate[3]))

        return dataAll

try:

    allArr = getExcelByFile(READ_PATH, COL)
    if allArr:
        len = 0
        w = Workbook()
        ws = w.add_sheet('列表'.decode('utf8'))
        for i in allArr:
            len = len + 1
            rstr = i[0]
            if isinstance(i[0], str):
                rstr = i[0].decode('utf8')
            print("id = " + str(len) + str(rstr) + "  is add success")
            ws.write(len, 0,rstr )
        w.save(RESULT_PATH + RESULT_NAME)


except NameError:
    pass
