# -*- coding: utf-8 -*-
# @Time    : 2018/5/19 下午5:44
# @Author  : myTool
# @File    : doTranslateCCB.py
# @Software: PyCharm

'''法语版   通过ccb excel 替换 ccb 里面的文字 如果没有  则直接使用英文的 '''


import sys
import os
import shutil
import re
import xlrd
import os
import os.path
import shutil

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


baseCCBPath = "/Users/admin/Desktop/pikachuCCB_base/ccb"

svnPath = "/Users/admin/Documents/ljworkspace/local/cocos/assets/pikachu/sanguo/"
allPngFntPath = svnPath + "aiweiyou_pokmon/pika_foreign/Font/fnt_png/pngfnt_法语/"
excelFiles=[
    #'/Users/lan/Downloads/历次翻译整理/整理汇总翻译/CCBReplaceEnglish_最终.xls'
    '/Users/admin/Documents/ljworkspace/local/cocos/assets/pikachu/sanguo/aiweiyou_pokmon/pika_foreign/ccbTranslate.xls'
]
'''origin pth translate sheetIdx'''
'''1中文 3英文 4俄文 5 越南 6 法语'''
useIdx=[
    [0,1,2,3,4,5,6]
]
'''1中文 3英文 4俄文 5 越南 6 法语'''
'''基础替换字符串 '''
originIdx =  "ccbTranslate_"  #  后面 需要添加id
'''将要替换到外文版本  !!!!!  '''

translateIdx = 6

isOnlyTranslateCCB = False
"警告⚠️ 程序内的艺术字备份会把备份路径内的东西覆盖，请确认程序语言类型 originIdx，一定要正确！"
isNeedBeifen = True
translateTxt = ["",'chinese','chinese','english','russion',"vietnamese","french"]

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
    print("替换文字 " +  originText + " ====>> " + newText)
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

# def sqlReplace():
#     '''获取数据库连接'''
#     conn=pymysql.connect(host='localhost',user='root',password='',db='russionFont',port=3306,charset='utf8')
#     '''获取一个游标'''
#     cur=conn.cursor()
#     '''limit 10 #where isSpecial=0'''
#     cur.execute('select * from english_0506 order by LENGTH(originText) DESC ')
#     data=cur.fetchall()
#     '''遍历输出'''
#     arr = []
#     for d in data:
#         fields = (str(d[1]), str(d[originIdx]), str(d[translateIdx]))
#         arr.append(fields)
#     '''释放游标'''
#     cur.close()
#
#     for item in arr:
#         print('item[0]:' + item[0] + ',item[1]:' + item[1] + ',item[2]:' + item[2] )
#         if item[0] == '' or item[0] == None:
#             continue
#         else:
#             replaceText(item)
#     '''释放资源'''
#     conn.close()

def excelReplace(filepth,indexMap):
    table_translate = xlrd.open_workbook(filepth)
    sheet_translate = table_translate.sheet_by_index(indexMap[0])
    nrows_translate = sheet_translate.nrows
    ncols_translate = sheet_translate.ncols
    dataArray = []
    for j in range(nrows_translate):
        if j <= 0:
            continue

        ##
        translate = sheet_translate.row_values(j, 0, ncols_translate)
        arrayitem = []
        # index = 0 时 为当前语言 1 为当前ccb   2 为目标语言 剩下的是其他语言
        newndexMapI= indexMap

        num = str(translate[0])[-2:] == '.0' and str(translate[0])[:-2] or str(translate[0])

        instr =  originIdx +  num
        arrayitem.append(instr)
        if instr.__len__() == 0 :#基础语言为空 没的替换 直接跳过
            continue
        arrayitem.append(str(translate[newndexMapI[2]])) #ccb
        #判断是否存在  不存在则用原来的 不需要替换
        newStr = str(translate[newndexMapI[translateIdx]])
        if newStr.__len__() != 0 :
            # newStr = str(translate[newndexMapI[originIdx]])
            # print "cannot find word translate " + newStr + " to " + str(translateIdx)
            arrayitem.append(newStr)
            dataArray.append(arrayitem)
        else:
            print(str(j) + "为 空")
            ''' 如果为空  写入 英文  3  '''
            newStr = str(translate[newndexMapI[3]])
            arrayitem.append(newStr)
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



