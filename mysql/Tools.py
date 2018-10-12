# -*- coding: utf-8 -*-
# @Time    : 2018/10/12 下午5:29
import os
import json
import pymysql



def connectMysql():
    print("begin makeCcbTranslate")
    # 打开数据库连接
    # db = pymysql.connect("192.168.1.207", "root", "", "CHARACTER_SETS")
    db = pymysql.connect(host='xxx', port=0, user='xxx', passwd='', db='xxx')
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()

    # SQL 查询语句
    sql = "SELECT Id,xxx,xxx,xxx from xxx WHERE Id IS NOT NULL and Id != 0"
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
            obj["RECORDS"].append(itme)
    except:
        print("Error: unable to fetch data")
    # 关闭数据库连接
    db.close()
    print("begin makeCcbTranslate success")