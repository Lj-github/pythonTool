# -*- coding: utf-8 -*-
# @Time    : 2018/10/12 下午5:23

import json

#  格式化

def createJsonFileFormat(jsonObj,fileName):

    with open(fileName + ".json", 'w') as f:
        json.dump(jsonObj, f, sort_keys=True, indent=4, separators=(',', ':'))

#  只有一行
def createJsonFile(jsonObj,fileName):
    with open(fileName + ".json", 'w') as f:
        json.dump(jsonObj, f)