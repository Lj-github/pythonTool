# -*- coding: utf-8 -*-
# @Time    : 2018/10/23 下午3:50


# 目前只是简单的 更新后端数据


import os
import pymysql
import shutil

svn = "/Users/admin/Documents/ljworkspace/local/cocos/assets/pikachu/sanguo/aiweiyou_pokmon/EnglishResources/tools/exceltojson/sql"
sqlFile = [svn + '/gamedata_tables.sql',
           svn + '/gamedata_update.sql'
           ]

def run():
    print("update pkc_gamedata")
    # 打开数据库连接
    # db = pymysql.connect("192.168.1.207", "root", "", "CHARACTER_SETS")
    db = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='root', db='pkc_gamedata', charset='utf8')
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()

    # SQL 查询语句
    for f in sqlFile:
        with open(f, 'r+') as f:
            sql_list = f.read().split(';\n')
            ##执行sql语句，使用循环执行sql语句
        for sql_item in sql_list:
            print(sql_item)
            try:
                # 执行SQL语句
                cursor.execute(sql_item)
                # 获取所有记录列表

            except:
                print("Error: unable to fetch data")

    # 关闭数据库连接
    db.close()


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


if __name__ == '__main__':
    # os.system("svn up " + svn)
    run()


# mysql -h192.168.1.8 -uroot -proot gamedata < /Users/admin/Documents/ljworkspace/local/cocos/assets/pikachu/sanguo/aiweiyou_pokmon/EnglishResources/tools/exceltojson/sql/gamedata_tables.sql
# mysql -h192.168.1.8 -uroot -proot gamedata < /Users/admin/Documents/ljworkspace/local/cocos/assets/pikachu/sanguo/aiweiyou_pokmon/EnglishResources/tools/exceltojson/sql/gamedata_update.sql