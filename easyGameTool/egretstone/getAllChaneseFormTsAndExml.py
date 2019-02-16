# -*- coding: utf-8 -*-
# @Time    : 2019/2/15 下午8:53


# 从 egret 项目中所有的 ts  exml 中 获取 所有中文翻译...

import easyGameTool.foreignTools.cocosPikachuTools.ExcelTools as et
import easyGameTool.projectConfig as cf

tsFile = cf.MACMINI_EGRET_STONE_PRO + "/src"
exmlFile = cf.MACMINI_EGRET_STONE_PRO + "/resource"


EXMLTRANSLATESTR = "xmlList_"


def getTableKey(tab, val):
    for i in tab:
        if val == tab[i]:
            return i
    return None

def main():
    allTsFile = et.getFileName(tsFile, ["ts"], [])
    allExmlFile = et.getFileName(exmlFile, ["exml"], [])
    tsIDIdx = 1231
    xmlIDIdx = 729
    xml_t = {}
    for xml in allExmlFile:
        line = ""
        with open(xml, 'r') as f:
            line = f.read()
            #line = line.replace(EXMLTRANSLATESTR, "xmlList_")
            #用两点 拆分 如果有中文 / 如果 有 19... 说明有问题 打印出来 没有直接替换
            dd = line.split('"')
            for i in range(len(dd)):
                if i % 2 != 0:
                    s = dd[i]
                    if et.isIncludeChinese(s):
                        if s.find(EXMLTRANSLATESTR)>-1:
                            print("文件有问题 = >" + xml,"s = >" + s)
                        else:
                            k = getTableKey(xml_t, s)
                            # 是否已经换过的值
                            if k:
                                _k = k.replace("_", "")
                            else:
                                xml_t["_" + str(xmlIDIdx)] = s
                                _k = xmlIDIdx
                                xmlIDIdx = xmlIDIdx + 1
                            print("xmlID = > ", _k, "replace Str = > ", s,"file = >" + xml)
                            line = line.replace(s, str(EXMLTRANSLATESTR + str(_k)))
            # strList = et.getChineseStr(line)
            # if len(strList) > 0:
            #     for s in strList:
            #         k = getTableKey(xml_t, s)
            #         # 是否已经换过的值
            #         _k = 0
            #         if k:
            #             _k = k.replace("_","")
            #         else:
            #             xml_t["_"+str(xmlIDIdx) ] = s
            #             _k = xmlIDIdx
            #             xmlIDIdx = xmlIDIdx+1
            #         print("xmlID = > ", _k, "replace Str = > ", s)
            #         line = line.replace(s, str(EXMLTRANSLATESTR + str(_k) ))
        with open(xml, 'w') as f:
            f.write(line)
if __name__ == '__main__':
    print("begin search")
    main()

