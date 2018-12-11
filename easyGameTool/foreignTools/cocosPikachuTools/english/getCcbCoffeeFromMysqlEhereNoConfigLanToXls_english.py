# -*- coding: utf-8 -*-
# @Time    : 2018/10/15 下午2:26

# -*- coding: utf-8 -*-
# @Time    : 2018/9/13 下午8:14

import easyGameTool.foreignTools.cocosPikachuTools.unionTools.getCcbCoffeeFromMysqlEhereNoConfigLan as nl
if __name__ == '__main__':
    ccbSql = "SELECT Id,English,Chinese,FilePth from ccbTranslate WHERE Id IS NOT NULL and Id != 0"
    coffeeSql = "SELECT Id,English,Chinese,FilePth from coffeeTranslate WHERE Id IS NOT NULL and Id != 0"
    nl.makeCcbTranslate(ccbSql)
    nl.makeCoffeeTranslate(coffeeSql)
