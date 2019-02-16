# -*- coding: utf-8 -*-
# @Time    : 2019/2/16 下午4:17

#把 所有的图片  放一块 找没翻译的...  c

import easyGameTool.foreignTools.cocosPikachuTools.ExcelTools as et
import easyGameTool.projectConfig as cf
import os

if __name__ == '__main__':
    allTsFile = et.getFileName("/Users/admin/Documents/ljworkspace/local/egret/ProStoneAge/ProStoneAge/tools/sheets", ["png","jpg"], [])
    allTsFile = et.getFileName("/Users/admin/Documents/ljworkspace/local/egret/ProStoneAge/ProStoneAge/StoneAppPro/resource/images", ["png", "jpg"], allTsFile)
    for f in allTsFile:
        fp,fn = os.path.split(f)
        et.copyfile(f,"/Users/admin/Desktop/ffushiqitupian/" + fn)
    pass