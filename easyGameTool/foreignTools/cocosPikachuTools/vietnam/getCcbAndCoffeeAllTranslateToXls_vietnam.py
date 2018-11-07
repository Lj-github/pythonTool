# -*- coding: utf-8 -*-
# @Time    : 2018/9/13 下午8:14

# 拿到越南的翻译  和 中文

'''
    从mysql 里面 直接提取 数据  复制到两个 translate 文件夹里面
    # 可以分开 没有翻译的

'''

import os
import json
import pymysql
import shutil

import foreignTools.cocosPikachuTools.ExcelTools as et

projectFile = "/Users/admin/Documents/ljworkspace/local/cocos/project/pikachu_vietnam/pikachu_english/app/static/"

def createJsonFile(jsonObj,fileName):

    with open(fileName + ".json", 'w') as f:
        json.dump(jsonObj, f, sort_keys=True, indent=4, separators=(',', ':'))

def makeCcbTranslate():
    print("begin makeCcbTranslate")
    # 打开数据库连接
    # db = pymysql.connect("192.168.1.207", "root", "", "CHARACTER_SETS")
    db = pymysql.connect(host='192.168.1.207', port=3306, user='root', passwd='', db='foreign-project')
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()

    # SQL 查询语句
    sql = "SELECT Id,Vietnamese,Chinese from ccbTranslate WHERE Id IS NOT NULL and Id != 0 and Vietnamese is not NULL"
    try:
        # 执行SQL语句
        cursor.execute(sql)
        # 获取所有记录列表
        results = cursor.fetchall()
        obj = {}
        obj["RECORDS"] = []
        listt = []
        ds = {}
        for row in results:
            itme = [str(row[0]),str(row[2]),str(row[1])]
            listt.append(itme)


        ds["ccb"] = listt
        et.makeExcel(ds,"ccb.xls")

    except:
        print("Error: unable to fetch data")

    # 关闭数据库连接
    db.close()
    print("begin makeCcbTranslate success")

def makeCoffeeTranslate():
    print("begin makeCoffeeTranslate")
    # 打开数据库连接
    # db = pymysql.connect("192.168.1.207", "root", "", "CHARACTER_SETS")
    db = pymysql.connect(host='192.168.1.207', port=3306, user='root', passwd='', db='foreign-project')
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()

    # SQL 查询语句
    sql = "SELECT Id,Vietnamese,Chinese from coffeeTranslate WHERE Id IS NOT NULL and Id != 0 and Vietnamese is not NULL"
    try:
        # 执行SQL语句
        cursor.execute(sql)
        # 获取所有记录列表
        results = cursor.fetchall()
        listt = []
        ds = {}
        for row in results:
            itme = [str(row[0]), str(row[2]), str(row[1])]
            listt.append(itme)

        ds["coffee"] = listt
        et.makeExcel(ds, "coffee.xls")
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



