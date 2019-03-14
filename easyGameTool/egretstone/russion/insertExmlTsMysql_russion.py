# -*- coding: utf-8 -*-
# @Time    : 2018/10/15 下午3:45


#插入到mysql  数据


import easyGameTool.foreignTools.cocosPikachuTools.unionTools.insertCcbCoffeeMysql as ins
ccbFile = "/Users/admin/Desktop/石器俄服/石器俄语完成0220/xml.xls"
coffeeFile = "/Users/admin/Desktop/石器俄服/石器俄语完成0220/ts.xls"
import easyGameTool.projectConfig as cf
ccbSql = "UPDATE xmlTranslate SET Russion='{0}' WHERE Id={1}"
coffeeSql ='UPDATE TsTranslate SET Russion="{0}" WHERE Id={1}'

if __name__ == '__main__':
    ins.database = cf.stoneDataBase
    ins.makeCcbTranslate(ccbSql,ccbFile)
    ins.makeCoffeeTranslate(coffeeSql,coffeeFile)
