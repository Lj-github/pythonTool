__author__ = 'lan'
__author__ = 'lan'
"""
3.需要替换完成后删除相应项目，或者添加已处理标记
俄文版替换错误例子：_DigGemRsps = ["DigBaoshiRsp", "DigHighBaoshiRsp", "DigTopLevelBaoshiRsp"] 替换了Dig

LayerSelectHero.coffee Grass
ChessStep.coffee Grass

"""
'''替换翻译 改成程序读json'''

import pymysql
from collections import OrderedDict
import os
import fileinput
import re
import xlrd
import  xlwt

ccb_path = '/Users/lan/clientprojects/pikachu_english/tools/pikachuCCB/ccb'

excelFiles=[
    '/Users/lan/sanguo/aiweiyou_pokmon/pika_foreign/ccbTranslate.xls'
]

ccbLblXlsPth = '/Users/lan/Downloads/Language/英文/ccbLbl/'

textKeyWords = ['CCLabelBMFont','CCLabelTTF']

'''Id filepth char originTxt(4.中文 3。英文 5。俄文)'''
'''originTxt 当前程序语言'''
useIdx=[
    [0,1,2,4,0]
]

def search(path, word):
    for filename in os.listdir(path):
        fp = os.path.join(path, filename)
        if os.path.isfile(fp) and word in filename:
            return fp
        elif os.path.isdir(fp):
            fp = search(fp, word)
            if fp:
                return fp
def reSetLblDisplayName(pth,ccbName):
    if not pth:
        return
    with open(pth,'r',32,'utf-8') as r:
        lines=r.readlines()


    with open(pth,'w',32,'utf-8') as w:
        isLabel = 0
        islblName = False
        lblIndex = 0
        for l in lines:
            if l.find('<key>baseClass</key>') > 0:
                isLabel = 0
            if (l.find('<string>CCLabelTTF</string>') > 0 or l.find('<string>CCLabelBMFont</string>') > 0) and isLabel == 0:
                print('find:',l.find('<string>CCLabelTTF</string>'))
                print('findCCLabelBMFont:',l.find('<string>CCLabelBMFont</string>'))
                isLabel = 1
                w.write(l)
                continue

            if (isLabel == 0):
                w.write(l)
                continue

            if l.find('<key>displayName</key>') > 0:
                islblName = True
                w.write(l)
                continue
            print('l:',islblName,l)

            if (islblName):
                if l.find('<string>CCLabelTTF</string>') >= 0:
                    w.write(l.replace('CCLabelTTF','CCLabelTTF'+str(lblIndex)))
                    print('ccbName:',ccbName)

                elif l.find('<string>CCLabelBMFont</string>') >= 0:
                    w.write(l.replace('CCLabelBMFont','CCLabelBMFont'+str(lblIndex)))
                else:
                    w.write(l)
                lblIndex = lblIndex + 1
                islblName = False
                isLabel = 0
            else:
                w.write(l)





try:
    # _fileCount = len(useIdx)
    # print('_fileCount:',_fileCount)
    # for _idx in range(_fileCount):
    #     print('_idx:',_idx)
    #     file = excelFiles[_idx]
    #     print('file:',file)
    #     print(file,useIdx[_idx])
    #     excelReplace(file,useIdx[_idx])

    for root, dirs, files in os.walk(ccb_path):
        for OneFileName in files:
            if OneFileName.find('.ccb') == -1:
                continue

            reSetLblDisplayName(os.path.join(root, OneFileName),OneFileName)




except Exception as e:
    print("异常"+e)