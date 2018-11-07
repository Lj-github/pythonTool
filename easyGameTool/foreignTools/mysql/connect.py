# -*- coding: utf-8 -*-
# @Time    : 2018/9/13 下午8:14


'''
    从mysql 里面 直接提取 数据  复制到两个 translate 文件夹里面
'''

import os

import pymysql



if __name__ == '__main__':
    print("begin")
    # 打开数据库连接
    #db = pymysql.connect("192.168.1.207", "root", "", "CHARACTER_SETS")
    db = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='root',db='mydb')
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()

    # SQL 查询语句
    sql = "SELECT * FROM CCBReplaceEnglish WHERE ID = 1"
    try:
        # 执行SQL语句
        cursor.execute(sql)
        # 获取所有记录列表
        results = cursor.fetchall()
        print(results)

    except:
        print("Error: unable to fetch data")

    # 关闭数据库连接
    db.close()



