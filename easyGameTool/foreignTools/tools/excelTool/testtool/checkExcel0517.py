# -*- coding: utf-8 -*-
# @Time    : 2018/5/17 下午12:44
# @Author  : myTool
# @File    : checkExcel0517.py
# @Software: PyCharm
import sys
import os
import xlrd
from xlwt import Workbook
import sys
import json
import  ExcelTools as et







if __name__ == '__main__':
    newXlsAllXls_witchForJSONPATH = "/Users/admin/Documents/ljworkspace/local/cocos/assets/pikachu/sanguo/aiweiyou_pokmon/VietnamResources/资源表0512/"
    newXlsAllXls_witchForJSONPATH ="/Users/admin/Desktop/out1/"

    allss = et.GetFileList(newXlsAllXls_witchForJSONPATH,[])

    for i in allss:
        fpath, fname = os.path.split(i)
        if fname.split(".").pop() == "xls":

            table_translate = xlrd.open_workbook(i)
            count = len(table_translate.sheets())
            allName = table_translate.sheet_names()
            ishav = False
            for nam in allName:
                fpath, fname = os.path.split(i)
                fnameL = fname.split(".")[0]



                if fnameL == nam:
                    if "lianaijineng" == fnameL:
                        print("rrrrrrr")
                    ishav = True
                    print("can = >> " + fnameL)
                    continue
            if not ishav:
                print("can not = >> " + fnameL)