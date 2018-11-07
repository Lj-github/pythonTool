# -*- coding: utf-8 -*-
# @Time    : 18/4/16 下午12:15
# @Author  : myTool
# @File    : diffPngAndJpg.py
# @Software: PyCharm
# 获取文件夹下的名称相同 后缀不同的文件  并输出文件目录 json


#需要查找的文件目录

import os
from xlwt import Workbook
import xlrd
import json

#本地项目路径
PATH = "/Users/admin/Documents/ljworkspace/local/cocos/assets/pikachu/"

#svn 主路径 （所有人一致）

Spath = "sanguo/art_pikachu/"

def GetFileList(dir, fileList):
    newDir = dir
    if os.path.isfile(dir):
        fileList.append(dir.decode('utf-8'))
    elif os.path.isdir(dir):
        for s in os.listdir(dir):
            newDir=os.path.join(dir,s)
            GetFileList(newDir, fileList)
    return fileList

#需求 0416
# 从英文版中获取正常路径  去从中国文版中查找 然后 返回相同名字的png jpg  生成excel 并添加超链接  查看是否为中英文乱了

import xlwt
if __name__ == '__main__':
    print("start => run")

    englistPath = "/Users/admin/Documents/ljworkspace/local/cocos/assets/pikachu/sanguo/art_pikachu/翻译美术图/"
    chPath = "/Users/admin/Documents/ljworkspace/local/cocos/assets/pikachu/sanguo/art_pikachu/"

    allList = GetFileList(englistPath,[])
    for i in range(allList.__len__()):

        allList[i] = allList[i].encode("utf8").replace(englistPath, chPath)

    resArr = []
    for path in allList:
        fpath, fname = os.path.split(path)
        fpath = fpath  + "/" + fname.split(".")[0]
        fname = fname.split(".").pop()
        if os.path.isfile(fpath + ".jpg"):
            if os.path.isfile(fpath + ".png"):
                pngFile = fpath + ".png"
                jpgFile = fpath + ".jpg"
                if not (path  in resArr) :
                    resArr.append(pngFile)
                    resArr.append(jpgFile)


    ##写入excel 只需要一列即可
    col = 0
    w = Workbook()
    ws = w.add_sheet('列表'.decode('utf8'))
    for path in resArr:
        col = col + 1

        print("id = " + str(col) + str(path) + "  is add success")
        Rpath = path.replace(PATH,"").decode('utf8')
        ws.write(col + col % 3, 0, xlwt.Formula('HYPERLINK(" ' + Rpath + '";"' + Rpath+ '")'))
            #ws.write(col, 0, path)
    w.save("jpgpngerror.xls")

# import xlwt
# workbook = xlwt.Workbook()
# worksheet = workbook.add_sheet('My Sheet')
# worksheet.write(0, 0, xlwt.Formula('HYPERLINK(" '+ "   " + '";"'+ "   " + '")')) # Outputs the text "Google" linking to http://www.google.com
# workbook.save('Excel_Workbook2.xls')

# sheet2.write_merge(9, 9, 2, 8, xlwt.Formula(n + '("http://www.cnblogs.com/zhoujie";"jzhou\'s blog")'),
#                    set_style('Arial', 300, True))
# sheet2.write_merge(10, 10, 2, 8, xlwt.Formula(n + '("mailto:zhoujie0111@126.com";"contact me")'),
#                    set_style('Arial', 300, True))








