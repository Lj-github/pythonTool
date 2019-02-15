# -*- coding: utf-8 -*-
# @Time    : 2019/2/15 下午8:53


# 从 egret 项目中所有的 ts  exml 中 获取 所有中文翻译...

import easyGameTool.foreignTools.cocosPikachuTools.ExcelTools as et
import easyGameTool.projectConfig as cf
tsFile = cf.MACMINI_EGRET_STONE_PRO + "/StoneAppPro/src"
exmlFile = cf.MACMINI_EGRET_STONE_PRO + "/StoneAppPro/resource"




def main():
    allTsFile = et.getFileName(tsFile,["ts"],[])
    allExmlFile = et.getFileName(exmlFile,["exml"],[])
    #todo 检查 中文
    et.isIncludeChinese("")





if __name__ == '__main__':
    print("begin search")
    main()