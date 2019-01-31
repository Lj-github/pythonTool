# -*- coding: utf-8 -*-
# @Time    : 2018/10/15 下午3:45
#插入到mysql  数据
import easyGameTool.foreignTools.cocosPikachuTools.unionTools.insertCcbCoffeeMysql as ins
ccbFile = "/Users/admin/Downloads/ccb_RU.xls"
coffeeFile = "/Users/admin/Downloads/coffee_RU.xls"
ccbSql = "UPDATE ccbTranslate SET Russion='{0}' WHERE Id={1}"
coffeeSql ="UPDATE coffeeTranslate SET Russion='{0}' WHERE Id={1}"

if __name__ == '__main__':
    ins.makeCcbTranslate(ccbSql,ccbFile)
    ins.makeCoffeeTranslate(coffeeSql,coffeeFile)



