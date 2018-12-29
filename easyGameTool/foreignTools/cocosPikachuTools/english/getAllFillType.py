# -*- coding: utf-8 -*-
# @Time    : 2018/12/29 上午11:45


# 获取 所有文件 类型


import easyGameTool.foreignTools.tools.excelTool.ExcelTools as et
import easyGameTool.projectConfig as cf
import os

if __name__ == '__main__':
    allFIle = et.GetFileList("/Users/admin/Documents/ljworkspace/local/cocos/project/pikachu_englishGit/pikachu_english/app/static",[])
    allType = []

    for f in allFIle:
        fp,fn = os.path.split(f)
        ftype = fn.split(".").pop()
        if ftype in allType:
            continue
        else:
            allType.append(ftype)

    print(allType)