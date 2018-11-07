#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

# 添加md5版本号,方法发布目录的上层目录
__author__ = 'yxs'

import sys
import os
import shutil
import json
import hashlib

pathFile = sys.argv[0]
pathFile = os.path.abspath(pathFile)
pathNow = os.path.split(pathFile)[0] + '/'
srcPath = pathNow + "/../SmartpikachuGame_wxgame"
resPath = srcPath + '/resource'
noMD5Files = ({'type': "file", 'url': "images/login/clickRefresh.png"}, {'type': "dir", 'url': "images/sdk/"},{'type':"file", 'url':"images/dtl_dddt.jpg"})

srcPath = os.path.abspath(srcPath)
resPath = os.path.abspath(resPath)
print("srcPath=" + srcPath)
print("resPath=" + resPath)

# 先处理 res 的 md5

# 根据目录加载json
def loadJson(jsonPath):
    # if os.path.isfile(jsonPath):
    content = dict()
    try:
        f = open(jsonPath, encoding='utf-8')
        content = json.load(f)
    except ValueError:
        print("ivaled json")
        content = dict()
    except IOError:
        print("file is not Exit")
    return content


# 存储文件
def storeFile(content, path):
    with open(path, 'w') as store_file:
        store_file.write(content)


resPathAbs = os.path.abspath(resPath)


def getComparePath(absFPath):
    return absFPath.replace(resPathAbs + '/', '', 1)


def CalcSha1(filepath):
    with open(filepath, 'rb') as f:
        sha1obj = hashlib.sha1()
        sha1obj.update(f.read())
        hash = sha1obj.hexdigest()
        # print(hash[0:5])
        return hash[0:5]


md5Config = dict()

def makeMD5ByPath(fPath):
    if fPath.find('.DS_Store') >= 0:
        return
    fAbsPath = os.path.abspath(fPath)
    oldConfig = {"time": 0, "md5": ""}
    cPath = getComparePath(fAbsPath)
    if (md5Config.get(cPath)):
        oldConfig = md5Config[cPath]
    mTime = os.path.getmtime(fAbsPath)
    if (oldConfig["time"] != mTime):
        oldConfig["time"] = mTime
        oldConfig["md5"] = CalcSha1(fAbsPath)
        md5Config[cPath] = oldConfig


def makeMD5ByDir(dir):
    for path, d, filelist in os.walk(dir):
        for filename in filelist:
            if (filename[0] == '.'):
                continue
            fPath = os.path.join(path, filename)
            if (not os.path.isdir(fPath)):
                makeMD5ByPath(fPath)


# 资源先计算md5
dirs = os.listdir(resPath)
for fName in dirs:
    faPath = resPath + '/' + fName
    if (os.path.isdir(faPath)):
        makeMD5ByDir(faPath)


# 检查该文件是否需要MD5
def checkResFileNoMD5(url):
    for obj in noMD5Files:
        if obj["type"] == "file":
            if obj["url"] == url:
                return True
        elif obj["type"] == "dir":
            index = url.rfind("/")
            dirPath = url[:(index+1)]
            if obj["url"] == dirPath:
                return True

# 资源md5写入res.json
resConfigPath = resPath + "/default.res.json"
resConfig = loadJson(resConfigPath)
fileReplaced = dict()
processedResNameMap = dict()
# 优先处理字体文件
for rConfig in resConfig["resources"]:
    # print(rConfig['url'])
    if rConfig['type'] != "font":
        continue
    baseUrl = rConfig['url']
    if checkResFileNoMD5(baseUrl):
        continue

    md5 = md5Config[rConfig['url']]['md5']
    oldFile = os.path.abspath(resPath + "/" + baseUrl)
    fileName, fileExtension = os.path.splitext(oldFile)
    newFileName = fileName + "._" + md5 + fileExtension
    # print("baseUrl" + baseUrl + ", oldFile: " + oldFile + ", newFileName: " + newFileName)

    # 兼容不同name但是url相同的错误
    if oldFile not in fileReplaced:
        os.rename(oldFile, newFileName)
        oldPng = oldFile.replace('.fnt', '.png')
        newPng = newFileName.replace('.fnt', '.png')
        os.rename(oldPng, newPng)
        fileReplaced[oldPng] = 1
        webpFile = oldPng.replace('.png', '.webp')
        newWebpFile = newPng.replace('.png', '.webp')
        if os.path.exists(webpFile):
            os.rename(webpFile, newWebpFile)
        fileReplaced[oldFile] = 1
        # 处理PNG url
        relativePngPath = newPng.replace(resPath + "/", "")
        resName4Png = rConfig["name"][0:-4] + "_png"
        for rConfigPng in resConfig["resources"]:
            if rConfigPng['name'] == resName4Png:
                rConfigPng['url'] = relativePngPath
                processedResNameMap[resName4Png] = 1
                break
    # 相对路径
    relativePath = newFileName.replace(resPath + "/", "")
    rConfig['url'] = relativePath
    processedResNameMap[rConfig["name"]] = 1

