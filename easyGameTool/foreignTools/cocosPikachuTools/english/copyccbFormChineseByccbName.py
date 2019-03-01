# -*- coding: utf-8 -*-
# @Time    : 2018/12/19 下午6:01


# 冬季皮肤替换
import easyGameTool.foreignTools.cocosPikachuTools.ExcelTools as et
import os

ch ="/Users/admin/Documents/ljworkspace/local/cocos/project/Pikachu/tools/pikachuCCB/ccb"

en ="/Users/admin/Documents/ljworkspace/local/cocos/project/pikachu_englishGit/pikachu_english/tools/pikachuCCB/ccb"

ccbname = "FormYiyuan"




if __name__ == '__main__':

    allImgFile = et.getFileName(ch,["ccb"])

    for f in allImgFile:
        fp,fn = os.path.split(f)
        if fn == ccbname + ".ccb":
            et.copyfile(f,en+"/"+fn)

    pass