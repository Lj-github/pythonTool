# -*- coding: utf-8 -*-
# @Time    : 2018/10/11 下午4:04


filename = "/Users/admin/Desktop/英文版更新/img2/"
import os
import shutil
def GetFileList(dir, fileList = []):

    newDir = dir
    if os.path.isfile(dir):
        fp,fn = os.path.split(dir)
        if fn[0] != ".":
            fileList.append(dir)
    elif os.path.isdir(dir):
        for s in os.listdir(dir):
            newDir = os.path.join(dir, s)
            GetFileList(newDir, fileList)
    return fileList
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
        # print("copy %s -> %s" % (srcfile, dstfile))


if __name__ == '__main__':
    allFileList = GetFileList(filename)
    print("")
    for fi in allFileList:

        copyfile(filename.replace("img2/","test.txt"),fi.replace("png","txt").replace("jpg","txt"))





