# -*- coding: utf-8 -*-
'''
    提前下载线上重要文件
    html
    resource.js
    main.js
    安装webp
    brew install webp    ||   npm install cwebp -g
    支持更新三个scriptjs 文件
    支持更新 sdkjs 文件

    支持更新mainjs  本地打包后直接更新到线上
    支持更新 引擎文件 game.min.js  可配置  需要提前生成新的引擎文件 更新只是上传 本地打包后直接更新到线上
    支持更新 翻译文件 translate js 自动对比

    error  : Host key verification failed.
    在控制台执行 ssh name@host -p port -A
    添加 webp size  和 png size 比较

'''
import execjs
import json
import io
import hashlib
import shutil
import binascii
import os
import datetime
import LoadConfig as Update_joyfun
import sys
import copy
import uuid
import deploy.makeMainjs as makemainjs
# reload(sys)
# sys.setdefaultencoding('utf-8')

'''  res 资源 生成时候 需要过滤的  后缀 || 文件名  '''

resFilterHouZui = ["css"]
''' 不要md5 的资源 '''


resFilterFileName = ["hengpingqiehuan","ditu000","GonggaoDef","dld_wjj1","clickRefresh",
                     "dtl_dddt","denglut_nilt2","denglut_nilt1","game_logo","dcagent.v2.min","startCheck","sdkCheck"]



# 是否更新js 文件  如果更新js 文件 则会直接打包本地mainjs
isUpdateMainJS = False
# 是否一键直接更新到线上 否  则会打印出shell 语句  直接在命令行执行即可完成更新
isOneKeyUpdate = True
# 打包mainjs 格式 isDebug  debug模式  会打开log  等
''' 线上版本需要变为 False  测试版本为 True '''
isDebugMainJS = False
''' 是否更新引擎文件 !!!  默认不更新 |||  直接更新 不下载  需要提前做好 引擎文件 game.min.js'''
isUpdateEngine = False


configJSONFIle = "server.json"


def getConfig():
    filee = os.path.realpath(__file__)
    fpath,fname = os.path.split(filee)
    sdkType = fname.split(".")[0].split("_").pop()

    if not sdkType:
        print("no sdk type init = >> " + sdkType)
        return None

    with open(configJSONFIle, 'r') as f:
        sdkJson = json.load(f)
        if not sdkType in sdkJson:
            print("配置文件中不存在 sdktype  = >> " + sdkType)
            return None

        return sdkJson[sdkType]




filee = os.path.realpath(__file__)
projectToolPath, projectToolName = os.path.split(filee)
projectFile = filee[0:filee.find("app/update")] + "app/static/"
print("项目static 路径 ====>>> " + projectFile)

'''#########           js文件读取 写入          #########'''

def get_js(jsFile):
    f = io.open(jsFile, "r", encoding='utf-8')
    line = f.readline()
    htmlstr = ''
    while line:
        htmlstr = htmlstr + line
        line = f.readline()
    return htmlstr


def jsStrTOTable(jsStr):
    addedFunStr = "function getWindow() {var window = {};window.document = {};" + jsStr + "; return window}"
    ctx = execjs.compile(addedFunStr)
    allObj = ctx.call('getWindow')
    return allObj


# 制作最终js str
def exportFinallResourceJS(allObj, fileName):
    windowmd5_resource = allObj["md5_resource"]
    windowdocumentccConfig = allObj["document"]["ccConfig"]
    windownoWebpImages = allObj["noWebpImages"]
    windowmd5_resourceStr = "window.md5_resource = " + json.dumps(windowmd5_resource)
    windowdocumentccConfigStr = "window.document.ccConfig = " + json.dumps(windowdocumentccConfig)
    windownoWebpImagesStr = " window.noWebpImages = " + json.dumps(windownoWebpImages)
    fpath, fname = os.path.split(fileName)
    if not os.path.exists(fpath):
        '''创建路径'''
        mkdir(fpath)
    with open(fileName, 'w') as f:
        f.write(windowmd5_resourceStr + "\n" + windowdocumentccConfigStr + "\n" + windownoWebpImagesStr)


# allObj = jsStrTOTable(jsStr)
# exportFinallResourceJS(allObj, filename)
'''#########           md5 获取  6为字符串获取       #########'''


