# -*- coding: utf-8 -*-
# @Time    : 2018/10/15 下午3:45


#插入到mysql  数据


import easyGameTool.foreignTools.cocosPikachuTools.unionTools.insertCcbCoffeeMysql as ins
ccbFile = "/Users/admin/Desktop/pikachu越南版/越南翻译1226fankui/越南翻译1226/ccbcoffee/ccb.xls"
coffeeFile = "/Users/admin/Desktop/pikachu越南版/越南翻译1226fankui/越南翻译1226/ccbcoffee/coffee.xls"

ccbSql = "UPDATE ccbTranslate SET Vietnamese='{0}' WHERE Id={1}"
coffeeSql ='UPDATE coffeeTranslate SET Vietnamese="{0}" WHERE Id={1}'

if __name__ == '__main__':
    ins.makeCcbTranslate(ccbSql,ccbFile)
    ins.makeCoffeeTranslate(coffeeSql,coffeeFile)
