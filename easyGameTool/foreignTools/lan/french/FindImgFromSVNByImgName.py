# -*- coding: utf-8 -*-
# @Time    : 2018/7/11 下午5:13

''' 通过图片的内容  获取 svn 下翻译 图片的名字 路径 '''

import os
import io
from sys import argv
#script,first = argv
import codecs
import sys
reload(sys)
first = "Coupon mua"


# # 是否全称
# isFullName = False

sys.setdefaultencoding('utf-8')
svnPath = "/Users/admin/Documents/ljworkspace/local/cocos/assets/pikachu/sanguo/art_pikachu/翻译美术（法国）/"
svnPath = "/Users/admin/Documents/ljworkspace/local/cocos/assets/pikachu/sanguo/art_pikachu/翻译美术图（英文）/"


import commands
#print "the script is called:", script
print "需要查找的图片内容为", first
def GetFileList(dir, fileList):
    newDir = dir
    if os.path.isfile(dir):
        fileList.append(dir.decode('utf-8'))
    elif os.path.isdir(dir):
        for s in os.listdir(dir):
            newDir=os.path.join(dir,s)
            GetFileList(newDir, fileList)
    return fileList
def getFindFileName(File,findStr):
    #f = io.open(File, "r", encoding='utf-8')
    f = codecs.open(File, 'r', encoding="ISO-8859-1")
    line = f.readline()
    fileN = ""
    while line:
        if line.find(findStr) > -1 :
            fileN = File
            break
        line = f.readline()
    return fileN

if __name__ == '__main__':
    allFindList = []
    allList = GetFileList(svnPath,[])
    for fileName in allList:
        if fileName.split(".").pop() == "txt":
            ff =  getFindFileName(fileName,first)
            if ff != "":
                allFindList.append(ff)
    print "获取到文件："

    for i in allFindList:
        name = i.split("/").pop().split(".")[0]
        print "txt格式==>>" +  i
        shShell = "find " + svnPath +" -name "+ name + "*"
        status, output = commands.getstatusoutput(shShell)
        allL = output.split("\n")
        for sa in allL:
            if sa.split("/").pop().split(".")[0] == name and sa.split(".").pop() != "txt":
                print "图片资源路径==>>" + sa


    print "获取完成"
