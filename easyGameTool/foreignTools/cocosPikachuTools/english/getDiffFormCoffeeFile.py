# -*- coding: utf-8 -*-
# @Time    : 2019/2/28 上午10:52


# TODO 期望 实现 两个不同coffee 文件 获取互相没有的函数  是否需要复制 并且追加

chFile = '/Users/admin/Documents/ljworkspace/local/cocos/project/Pikachu/app/static/coffee'#/commons/EasyCommon.coffee
enFile = '/Users/admin/Documents/ljworkspace/local/cocos/project/pikachu_englishGit/pikachu_english/app/static/coffee' #/commons/EasyCommon.coffee

import easyGameTool.foreignTools.cocosPikachuTools.ExcelTools as et
import os

def printDiffFunc(fileMore, filelow):
    cont = ''
    with open(filelow, 'r') as enf:
        cont = enf.read()
    with open(fileMore, 'r') as f:
        li = f.readlines()
        for l in li:
            if l.find("->") > -1:
                if cont.find(l) == -1:
                    print("错误文件 ==>   " + fileMore )
                    print(l)

if __name__ == '__main__':
    # cont = ''
    # with open(enFile, 'r') as enf:
    #     cont = enf.read()
    # with open(chFile, 'r') as f:
    #     li = f.readlines()
    #     for l in li:
    #         if l.find("EasyCommon") > -1:
    #             if cont.find(l) == -1:
    #                 print(l)

    print("done")

    print("其他文件")

    allcncoffee = et.getFileName(chFile,['coffee'],[])
    allEnCoffee = et.getFileName(enFile,['coffee'],[])

    for f in allcncoffee:
        printDiffFunc( f,  f.replace(chFile,enFile) )