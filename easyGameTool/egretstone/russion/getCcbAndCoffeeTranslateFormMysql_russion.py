# -*- coding: utf-8 -*-
# @Time    : 2018/9/13 下午8:14


'''
    从mysql 里面 直接提取 数据  复制到两个 translate 文件夹里面


'''

import easyGameTool.foreignTools.cocosPikachuTools.unionTools.getCcbAndCoffeeTranslateFormMysql as gx

projectFile = "/Users/admin/Documents/ljworkspace/local/egret/ProStoneAge/ProStoneAge/StoneAppPro/config/"
# 样式
ccbSqlStr = "SELECT Id,Russion,Chinese,FilePth from xmlTranslate WHERE Id IS NOT NULL and Id != 0"
# 脚本
coffeeSalStr = "SELECT Id,Russion,Chinese,FilePth from TsTranslate WHERE Id IS NOT NULL and Id != 0"

gx.database = gx.cf.stoneDataBase

if __name__ == '__main__':
    gx.makeCcbTranslate(ccbSqlStr)
    gx.makeCoffeeTranslate(coffeeSalStr)
    gx.copyfile("coffeeTranslate.json", projectFile + "tsTranslate.json")
    gx.copyfile("ccbTranslate.json", projectFile + "exmlTranslate.json")



