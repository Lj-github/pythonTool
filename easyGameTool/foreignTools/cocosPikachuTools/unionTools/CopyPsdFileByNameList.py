# -*- coding: utf-8 -*-
# @Time    : 2018/12/11 下午2:09

import os
import easyGameTool.projectConfig as CF
import easyGameTool.foreignTools.cocosPikachuTools.ExcelTools as et
outFile = ''

imgList = [
    'zuq_czjx.png',
]

if __name__ == '__main__':

    allPsdFile = et.getFileOnlyName(CF.MACMINI_COCOS_ALLPSDPATH,["psd"],[])
    allImgDir = {}
    for _path in imgList:
        allImgDir[_path] = 0

    for _path in allPsdFile:
        fp,fn = os.path.split(_path)
        if fn.split('.').pop() == 'psd':
            if fn in imgList:
                et.copyfile(_path,'/Users/admin/Desktop/越南修改1211/' + fn)
                allImgDir[fn] = allImgDir[fn] + 1

    for _name in allImgDir:
        if allImgDir[_name] == 0 :
            print(_name + "不存在！！")











