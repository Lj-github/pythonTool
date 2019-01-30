# -*- coding: utf-8 -*-
# @Time    : 2018/10/12 下午5:42


import hashlib
import os


'''#########           md5 获取  6为字符串获取       ######### md5 短连接   '''
#  md5 =  shortMD5(get_file_md5(fineName))

def shortMD5(md5):
    chars = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j",
             "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v",
             "w", "x", "y", "z", "0", "1", "2", "3", "4", "5", "6", "7",
             "8", "9", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J",
             "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V",
             "W", "X", "Y", "Z"]
    sTempSubString = md5[8:16]
    lHexLong = 0x3FFFFFFF & int(sTempSubString, 16);
    outChars = "";
    for i in range(0, 6):
        index = 0x0000003D & lHexLong
        outChars = outChars + chars[index]
        lHexLong = lHexLong >> 5
    return outChars

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

# sha1 加密
def CalcSha1(filepath):
    with open(filepath, 'rb') as f:
        sha1obj = hashlib.sha1()
        sha1obj.update(f.read())
        hash = sha1obj.hexdigest()
        # print(hash[0:5])
        return hash[0:5]



print(CalcSha1("***.json"))