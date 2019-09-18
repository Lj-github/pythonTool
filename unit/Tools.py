# -*- coding: utf-8 -*-
# @Time    : 2018/10/12 下午5:14


# 库函数
import os
import shutil
import io
import datetime

'''
    获取文件路径下所有文件列表 list
'''


def GetFileList(dir, fileList=[]):
    newDir = dir
    if os.path.isfile(dir):
        fileList.append(dir)  # .decode('utf-8') python3 不用
    elif os.path.isdir(dir):
        for s in os.listdir(dir):
            newDir = os.path.join(dir, s)
            GetFileList(newDir, fileList)
    return fileList


def GetFileListByType(dir, fType=[], fileList=[]):
    newDir = dir
    if os.path.isfile(dir):
        fpath, fname = os.path.split(dir)
        if (fname.split(".").pop() in fType) and fname[0] != ".":
            fileList.append(dir)
    elif os.path.isdir(dir):
        for s in os.listdir(dir):
            newDir = os.path.join(dir, s)
            GetFileListByType(newDir, fType, fileList)
    return fileList


'''
    判断是否number

'''


def isNumber(str5):
    try:
        f = float(str5)
        True
    except ValueError:
        return False


'''
    创建文件夹
'''


def mkdir(path):
    path = path.strip()
    path = path.rstrip("\\")
    isExists = os.path.exists(path)
    if not isExists:
        os.makedirs(path)
        return True
    else:
        return False


'''
    复制文件，不需要考虑路径是否存在  不存在会直接创建
'''


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


'''
    
'''


def isNotIntAndNotFloat(num):
    num = str(num)
    if num.replace(".", '').isdigit():
        if num.count(".") == 0:
            return False
        elif num.count(".") == 1:
            return False
    else:
        return True


'''
    获取当前文件夹 目录
'''


def getLocalPath():
    return os.path.realpath(__file__)


def get_js(jsFile):
    f = io.open(jsFile, "r", encoding='utf-8')
    line = f.readline()
    htmlstr = ''
    while line:
        htmlstr = htmlstr + line
        line = f.readline()
    return htmlstr


'''
    获取当前时间字符串
'''


def getDataStr():
    today = datetime.datetime.now()
    ISOFORMAT = '%Y%m%d'
    return today.strftime(ISOFORMAT)[2:] + "%s" % today.hour + "%s" % today.second


'''
    删除文件夹下所有文件 
'''


def del_file(path):
    for i in os.listdir(path):
        path_file = os.path.join(path, i)
        if os.path.isfile(path_file):
            # 可以在此  做限制
            os.remove(path_file)
        else:
            del_file(path_file)


'''
    获取文件中的 字符所在行 并返回行
'''


def getStrFromFile(str, file):
    f = io.open(file, "r", encoding='utf-8')
    line = f.readline()
    findStr = ''
    while line:
        if line.find(str) > -1:
            findStr = line
            break
        line = f.readline()
    f.close()
    return findStr


'''
    判断文件中是否包含字符串
'''


def isInclodeStrFromPath(file, str):
    f = io.open(file, "r", encoding='utf-8')
    line = f.readline()
    while line:
        if line.find(str) > -1:
            f.close()
            return True
        line = f.readline()
    f.close()
    return False


'''  gz 压缩文件夹下所有文件  '''


def makeGzFile(filePath):
    allFileNeedGzList = GetFileList(filePath, [])
    for pgz in allFileNeedGzList:
        gzSh = "gzip -c " + pgz + " > " + pgz + ".gz"
        os.system(gzSh)
        print("gzFile = > " + pgz + ".gz")
