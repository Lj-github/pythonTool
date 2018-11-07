__author__ = 'lan'

#修改某个ID对应某列的内容

import os
from os.path import join
import re
import xlrd
import xlwt
# import sys
#
# reload(sys)
# sys.setdefaultencoding('utf8')
#

#replaceFile
# filePth = '/Users/lan/Downloads/历次翻译整理/整理汇总翻译/coffeeReplace.xls'
filePth = '/Users/lan/Downloads/历次翻译整理/整理汇总翻译/CCBReplaceEnglish_最终.xls'
# replaceFileList = [
#     '/Users/lan/Downloads/历次翻译整理/整理汇总翻译/coffeeReplace.xls',
#     '/Users/lan/Downloads/历次翻译整理/整理汇总翻译/CCBReplaceEnglish_最终.xls'
# ]

#coffeeReplace  0id 4中文 3英文 5俄文 6越南 7法语
#CCBReplaceEnglish_最终 1.路径 0中文 2英文 3俄文 4.越南 5.法语
# originColum = 0
# translateColum = 5
originColum = 2
translateColum = 3
fileIndexColum = 1

originTxt = 'None'
translateTxt = 'Нет'
fileNameTxt = 'resources/ccb/FormKillReward.ccb'

def writeExcel():
#     replaceFile = '/Users/lan/Downloads/历次翻译整理/整理汇总翻译/cofeeTest.xls'
# fileIdx = [4,1,3,5,0] #中文，路径，英文，俄文，ID

    table_translate = xlrd.open_workbook(filePth)
    table = table_translate.sheet_by_index(0)
    nrows = table.nrows                         # 获取table工作表总行数
    ncols = table.ncols                         # 获取table工作表总列数
    print('rows:',nrows)
    workbook = xlwt.Workbook()  #创建一个excel文件
    newSheet = workbook.add_sheet('sheet0',cell_overwrite_ok=True)

    isFindRestString = False
    for i in range(nrows):
        originTxtValue = table.cell_value(i, originColum)
        isResetString = False
        if originColum == 0:
            if originTxtValue == int(originTxt):
                isResetString = True
                isFindRestString = True
        else:
            if str(originTxtValue) == originTxt:
                isResetString = True
                isFindRestString = True

        for j in range(ncols):
            if j == translateColum and isResetString:
                print('changeRwo:',i)
                print('old_value:',table.cell_value(i, j))
                print('new_value:',translateTxt)
                newSheet.write(i, j, translateTxt)
            elif fileIndexColum and fileIndexColum >= 0 and j == fileIndexColum and isResetString:
                filename = fileNameTxt.split('/')[-1:][0]
                fileStr = table.cell_value(i, j)
                print('fileList_Old:',fileStr)
                if fileStr.find(filename) >= 0:
                    newSheet.write(i, j, fileStr)
                    print('fileList_New:',fileStr)
                else:
                    newSheet.write(i, j, fileStr+';'+filename)
                    print('fileList_New:',fileStr+';'+filename)
            else:
                ncell_value1 = table.cell_value(i, j)
                newSheet.write(i, j, ncell_value1)
    if not isFindRestString and originColum > 0:
        newSheet.write(nrows, originColum, originTxt)
        if fileIndexColum and fileIndexColum >= 0:
            filename = fileNameTxt.split('/')[-1:][0]
            newSheet.write(nrows, fileIndexColum, filename)
        newSheet.write(nrows, translateColum, translateTxt)
        print('newLine:',filename,'originTxt:',originTxt,'translateTxt:',translateTxt)
    workbook.save(filePth)

if __name__ == "__main__":
    try:
        writeExcel()

        print('处理完毕！')

    except Exception as e:
        print("异常" + e)