def shortMD5(md5):
    chars = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j",
             "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v",
             "w", "x", "y", "z", "0", "1", "2", "3", "4", "5", "6", "7",
             "8", "9", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J",
             "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V",
             "W", "X", "Y", "Z"]
    sTempSubString = md5[8:16]
    lHexLong = 0x3FFFFFFF & int(sTempSubString, 16);
    outChars = "";
    for i in range(0, 6):
        index = 0x0000003D & lHexLong
        outChars = outChars + chars[index]
        lHexLong = lHexLong >> 5
    return outChars


def get_file_md5(file_path):
    if not os.path.isfile(file_path):
        return
    myhash = hashlib.md5()
    f = open(file_path, 'rb')
    while True:
        b = f.read(8192)
        if not b:
            break
        myhash.update(b)
    f.close()
    return myhash.hexdigest()


'''#########           获取所有res文件夹下md5     //更新资源  #########'''


def GetFileList(dir, fileList):
    newDir = dir
    if os.path.isfile(dir):
        fileList.append(dir.decode('utf-8'))
    elif os.path.isdir(dir):
        for s in os.listdir(dir):
            newDir = os.path.join(dir, s)
            GetFileList(newDir, fileList)
    return fileList


def pathAddMd5Str(filePath, md5):  # 是否需要提前截取filePath
    fpath, fname = os.path.split(filePath)
    fType = fname.split(".").pop()
    fname = fname.replace("." + fType, "_" + md5 + "." + fType)
    return filePath, fpath + "/" + fname


"""
复制文件到需要更新的目录并且做好webp
"""


def copyAllResFileAndMakeWebP(oldpath, newPath, isNeedMakeWebP):
    copyfile(oldpath, newPath)
    path, fname = os.path.split(oldpath)
    fType = fname.split(".").pop()
    if fType == "png" or fType == "jpg":
        if isNeedMakeWebP:
            shShell = 'cwebp -mt -quiet ' + oldpath + ' -o ' + newPath.replace(fType, "webp")
            print('make webP  Shell:', shShell)
            try:
                os.system(shShell)
            except Exception as e:
                print("error " + e)


def mkdir(path):
    path = path.strip()
    path = path.rstrip("\\")
    isExists = os.path.exists(path)
    if not isExists:
        os.makedirs(path)
        return True
    else:
        return False


def copyfile(srcfile, dstfile):
    if not os.path.isfile(srcfile):
        print("%s not exist!" % (srcfile))
    else:
        fpath, fname = os.path.split(dstfile)
        if not os.path.exists(fpath):
            '''创建路径'''
            mkdir(fpath)
        '''复制文件'''
        shutil.copyfile(srcfile, dstfile)
        print("copy %s -> %s" % (srcfile, dstfile))


def getDataStr():
    today = datetime.datetime.now()
    ISOFORMAT = '%Y%m%d'
    return today.strftime(ISOFORMAT)[2:] + "%s" % today.hour + "%s" % today.second


def makeLoaclNoWebpImagesTable(oldTable):
    newTable = {}
    for nam in oldTable:
        newName = nam[:-7]
        newTable[newName] = oldTable[nam]
    return newTable


def getPathByFileName(allTable, fileName):
    for fileNa in allTable:
        if fileNa == fileName:
            return True
    return False


def getPathStrValueByFileName(allTable, fileName):
    for fileNa in allTable:
        if fileNa.find(fileName) > -1:
            return allTable[fileNa]
    return ""

def getPathStrKeyByFileName(allTable, fileName):
    for fileNa in allTable:
        if fileNa.find(fileName) > -1:
            return fileNa
    return ""


def del_file(path):
    for i in os.listdir(path):
        path_file = os.path.join(path, i)
        if os.path.isfile(path_file) :
            if path_file.find("html") <= -1:
                os.remove(path_file)
        else:
            del_file(path_file)


