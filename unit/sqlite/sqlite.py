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
    c.executescript(tableSql)
    print("Table created successfully")
    # c.execute() 这个 一次 只能执行 一个 sql
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
        print("插入数据成功")
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

    tableSql = '''DROP TABLE IF EXISTS "dataBaseXJ";
CREATE TABLE "dataBaseXJ" (
"id"  INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
"itemID"  INTEGER NOT NULL,
"createtime"  TEXT,
"lastModifytime"  TEXT,
"logicDelete"  TEXT,
"createBy"  TEXT,
"customerId"  INTEGER,
"lastmodifiedBy"  TEXT,
"customerName"  TEXT,
"customerType"  TEXT,
"gasPropertiesCode"  TEXT,
"gasProperties"  TEXT,
"gasAddress"  TEXT,
"liableOrgId"  INTEGER,
"liableOrgName"  TEXT,
"liableId"  INTEGER,
"liableName"  TEXT,
"lastInspectionPlanDate"  TEXT,
"inspectionPlanDate"  TEXT,
"meterId"  INTEGER,
"meterNo"  INTEGER,
"planYear"  TEXT,
"planMonth"  TEXT,
"state"  INTEGER
);
'''
    print(tableSql)
    createDateBase(dataBaseName)
    createTableFormDataBase(dataBaseName, "drop table if exists USER;")
    createTableFormDataBase(dataBaseName, tableSql)
    print(isTableExitFormDB(dataBaseName, "USER"))
    insertDataToDB(dataBaseName,'INSERT INTO "main"."dataBaseXJ" VALUES (null, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 11, 1, 1, 1, 1, 1, 1, 1);')
    insertDataToDB(dataBaseName, 'INSERT INTO "dataBaseXJ" VALUES (null, "182716426212085760","2019-02-25 17:24:48","2019-02-25 17:24:48","null","0","1000000000000000227","0","昌平区龙域北街3号楼（116）","BUS","310","公共服务用户-营业","昌平区龙域北街3号楼（116）","1000000000000000364","第五分公司户内服务四所西三旗燃气服务中心（非民用）","1000000000000000259","夏维","2019-02-25 17:24:46","2019-03-25 17:24:46","1000000000000040804","5000046411","2019","03","2");')
    insertDataToDB(dataBaseName,"INSERT INTO 'dataBaseXJ'( id,itemID,createtime,lastModifytime,logicDelete,createBy,customerId,lastmodifiedBy,customerName,customerType,gasPropertiesCode,gasProperties,gasAddress,liableOrgId,liableOrgName,liableId,liableName,lastInspectionPlanDate,inspectionPlanDate,meterId,meterNo,planYear,planMonth,state) VALUES (null, '182716577743900674','2019-02-25 17:25:24','2019-02-25 17:25:24','null','0','1000000000000028623','0','上地三街9号E座底商（104室）（金额表）','BUS','310','公共服务用户-营业','上地三街9号E座底商（104室）（金额表）','1000000000000000364','第五分公司户内服务四所西三旗燃气服务中心（非民用）','1000000000000000076','王保成','2019-02-25 17:25:12','2019-03-25 17:25:12','1000000000000059581','5000074931','2019','03','null');")
    insertDataToDB(dataBaseName,"INSERT INTO dataBaseXJ (itemID,createtime,lastModifytime,logicDelete,createBy,customerId,lastmodifiedBy,customerName,customerType,gasPropertiesCode,gasProperties,gasAddress,liableOrgId,liableOrgName,liableId,liableName,lastInspectionPlanDate,inspectionPlanDate,meterId,meterNo,planYear,planMonth,state) VALUES ('182716426484715521','2019-02-25 17:24:48','2019-02-25 17:24:48','null','0','1000000000000000228','0','昌平区龙域北街3号楼（117）','BUS','310','公共服务用户-营业','昌平区龙域北街3号楼（117）','1000000000000000364','第五分公司户内服务四所西三旗燃气服务中心（非民用）','1000000000000000259','夏维','2019-02-25 17:24:46','2019-03-25 17:24:46','1000000000000006597','5000038033','2019','03','2');")
    # insertDataToDB(dataBaseName, "INSERT INTO USER (ID,NAME,AGE,ADDRESS,SALARY) \
    #   VALUES (2, 'Allen', 25, 'Texas', 15000.00 )")
    # print("Opened database successfully")
    # cursor = selectDataFormDB(dataBaseName, "SELECT id, name, address, salary  from USER")
    # for row in cursor:
    #     print("ID = ", row[0])
    #     print("NAME = ", row[1])
    #     print("ADDRESS = ", row[2])
    #     print("SALARY = ", row[3], "\n")