# 处理其他文件
for rConfig in resConfig["resources"]:
    # print(rConfig['url'])
    if rConfig['url'].find('.DS_Store') >= 0:
        continue
    # 不要重复处理字体文件及其png
    if rConfig["name"] in processedResNameMap:
        continue
    # print(md5Config[rConfig['url']])
    # print(md5Config[rConfig['url']]['md5'])
    baseUrl = rConfig['url']
    if checkResFileNoMD5(baseUrl):
        continue

    md5 = md5Config[rConfig['url']]['md5']
    if (rConfig['type'] == 'sheet'):
        md5 += md5Config[baseUrl.replace('.json', '.png')]['md5']

    oldFile = os.path.abspath(resPath + "/" + baseUrl)
    fileName, fileExtension = os.path.splitext(oldFile)
    newFileName = fileName + "._" + md5 + fileExtension
    # print("baseUrl" + baseUrl + ", oldFile: " + oldFile + ", newFileName: " + newFileName)

    # 兼容不同name但是url相同的错误
    if oldFile not in fileReplaced:
        os.rename(oldFile, newFileName)
        if fileExtension == ".png":
            webpFile = oldFile.replace('.png', '.webp')
            newWebpFile = newFileName.replace('.png', '.webp')
            if os.path.exists(webpFile):
                os.rename(webpFile, newWebpFile)
        if (rConfig['type'] == 'sheet'):
            oldPng = oldFile.replace('.json', '.png')
            newPng = newFileName.replace('.json', '.png')
            os.rename(oldPng, newPng)
            fileReplaced[oldPng] = 1
            webpFile = oldPng.replace('.png', '.webp')
            newWebpFile = newPng.replace('.png', '.webp')
            if os.path.exists(webpFile):
                os.rename(webpFile, newWebpFile)
        fileReplaced[oldFile] = 1
    # 相对路径
    relativePath = newFileName.replace(resPath + "/", "")
    rConfig['url'] = relativePath


storeFile(json.dumps(resConfig, indent=4), resConfigPath)


# makeMD5ByPath(resPath+"/default.res.json")
def madeMd5FileAndChangeName(filePath, usePath=''):
    md5V = CalcSha1(filePath)
    fileInfo = os.path.split(filePath)
    fileDir = fileInfo[0]
    fileName = fileInfo[1]
    typeInfo = os.path.splitext(fileName)
    nameVue = typeInfo[0]
    typeVue = typeInfo[1]
    nameNew = nameVue + '._' + md5V + typeVue
    pathNew = fileDir + '/' + nameNew
    os.rename(filePath, pathNew)

    # print("fileName, nameNew, usePath",fileName, nameNew, usePath)
    if (len(usePath) > 0 and os.path.isfile(usePath)):
        # cmd = "sed -i \"\" \"s/%s/%s/g\" %s" % (fileName, nameNew, usePath)
        cmd = "sed -i '.original' \"s/%s/%s/g\" %s" % (fileName, nameNew, usePath)
        os.system(cmd)
    return nameNew


resConPOld = "default.res.json"
theConPOld = "default.thm.json"
# 处理 res.json 与 theme.json 的md5
resConPNew = madeMd5FileAndChangeName(resPath + '/' + resConPOld, srcPath + '/config/EzConfig.js')
theConPNew = madeMd5FileAndChangeName(resPath + '/' + theConPOld, srcPath + '/config/EzConfig.js')


# 处理js文件, 微信小游戏不需要
# dirs = os.listdir(srcPath)
# for fName in dirs:
#     faPath = srcPath + '/' + fName
#     if (os.path.isdir(faPath) and fName != 'mySkins'):
#         for path, d, filelist in os.walk(faPath):
#             for filename in filelist:
#                 fPathE = os.path.join(path, filename)
#                 typeInfo = os.path.splitext(fPathE)
#                 if (typeInfo[1] == '.js'):
#                     madeMd5FileAndChangeName(fPathE, srcPath + "/index.html")
#     else:
#         typeInfo = os.path.splitext(faPath)
#         if (typeInfo[1] == '.js'):
#             madeMd5FileAndChangeName(faPath, srcPath + "/index.html")

# 保存配置文件 暂时先没必要
