# -*- coding: utf-8 -*-
# @Time    : 2018/8/30 下午4:25


import os



from bypy import ByPy

# bp = ByPy()
#
# bp.mkdir(remotepath='bypy')  #在网盘中新建目录

import bypy
#e1aada6218a29a8bc91177a86f8b128a



resFilterFileName =  ["hengpingqiehuan","ditu000"]
filePDName = "hengpingqiehuan"
for pdNameOne in resFilterFileName:
    if pdNameOne.find(filePDName) > -1:
        isFind = True
        print("ddd")