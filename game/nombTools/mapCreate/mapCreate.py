# -*- coding: utf-8 -*-
# @Time    : 2019/10/18 下午5:29 
#  地图生成工具

import json
import os
import shutil


def mkdir(path):
    path = path.strip()
    path = path.rstrip("\\")
    isExists = os.path.exists(path)
    if not isExists:
        os.makedirs(path)
        return True
    else:
        return False


def copyfile(srcfile, dstfile):
    if not os.path.isfile(srcfile):
        print("%s not exist!" % (srcfile))
    else:
        fpath, fname = os.path.split(dstfile)
        if not os.path.exists(fpath):
            '''创建路径'''
            mkdir(fpath)
        '''复制文件'''
        shutil.copyfile(srcfile, dstfile)
        print("copy %s -> %s" % (srcfile, dstfile))


#  只有一行
def createJsonFile(jsonObj, fileName):
    with open(fileName + ".json", 'w') as f:
        json.dump(jsonObj, f)


import xlrd

'''
    excel 转list
'''


def excelToList(file):
    allTable = {}
    if file:
        print("<------  " + "file" + file + " begin search  " + " ------>")
        table_translate = xlrd.open_workbook(file)
        count = len(table_translate.sheets())
        allName = table_translate.sheet_names()
        for ins in range(0, count):
            allList = []
            sheet_translate = table_translate.sheet_by_name(allName[ins])
            nrows_translate = sheet_translate.nrows
            ncols_translate = sheet_translate.ncols
            for j in range(nrows_translate):
                translate = sheet_translate.row_values(j, 0, ncols_translate)
                arrayitem = []
                for st in translate:
                    arrayitem.append(st)
                allList.append(arrayitem)
            allTable[allName[ins]] = allList
    print("<------  " + "file" + file + "  search finesh " + " ------>")
    return allTable


def createMap(fileName):
    arr = excelToList(fileName)
    print(arr)
    for i in range(0, len(arr["map"])):
        for j in range(0, len(arr["map"][i])):
            if arr["map"][i][j] == "":
                arr["map"][i][j] = 0
            arr["map"][i][j] = int(arr["map"][i][j])
    createJsonFile(arr['map'], "json/map")

    copyfile()


if __name__ == "__main__":
    mapXls = "mapXls/map1.xls"
    createMap(mapXls)
