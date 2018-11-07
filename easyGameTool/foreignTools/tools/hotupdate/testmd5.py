# -*- coding: utf-8 -*-
# @Time    : 2018/7/4 下午9:12
# @Author  : liujiang
# @File    : testmd5.py
# @Software: PyCharm
from Tkinter import *
from tkMessageBox import *
import  os
import  datetime
import  os.path
import json
from  hashlib import md5
import shutil
import binascii

def generate_file_md5value(fpath):
    m = md5()
    a_file = open(fpath, 'rb')
    #m.update(str.upper(binascii.b2a_hex(a_file.read()))+"3c6e0b8a9c15224a8228b9a98ca1531d")

    m.update(str.upper(binascii.b2a_hex(a_file.read())) )
    a_file.close()
    return m.hexdigest()

if __name__ == '__main__':
    print(generate_file_md5value("baijinbaoxiang_eEzuMf.png"))