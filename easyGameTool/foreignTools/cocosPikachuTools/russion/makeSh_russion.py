# -*- coding: utf-8 -*-
# @Time    : 2018/12/25 下午3:03

import os
ROOTPATH = '/Users/admin/Documents/ljworkspace/local/cocos/project/pikachu_russion_update/'

# '''执行脚本文件 plist fnt'''
binPth = ROOTPATH + 'pikachu_english/tools/pikachuFontAndPlist/bin'
for root, dirs, files in os.walk(binPth):
    for OneFileName in files:
        if OneFileName.find('.sh') > 0:
            os.system('sh ' + os.path.join(root, OneFileName))

