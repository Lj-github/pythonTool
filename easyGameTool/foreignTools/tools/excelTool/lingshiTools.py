# -*- coding: utf-8 -*-
# @Time    : 2018/10/15 下午2:29
import foreignTools.tools.excelTool.ExcelTools as et

import copy


if __name__ == '__main__':
    tab = et.excelToList("/Users/admin/Desktop/英文版1016翻译/ccb/ccb.xlsx")
    allList = tab["Sheet1"]


    newObj = {}
    newList = []

    key  = 0
    isNum = False
    item = [None,None]
    for it in allList:
        if isNum:
            item[0] = it[1]
            newList.append(copy.deepcopy(item))
        else:
            item[1] = it[1]
        isNum = not isNum
    newObj["Sheet1"] = newList
    print("done")
    et.makeExcel(newObj,"/Users/admin/Desktop/英文版1016翻译/ccb/ccb.xlsx")