# -*- coding: utf-8 -*-
# @Time    : 2019/10/18 下午5:29 
#  地图生成工具

import unit.excel.ExcelTools as et

import unit.json.Tools as json


def createMap(fileName):
    arr = et.excelToList(fileName)
    print(arr)
    for i in range(0, len(arr["map"])):
        for j in range(0, len(arr["map"][i])):
            if arr["map"][i][j] == "":
                arr["map"][i][j] = 0
            arr["map"][i][j] = int(arr["map"][i][j])
    json.createJsonFile(arr['map'], "json/map")


if __name__ == "__main__":
    mapXls = "mapXls/map1.xls"
    createMap(mapXls)

    pass
