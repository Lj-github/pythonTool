# -*- coding: utf-8 -*-
# @Time    : 2018/10/22 下午5:52


# 把中文 转为 ccbList
# "cc{0}".format()
strFormid = "ccbList_{0}"
import os
import io

import foreignTools.tools.excelTool.ExcelTools as et

projectFile = "/Users/admin/Documents/ljworkspace/local/cocos/project/pikachu_englishGit/pikachu_english/tools/pikachuCCB/ccb"

ss = "万恶了"
print(ss.replace("万恶了", "d"))


def GetFileListOnlyImg(dir, fileList=[]):
    newDir = dir
    if os.path.isfile(dir):
        fPath, fName = os.path.split(dir)
        fType = fName.split(".").pop()
        if fType in ["ccb"]:
            fileList.append(dir)
    elif os.path.isdir(dir):
        for s in os.listdir(dir):
            newDir = os.path.join(dir, s)
            GetFileListOnlyImg(newDir, fileList)
    return fileList


def getStrFromFile(file):
    f = io.open(file, "r")
    line = f.read()
    f.close()
    return line


def check_contain_chinese(check_str):
    for ch in check_str:
        if u'\u4e00' <= ch <= u'\u9fff':
            return True
    return False


def sortFun(item):
    return len(item[1])


if __name__ == '__main__':
    allChinest = et.excelToList("/Users/admin/Desktop/英文版更新/ccb/ccb.xls")["RECORDS"]
    #先用长的  后用短的  就可以完美替换
    allChinest.sort(key=sortFun, reverse=True)

    allFileName = GetFileListOnlyImg(projectFile)

    for ff in allFileName:
        print("begin replace = >" + ff)
        ss = ""
        with open(ff, 'r') as f:
            ss = f.read()
            for item in allChinest:
                r = strFormid.format(str(item[0]).split(".")[0])
                ind = ss.find(item[1])
                if ind > -1:
                    lene = f.read(ind)
                    chStrr = str(item[1])
                    leneRE = lene.replace(chStrr, r)
                    if not check_contain_chinese(leneRE):
                        ss = ss.replace(chStrr, r)
        with open(ff, 'w') as fff:
            fff.write(ss)
