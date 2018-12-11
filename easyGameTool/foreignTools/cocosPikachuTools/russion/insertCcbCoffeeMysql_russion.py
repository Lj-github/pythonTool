# -*- coding: utf-8 -*-
# @Time    : 2018/10/15 下午3:45
#插入到mysql  数据
import easyGameTool.foreignTools.cocosPikachuTools.unionTools.insertCcbCoffeeMysql as ins
ccbFile = "/Users/admin/Desktop/pikachu俄文版/更新/POK_Translation_2018-12-07/needTranslateWords/needTranslateRussionCCB.xls"
coffeeFile = "/Users/admin/Desktop/pikachu俄文版/更新/POK_Translation_2018-12-07/needTranslateWords/needTranslateRussionCoffee.xls"
ccbSql = "UPDATE ccbTranslate SET Russion='{0}' WHERE Id={1}"
coffeeSql ='UPDATE coffeeTranslate SET Russion="{0}" WHERE Id={1}'

if __name__ == '__main__':
    ins.makeCcbTranslate(ccbSql,ccbFile)
    ins.makeCoffeeTranslate(coffeeSql,coffeeFile)



