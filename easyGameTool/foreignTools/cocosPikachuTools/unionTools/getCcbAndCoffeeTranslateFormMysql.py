# -*- coding: utf-8 -*-
# @Time    : 2018/9/13 下午8:14
#getCcbAndCoffeeTranslateFormMysql

'''
    从mysql 里面 直接提取 数据  复制到两个 translate 文件夹里面
'''

import os
import json
import pymysql
import shutil
import requests

import easyGameTool.projectConfig as cf
# 是否为本地 数据库
isLocal = True
host = cf.host
port = cf.port
user = cf.user
passwd = cf.passwd
database = cf.database


def createJsonFile(jsonObj, fileName):
    with open(fileName + ".json", 'w') as f:
        json.dump(jsonObj, f, sort_keys=True, indent=4, separators=(',', ':'),ensure_ascii=False)
def makeCcbTranslate(ccbSqlStr):
    print("begin makeCcbTranslate")
    # 打开数据库连接
    # db = pymysql.connect("192.168.1.207", "root", "", "CHARACTER_SETS")
    db = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=database)
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()
    # SQL 查询语句
    sql = ccbSqlStr
    try:
        # 执行SQL语句
        cursor.execute(sql)
        # 获取所有记录列表
        results = cursor.fetchall()
        obj = {}
        obj["RECORDS"] = []
        for row in results:
            itme = {}
            itme["Id"] = str(row[0])

            itme["text"] = str(row[1])
            if str(row[1]) == "None":
                itme["text"] = str(row[2])
                if "Team" in str(row[3]):
                    print(itme["text"])
                    print(itme["Id"])
            obj["RECORDS"].append(itme)
        createJsonFile(obj, "ccbTranslate")
    except:
        print("Error: unable to fetch data")

    # 关闭数据库连接
    db.close()
    print("begin makeCcbTranslate success")


def makeCoffeeTranslate(coffeeSalStr):
    print("begin makeCoffeeTranslate")
    # 打开数据库连接
    db = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=database)

    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()

    # SQL 查询语句
    sql = coffeeSalStr
    try:
        # 执行SQL语句
        cursor.execute(sql)
        # 获取所有记录列表
        results = cursor.fetchall()
        obj = {}
        obj["RECORDS"] = []
        for row in results:
            itme = {}
            itme["Id"] = str(row[0])
            itme["text"] = str(row[1])
            if itme["Id"] == 193:
                print("err")
            if str(row[1]) == "None" and itme["Id"] != "193":
                itme["text"] = str(row[2])
                itme["Id"]
                print(itme["Id"])
                print(itme["text"])
                if "Team" in str(row[3]):
                    print(itme["text"])

            obj["RECORDS"].append(itme)
        createJsonFile(obj, "coffeeTranslate")

    except:
        print("Error: unable to fetch data")

    # 关闭数据库连接
    db.close()
    print("begin makeCoffeeTranslate success")


def copyfile(srcfile, dstfile):
    if not os.path.isfile(srcfile):
        print("%s not exist!" % (srcfile))
    else:
        fpath, fname = os.path.split(dstfile)
        if not os.path.exists(fpath):
            '''创建路径'''
            mkdir(fpath)
        '''复制文件'''
        "".replace("png", "txt").replace("jpg", "txt")
        shutil.copyfile(srcfile, dstfile)
        print("copy %s -> %s" % (srcfile, dstfile))


def mkdir(path):
    path = path.strip()
    path = path.rstrip("\\")
    isExists = os.path.exists(path)
    if not isExists:
        os.makedirs(path)
        return True
    else:
        return False


