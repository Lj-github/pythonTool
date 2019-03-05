# -*- coding: utf-8 -*-
# @Time    : 2018/9/13 下午8:14


'''
    从mysql 里面 直接提取 数据  复制到两个 translate 文件夹里面

'''

import easyGameTool.foreignTools.cocosPikachuTools.unionTools.getCcbAndCoffeeTranslateFormMysql as gx

projectFile = "/Users/admin/Documents/ljworkspace/local/cocos/project/pikachu_english_180511/pikachu_english/app/static/"

ccbSqlStr = "SELECT Id,English,Chinese,FilePth from ccbTranslate WHERE Id IS NOT NULL and Id != 0"
coffeeSalStr = "SELECT Id,English,Chinese,FilePth from coffeeTranslate WHERE Id IS NOT NULL and Id != 0"

if __name__ == '__main__':
    gx.makeCcbTranslate(ccbSqlStr)
    gx.makeCoffeeTranslate(coffeeSalStr)
    gx.copyfile("coffeeTranslate.json", projectFile + "res/coffeeTranslate.json")
    gx.copyfile("ccbTranslate.json", projectFile + "res/ccbTranslate.json")



