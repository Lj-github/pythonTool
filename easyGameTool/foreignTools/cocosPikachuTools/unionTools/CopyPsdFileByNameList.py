# -*- coding: utf-8 -*-
# @Time    : 2018/12/11 下午2:09

import os
import easyGameTool.projectConfig as CF
import easyGameTool.foreignTools.cocosPikachuTools.ExcelTools as et

outFile = ''

imgList = [
    'UI_VIP_zishebeijing.jpg',
    'cz_zti3.png',
    'ui_zhaunsdj.png',
    'zzz_yff.png',
    "qy_204k.png",

    "ui_dshoq.png",

    "doq_diksmgz.jpg",

]

if __name__ == '__main__':

    allPsdFile = et.getFileName(CF.MACMINI_COCOS_ALLPSDPATH, ["psd"], [])
    allImgDir = {}
    for _path in imgList:
        allImgDir[_path] = 0

    for _path in allPsdFile:
        fp, fn = os.path.split(_path)
        if fn.split('.').pop() == 'psd':
            if fn.replace("psd","png") in imgList :
                et.copyfile(_path, '/Users/admin/Desktop/psd/' + fn)
                allImgDir[fn.replace("psd","png")] = 1
            if fn.replace("psd", "jpg") in imgList:
                et.copyfile(_path, '/Users/admin/Desktop/psd/' + fn)
                allImgDir[fn.replace("psd", "jpg")] = 1

    for _name in allImgDir:
        if allImgDir[_name] == 0:
            print(_name + "不存在！！")
