# -*- coding: utf-8 -*-
# @Time    : 18/4/17 下午5:08
# @Author  : myTool
# @File    : getCNfromCoffeeScript.py
# @Software: PyCharm

import os
import sys




def check_contain_chinese(check_str):
    for ch in check_str.decode('utf-8'):
        if u'\u4e00' <= ch <= u'\u9fff':
            return True
    return False

def check_contain_english(str):
    str_1 = list(str)
    for i in str_1:
        if i.isalpha():
            return True
            break
    return False

def GetFileList(dir, fileList):
    newDir = dir
    if os.path.isfile(dir):
        if dir.split(".").pop() == "coffee" :
            fileList.append(dir.decode('utf-8'))
    elif os.path.isdir(dir):
        for s in os.listdir(dir):
            newDir=os.path.join(dir,s)
            GetFileList(newDir, fileList)
    return fileList





def getStrFromFile(path):
    allArr = []
    lines = None
    with open(path, 'r') as r:
        lines = r.readlines()
    print('path:', path)
    for l in lines:
        if check_contain_chinese(l):
            if not("#" in l) :
                if not("@p" in l):
                    if not ("log" in l ):
                        if check_contain_english(l):
                            allArr.append(l)
    return allArr


if __name__ == '__main__':
    allList = GetFileList("/Users/admin/Documents/ljworkspace/local/cocos/project/pikachu_english/app/static/coffee/",[])
    allstr = []
    for path in allList:
        smList = getStrFromFile(path)
        if smList.__len__()>0:
            for i in smList:
                allstr.append(i)

    print("success")
    print(allstr)