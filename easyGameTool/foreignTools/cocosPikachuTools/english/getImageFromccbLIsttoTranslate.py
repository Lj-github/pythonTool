# -*- coding: utf-8 -*-
# @Time    : 2018/10/11 下午3:30
# 通过ccb  拿到所有图片资源  只能是手动看 是不是 需要翻译了

ccblist = [
    "FormJieRiJiJin",
    "NodeActivityJiRi"


]

projectFile = "/Users/admin/Documents/ljworkspace/local/cocos/project/pikachu_englishGit/pikachu_english/app/static/"

import requests
import json
import os
import shutil
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

    filee = os.path.realpath(__file__)
    fpath,fname = os.path.split(filee)


    for ccb in ccblist:
        baidu_url = 'http://0.0.0.0:5000/ccb/' + ccb
        response = requests.get(baidu_url)
        ccbstr = response.content.decode()
        ccbObj = json.loads(ccbstr)
        res = ccbObj['blobFiles']
        for re in res:
            typ = re.split(".").pop()
            if typ == "png" or typ == "jpg":
                ''' 复制 '''
                plist = re.replace("png","plist").replace("jpg","plist")
                print(plist)
                if os.path.isfile( projectFile + plist):
                    print(plist)
                    fp,fn = os.path.split(projectFile + plist)
                    copyfile(projectFile + plist, fpath + "/split/" + fn)
                    fp1, fn1 = os.path.split(projectFile + re)
                    copyfile(projectFile + re, fpath + "/split/" + fn1)
                else:
                    copyfile(projectFile+re,fpath + "/imageTranslate/" + re)

        os.system("/Users/admin/Documents/environment/python3/bin/python " +fpath + "/split/split.py" )