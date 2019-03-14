# -*- coding: utf-8 -*-
# @Time    : 2018/12/11 下午2:09

import os
import easyGameTool.projectConfig as CF
import easyGameTool.foreignTools.cocosPikachuTools.ExcelTools as et

outFile = ''

imgList = [
    'genxintc1.png',
    '7r_chengha6.png',
    'chh_sijlhl.png',
    'chh_xhh.png',
    "dcq_chnh1.png", "dcq_chnh2.png", "dcq_chnh3.png", "dcq_chnh4.png", "dcq_chnh5.png", "gr_tiaxdy.png",
    'hwhd_cybyunt.png', "pvp_ddqf1.png", "pvp_ddqf2.png"
    , "pvp_gxfcai.png", 'pvp_lmzbs1.png', "pvp_lmzbs2.png", "pvp_qunbe1.png", "pvp_qunbe2.png", "pvp_qunbe3.png",
    "pvp_zhongji1.png", "pvp_zhongji2.png", "tlysff.png"
    , "UI_520pbsds.png", "UI_chenghao10.png", "UI_chenghao11.png", "UI_chenghao12.png", "wz_wzguila.png"
]

if __name__ == '__main__':

    allPsdFile = et.getFileName(CF.MACMINI_COCOS_ALLPSDPATH, ["psd"], [])
    allImgDir = {}
    for _path in imgList:
        allImgDir[_path] = 0

    for _path in allPsdFile:
        fp, fn = os.path.split(_path)
        if fn.split('.').pop() == 'psd':
            if fn.replace("psd","png") in imgList:
                et.copyfile(_path, '/Users/admin/Desktop/psd/' + fn)
                allImgDir[fn.replace("psd","png")] = 1

    for _name in allImgDir:
        if allImgDir[_name] == 0:
            print(_name + "不存在！！")
