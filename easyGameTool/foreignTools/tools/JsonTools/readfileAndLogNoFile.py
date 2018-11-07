# -*- coding: utf-8 -*-
# @Time    : 2018/5/25 下午4:57
# @Author  : myTool
# @File    : readfileAndLogNoFile.py
# @Software: PyCharm

import os
import json
import shutil
def GetFileList(dir, fileList):
    newDir = dir
    if os.path.isfile(dir):
        fileList.append(dir.decode('utf-8'))
    elif os.path.isdir(dir):
        for s in os.listdir(dir):
            newDir=os.path.join(dir,s)
            GetFileList(newDir, fileList)
    return fileList

def copyfile(srcfile,dstfile):
    if not os.path.isfile(srcfile):
        print("%s not exist!"%(srcfile))
    else:
        fpath,fname=os.path.split(dstfile)
        if not os.path.exists(fpath):
            '''创建路径'''
            os.makedirs(fpath)
        '''复制文件'''
        shutil.copyfile(srcfile,dstfile)
        print("copy %s -> %s"%( srcfile,dstfile))

if __name__ == '__main__':
    #readFil = "/Users/admin/Documents/ljworkspace/local/egret/SmartPikachu/SmartPikachuGit/SmartPikachu/SmartpikachuGame/resource/skill/"
    readFil = "/Users/admin/Documents/ljworkspace/local/cocos/assets/pikachu/sanguo/art_pikachu/动画/"

    # with open("SkilleffectDef.json", 'r') as load_f:
    #
    #     load_dict = json.load(load_f)
    #     fir = GetFileList(readFil,[])
    #     print(len(load_dict))
    #     noList = []
    #     for strCat in range(0,load_dict.__len__()):
    #         isHave = False
    #         for fileName in fir:
    #             nam = load_dict[strCat]["imgFile"]
    #             fpath, fname = os.path.split(fileName)
    #             pandname = fname.split(".")[0]
    #             #
    #             # if pandname ==  nam:
    #             #     isHave = True
    #             if nam in  fileName:
    #                 isHave = True
    #
    #         if not isHave:
    #             noList.append(load_dict[strCat])
    #
    # with open("SkilleffectDef2.json", 'w') as f:
    #     json.dump(noList, f)
    #     print(noList)
    #     print(noList.__len__())


    #复制到目录
    with open("SkilleffectDef2.json", 'r') as load_f:

        load_dict = json.load(load_f)
        fir = GetFileList(readFil, [])
        noList = []
        for strCat in range(0, load_dict.__len__()):
            isHave = False
            for fileName in fir:
                nam = load_dict[strCat]["imgFile"]
                if nam in fileName:
                    isHave = True
                    fpath, fname = os.path.split(fileName)
                    #if fname.split(".")[0] == nam:

                    copyfile(fileName,"/Users/admin/Desktop/test11/"  + fname)




