# -*- coding: utf-8 -*-
# @Time    : 2018/10/15 下午2:26

# -*- coding: utf-8 -*-
# @Time    : 2018/9/13 下午8:14


'''
    从mysql 里面 直接提取 数据  复制到两个 translate 文件夹里面


'''

import os
import json
import pymysql
import shutil
import requests
import easyGameTool.foreignTools.tools.excelTool.ExcelTools as et

# 是否为本地 数据库
isLocal = True

host = '127.0.0.1'
port = 3306
user = 'root'
passwd = '123456'
database = 'foreign-project'
if not isLocal:
    host = '192.168.1.207'
    passwd = ''


projectFile = "/Users/admin/Documents/ljworkspace/local/cocos/project/pikachu_englishGit/pikachu_english/app/static/"

def createJsonFile(jsonObj,fileName):

    with open(fileName + ".json", 'w') as f:
        json.dump(jsonObj, f, sort_keys=True, indent=4, separators=(',', ':'))

def makeCcbTranslate():
    print("begin makeCcbTranslate")
    # 打开数据库连接
    # db = pymysql.connect("192.168.1.207", "root", "", "CHARACTER_SETS")
    db = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=database,charset='utf8mb4')
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()

    # SQL 查询语句
    sql = "SELECT Id,English,Chinese,FilePth from ccbTranslate WHERE Id IS NOT NULL and Id != 0"
    try:
        # 执行SQL语句
        cursor.execute(sql)
        # 获取所有记录列表
        results = cursor.fetchall()
        obj = {}
        obj["RECORDS"] = []

        for row in results:

            # itme["text"] = str(row[1])
            if str(row[1]) == "None":
                itme = [row[0],row[2]]
                obj["RECORDS"].append(itme)
        et.makeExcel(obj,"ccb.xls")

    except:
        print("Error: unable to fetch data")

    # 关闭数据库连接
    db.close()
    print("begin makeCcbTranslate success")

def makeCoffeeTranslate():
    print("begin makeCoffeeTranslate")
    # 打开数据库连接
    # db = pymysql.connect("192.168.1.207", "root", "", "CHARACTER_SETS")
    db = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=database,charset='utf8mb4')
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()

    # SQL 查询语句
    sql = "SELECT Id,English,Chinese,FilePth from coffeeTranslate WHERE Id IS NOT NULL and Id != 0"
    try:
        # 执行SQL语句
        cursor.execute(sql)
        # 获取所有记录列表
        results = cursor.fetchall()
        obj = {}
        obj["RECORDS"] = []

        for row in results:
            # itme["text"] = str(row[1])
            if str(row[1]) == "None":
                itme = [row[0],row[2]]
                obj["RECORDS"].append(itme)
        #createJsonFile(obj,"coffeeTranslate")
        et.makeExcel(obj, "coffee.xls")
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


if __name__ == '__main__':
    makeCcbTranslate()
    makeCoffeeTranslate()