def mergeMainJS(oldMainJSFile, newMaisJSFile):
    print("合并main  js")
    # oldMainJSStr = get_js(oldMainJSFile)
    # newMainJSStr = get_js(newMaisJSFile)
    oldf = io.open(oldMainJSFile, "r", encoding='utf-8')
    line = oldf.readline()
    htmlstr = ''
    while line:
        htmlstr = htmlstr + line
        line = oldf.readline()
        if line.find("//cc.game.run()") > -1:
            htmlstr = htmlstr + line
            break
        '''  从 //cc.game.run(); 开始 取新的js 文件 里面的压缩内容   '''
    oldf.close()
    newf = io.open(newMaisJSFile, "r", encoding='utf-8')
    line = newf.readline()
    isFindCCGAMERUN = False
    while line:
        if isFindCCGAMERUN:
            htmlstr = htmlstr + line
        if line.find("//cc.game.run()") > -1:
            isFindCCGAMERUN = True
        line = newf.readline()
    newf.close()
    return htmlstr


def getStrFromFile(str, file):
    f = io.open(file, "r", encoding='utf-8')
    line = f.readline()
    findStr = ''
    while line:
        if line.find(str) > -1:
            findStr = line
            break
        line = f.readline()

    return findStr

## 判断文件中是否包括字符串
def isInclodeStrFromPath(file,str):
    f = io.open(file, "r", encoding='utf-8')
    line = f.readline()
    while line:
        if line.find(str) > -1:
            f.close()
            return True
        line = f.readline()
    f.close()
    return False
# 在list 里面 是否有str

def isIncludeInList(list,str):
    for i in list:
        if i.find(str)>-1:
            return True
    return False
'''  正在遍历的 table  不能修改 需要转换为list   '''
def delKeyByKeyStrFromDir(allTable,str):
    for fileNa in list(allTable.keys()):
        if fileNa[:-7] == str:
            del allTable[fileNa]
            print("删除 旧的 不需要 生成 webp 资源名字 == >>" + fileNa)

'''  判断需要的dir  是否存在  创建等   '''

def create_Base_File():
    serverFilePath = os.path.dirname(__file__) + "/serverFile/"
    if not os.path.isdir(serverFilePath):
        mkdir(serverFilePath)
    doUpdateFilePath = os.path.dirname(__file__) + "/doUpdateFile/"
    if not os.path.isdir(doUpdateFilePath):
        mkdir(doUpdateFilePath)
    fileDirPath = os.path.dirname(__file__) + "/file/"
    if not os.path.isdir(fileDirPath):
        mkdir(fileDirPath)


''' 添加 gz 压缩 nginx 使用 gz压缩文件  status 目录下全部都应该压缩  '''


def makeGzFile(filePath):
    allFileNeedGzList = GetFileList(filePath,[])
    for pgz in allFileNeedGzList:
        gzSh = "gzip -c " + pgz + " > " + pgz + ".gz"
        # 压缩 使用命令
        os.system(gzSh)
        print("gzFile = > " + pgz + ".gz")

