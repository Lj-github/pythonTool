# -*- coding: utf-8 -*-
# @Time    : 2018/12/19 下午6:01


# 冬季皮肤替换
import easyGameTool.foreignTools.cocosPikachuTools.ExcelTools as et
import os

isShenDan = True

shendanFile = '/Users/admin/Documents/ljworkspace/local/cocos/assets/pikachu/sanguo/art_pikachu/动画/替换怪物/节日精灵/圣诞'

baseFile =  "/Users/admin/Documents/ljworkspace/local/cocos/assets/pikachu/sanguo/art_pikachu/动画/替换怪物"


projectFile = '/Users/admin/Documents/ljworkspace/local/cocos/project/pikachu_vietnam/pikachu_english/app/static/res/unit'

if __name__ == '__main__':

    allImgFile = et.getFileOnlyName(shendanFile,["png"])

    for f in allImgFile:
        fp,fn = os.path.split(f)
        if not isShenDan:
            shendanFile = baseFile

        et.copyfile(shendanFile+ "/" + fn,projectFile+ "/" + fn)


    pass