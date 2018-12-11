# -*- coding: utf-8 -*-
# @Time    : 2018/10/15 下午3:45


#插入到mysql  数据

import easyGameTool.foreignTools.cocosPikachuTools.unionTools.insertCcbCoffeeMysql as ins

ccbFile = "/Users/admin/Downloads/英文版翻译1210/ccb.xls"
coffeeFile = "/Users/admin/Downloads/英文版翻译1210/coffee.xls"
ccbSql = "UPDATE ccbTranslate SET English='{0}' WHERE Id={1}"
coffeeSql ='UPDATE coffeeTranslate SET English="{0}" WHERE Id={1}'


if __name__ == '__main__':
    ins.makeCcbTranslate(ccbSql,ccbFile)
    ins.makeCoffeeTranslate(coffeeSql,coffeeFile)


