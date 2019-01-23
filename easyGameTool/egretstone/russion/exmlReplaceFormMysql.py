# -*- coding: utf-8 -*-
# @Time    : 2019/1/23 上午11:49


import easyGameTool.foreignTools.cocosPikachuTools.ExcelTools as et
import easyGameTool.projectConfig as cf
import os
import json
import pymysql
import shutil

resourceFile = cf.MACMINI_EGRET_STONE_PRO + "/resource"
allExmlFile = et.getFileName(resourceFile, ["exml"])


def getTableFormMysql(host, port, user, passwd, database, sqlStr):
    db = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=database)
    cursor = db.cursor()
    sql = sqlStr
    try:
        # 执行SQL语句
        cursor.execute(sql)
        # 获取所有记录列表
        results = cursor.fetchall()
        obj = []
        for row in results:
            itme = {}
            itme["Id"] = str(row[0])
            itme["text"] = str(row[1])
            obj.append(itme)
        return obj
    except:
        print("Error: unable to fetch data")
    # 关闭数据库连接
    db.close()


if __name__ == '__main__':
    sql = "select Id,Chinese FROM xmlTranslate  WHERE Id IS NOT NULL and Id != 0"
    alltraslateData = getTableFormMysql(cf.host, cf.port, cf.user, cf.passwd, cf.stoneDataBase, sql)


    def takeSecond(item):
        return len(item["text"])


    alltraslateData.sort(key=takeSecond, reverse=True)

    EXMLTRANSLATESTR = "19012398989"

    ''' !!! 先替换长的 后替换 短的   '''
    for fileName in allExmlFile:
        xmlTxt = ""
        with open(fileName) as f:
            xmlTxt = f.read()
        for item in alltraslateData:
            xmlTxt = xmlTxt.replace(item["text"], EXMLTRANSLATESTR + item["Id"])
        with open(fileName, "w") as f:
            f.write(xmlTxt)
        print(fileName + " ==>> finish ")
    print("done!")
    pass
