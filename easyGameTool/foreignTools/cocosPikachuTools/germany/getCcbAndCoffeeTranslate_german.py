# -*- coding: utf-8 -*-
# @Time    : 2018/9/13 下午8:14


'''
    从mysql 里面 直接提取 数据  复制到两个 translate 文件夹里面
'''

import easyGameTool.foreignTools.cocosPikachuTools.unionTools.getCcbAndCoffeeTranslateFormMysql as gx
ccbSqlStr = "SELECT Id,German,English from ccbTranslate WHERE Id IS NOT NULL and Id != 0"
coffeeSalStr = "SELECT Id,German,English from coffeeTranslate WHERE Id IS NOT NULL and Id != 0"
projectFile = "/Users/admin/Documents/ljworkspace/local/cocos/project/pikachu_german/pikachu_english/app/static/"

if __name__ == '__main__':
    gx.makeCcbTranslate(ccbSqlStr)
    gx.makeCoffeeTranslate(coffeeSalStr)
    gx.copyfile("coffeeTranslate.json", projectFile + "res/coffeeTranslate.json")
    gx.copyfile("ccbTranslate.json", projectFile + "res/ccbTranslate.json")

