# -*- coding: utf-8 -*-
# @Time    : 2018/7/11 下午5:13

''' 通过图片的内容  获取 svn 下翻译 图片的名字 路径  返回 图片路径名字  '''

import os
import io
from sys import argv
#script,first = argv
import codecs
import sys
import shutil
first = "pour challenger"

# # 是否全称
# isFullName = False

svnPath = "/Users/admin/Documents/ljworkspace/local/cocos/assets/pikachu/sanguo/art_pikachu/翻译美术（法国）/"
# svnPath = "/Users/admin/Documents/ljworkspace/local/cocos/assets/pikachu/sanguo/art_pikachu/翻译美术图（英文）/"

''' eprecated since version 2.6: The commands module has been removed in Python 3. Use the subprocess module instead. '''
import subprocess
#print "the script is called:", script
print("需要查找的图片内容为", first)

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
        "".replace("png","txt").replace("jpg","txt")
        shutil.copyfile(srcfile, dstfile)
        print("copy %s -> %s" % (srcfile, dstfile))


def GetFileList(dir, fileList):
    newDir = dir
    if os.path.isfile(dir):
        fileList.append(dir)
    elif os.path.isdir(dir):
        for s in os.listdir(dir):
            newDir=os.path.join(dir,s)
            GetFileList(newDir, fileList)
    return fileList
def getFindFileName(File,findStr):
    #f = io.open(File, "r", encoding='utf-8')
    f = codecs.open(File, 'r', encoding="ISO-8859-1")
    line = f.readline()
    fileN = ""
    while line:
        if line.find(findStr) > -1 :
            fileN = File
            break
        line = f.readline()
    return fileN
def del_file(path):
    for i in os.listdir(path):
        path_file = os.path.join(path, i)
        if os.path.isfile(path_file) :
             os.remove(path_file)
        else:
            del_file(path_file)

if __name__ == '__main__':
    allFindList = []
    allList = GetFileList(svnPath,[])
    for fileName in allList:
        if fileName.split(".").pop() == "txt":
            ff =  getFindFileName(fileName,first)
            if ff != "":
                allFindList.append(ff)
    print("获取到文件：")
    print("清空结果")
    del_file(os.path.dirname(__file__) + "/imgGarbage/")

    for i in allFindList:
        name = i.split("/").pop().split(".")[0]
        print("txt格式==>>" +  i)
        shShell = "find " + svnPath +" -name "+ name + "*"
        status, output = subprocess.getstatusoutput(shShell)
        allL = output.split("\n")
        for sa in allL:
            if sa.split("/").pop().split(".")[0] == name and sa.split(".").pop() != "txt":
                print( "图片资源路径==>>" + sa)
                fPath ,fName = os.path.split(sa)
                copyfile(sa,"imgGarbage/" + fName)

    print("获取完成")
