# -*- coding: utf-8 -*-
# @Time    : 2019/3/2 下午4:48
# 处理 sqlite  sqlite 嵌入式 数据库  比较小  一版都是 植入 客户端把？

import sqlite3

"""
   数据库不存在，那么它就会被创建，最后将返回一个数据库对象。 会再sql 里面做判断 
"""


def createDateBase(dbName):
    conn = sqlite3.connect(dbName)
    return conn


"""
   指定dataBaseName  创建 Table 
"""


def createTableFormDataBase(dataBase, tableSql):
    conn = sqlite3.connect(dataBase)
    print("Opened database successfully")
    c = conn.cursor()
    c.execute(tableSql)
    print("Table created successfully")
    conn.commit()
    conn.close()


"""
   指定dataBaseName  判断 Table 是否存在
"""


def isTableExitFormDB(db, tbName):
    isExit = False
    conn = sqlite3.connect(db)
    try:
        c = conn.cursor()
        cursor = c.execute(
            "select count(*) as ctn from " + "sqlite_master" + " where type='table' and name = '{0}';".format(tbName))
        if cursor.fetchone()[0] > 0:
            isExit = True
        conn.close()
    except Exception:
        print("select table failed")
    return isExit


"""
   insert 数据 到指定数据库
"""


def insertDataToDB(db, sql):
    conn = sqlite3.connect(db)
    try:
        c = conn.cursor()
        c.execute(sql)
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError as e:
        print("insert table failed", e)
    return False


"""
   select 数据 到指定数据库
"""


def selectDataFormDB(db, sql):
    resoult = None
    conn = sqlite3.connect(db)
    try:
        c = conn.cursor()
        cursor = c.execute(sql)
        resoult = cursor.fetchall()
        conn.commit()
        conn.close()
    except sqlite3.IntegrityError as e:
        print("insert table failed", e)
    return resoult


if __name__ == '__main__':
    dataBaseName = "test.db"
    #
    tableSql = '''CREATE TABLE IF NOT EXISTS USER
       (ID INT PRIMARY KEY     NOT NULL,
       NAME           TEXT    NOT NULL,
       AGE            INT     NOT NULL,
       ADDRESS        CHAR(50),
       SALARY         REAL);'''
    print(tableSql)
    createDateBase(dataBaseName)
    createTableFormDataBase(dataBaseName, tableSql)
    print(isTableExitFormDB(dataBaseName, "USER"))
    # insertDataToDB(dataBaseName, "INSERT INTO USER (ID,NAME,AGE,ADDRESS,SALARY) \
    #   VALUES (1, 'Paul', 32, 'California', 20000.00 )")
    #
    # insertDataToDB(dataBaseName, "INSERT INTO USER (ID,NAME,AGE,ADDRESS,SALARY) \
    #   VALUES (2, 'Allen', 25, 'Texas', 15000.00 )")
    print("Opened database successfully")
    cursor = selectDataFormDB(dataBaseName, "SELECT id, name, address, salary  from USER")
    for row in cursor:
        print("ID = ", row[0])
        print("NAME = ", row[1])
        print("ADDRESS = ", row[2])
        print("SALARY = ", row[3], "\n")