def run():
    # 先将 基础版本的  复制过来
    removeFileInFirstDir(ccb_path+ "/")
    copyFiles(baseCCBPath + "/", ccb_path + "/")

    # ccb 里面的翻译 替换
    _fileCount = len(useIdx)
    for _idx in range(_fileCount):
        file = excelFiles[_idx]
        excelReplace(file, useIdx[_idx])
    '''生成ccbi'''
    os.system('sh '+ ROOTPATH +'pikachu_english/tools/pikachuCCB/bin/openBin/copy_ccb.sh')
    print('ccb替换完毕')

    # if not isOnlyTranslateCCB:
    # print("do")
    # resetProgectTag()
    # print('程序语言标志替换完毕',translateIdx)
    # 替换所有图片资源
    # if translateIdx == 2:
    #     os.system('sh '+TOOLSPATH +'DataCopyPK_yuenan.sh')
    #     os.system('sh '+TOOLSPATH +'updateAllSrc_english.sh')
    # elif translateIdx == 3:
    #     os.system('sh '+TOOLSPATH +'DssataCopyPKen_Russion.sh')
    #     os.system('sh '+TOOLSPATH +'updateAllSrc_yuenan.sh')
    # elif translateIdx == 0:
    #     '''这里应该不会回退到中文版本，只是在前期测试使用'''
    #     os.system('sh '+TOOLSPATH +'DataCopyPK_Chinese.sh')
    #     os.system('sh '+TOOLSPATH +'updateAllSrc_chinese.sh')
    #
    #  # 替换越南
    # elif translateIdx == 4 :
    #     os.system('sh ' + TOOLSPATH + '/yuenantools/DataCopyPK_yuenan.sh')
    #     os.system('sh ' + TOOLSPATH + '/yuenantools/updateAllSrc_yuenan.sh')
    # #替换法语
    # elif translateIdx == 5 :
    #     #os.system('sh ' + TOOLSPATH + '/french/DataCopyPK_french.sh')
    #     os.system('sh ' + TOOLSPATH + '/french/updateAllSrc_french.sh')

    #
    # print('图片资源 数据替换完毕')
    #
    # '''备份程序使用中的字体文件'''
    # desPth = ROOTPATH+ 'pikachu_english/tools/pikachuFontAndPlist/Font'
    # filePth1 =  TOOLSPATH #'/Users/lan/resBin/english/'
    # fontPth = 'Font_english/'
    # outPth = 'Out_english/'
    # if originIdx == 3:
    #     fontPth = 'Font_russion/'
    #     outPth = 'Out_russion/'
    # elif originIdx == 0:
    #     fontPth = 'Font_chinese/'
    #     outPth = 'Out_chinese/'
    # pthSrc1 = filePth1 + fontPth
    # '''先删除原文件夹才能拷贝'''
    # if os.path.exists(pthSrc1):
    #
    # if isNeedBeifen:
    #     '''备份工具文件'''
    #     shutil.copytree(desPth, pthSrc1)
    #     filepth = ROOTPATH +  'pikachu_english/tools/pikachuFontAndPlist/Out/'#'/Users/lan/clientprojects/pikachu_english/tools/pikachuFontAndPlist/Out/'
    #     '''备份 文件fnt png'''
    #     print(filepth + ' To ' + filePth1 + outPth)
    #     for filename in os.listdir(filepth):
    #         if filename.endswith(".fnt"):
    #             path = filepth + filename
    #             if not os.path.exists(path):
    #                 shutil.copyfile(path,filePth1 + outPth + filename)
    #                 fileRealNameArray = filename.split('.')
    #                 fileRealName = fileRealNameArray[0] + '.png'
    #                 shutil.copyfile(filepth + fileRealName,filePth1 + outPth + fileRealName)
    # '''目的文件'''
    # filepth2 = svnPath  + "aiweiyou_pokmon/pika_foreign/Font/fnt_png/pngfnt_越南/"  #'/Users/lan/resBin/english/
    # fontPth2 = 'Font_english/'
    # outPth2 = 'Out_english/'
    # if translateIdx == 3:
    #     fontPth2 = 'Font_russion/'
    #     outPth2 = 'Out_russion/'
    # elif translateIdx == 0:
    #     fontPth2 = 'Font_chinese/'
    #     outPth2 = 'Out_chinese/'
    #
    # #目前只考虑越南
    # elif translateIdx == 4 :
    #     fontPth2 = ''
    #     outPth2 = 'Out_chinese/'
    #
    # pthSrc2 = filepth2+fontPth2
    #
    # if os.path.exists(desPth):
    #     shutil.rmtree(desPth)
    #
    # shutil.copytree(pthSrc2, desPth)
    # pthOut = filepth2 + outPth2
    # print(pthOut + ' To ' + filepth)
    # for filename in os.listdir(pthOut):
    #     if filename.endswith(".fnt"):
    #         path = pthOut + filename
    #         shutil.copyfile(path,filepth + filename)
    #         fileRealNameArray = filename.split('.')
    #         fileRealName = fileRealNameArray[0] + '.png'
    #         if os.path.exists(pthOut + fileRealName):
    #             shutil.copyfile(pthOut + fileRealName,filepth + fileRealName)
    #         print(filename,' ; ',fileRealName)
    #

    # 复制png  fnt
    #
    # allpngFntList = GetFileList(allPngFntPath,[])
    # toolPath = "/Users/admin/Documents/ljworkspace/local/cocos/project/pikachu_french/pikachu_english/tools/pikachuCCB/ui/actorLevelUp.png"
    # toolPath2 = "/Users/admin/Documents/ljworkspace/local/cocos/project/pikachu_french/pikachu_english/tools/pikachuCCB/font/fnt_purple.png"
    #
    # print("png fnt 替换完成")

    # '''执行脚本文件 plist fnt'''
    # binPth = ROOTPATH + 'pikachu_english/tools/pikachuFontAndPlist/bin'
    # for root, dirs, files in os.walk(binPth):
    #     for OneFileName in files:
    #         if OneFileName.find('.sh') > 0:
    #             os.system('sh ' + os.path.join(root, OneFileName))
    #             print("run "  + OneFileName)
    # print('脚本文件执行完毕')

    # os.system('sh '+ TOOLSPATH  + "/yuenantools/" +'make_all_plist_yuenan.sh')
    #
    # #复制plist
    # os.system('sh '+ TOOLSPATH  + "/yuenantools/" +'PlistCopyPK_yuenan.sh')
    # print('font资源替换完毕')


if __name__ == '__main__':

    # root = Tkinter.Tk()
    # root.title('提示')  # 窗口标题
    # root.resizable(False, False)  # 固定窗口大小
    # windowWidth = 320 # 获得当前窗口宽
    # windowHeight = 200  # 获得当前窗口高
    # screenWidth, screenHeight = root.maxsize()  # 获得屏幕宽和高
    # geometryParam = '%dx%d+%d+%d' % (
    # windowWidth, windowHeight, (screenWidth - windowWidth) / 2, (screenHeight - windowHeight) / 2)
    #
    # import tkMessageBox
    # def cancleCB():
    #     print("cancle")
    #     sys.exit()
    #     #tkMessageBox.showinfo("tip", "cancle Run")
    # def confCB():
    #     print("run")
    #     run()
    # BtnCancle = Tkinter.Button(root, text="取消执行", command=cancleCB)
    # BtnCancle.pack()
    # BtnConfirm =Tkinter.Button(root, text="执行", command=confCB)
    # BtnConfirm.pack()
    # root.geometry(geometryParam)  # 设置窗口大小及偏移坐标
    # root.mainloop()

    run()