if __name__ == '__main__':
    create_Base_File()

    sdkConfig = getConfig()

    uuidMd5 = shortMD5(str(uuid.uuid3(uuid.NAMESPACE_DNS, 'python')).replace("-", ""))
    if not sdkConfig:
        exit(0)
    if not sdkConfig.get("key_file_" + uuidMd5):
        print("填写ssh 公钥 路径")
    ''' 填写默认信息  '''
    # 就是类是 俄服 内部测试服务器  ！ 去掉
    testServerConfig = Update_joyfun.serverConfig()
    liveServerConfir = Update_joyfun.serverConfig()
    liveServerConfir.host = sdkConfig.get("host") # '185.236.180.146'
    liveServerConfir.key_file = sdkConfig.get("key_file_" + uuidMd5)  # '/Users/admin/.ssh/id_rsa'
    liveServerConfir.port = int(sdkConfig.get("port"))  #  2202
    liveServerConfir.username = sdkConfig.get("username")  # 'pikachuadmin'
    liveServerConfir.staticFile = sdkConfig.get("staticFile")  #'/easygame/pikachu/gameweb/static/'
    liveServerConfir.gameHtmlFile = sdkConfig.get("gameHtmlFile")  #"/easygame/pikachu/gameweb/game.html"


    ''' 同意时间字符串   '''
    dataStr = getDataStr()
    print("清理文件目录 serverFile  doUpdateFile  开始 ( 保证 每次都是最新的  )")
    del_file(os.path.dirname(__file__) + "/serverFile/")
    del_file(os.path.dirname(__file__) + "/doUpdateFile/")
    print("serverFile  doUpdateFile 文件夹清理完毕")
    print("开始下载 相关 js html 等 文件...")
    Update_joyfun.loadHtml(testServerConfig, liveServerConfir)
    gameFileNameP, gameFileNameF = os.path.split(liveServerConfir.gameHtmlFile)
    gameFileNameFAnd = "serverFile/" + gameFileNameF
    if os.path.isfile(gameFileNameFAnd ):
        oldMainjsNameStr = getStrFromFile("main_", gameFileNameFAnd).split("/static/").pop().split("js")[0]+"js"
        oldResoiurcejsNameStr = getStrFromFile("resource_", gameFileNameFAnd).split("/static/").pop().split("js")[0] + "js"
        liveServerConfir.oldMainjsNameStr = oldMainjsNameStr
        liveServerConfir.oldResoiurcejsNameStr = oldResoiurcejsNameStr

    Update_joyfun.run(testServerConfig, liveServerConfir)
    print("相关 文件 下载完成 ...")

    if isUpdateMainJS:
        print("开始打包mainjs")
        makeMain = makemainjs.makeMainjs(isDebugMainJS)
        makeMain.startRun()
        print("打包mainjs 完成")
        print("合并 mainjs  开始  ")
        liveMaisJSFile = Update_joyfun.getLocalPathByDir_Name("doUpdateFile/", "main")
        oldMainJSFile = Update_joyfun.getLocalPathByDir_Name("serverFile/", "main")  # 正式线上的
        newMainJSStr = mergeMainJS(oldMainJSFile, liveMaisJSFile)
        newMainJsFileName = "file/" + dataStr + "/static/" + oldMainJSFile.split("/").pop().split(".")[
            0][0:11] + "_" + dataStr + ".js"
        fMainJSpath, fMainJSname = os.path.split(newMainJsFileName)
        if not os.path.exists(fMainJSpath):
            mkdir(fMainJSpath)
        with open(newMainJsFileName, 'w') as f:
            f.write(newMainJSStr)
        print("合并 mainjs  完成  新的js文件  ==>> " + "" + newMainJsFileName)
        print("修改 html 中main js 替换 " + liveMaisJSFile.split("/").pop() + " ===>>  " + "" + newMainJsFileName.split("/").pop())
        ''' mac 和linux 不一样 先获取main_ 所在行数的内容 '''
        oldMainStr = getStrFromFile("main_", gameFileNameFAnd).split("/static/").pop().split("js")[0]
        newMainStr = oldMainJSFile.split("/").pop().split(".")[0][0:11] + "_" + dataStr + "."
        sedShell = 'sed -i ""  "s/' + oldMainStr + '/' + newMainStr + '/g" ' + gameFileNameFAnd
        os.system(sedShell)
        print(" html 中main js 替换 完成 ")
    print("开始执行 md5 对比 ...")
    uiFile = projectFile
    allFileList = GetFileList(uiFile + "res", [])
    allDir = {}
    for fileN in allFileList:
        fpath, fname = os.path.split(fileN)
        if fname[0] == ".":
            continue
        md5_6_Str = shortMD5(get_file_md5(fileN))
        filePath, mdPath = pathAddMd5Str(fileN[fileN.find("/static/") + len("/static/"):], md5_6_Str)
        allDir[filePath] = mdPath
    res_Obj = allDir
    reaourceOldPath = Update_joyfun.getLocalPathByDir_Name("serverFile/", "resource")
    # reaourceOldPath = "serverFile/tes.js"
    # filename = 'write_data.js'
    jsStr = get_js(reaourceOldPath)
    allReaourceOld = jsStrTOTable(jsStr)
    windowmd5_resource = allReaourceOld["md5_resource"]
    windowdocumentccConfig = allReaourceOld["document"]["ccConfig"]
    if 'noWebpImages' not in allReaourceOld:
        allReaourceOld["noWebpImages"] = {}
    windownoWebpImages = allReaourceOld["noWebpImages"]
    needUpdataRES = {}
    ## 修改noWebpImages里面的字段  去掉md5 字段
    localNoWebpImagesTable = makeLoaclNoWebpImagesTable(allReaourceOld["noWebpImages"])
    newnoWebpImagesTable = copy.deepcopy(allReaourceOld["noWebpImages"])
    ''' 对比 res 里面所有的文件md5 '''
    for path in res_Obj:

        ''' 排除需要过滤的 '''
        pdPath, pdName = os.path.split(path)
        houzui = pdName.split(".").pop()
        if houzui in resFilterHouZui:
            windowmd5_resource[path] = path
            continue
        filePDName = pdName.split(".")[0]
        isFind = False
        for pdNameOne in resFilterFileName:
            if pdNameOne == filePDName:
                isFind = True
        if isFind:
            windowmd5_resource[path] = path
            continue

        if not windowmd5_resource.has_key(path):
            needUpdataRES[path] = res_Obj[path]
            continue
        if windowmd5_resource[path] != res_Obj[path]:

            needUpdataRES[path] = res_Obj[path]
    print("开始复制新的 md5 文件 ...")
    for fi in needUpdataRES:
        path, fname = os.path.split(fi)
        fType = fname.split(".").pop()
        localName = uiFile + fi  # + path+ "/" +  [:-7] + "." + fname
        isNeedMakeWebP = not getPathByFileName(localNoWebpImagesTable, fname.split(".")[0])
        # add 180808  如果是不需要做webp  并且 需要更新  那就需要吧 localNoWebpImagesTable 里买的md5 值  替换了  用新的
        if not isNeedMakeWebP:
            fType = fname.split(".").pop()
            if fType == "png" or fType == "jpg":
                md5fpath,md5fname = os.path.split(needUpdataRES[fi])
                delKeyByKeyStrFromDir(newnoWebpImagesTable, fname.split(".")[0])
                newnoWebpImagesTable[md5fname.split(".")[0]] = 1

        copyAllResFileAndMakeWebP(localName, "file/" + dataStr + "/static/" + needUpdataRES[fi], isNeedMakeWebP)
        ''' 如果 需要   webp  通过webp 文件的大小  和 png 图片大小做比较  如果  webp 的大小 大于 png 的 1/2  则不需要再使用webp 打包  但是也会上传 避免出错...  '''
        if isNeedMakeWebP:
            pngFIle = "file/" + dataStr + "/static/" + needUpdataRES[fi]
            fp, fn = os.path.split(pngFIle)
            ft = fn.split(".").pop()
            if ft == "png" or ft == "jpg":
                pngSize = os.path.getsize(pngFIle)
                webpSize = os.path.getsize(pngFIle.replace(ft, "webp"))
                if webpSize * 2 > pngSize:
                    md5fpath, md5fname = os.path.split(needUpdataRES[fi])
                    delKeyByKeyStrFromDir(newnoWebpImagesTable, fname.split(".")[0])
                    newnoWebpImagesTable[md5fname.split(".")[0]] = 1

    print("需要更新的文件列表生成...")
    # 几个js 单独处理
    # "static/script/commons/Constants_B7V3Iz.js",
    # "static/script/commons/LocalizeContext_fAr2m2.js",
    # "static/script/net/GameProtocol_VVBnQr.js"
    oldjsList = windowdocumentccConfig["jsList"]
    ## 判断js 是否需要更新 生成 md5 js 文件
    allJSList = GetFileList(uiFile + "script", [])
    allJSTable = {}
    for fileN in allJSList:
        fpath, fname = os.path.split(fileN)
        if fname[0] == ".":
            continue
        if fname.split(".").pop() == "map":
            continue
        #如果有 则删除 没有就不删了
        compStr = fileN.replace(projectFile,"").split(".")[0]
        if isIncludeInList(oldjsList,compStr  ):
            if isInclodeStrFromPath(fileN,"//# sourceMappingURL"):
                print("删除Map link")
                deleteMapLinkShell = "sed -i '' '$d' " +fileN
                print("删除Map link shell =>" + deleteMapLinkShell)
                os.system(deleteMapLinkShell)
        md5_6_Str = shortMD5(get_file_md5(fileN))
        filePath, mdPath = pathAddMd5Str(fileN[fileN.find("/static/") + len("/static/"):], md5_6_Str)
        allJSTable[filePath] = mdPath
    """ resource里面 jsList 替换  """
    # exportFinallResourceJS(allObj, filename)

    '''  生成新的 resource 文件  '''
    newResourceTable = copy.deepcopy(allReaourceOld)
    finalResourceMd5Obj = copy.deepcopy(windowmd5_resource)
    for path in needUpdataRES:
         finalResourceMd5Obj[path] = needUpdataRES[path]

    '''  jsList 处理 只有三个 读取旧的 由于 script js 里面的文件 有map 文件对应  文件最后一行会多一句注释 需要提前删除后才能获取md5 '''
    print("处理三个js 文件 window.document.ccConfig.jsList ")



    newJsList = []
    for js in oldjsList:
        localNameStr = js.split("/").pop().split(".")[0][:-7]
        newJS = getPathStrValueByFileName(allJSTable, localNameStr)
        newJSKey = getPathStrKeyByFileName(allJSTable, localNameStr)

        newContentJsName = newJS.split("/").pop()
        oldContentJsName = js.split("/").pop()
        if newContentJsName != oldContentJsName:
            newJsList.append("static/" + newJS)
        else:
            newJsList.append(js)
        if "static/"+ allJSTable[ newJSKey] != finalResourceMd5Obj["static/"+ newJSKey]:
            finalResourceMd5Obj["static/"+ newJSKey] = "static/" + allJSTable[newJSKey]
            ''' 需要更新 '''
            localName = uiFile + newJSKey   # + path+ "/" +  [:-7] + "." + fname
            copyfile(localName, "file/" + dataStr + "/static/" + allJSTable[newJSKey].replace("static/",""))


    '''  jsSDK 处理 sdk 里面可能有.min.js 文件 不做md5  '''
    newSDKJSList = GetFileList(uiFile + "sdk", [])
    allSDKTable = {}
    for fileN in newSDKJSList:
        fpath, fname = os.path.split(fileN)
        if fname[0] == ".":
            continue
        if fname.find(".min.js") > -1:
            continue
        md5_6_Str = shortMD5(get_file_md5(fileN))
        filePath, mdPath = pathAddMd5Str(fileN[fileN.find("/static/") + len("/static/"):], md5_6_Str)
        allSDKTable[filePath] = mdPath
    for sdkKey in allSDKTable:

        if not finalResourceMd5Obj.has_key("static/" + sdkKey):
            finalResourceMd5Obj["static/" + sdkKey] = "static/" +  allSDKTable[sdkKey]
            ''' 需要更新 '''
            localName = uiFile + sdkKey
            copyfile(localName, "file/" + dataStr + "/static/" + allSDKTable[sdkKey].replace("static/", ""))
            continue
        if finalResourceMd5Obj["static/" + sdkKey] != "static/"+ allSDKTable[sdkKey]:
            finalResourceMd5Obj["static/" + sdkKey] = "static/" + allSDKTable[sdkKey]
            ''' 需要更新 '''
            localName = uiFile + sdkKey
            copyfile(localName, "file/" + dataStr + "/static/" + allSDKTable[sdkKey].replace("static/", ""))


    newResourceTable["md5_resource"] = finalResourceMd5Obj
    newResourceTable["document"]["ccConfig"]["jsList"] = newJsList
    newResourceTable["noWebpImages"] = newnoWebpImagesTable


    oldResourceJSFile = Update_joyfun.getLocalPathByDir_Name("serverFile/", "resource")
    exportFinallResourceJS(newResourceTable, "file/" + dataStr + "/static/" + oldResourceJSFile.split("/").pop().split(".")[0][0:15] + "_" + dataStr + ".js")
    print("修改 html resource js 替换 " + reaourceOldPath + " ===>>  " + "" + oldResourceJSFile)
    ''' mac 和linux 不一样 先获取 resource_ 所在行数的内容 '''
    oldResourceStr = getStrFromFile("resource_", gameFileNameFAnd).split("/static/").pop().split("js")[0]
    newResourceStr = oldResourceJSFile.split("/").pop().split(".")[0][0:15] + "_" + dataStr + "."
    sedShell = 'sed -i ""  "s/' + oldResourceStr + '/' + newResourceStr + '/g" ' + gameFileNameFAnd
    os.system(sedShell)
    print(" html 中 resource js  替换 完成 ")
    if isUpdateEngine:
        print("开始生成新的引擎文件 ")
        gameminjsFile = projectFile + "game.min.js"
        Gstr = "game.min_"

        md5_6_Str = shortMD5(get_file_md5(gameminjsFile))
        oldGameMinjsStr = getStrFromFile(Gstr, gameFileNameFAnd).split("/static/").pop().split("js")[0]
        newGameMinjsStr = Gstr + md5_6_Str + "_" + dataStr + "."
        sedShell = 'sed -i ""  "s/' + oldGameMinjsStr + '/' + newGameMinjsStr + '/g" ' + gameFileNameFAnd
        os.system(sedShell)
        print(" html 中 game.min.js  替换 完成 ")

        newGameMinJsFileName = "file/" + dataStr + "/static/" + newGameMinjsStr+ "js"

        copyfile(gameminjsFile,newGameMinJsFileName)
        print("复制新的game.min.js html 中 game.min.js  替换 完成 ")

    '''  更新maketranslate js   '''

    gameminjsFile = projectFile + "makeTranslate.js"
    Gstr = "makeTranslate_"

    md5_6_Str = shortMD5(get_file_md5(gameminjsFile))
    oldGameMinjsStr = getStrFromFile(Gstr, gameFileNameFAnd).split("/static/").pop().split("js")[0]
    newGameMinjsStr = Gstr + md5_6_Str + "_" + dataStr + "."
    if oldGameMinjsStr.split("_")[1] != newGameMinjsStr.split("_")[1]:
        print(" 需要更新 makeTranslate_  文件 ")
        sedShell = 'sed -i ""  "s/' + oldGameMinjsStr + '/' + newGameMinjsStr + '/g" ' + gameFileNameFAnd
        os.system(sedShell)
        print(" html 中 makeTranslate_  替换 完成 ")

        newGameMinJsFileName = "file/" + dataStr + "/static/" + newGameMinjsStr + "js"

        copyfile(gameminjsFile, newGameMinJsFileName)
        print("复制新的makeTranslate.js html 中 makeTranslate.js  替换 完成 ")



    print(" 复制html 到指定 时间目录 ")
    copyfile(gameFileNameFAnd , "file/" + dataStr + "/" + gameFileNameF)
    print(" 复制" +gameFileNameF +" 到指定 时间目录 完成 ")

    #add 0927  添加 gz 文件

    allStatusFilePath = projectToolPath + "/file/" + dataStr + "/static/"
    if not isDebugMainJS:
        print("开始生成 status 文件下 所有 gz 文件 =>>" +allStatusFilePath)
        makeGzFile(allStatusFilePath)
        print("status 文件下 所有 gz 文件 生成完毕")

    ''' 直接上传 datastr 下 的所有文件  '''
    # # 需要文件夹全部上传
    upLoadSH = "scp -P " + str(liveServerConfir.port) + " -r " + projectToolPath + "/file/" + dataStr + "/static/" + " " + liveServerConfir.username + "@" + liveServerConfir.host + ":" + liveServerConfir.staticFile.replace(
        "static/", "")
    print("upLoad allFile ssh str => " + upLoadSH)
    if isOneKeyUpdate:
        print("开始更新所有资源(包括js)")
        os.system(upLoadSH)
        print("所有资源(包括js) 更新完成")

    uploadHtmlShell = "scp -P " + str(
        liveServerConfir.port) + " " + projectToolPath + "/file/" + dataStr + "/" + gameFileNameF + " " + liveServerConfir.username + "@" + liveServerConfir.host + ":" + liveServerConfir.staticFile.replace(
        "static/", "")
    print("upLoad " + gameFileNameF + " ssh str => " + uploadHtmlShell)

    if isOneKeyUpdate:
        print("开始更新 => " + gameFileNameF)
        os.system(uploadHtmlShell)
        print(gameFileNameF + " => 更新完成")
    if not isOneKeyUpdate:
        print("可以执行上面的log   热更新  ")
    print("去线上make一下 channel ")
    ##do update
    ''' !!!!!   上传之前  做提示  是否更新  本次全部内容到服务器    '''

