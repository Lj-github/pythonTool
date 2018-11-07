# -*- coding: utf-8 -*-
# @Time    : 2018/7/3 下午8:52
# @Author  : liujiang
# @File    : getChineseFromeCCBFile.py
# @Software: PyCharm

"""
    读取ccb 里面的所有中文  或者通过某一列表读取

"""


import os
import os.path


def GetFileList(dir, fileList):
    newDir = dir
    if os.path.isfile(dir):
        fileList.append(dir.decode('utf-8'))
    elif os.path.isdir(dir):
        for s in os.listdir(dir):
            newDir=os.path.join(dir,s)
            GetFileList(newDir, fileList)
    return fileList

def readeCCB(file):
    if file:
        print("reade ccb file =>> " + file)




if __name__ == '__main__':

    allFile = GetFileList("/Users/admin/Documents/ljworkspace/local/cocos/project/pikachu_englishGit/pikachu_english/tools/pikachuCCB/ccb",[])

