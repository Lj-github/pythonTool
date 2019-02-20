# -*- coding: utf-8 -*-
# @Time    : 2019/2/20 下午8:20

import pymysql
from collections import OrderedDict
import os
import fileinput
import re
import xlrd
import xlwt

import easyGameTool.foreignTools.cocosPikachuTools.ExcelTools as et



allchilesexlsFile = et.getFileName('/Users/admin/Documents/ljworkspace/local/egret/design/stone_age/RussianStone/peizhi',["xls","xlsx"],[])
for f in allchilesexlsFile:
    if not os.path.isfile(f.replace("xlsx","xls")):
        et.copyfile(f,f.replace("xlsx","xls"))

    fp,fn = os.path.split(f)
    ft = fn.split(".")[1]
    if ft == 'xlsx':
        os.remove(f)

