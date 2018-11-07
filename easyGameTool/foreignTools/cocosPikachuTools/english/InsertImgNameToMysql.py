# -*- coding: utf-8 -*-
# @Time    : 2018/10/27 下午4:46

# 把文件名字  加入到sql


import os
import json
import pymysql
import shutil
import requests
import foreignTools.cocosPikachuTools.ExcelTools as et


def getFileOnlyName(dir, type = [],fileList=[]):
    newDir = dir
    if os.path.isfile(dir):
        fp,fn = os.path.split(dir)
        ft = fn.split(".").pop()
        if ft in type:
            fileList.append(fn)
    elif os.path.isdir(dir):
        for s in os.listdir(dir):
            newDir=os.path.join(dir,s)
            getFileOnlyName(newDir,type = type ,fileList= fileList)
    return fileList


imgFile = "/Users/admin/Desktop/英文版更新/img2"

def createJsonFile(jsonObj,fileName):

    with open(fileName + ".json", 'w') as f:
        json.dump(jsonObj, f, sort_keys=True, indent=4, separators=(',', ':'))

def main():
    print("begin run")

    allFileName = getFileOnlyName(dir= imgFile,type = ["png","jpg"])

    # 打开数据库连接
    db = pymysql.connect(host='192.168.1.207', port=3306, user='root', passwd='', db='foreign-project')
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()
    #INSERT INTO tablename SET column_name1 = value1, column_name2 = value2，…;
    # SQL 查询语句
    try:
        # 执行SQL语句
        for f in allFileName:
            sql = "INSERT INTO translateImgData SET fileName = '"+ f + "', English = '', Russion = '' ,Vietnam = '' ,French= '' ,Germany = '' ,TraditionalChinese = '' "
            print(sql)
            cursor.execute(sql )
            # 获取所有记录列表
            db.commit()
            print(f + "success")

    except:
        print("Error: unable to fetch data")

    # 关闭数据库连接
    db.close()
    print("run success")



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
    main()

