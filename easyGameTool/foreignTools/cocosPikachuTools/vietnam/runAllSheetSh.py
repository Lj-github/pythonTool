# -*- coding: utf-8 -*-
# @Time    : 2018/10/17 下午2:58

'''  发布 ccb 的   '''
import os


import easyGameTool.foreignTools.cocosPikachuTools.ExcelTools as et

alsh = et.getFileName('/Users/admin/Documents/ljworkspace/local/cocos/project/pikachu_vietnam/pikachu_english/tools/pikachuFontAndPlist/bin',["sh"],[])
for i in alsh:
    os.system("sh " + i)