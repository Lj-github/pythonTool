# -*- coding: utf-8 -*-
# @Time    : 2018/10/15 下午3:45


#插入到mysql  数据


import easyGameTool.foreignTools.cocosPikachuTools.unionTools.insertCcbCoffeeMysql as ins
ccbFile = "/Users/admin/Desktop/pikachu越南版/越南版翻译1011/越南版翻译1011/ccb.xls"
coffeeFile = "/Users/admin/Desktop/pikachu越南版/越南版翻译1011/越南版翻译1011/coffee.xls"

ccbSql = "UPDATE ccbTranslate SET Vietnamese='{0}' WHERE Id={1}"
coffeeSql ='UPDATE coffeeTranslate SET Vietnamese="{0}" WHERE Id={1}'

if __name__ == '__main__':
    ins.makeCcbTranslate(ccbSql,ccbFile)
    ins.makeCoffeeTranslate(coffeeSql,coffeeFile)
