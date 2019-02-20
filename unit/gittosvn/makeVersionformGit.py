# -*- coding: utf-8 -*-
# @Time    : 2019/2/20 下午8:48


# 每次提交  新建一份 文件  用于 svn 提交 ...


gitFile = "/Users/admin/Documents/ljworkspace/local/js/appcantest"
svnFile = ""

import os
import shutil
import datetime


def mkdir(path):
    path = path.strip()
    path = path.rstrip("\\")
    isExists = os.path.exists(path)
    if not isExists:
        os.makedirs(path)
        return True
    else:
        return False


def copyfile(srcfile, dstfile):
    if not os.path.isfile(srcfile):
        print("%s not exist!" % (srcfile))
    else:
        fpath, fname = os.path.split(dstfile)
        if not os.path.exists(fpath):
            '''创建路径'''
            mkdir(fpath)
        '''复制文件'''
        shutil.copyfile(srcfile, dstfile)
        print("copy %s -> %s" % (srcfile, dstfile))


def getFileName(dir, type=[], fileList=[]):
    if os.path.isfile(dir):
        fp, fn = os.path.split(dir)
        if fn[0] != "." and dir.find(".git") == -1:
            fileList.append(dir)
    elif os.path.isdir(dir):
        for s in os.listdir(dir):
            newDir = os.path.join(dir, s)
            getFileName(newDir, type=type, fileList=fileList)
    return fileList


def getDataStr():
    today = datetime.datetime.now()
    ISOFORMAT = '%Y%m%d'
    return today.strftime(ISOFORMAT)[2:] + "%s" % today.hour + "%s" % today.second


import json

if __name__ == '__main__':
    ob = 0
    with open("data.json", 'r') as f:
        ob = json.load(f)

    beifengFile = "/Users/admin/Documents/ljworkspace/local/js/bf/" + str(ob['id'])
    fil = getFileName(gitFile)
    for f in fil:
        copyfile(f, f.replace(gitFile, beifengFile))
    ob['id'] = ob['id']+1
    with open("data.json", 'w') as f:
        f.write(json.dumps(ob))
