# -*- coding: utf-8 -*-
# @Time    : 2018/9/13 下午8:14

# 拿到越南的翻译  和 中文

'''
    从mysql 里面 直接提取 数据  复制到两个 translate 文件夹里面
    # 可以分开 没有翻译的

'''
import easyGameTool.foreignTools.cocosPikachuTools.unionTools.getCcbCoffeeFromMysqlEhereNoConfigLanToXls as nl
if __name__ == '__main__':
    ccbSql = "SELECT Id,Vietnamese,Chinese from ccbTranslate WHERE Id IS NOT NULL and Id != 0"  # and Vietnamese is not NULL
    coffeeSql = "SELECT Id,Vietnamese,Chinese from coffeeTranslate WHERE Id IS NOT NULL and Id != 0"  # and Vietnamese is not NULL
    nl.makeCcbTranslate(ccbSql)
    nl.makeCoffeeTranslate(coffeeSql)



