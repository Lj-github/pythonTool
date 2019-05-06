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

    tableSql = ''' DROP TABLE IF EXISTS "main"."yunxinweihu";
CREATE TABLE "yunxinweihu" (
"autoID"  INTEGER NOT NULL,
"addressId"  TEXT,
"addressInfo"  TEXT,
"baseMeterFactoryNo"  TEXT,
"baseMeterType"  TEXT,
"baseMeterVersionName"  TEXT,
"cardControllerFactoryNo"  TEXT,
"cardControllerManufacturer"  TEXT,
"chargingServerNo"  TEXT,
"county"  TEXT,
"countyId"  TEXT,
"createBy"  TEXT,
"createtime"  TEXT,
"gasCustomerId"  TEXT,
"gasCustomerLevel"  TEXT,
"gasCustomerName"  TEXT,
"gasLocationNo"  TEXT,
"gasProperties"  TEXT,
"gasPropertiesCode"  TEXT,
"gasPropertiesType"  TEXT,
"id"  TEXT,
"installPositionId"  TEXT,
"lastModifytime"  TEXT,
"lastmodifiedBy"  TEXT,
"leaks"  TEXT,
"liableId"  TEXT,
"liableName"  TEXT,
"logicDelete"  TEXT,
"meterId"  TEXT,
"meterNo"  TEXT,
"meterType"  TEXT,
"operationPlanDate"  TEXT,
"orgId"  TEXT,
"orgName"  TEXT,
"planMonth"  TEXT,
"planYear"  TEXT,
"position"  TEXT,
"positionNo"  TEXT,
"rteCode"  TEXT,
"rteName"  TEXT,
"state"  TEXT,
"steal"  TEXT,
"code1"  TEXT,
"code2"  TEXT,
"code3"  TEXT, 
"commitData" TEXT, 
PRIMARY KEY ("autoID" ASC)
);

'''
    print(tableSql)
    createDateBase(dataBaseName)
    # createTableFormDataBase(dataBaseName, "drop table if exists USER;")
    createTableFormDataBase(dataBaseName, tableSql)
    print("创建成功！")
    print(isTableExitFormDB(dataBaseName, "USER"))
    # insertDataToDB(dataBaseName,'INSERT INTO "main"."dataBaseXJ" VALUES (null, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 11, 1, 1, 1, 1, 1, 1, 1);')
    # insertDataToDB(dataBaseName, 'INSERT INTO "dataBaseXJ" VALUES (null, "182716426212085760","2019-02-25 17:24:48","2019-02-25 17:24:48","null","0","1000000000000000227","0","昌平区龙域北街3号楼（116）","BUS","310","公共服务用户-营业","昌平区龙域北街3号楼（116）","1000000000000000364","第五分公司户内服务四所西三旗燃气服务中心（非民用）","1000000000000000259","夏维","2019-02-25 17:24:46","2019-03-25 17:24:46","1000000000000040804","5000046411","2019","03","2");')
    # insertDataToDB(dataBaseName,"INSERT INTO 'dataBaseXJ'( id,itemID,createtime,lastModifytime,logicDelete,createBy,customerId,lastmodifiedBy,customerName,customerType,gasPropertiesCode,gasProperties,gasAddress,liableOrgId,liableOrgName,liableId,liableName,lastInspectionPlanDate,inspectionPlanDate,meterId,meterNo,planYear,planMonth,state) VALUES (null, '182716577743900674','2019-02-25 17:25:24','2019-02-25 17:25:24','null','0','1000000000000028623','0','上地三街9号E座底商（104室）（金额表）','BUS','310','公共服务用户-营业','上地三街9号E座底商（104室）（金额表）','1000000000000000364','第五分公司户内服务四所西三旗燃气服务中心（非民用）','1000000000000000076','王保成','2019-02-25 17:25:12','2019-03-25 17:25:12','1000000000000059581','5000074931','2019','03','null');")
    # insertDataToDB(dataBaseName,"INSERT INTO dataBaseXJ (itemID,createtime,lastModifytime,logicDelete,createBy,customerId,lastmodifiedBy,customerName,customerType,gasPropertiesCode,gasProperties,gasAddress,liableOrgId,liableOrgName,liableId,liableName,lastInspectionPlanDate,inspectionPlanDate,meterId,meterNo,planYear,planMonth,state) VALUES ('182716426484715521','2019-02-25 17:24:48','2019-02-25 17:24:48','null','0','1000000000000000228','0','昌平区龙域北街3号楼（117）','BUS','310','公共服务用户-营业','昌平区龙域北街3号楼（117）','1000000000000000364','第五分公司户内服务四所西三旗燃气服务中心（非民用）','1000000000000000259','夏维','2019-02-25 17:24:46','2019-03-25 17:24:46','1000000000000006597','5000038033','2019','03','2');")
    insertDataToDB(dataBaseName,
                   "INSERT INTO yunxinweihu (id,baseMeterFactoryNo,baseMeterType,baseMeterVersionName,cardControllerFactoryNo,cardControllerManufacturer,chargingServerNo,county,countyId,createBy,addressId,addressInfo,steal,state,rteName,rteCode,positionNo,position,planYear,planMonth,orgName,orgId,operationPlanDate,meterType,meterNo,meterId,logicDelete,liableName,liableId,leaks,lastmodifiedBy,lastModifytime,installPositionId,gasPropertiesType,gasPropertiesCode,gasProperties,gasLocationNo,gasCustomerName,gasCustomerLevel,gasCustomerId,createtime,code1,code2,code3,commitData) VALUES ('199379903953506304','05217040023717','3','TBQJ-100B','05117040023719','天信','2757104754','丰台区','1000000000000000023','199340941184602112','1000000000000005172','丰台区南苑乡右安门村','','2','杨东虹卡表查表册','YDH_KB','4000074776','其它','2019','04','第四分公司户内服务四所西便门燃气服务中心（非民用）','1000000000000000243','2019-04-30 23:59:59','MONMETER','5000075503','1000000000000053223','','杨东虹','1000000000000000160','','199340941184602112','2019-04-12 16:59:30','1000000000000027127','HEATANDCOOL','430','采暖制冷用户-冷暖用户','3000033868','北京市嘉祥工贸公司','0','1000000000000023270','2019-04-12 16:59:30','','','','%7B%22id%22:%22199379701666418688%22,%22operationPlanDate%22:%222019-04-20%2014:03:00%22,%22operationUnitId%22:%22%22,%22operationUnitName%22:%22%22,%22recordItems%22:%5B%7B%22descVal%22:%22%22,%22operationPlanId%22:%22199379701666418688%22,%22parentId%22:%22183438489059069952%22,%22quotaItemId%22:%22183438308192292864%22,%22widgetVal%22:%22%22%7D,%7B%22descVal%22:%22%22,%22operationPlanId%22:%22199379701666418688%22,%22parentId%22:%22183438489059069952%22,%22quotaItemId%22:%22183438489059069952%22,%22widgetVal%22:%22%22%7D,%7B%22descVal%22:%22%22,%22operationPlanId%22:%22199379701666418688%22,%22parentId%22:%22183438489059069952%22,%22quotaItemId%22:%22183454828049993728%22,%22widgetVal%22:%22%22%7D,%7B%22descVal%22:%22%22,%22operationPlanId%22:%22199379701666418688%22,%22parentId%22:%22183438489059069952%22,%22quotaItemId%22:%22183439214673661952%22,%22widgetVal%22:%22%22%7D,%7B%22descVal%22:%22%22,%22operationPlanId%22:%22199379701666418688%22,%22parentId%22:%22183438489059069952%22,%22quotaItemId%22:%22183439293958590464%22,%22widgetVal%22:%22%22%7D,%7B%22descVal%22:%22%22,%22operationPlanId%22:%22199379701666418688%22,%22parentId%22:%22183438489059069952%22,%22quotaItemId%22:%22183439375911096320%22,%22widgetVal%22:%22%22%7D,%7B%22descVal%22:%22%22,%22operationPlanId%22:%22199379701666418688%22,%22parentId%22:%22183438489059069952%22,%22quotaItemId%22:%22183439436829167616%22,%22widgetVal%22:%22%22%7D,%7B%22descVal%22:%22%22,%22operationPlanId%22:%22199379701666418688%22,%22parentId%22:%22183438489059069952%22,%22quotaItemId%22:%22183439519352098816%22,%22widgetVal%22:%22%22%7D,%7B%22descVal%22:%22%22,%22operationPlanId%22:%22199379701666418688%22,%22parentId%22:%22183438489059069952%22,%22quotaItemId%22:%22183439615359717376%22,%22widgetVal%22:%22%22%7D,%7B%22descVal%22:%22%22,%22operationPlanId%22:%22199379701666418688%22,%22parentId%22:%22183438489059069952%22,%22quotaItemId%22:%22183439702387331072%22,%22widgetVal%22:%22%22%7D,%7B%22descVal%22:%22%22,%22operationPlanId%22:%22199379701666418688%22,%22parentId%22:%22183438489059069952%22,%22quotaItemId%22:%22183439826299654144%22,%22widgetVal%22:%22%22%7D,%7B%22descVal%22:%22%22,%22operationPlanId%22:%22199379701666418688%22,%22parentId%22:%22183438489059069952%22,%22quotaItemId%22:%22183439885917491200%22,%22widgetVal%22:%22%22%7D,%7B%22descVal%22:%22%22,%22operationPlanId%22:%22199379701666418688%22,%22parentId%22:%22183438489059069952%22,%22quotaItemId%22:%22183440087290220544%22,%22widgetVal%22:%22%22%7D,%7B%22descVal%22:%22%22,%22operationPlanId%22:%22199379701666418688%22,%22parentId%22:%22183438489059069952%22,%22quotaItemId%22:%22183440220862025728%22,%22widgetVal%22:%22%22%7D,%7B%22descVal%22:%22%22,%22operationPlanId%22:%22199379701666418688%22,%22parentId%22:%22183438489059069952%22,%22quotaItemId%22:%22183440406657110016%22,%22widgetVal%22:%22%22%7D,%7B%22descVal%22:%22%22,%22operationPlanId%22:%22199379701666418688%22,%22parentId%22:%22183438489059069952%22,%22quotaItemId%22:%22183440862108192768%22,%22widgetVal%22:%22%22%7D,%7B%22descVal%22:%22%22,%22operationPlanId%22:%22199379701666418688%22,%22parentId%22:%22183438489059069952%22,%22quotaItemId%22:%22183440928583716864%22,%22widgetVal%22:%22%22%7D,%7B%22descVal%22:%22%22,%22operationPlanId%22:%22199379701666418688%22,%22parentId%22:%22183438489059069952%22,%22quotaItemId%22:%22183441028307488768%22,%22widgetVal%22:%22%22%7D,%7B%22descVal%22:%22%22,%22operationPlanId%22:%22199379701666418688%22,%22parentId%22:%22183438489059069952%22,%22quotaItemId%22:%22183441112495558656%22,%22widgetVal%22:%22%22%7D%5D%7D');")

    # insertDataToDB(dataBaseName, "INSERT INTO USER (ID,NAME,AGE,ADDRESS,SALARY) \
    #   VALUES (2, 'Allen', 25, 'Texas', 15000.00 )")
    # print("Opened database successfully")
    # cursor = selectDataFormDB(dataBaseName, "SELECT *  from dataBaseXJ WHERE id = 3")
    # print(selectDataFormDB(dataBaseName,"SELECT *  from file WHERE id = 'asfdsa'"))
    # for row in cursor:
    #     print(row)
    #     print("ID = ", row[0])
    #     print("NAME = ", row[1])
    #     print("ADDRESS = ", row[2])
    #     print("SALARY = ", row[3], "\n")
