# -*- coding: utf-8 -*-
# @Time    : 2019/3/27 下午5:03
'''
    从 所有的exml 里面 过滤出来 关闭 按钮  看是否 有注册  没有  的话 要现实出来


'''
import easyGameTool.foreignTools.cocosPikachuTools.ExcelTools as et

pro = '/Users/admin/Documents/ljworkspace/local/egret/SmartPikachu/SmartPikachuGit/SmartPikachu/SmartpikachuGame/resource/pikSkins'
ts = '/Users/admin/Documents/ljworkspace/local/egret/SmartPikachu/SmartPikachuGit/SmartPikachu/SmartpikachuGame/src'

import os


def fundAllBtnExit(xmlFile):
    with open(xmlFile, 'r') as f:
        line = f.readlines()
        for i in range(0, len(line)):
            l = line[i]
            if l.find('skinName="btnExit') > -1:
                if l.find("<Pb:Button") == -1:
                    l = line[i - 1].replace("\n", "") + l
                ll = l.split(" ")
                for item in ll:
                    if item.find("id") > -1:
                        id = item.split("=").pop()
                        return id[1:-1]
                print("文件  存在 btnexit 但是 没定义 ID => " + xmlFile)
                return l


def findTsNotMediaByExml(allTs, exmlFile):
    for ts in allTs:
        if ts.find("Mediator") > -1 or ts.find("Meditor") > -1:
            continue
        with open(ts, 'r') as f:
            line = f.readlines()
            for i in range(0, len(line)):
                l = line[i]
                if l.find(exmlFile) > -1:  # and (l.find("return")>-1 or l.find("=")>-1)
                    return ts


# 有的 名字 是乱七八糟起的
def getTxClassByClassName(tsClassName, allTs):
    allFile = []
    for ts in allTs:
        with open(ts, 'r') as f:
            line = f.readlines()
            for i in range(0, len(line)):
                l = line[i]
                if l.find("export class") > -1 and l.find(tsClassName + " extend") > -1:
                    allFile.append(ts)
                if l.find("<" + tsClassName + ">") > -1:
                    allFile.append(ts)
    return allFile


def checkIsHasBtnCb(fileName, btnName):
    if fileName.find("Mediator") > -1 or fileName.find("Meditor") > -1:  # meditor  btnexit1
        if btnName.find('btnExit') == 0 or btnName.find('btnClose') == 0:
            return True
    with open(fileName, 'r') as f:
        line = f.readlines()
        for i in range(0, len(line)):
            l = line[i]
            if l.find(btnName + ".setCall") > -1:
                return True
    return False


if __name__ == '__main__':
    allExmlFile = et.getFileName(pro, ["exml"], [])
    allTsFile = et.getFileName(ts, ["ts"], [])
    allXlsCount = len(allExmlFile)
    idx = 0

    for exml in allExmlFile:
        # if exml.find("NodeActivityShenShou") > -1:
        #     print("ssss")
        idx = idx + 1
        btnID = fundAllBtnExit(exml)

        # print(exml + "不存在 btnid ") 不存在的 不管
        print("执行了==>>" + str(idx / allXlsCount))
        if btnID:
            exmlFp, exmlFn = os.path.split(exml)
            # 先通过 xml z找到 ts
            tsFile = findTsNotMediaByExml(allTsFile, exmlFn)
            if not tsFile:
                print("没有找到 ts 匹配" + btnID + "dddd " + exml)
            # print(tsFile)
            if tsFile:
                # if tsFile.find("NodeActivityShenShou")>-1:
                #     print("ssss")
                fp, fn = os.path.split(tsFile)
                tsClassName = fn.split(".")[0]
                # tsfile 就是  class 名 里面一些小的node  没用
                allMediatorandFile = getTxClassByClassName(tsClassName, allTsFile)
                if not (tsFile in allMediatorandFile):
                    allMediatorandFile.append(tsFile)
                isHasCb = False
                for f in allMediatorandFile:
                    if checkIsHasBtnCb(f, btnID):
                        isHasCb = True
                if len(allMediatorandFile) > 0:
                    if not isHasCb:
                        print(exml + ">>>##<<<<" + "" + btnID + ">>>##<<<<" + tsFile)
                        print("有问题")
                else:
                    print("error" + tsFile + exml)
