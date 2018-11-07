# -*- coding: utf-8 -*-
# @Time    : 2018/5/19 下午4:54
# @Author  : myTool
# @File    : MakeBaseCCBTranslateFile.py
# @Software: PyCharm
'''

    制作 所有ccb 文件里面的东西  此文件只为了  制作 base  版本
    从  english 里面直接 每次都会复制
    不要改代码

'''



from collections import OrderedDict
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import os
import shutil
import re
import xlrd

#TODO 可以修改  默认 是 english
baseCCBPath = "/Users/admin/Documents/ljworkspace/local/cocos/project/pikachu_englishGit/pikachu_english/tools/pikachuCCB/ccb"

baseCCBPath = "/Users/admin/Documents/ljworkspace/local/cocos/project/pikachu_french/pikachu_english/tools/pikachuCCB/ccb"

"警告⚠️ "
#项目路径
ROOTPATH = "/Users/admin/Documents/ljworkspace/local/cocos/project/pikachu_french/"
#工具路径
TOOLSPATH = "/Users/admin/Documents/ljworkspace/local/cocos/test/foreignTools/lan/"
coffee_path = ROOTPATH + 'pikachu_english/app/static/coffee'
json_path = ROOTPATH + 'pikachu_english/app/static/res'
res_path = ROOTPATH + 'pikachu_english/app/static/res/'
ccb_path = ROOTPATH + 'pikachu_english/tools/pikachuCCB/ccb'

####测试
ccb_path = "/Users/admin/Desktop/pikachuCCB_base/ccb"

svnPath = "/Users/admin/Documents/ljworkspace/local/cocos/assets/pikachu/sanguo/"
allPngFntPath = svnPath + "aiweiyou_pokmon/pika_foreign/Font/fnt_png/pngfnt_法语/"
excelFiles=[
    #'/Users/lan/Downloads/历次翻译整理/整理汇总翻译/CCBReplaceEnglish_最终.xls'
    #'/Users/admin/Documents/ljworkspace/local/cocos/assets/pikachu/sanguo/aiweiyou_pokmon/pika_foreign/CCBReplaceEnglish_6.xls'
    "/Users/admin/Documents/ljworkspace/local/cocos/assets/pikachu/sanguo/aiweiyou_pokmon/pika_foreign/ccbTranslate.xls"
]
'''origin pth translate sheetIdx'''
'''1中文 3英文 4俄文 5 越南 6 法语'''
useIdx=[
    [0,1,2,3,4,5]
]
'''当前外文版本'''
#originIdx = 1  #0
'''将要替换到外文版本'''
translateIdx = originIdx= 5 #  2
isOnlyTranslateCCB = False
"警告⚠️ 程序内的艺术字备份会把备份路径内的东西覆盖，请确认程序语言类型 originIdx，一定要正确！"
isNeedBeifen = True
translateTxt = ['chinese','chinese','english','russion',"vietnamese","french"]

def search(path, word):
    for filename in os.listdir(path):
        fp = os.path.join(path, filename)
        if os.path.isfile(fp) and word in filename:
            return fp
        elif os.path.isdir(fp):
            fp = search(fp, word)
            if fp:
                return fp

def replaceOneFile(originText, newText, path):
    if not path:
        return
    with open(path,'r') as r:
        lines=r.readlines()
    strOriginArray = originText.split('\n')
    print('path:',path)
    print('strOrigin:',strOriginArray)
    print("替换文字 " + originText + " ====>> " + newText)
    lastLineTrue = False
    isLastLine = False
    with open(path,'w') as w:
        for l in lines:
            i = 0
            isfind = False
            if len(strOriginArray) > 1:
                for i0 in range(len(strOriginArray)):
                    str = strOriginArray[i0]
                    if l.find(str) >= 0 and str.strip() != '<':
                        isfind = True
                        if i0 == 0:
                            w.write(l.replace(str + '\n', newText))
                        elif str.find('<') < 0:
                            '''不是最后一段匹配'''
                            w.write(l.replace(str + '\n', ''))
                        elif str.strip() != '<':
                            '''规避只有< 的替换'''
                            w.write(l.replace(str, ''))
                        elif str.strip() == '<':
                            '''规避只有< 的替换'''
                            w.write(l.replace(str, ''))
                    elif l.find(str) >= 0 and str.strip() == '<' and lastLineTrue:
                        isfind = True
                        lastLineTrue = False
                        isLastLine = True
                        print('str:',str)
                        w.write(l.replace(str, ''))
            if not isfind:
                lastLineTrue = False
                w.write(l.replace(originText,newText))
            elif not isLastLine:
                lastLineTrue = True


def replaceText(item):
    fileArr = item[1].split(";")
    for file in fileArr:
        print(file)
        if file.endswith(".ccb"):
            path = ccb_path + '/' + file
            if not os.path.exists(path):
                continue
            if item[2] == '' or item[2] == None:
                continue
            replaceOneFile('>' + item[0] + '<', '>' + item[2] + '<', path)
            #可能之前的语言
           # for index in range(len(item)):
            #    if index >= 2:
            #        if  replaceOneFile('>'+item[0]+'<', '>'+item[index]+'<', path):
            #            break
        elif file.endswith(".json"):
            path = search(json_path, file)
            if not path:
                continue
            originText = item[0]
            if originText == '' or originText == None:
                continue
            if len(originText) >= 2:
                replaceOneFile('\''+originText+'\'', '\''+item[2]+'\'', path)
            else:
                replaceOneFile('\"'+originText+'\"', '\"'+item[2]+'\"', path)


