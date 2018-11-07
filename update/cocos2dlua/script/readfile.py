# encoding: utf-8
from Tkinter import *
from tkMessageBox import *
import os
import datetime
import os.path
import json
from hashlib import md5
import shutil

ip = "http://www.17jike.com:3312/assets_hy/"


def IsSubString(SubStrList, Str):
    flag = False
    for substr in SubStrList:
        if not (substr in Str):
            flag = True
    return flag


def getDirList(p):
    p = str(p)
    if p == "":
        return []
    p = p.replace("/", "\\")
    if p[-1] != "\\":
        p = p + "\\"
    a = os.listdir(p)
    return [x for x in a if os.path.isdir(p + x)]


def getDirListAll(path):
    path = str(path)
    return


def getTxtFile(path):
    lis = path
    fileAllName = os.listdir(path)
    if fileAllName.__len__() > 0:
        for file in fileAllName:
            n = lis + "/" + file
            if not os.path.isdir(n):
                stt = n[10:]
                allFile.append(stt)
            else:
                getTxtFile(str(n))


def writeFile(name, arr=[]):
    r = open(name, "w")
    str = ""
    if arr.__len__() > 0:
        for fileName in arr:
            str = str + fileName + "\n"
    r.write(str)
    r.close()


def generate_file_md5value(fpath):
    m = md5()
    a_file = open(fpath, 'rb')
    m.update(a_file.read())
    a_file.close()
    return m.hexdigest()


def createProject(packageUrl, remoteVersionUrl, remoteManifestUrl, version, engineVersion, appV, assets=[]):
    project = {}
    project["packageUrl"] = packageUrl
    project["remoteVersionUrl"] = remoteVersionUrl
    project["remoteManifestUrl"] = remoteManifestUrl
    project["version"] = version
    project["engineVersion"] = engineVersion
    project["appV"] = appV
    project['assets'] = {}
    if assets.__len__() > 0:
        for file in assets:
            md = {}
            print
            file
            print
            generate_file_md5value("../assets/" + file)
            md['md5'] = generate_file_md5value("../assets/" + file)
            project["assets"][file] = md
    return project


def createVersion(packageUrl, remoteVersionUrl, remoteManifestUrl, version, engineVersion, appV):
    project = {}
    project["packageUrl"] = packageUrl
    project["remoteVersionUrl"] = remoteVersionUrl
    project["remoteManifestUrl"] = remoteManifestUrl
    project["version"] = version
    project["engineVersion"] = engineVersion
    project["appV"] = appV
    return project


def copyFiles(sourceDir, targetDir):
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
                open(targetFile, "wb").write(open(sourceFile, "rb").read())
        if os.path.isdir(sourceFile):
            First_Directory = False
            copyFiles(sourceFile, targetFile)


def moveFileto(sourceDir, targetDir):
    shutil.copy(sourceDir, targetDir)


allFile = []


def init(flag):  # 是否为热跟新
    appVersionFile = open('appVersion.manifest', 'r')
    appVersionJson = appVersionFile.read()
    appVersionDict = json.loads(appVersionJson)
    appVersion = appVersionDict['appVersion'].encode('unicode-escape')
    appVarr = str.split(appVersion, ".")

    apkV = appVarr[0]
    newApkV = int(apkV)
    if not flag:  ##版本号规则  不完善

        newApkV = '%d' % (int(apkV) + 1)

        print(str(newApkV))

    version = appVarr[-1]

    newVersion = '%d' % (int(version) + 1)
    appVersion = newVersion
    newVersionDict = {}
    newVersionDict["appVersion"] = str(newApkV) + ".0." + newVersion
    newVersionDict["flag"] = appVersionDict["flag"]
    newStr = json.dumps(newVersionDict)
    r = open("appVersion.manifest", "w")
    r.write(newStr)
    r.close()
    appVersion = str(newApkV) + ".0." + appVersion

    print(appVersion)
    root.destroy()
    today = datetime.datetime.now()
    ISOFORMAT = '%Y%m%d'
    dataStr = today.strftime(ISOFORMAT)[2:] + "%s" % today.hour + "%s" % today.second
    cpath = os.path.dirname(__file__)[:-7]
    cpath = cpath.replace("/", "\\")
    copy = 'xcopy "' + cpath + '\\update\\res"' + ' "' + cpath + '\\assets\\res" ' + '/e/s/h '
    luac = 'cocos luacompile -s ' + '"' + cpath + '\\update\\src"' + ' -d "' + cpath + '\\assets\\src"' + ' --disable-compile'
    os.system(copy)
    os.system(luac)

    getTxtFile("../assets")
    print(allFile)
    r = open("project.manifest", "w")
    r.write(json.dumps(
        createProject(ip + dataStr, ip + "version.manifest", ip + "project.manifest", dataStr, "Cocos2d-x v3.10",
                      appVersion, allFile)))
    r.close()
    v = open('version.manifest', 'w')
    v.write(json.dumps(
        createVersion(ip + dataStr, ip + "version.manifest", ip + "project.manifest", dataStr, "Cocos2d-x v3.10",
                      appVersion)))
    v.close()
    if not os.path.isdir("../mahjong/" + dataStr + "/assets"):
        os.makedirs("../mahjong/" + dataStr + "/assets")
    copyFiles("../assets", "../mahjong/" + dataStr + "/assets")
    moveFileto('project.manifest', "../mahjong")
    moveFileto('version.manifest', "../mahjong")
    moveFileto('project.manifest', "../update/assets")
    moveFileto('version.manifest', "../update/assets")


def updateRES():
    init(True)


def updateAPP():
    init(False)


root = Tk()


def _test():
    text = "是否为热更新"
    if TclVersion >= 8.1:
        try:
            text = text + "\n选择否会更新app版本"
        except NameError:
            pass  # no unicode support
    label = Label(root, text=text)
    label.pack()
    test = Button(root, text="是", command=updateRES).pack(fill=X)
    # test.pack()
    root.test = test
    quit = Button(root, text="否", command=updateAPP).pack(fill=X)
    ##quit.pack()
    root.iconify()
    root.update()
    root.deiconify()
    root.mainloop()


if __name__ == '__main__':
    _test()
