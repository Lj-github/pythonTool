# -*- coding: utf-8 -*-
# @Time    : 2018/7/5 上午10:44
# @Author  : liujiang
# @File    : test.py
# @Software: PyCharm
import hashlib
from  hashlib import md5
import shutil
import binascii
def CalcSha1(filepath):
    with open(filepath, 'rb') as f:
        sha1obj = hashlib.sha1()
        sha1obj.update(f.read())
        hash = sha1obj.hexdigest()
        # print(hash[0:5])
        return hash

def shortMD5( md5):
    chars = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j",
            "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v",
            "w", "x", "y", "z", "0", "1", "2", "3", "4", "5", "6", "7",
            "8", "9", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J",
            "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V",
            "W", "X", "Y", "Z" ]
    print(md5)

    sTempSubString = md5[8:16]
    lHexLong = 0x3FFFFFFF & int(sTempSubString, 16);
    outChars = "";
    for i in range(0,6) :
        # 把得到的值与 0x0000003D 进行位与运算，取得字符数组 chars 索引
        index = 0x0000003D & lHexLong
        # 把取得的字符相加
        outChars = outChars+ chars[index]
        #每次循环按位右移 5 位
        lHexLong = lHexLong >> 5

    return outChars;


def generate_file_md5value(fpath):
    m = md5()
    a_file = open(fpath, 'rb')
    m.update(str.upper(binascii.b2a_hex(a_file.read())))

    a_file.close()
    return m.hexdigest()

# print CalcSha1("ppika_fqaAVn.png")
# print shortMD5(generate_file_md5value("ppika_fqaAVn.png"))

import os

def get_file_md5(file_path):
    if not os.path.isfile(file_path):
        return
    myhash=hashlib.md5()
    f=  open(file_path,'rb')
    while True:
        b = f.read(8192)
        if not b:
            break
        myhash.update(b)
    f.close()
    return myhash.hexdigest()

print(shortMD5(get_file_md5("/Users/admin/Documents/ljworkspace/local/cocos/project/pikachu_english_180511/pikachu_english/app/static/res/ui/frmLogin.png")))
print(shortMD5(get_file_md5("/Users/admin/Desktop/frmLogin_JJ3Ar2.webp")))
# print generate_file_md5value("../hotupdate/baijinbaoxiang_eEzuMf.png")
#scp -P 2202 pikachuadmin@pikachu.instantfuns.com:/easygame/pikachu/gameweb/static/res/coffeeTranslate_UfqeEj.json /Users/admin/Desktop/
#scp -P 22 serverdeploy@test.easygametime.com:/mnt/web/gameweb/static/res/ccb/LayerConsortiaAssign_Mn6viu.ccbi /Users/admin/Desktop/



print("res/icons/pika_shengji_ding.png".find("pika_shengji_ding_AbEj63"[:-7])>-1)

print("/Users/admin/Documents/ljworkspace/local/cocos/project/pikachu_english_180511/pikachu_english/app/static".split("/").pop())
port = 22
username = 'serverdeploy'
hostname = 'test.easygametime.com'
serverPath = "/home/serverdeploy/english_deploy/liujiangTest"

upLoadSH = "scp -P " + str(port)  + " " + "file/" + "554564546" + "/" + " " + username + "@" + hostname + ":" + serverPath
print(upLoadSH)
js = "static/script/commons/Constants_B7V3Iz.js"
print(js.split("/").pop().split(".")[0][:-7])