def excelReplace(filepth,indexMap):
    table_translate = xlrd.open_workbook(filepth)
    sheet_translate = table_translate.sheet_by_index(indexMap[0])
    nrows_translate = sheet_translate.nrows
    ncols_translate = sheet_translate.ncols
    dataArray = []
    for j in range(nrows_translate):
        if j <= 3:
            continue
        translate = sheet_translate.row_values(j, 0, ncols_translate)
        arrayitem = []
        # index = 0 时 为当前语言 1 为当前ccb   2 为目标语言 剩下的是其他语言
        newndexMapI= indexMap
        instr = str(translate[newndexMapI[originIdx]])
        arrayitem.append(instr)
        if instr.__len__() == 0 :#基础语言为空  用英语  英语还没有 直接跳过
            instr = str(translate[newndexMapI[3]])
            if instr.__len__() == 0:
                continue

        arrayitem.append(str(translate[newndexMapI[2]])) #ccb
        #判断是否存在  不存在则用原来的 不需要替换
        newStr = str(translate[newndexMapI[translateIdx]])
        if newStr.__len__() != 0 :
            # newStr = str(translate[newndexMapI[originIdx]])
            # print "cannot find word translate " + newStr + " to " + str(translateIdx)
            num = str(translate[0])[-2:] == '.0' and str(translate[0])[:-2] or str(translate[0])
            basStr = "ccbTranslate_" + num
            arrayitem.append(basStr)
            dataArray.append(arrayitem)
        #arrayitem.append(newStr)
        #
        # for ind  in newndexMapI :
        #     if ind != originIdx and ind != translateIdx and ind !=1 :
        #         arrayitem.append(str(translate[newndexMapI[ind]]))

    for item in dataArray:
        if item[1] != '':

            replaceText(item)

def copyfile(srcfile,dstfile):
    if not os.path.isfile(srcfile):
        print("%s not exist!"%(srcfile))
    else:
        fpath,fname=os.path.split(srcfile)
        if not os.path.exists(fpath):
            '''创建路径'''
            os.makedirs(fpath)
        '''复制文件'''
        shutil.copyfile(srcfile,dstfile+fname)
        print("copy %s -> %s"%( srcfile,dstfile+fname))

def resetProgectTag():
    fileName = 'makeTranslate.js'
    path = search(ROOTPATH+ 'pikachu_english/app/static/', fileName)
    if not path:
        return
    replaceOneFile('window.languageTs = \''+translateTxt[originIdx]+'\'', 'window.languageTs = \''+translateTxt[translateIdx]+'\'', path)

def GetFileList(dir, fileList):
    newDir = dir
    if os.path.isfile(dir):
        #去掉. 文件
        fpath, fname = os.path.split(dir)
        if fname.split(".")[0] != "":
            fileList.append(dir)
    elif os.path.isdir(dir):
        for s in os.listdir(dir):
            newDir=os.path.join(dir,s)
            GetFileList(newDir, fileList)
    return fileList

def copyFiles(sourceDir, targetDir):  # 把某一目录下的所有文件复制到指定目录中
    if sourceDir.find(".svn") > 0:
        return
    for file in os.listdir(sourceDir):
        sourceFile = os.path.join(sourceDir, file)
        targetFile = os.path.join(targetDir, file)
        if os.path.isfile(sourceFile):
            if not os.path.exists(targetDir):
                os.makedirs(targetDir)
            if not os.path.exists(targetFile) or (
                    os.path.exists(targetFile) and (os.path.getsize(targetFile) != os.path.getsize(sourceFile))):
                if os.path.isfile(targetFile):
                    print("remove ==>> " + targetFile)
                    os.remove(targetFile)
                open(targetFile, "wb").write(open(sourceFile, "rb").read())
                print(sourceFile + " == >>>> " + targetFile)
        if os.path.isdir(sourceFile):
            First_Directory = False
            copyFiles(sourceFile, targetFile)

def removeFileInFirstDir(targetDir):#删除一级目录下的所有文件
    for file in os.listdir(targetDir):
        targetFile = os.path.join(targetDir,  file)
        if os.path.isfile(targetFile):
            print("remove ==>> " + targetFile)
            os.remove(targetFile)


if __name__ == '__main__':
    # ccb 里面的翻译 替换
    #TODO  可以修改  从哪儿 作为base
    #os.system('sh ccbCopy_english.sh')
    removeFileInFirstDir(ccb_path + "/")
    copyFiles(baseCCBPath + "/", ccb_path + "/")
    _fileCount = len(useIdx)
    for _idx in range(_fileCount):
        file = excelFiles[_idx]
        excelReplace(file,useIdx[_idx])
    '''生成ccbi'''
    #os.system('sh '+ ROOTPATH +'pikachu_english/tools/pikachuCCB/bin/openBin/copy_ccb.sh')
    print('ccb替换完毕')
