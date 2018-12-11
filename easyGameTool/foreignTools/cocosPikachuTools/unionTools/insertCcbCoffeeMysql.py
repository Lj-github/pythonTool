# -*- coding: utf-8 -*-
# @Time    : 2018/10/15 下午3:45


#插入到mysql  数据

import os
import json
import pymysql
import shutil
import easyGameTool.foreignTools.cocosPikachuTools.ExcelTools as et
import easyGameTool.projectConfig as cf
# 是否为本地 数据库
isLocal = True
host = cf.host
port = cf.port
user = cf.user
passwd = cf.passwd
database = cf.database


def createJsonFile(jsonObj,fileName):
    with open(fileName + ".json", 'w') as f:
        json.dump(jsonObj, f, sort_keys=True, indent=4, separators=(',', ':'))

def makeCcbTranslate(ccbSql,ccbFile):
    print("begin makeCcbTranslate")
    # 打开数据库连接
    # db = pymysql.connect("192.168.1.207", "root", "", "CHARACTER_SETS")
    db = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=database,charset='utf8mb4')
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()
    allList = et.excelToList(ccbFile)["RECORDS"]
    for item in allList:
        ID = item[0]
        vit = item[2]
        # SQL 查询语句
        # "cc{0}".format()
        strFormid = "ccbList_{0}"

        sql = ccbSql.format(vit,str(int(ID)))
        print(sql)
        try:
            # 执行SQL语句
            cursor.execute(sql)
            db.commit()
            # 获取所有记录列表
            print(cursor.rowcount)
        except:
            print("Error: unable to fetch data")

    # 关闭数据库连接
    db.close()
    print("begin makeCcbTranslate success")

def makeCoffeeTranslate(coffeeSql,coffeeFile):
    print("begin makeCoffeeTranslate")
    # 打开数据库连接
    # db = pymysql.connect("192.168.1.207", "root", "", "CHARACTER_SETS")
    db = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=database,charset='utf8mb4')
    cursor = db.cursor()
    allList = et.excelToList(coffeeFile)["RECORDS"]
    for item in allList:
        ID = item[0]
        vit = item[2]
        # SQL 查询语句
        sql = coffeeSql.format(vit, str(int(ID)))
        print(sql)
        try:
            # 执行SQL语句
            cursor.execute(sql)
            db.commit()
            # 获取所有记录列表
            print(cursor.rowcount)
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
        "".replace("png","txt").replace("jpg","txt")
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