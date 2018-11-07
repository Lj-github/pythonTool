# -*- coding: utf-8 -*-
# @Time    : 2018/10/13 下午4:31

# 从中文版里面 抽取 没有翻译的图片


chinesePro = "/Users/admin/Documents/ljworkspace/local/cocos/project/Pikachu"

svnPath = [
    "/Users/admin/Documents/ljworkspace/local/cocos/project/Pikachu/tools/pikachuFontAndPlist",
    "/Users/admin/Documents/ljworkspace/local/cocos/project/Pikachu/app/static/res/ui"
]

englishPro = "/Users/admin/Documents/ljworkspace/local/cocos/project/pikachu_englishGit/pikachu_english"

coped = "/Users/admin/Desktop/英文版更新/img/"
projectFile = [
    "/Users/admin/Documents/ljworkspace/local/cocos/project/pikachu_englishGit/pikachu_english/tools/pikachuFontAndPlist",
    "/Users/admin/Documents/ljworkspace/local/cocos/project/pikachu_englishGit/pikachu_english/app/static/res/ui"
]

# 复制 全部 中文版的资源  当然是没有的

import os
import json
import shutil
import hashlib

from PIL import Image
import pytesseract

import re

zh_pattern = re.compile(u'[\u4e00-\u9fa5]+')

def contain_zh(word):
    '''
    判断传入字符串是否包含中文
    :param word: 待判断字符串
    :return: True:包含中文  False:不包含中文
    '''
    word = word
    global zh_pattern
    match = zh_pattern.search(word)

    return match



#  没用  无法识别
def img_isHasCH(filName):
    fp, fn = os.path.split(filName)
    ftype = fn.split(".").pop()
    allLen = 0
    code = ""
    if ftype == "png" or ftype == "jpg":
        image = Image.open(filName)
        # im = image
        # rgb_im = im.convert('RGB')
        # rgb_im.save('colors.jpg')
        # print("openFIle = >" + filName)
        # enlcode = pytesseract.image_to_string(image, config='--psm 10 ')
        # print("------")
        # print("英文字符=>" + enlcode)
        # print("英文字符长度=>" + str(len(enlcode)))
        # print("------")

        code = pytesseract.image_to_string(image, lang="chi_sim", config='--psm 10 ')
        print("------")
        print("中文字符=>" + code)
        print("中文字符长度=>" + str(len(code)))
        print("------")
        allLen = len(code) #len(enlcode) +



    return contain_zh(code)


def GetFileListOnlyImg(dir, fileList):
    newDir = dir
    if os.path.isfile(dir):
        fp, fn = os.path.split(dir)
        type = fn.split(".").pop()
        if type == "png" or type == "jpg":
            fileList.append(dir)
    elif os.path.isdir(dir):
        for s in os.listdir(dir):
            newDir = os.path.join(dir, s)
            GetFileListOnlyImg(newDir, fileList)
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

        print("copy %s -> %s" % (srcfile, dstfile))


def get_file_md5(file_path):
    if not os.path.isfile(file_path):
        return
    myhash = hashlib.md5()
    f = open(file_path, 'rb')
    while True:
        b = f.read(8192)
        if not b:
            break
        myhash.update(b)
    f.close()
    return myhash.hexdigest()


def getFileListMd5Dir(fileList):
    obj = {}
    if fileList:
        for f in fileList:
            fpath, fname = os.path.split(f)
            key = fname.replace(".", "_")
            o = {}
            o["path"] = f
            o["md5"] = get_file_md5(f)
            obj[key] = o

    return obj


'''  由于 project 里面的图片 有两个路径 有的需要 都替换  o dir 需要加一个 字段  '''


def getProFileListMd5Dir(fileList):
    obj = {}
    if fileList:
        for f in fileList:
            fpath, fname = os.path.split(f)
            key = fname.replace(".", "_")
            o = {}
            if key in obj:
                o = obj[key]
                o["path2"] = f
                o["md52"] = get_file_md5(f)
            else:
                o["path"] = f
                o["md5"] = get_file_md5(f)
                obj[key] = o

    return obj


def getLocalPathByName(allFile, fName):
    for k in allFile:
        f = allFile[k]
        fp, fn = os.path.split(f["path"])
        if fn == fName:
            return f
    return None


def isEnglishHas(list, fileName):
    for ff in list:
        if ff == fileName:
            return True
    return False


def isNotIntAndNotFloat(num):
    num = str(num)
    if num.replace(".", '').isdigit():
        if num.count(".") == 0:
            return False
        elif num.count(".") == 1:
            return False
    else:
        return True


import re


def password_check_contain_num(password):
    pattern = re.compile('[0-9]+')
    match = pattern.findall(password)
    if match:
        return True
    else:
        return False


def ishasPlist(list, fileName):
    for ff in list:
        fp, fn = os.path.split(ff)
        ty = fn.split(".").pop()
        if ty == "plist":
            if ff.replace("plist", "png") == fileName:
                return True
    return False



if __name__ == '__main__':
    filee = os.path.realpath(__file__)
    fpath, fname = os.path.split(filee)

    # for i in range(len(svnPath)):
    #     chineseproAllName = GetFileListOnlyImg(svnPath[i], [])
    #     englishroAllName = GetFileListOnlyImg(projectFile[i], [])
    #
    #     for chineseFile in chineseproAllName:
    #
    #         comFi = chineseFile.replace(chinesePro, englishPro)
    #
    #         if not ishasPlist(chineseproAllName, chineseFile):  #not password_check_contain_num(chineseFile) and
    #
    #             if not isEnglishHas(englishroAllName, comFi):
    #                 copyfile(chineseFile, coped + comFi.replace(englishPro, ""))
    #                 # 如果没有 直接复制过来  如果有 比较md5
    #                 continue
    #
    #             if get_file_md5(chineseFile) == get_file_md5(comFi):
    #                 copyfile(chineseFile, coped + comFi.replace(englishPro, ""))
    #

    allNeedChickFile =  GetFileListOnlyImg(coped, [])

    for f in allNeedChickFile:
        fp,fn = os.path.split(f)
        copyfile(f,"/Users/admin/Desktop/英文版更新/img2/" + fn)
