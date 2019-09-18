# -*- coding: utf-8 -*-
# @Time    : 19/9/18   10:24
'''
    查看fairygui 里面重复的图片 并打印出来  自动修改 并删除旧的url(懒得做了)
    通过md5  对比 可能有的图片 名字不同 图片是一个
    有重复的：
        base 优先  没有base 直接复制到base id 自己定就行  随便使用一个 然后把旧的id 全部改成新的 并且 package 需要修改 需要用xml read
'''

import unit.Tools as tools
import unit.md5.Tools as md5Tools
import unit.xml.xmlRead as xmlTools
import os

needAutoReplace = True
fairyGuiPath = "F:/liujiang/svn/trunk/meishu/ProjectUI/assets"

# 需要过滤 的 fairly pkg  不进行筛选
filterPkg = ["Update"]


class fairyImgUnit:
    pkg = ''
    # fairy pkg
    fPkg = ''
    # fairy src
    src = ''
    file = ''
    fileName = ''


def getPkgXmlPath(pkgName):
    return fairyGuiPath + "/" + pkgName + "/package.xml"


def getFairyImgUnitByUrl(url):
    fileArr = url.replace(fairyGuiPath, "").split("\\")
    pkg = fileArr[1]
    unit = fairyImgUnit()
    unit.pkg = pkg
    unit.file = url
    unit.fileName = fileArr.pop()
    pkgXml = getPkgXmlPath(pkg)
    tree = xmlTools.read_xml(pkgXml)
    root = tree.getroot()
    unit.fPkg = root.get("id")
    nodes = xmlTools.find_nodes(tree, "resources/")
    for node in nodes:
        if node.get("name") == unit.fileName:
            unit.src = node.get("id")
    return unit


def getBaseUnit(unitArr):
    base = None
    for unit in unitArr:
        if unit.pkg == "_Base":
            base = unit
    if not base:
        base = unitArr[0]
    return base


def getFpakByPackageName(pkgName):
    pkgXml = getPkgXmlPath(pkgName)
    tree = xmlTools.read_xml(pkgXml)
    root = tree.getroot()
    return root.get("id")


def removeUnit2Pkg(unit, pkgName):
    oldUnitXml = getPkgXmlPath(unit.pkg)
    newXml = getPkgXmlPath(pkgName)
    # 把旧的 xml 里面的数据删了 加到新的里面
    treeOld = xmlTools.read_xml(oldUnitXml)
    treeTo = xmlTools.read_xml(newXml)
    nodesOld = xmlTools.find_nodes(treeOld, "resources/")
    _node = None
    root = treeOld.getroot()
    nodeoldPar = root.__getitem__(0)
    for nodeold in nodesOld:
        if nodeold.attrib["id"] == unit.src:
            _node = nodeold
            nodeoldPar.remove(nodeold)
    if _node == None:
        print("未查到 unit", unit.pkg, unit.file, unit.src, pkgName)
        return
    rootNew = treeTo.getroot()
    nodeNewPar = rootNew.__getitem__(0)
    # add_child_node
    nodeNewPar.append(_node)
    xmlTools.write_xml(treeTo, newXml)
    xmlTools.write_xml(treeOld, oldUnitXml)
    resFile = unit.file.replace("\\" + unit.pkg + "\\", "\\" + pkgName + "\\")
    tools.copyfile(unit.file, resFile)
    os.remove(unit.file)
    res = fairyImgUnit()
    res.file = resFile
    res.pkg = pkgName
    res.src = unit.src
    res.fileName = unit.fileName
    res.fPkg = getFpakByPackageName(pkgName)
    return res


def getRandem():
    pass


def removePkgById(pkgName, removeID):
    newXml = getPkgXmlPath(pkgName)
    treeTo = xmlTools.read_xml(newXml)
    nodes = xmlTools.find_nodes(treeTo, "resources/")
    root = treeTo.getroot()
    nodeoldPar = root.__getitem__(0)
    isDone = False
    for nodeold in nodes:
        if nodeold.attrib["id"] == removeID:
            nodeoldPar.remove(nodeold)
            isDone = True
    if isDone:
        xmlTools.write_xml(treeTo, newXml)


def removePkgByName(pkgName, removeName):
    newXml = getPkgXmlPath(pkgName)
    treeTo = xmlTools.read_xml(newXml)
    nodes = xmlTools.find_nodes(treeTo, "resources/")
    root = treeTo.getroot()
    nodeoldPar = root.__getitem__(0)
    isDone = False
    for nodeold in nodes:
        if nodeold.attrib["name"] == removeName:
            nodeoldPar.remove(nodeold)
            isDone = True
    if isDone:
        xmlTools.write_xml(treeTo, newXml)



def replaceUnit2Unit(baseUnit, needReplaceUnit, allXmlFile):
    print("replaceUnit2Unit", baseUnit, needReplaceUnit)

    # 旧的 pkgxml 需要移除 old id
    removePkgById(needReplaceUnit.pkg, needReplaceUnit.src)
    '''
        需要实现的是 
        1 把就得url 全部替换成新的 而且需要 把旧的图片删掉  注意icon
    '''
    for url in allXmlFile:
        fileArr = url.replace(fairyGuiPath, "").split("\\")
        fileName = fileArr.pop()
        if fileName == "package.xml":
            continue
        tree = xmlTools.read_xml(url)
        root = tree.getroot()
        nodes = xmlTools.find_nodes(tree, "displayList/")
        isRun = False
        for node in nodes:
            if node.tag == 'component':
                for i in range(len(node)):
                    _child = node.__getitem__(i)
                    if _child.tag == 'image':
                        if _child.get("src") == needReplaceUnit.src:
                            if not _child.attrib:
                                continue
                            _child.attrib['src'] = baseUnit.src
                            _child.attrib['pkg'] = baseUnit.fPkg
                            if os.path.isfile(needReplaceUnit.file):
                                os.remove(needReplaceUnit.file)
                            isRun = True
                    if _child.tag == 'loader':
                        if _child.get("url") == ("ui://" + needReplaceUnit.fPkg + needReplaceUnit.src):
                            if not _child.attrib:
                                continue
                            _child.attrib['url'] = ("ui://" + baseUnit.fPkg + baseUnit.src)
                            isRun = True
                            if os.path.isfile(needReplaceUnit.file):
                                os.remove(needReplaceUnit.file)

                    if _child.tag == 'Button':
                        if _child.get("icon") == ("ui://" + needReplaceUnit.fPkg + needReplaceUnit.src):
                            if not _child.attrib:
                                continue
                            _child.attrib['icon'] = ("ui://" + baseUnit.fPkg + baseUnit.src)
                            isRun = True
                            if os.path.isfile(needReplaceUnit.file):
                                os.remove(needReplaceUnit.file)

                        if _child.get("selectedIcon") == ("ui://" + needReplaceUnit.fPkg + needReplaceUnit.src):
                            if not _child.attrib:
                                continue
                            _child.attrib['selectedIcon'] = ("ui://" + baseUnit.fPkg + baseUnit.src)
                            isRun = True
                            if os.path.isfile(needReplaceUnit.file):
                                os.remove(needReplaceUnit.file)

            if node.tag == 'image':
                if node.get("src") == needReplaceUnit.src:
                    if not node.attrib:
                        continue
                    node.attrib['src'] = baseUnit.src
                    node.attrib['pkg'] = baseUnit.fPkg
                    if os.path.isfile(needReplaceUnit.file):
                        os.remove(needReplaceUnit.file)
                    isRun = True
            if node.tag == 'loader':
                if node.get("url") == ("ui://" + needReplaceUnit.fPkg + needReplaceUnit.src):
                    if not node.attrib:
                        continue
                    node.attrib['url'] = ("ui://" + baseUnit.fPkg + baseUnit.src)
                    isRun = True
                    if os.path.isfile(needReplaceUnit.file):
                        os.remove(needReplaceUnit.file)
            if node.tag == 'Button':
                if _child.get("icon") == ("ui://" + needReplaceUnit.fPkg + needReplaceUnit.src):
                    if not _child.attrib:
                        continue
                    _child.attrib['icon'] = ("ui://" + baseUnit.fPkg + baseUnit.src)
                    isRun = True
                    if os.path.isfile(needReplaceUnit.file):
                        os.remove(needReplaceUnit.file)

                if _child.get("selectedIcon") == ("ui://" + needReplaceUnit.fPkg + needReplaceUnit.src):
                    if not _child.attrib:
                        continue
                    _child.attrib['selectedIcon'] = ("ui://" + baseUnit.fPkg + baseUnit.src)
                    isRun = True
                    if os.path.isfile(needReplaceUnit.file):
                        os.remove(needReplaceUnit.file)
        if isRun:
            xmlTools.write_xml(tree, url)
        else:
            # 没有执行替换 说明 此文件 重复 不要了
            if os.path.isfile(needReplaceUnit.file):
                os.remove(needReplaceUnit.file)


def filterPkgFun(fileName):
    isCan = True
    for fi in filterPkg:
        if "\\" + fi + "\\" in fileName:
            isCan = False
    return isCan

if __name__ == "__main__":
    root = {}
    md5Table = {}
    allImageFile = tools.GetFileListByType(fairyGuiPath, ["png", "jpg"], [])
    allXmlSkinFile = tools.GetFileListByType(fairyGuiPath, ["xml"], [])

    allImageFile = list(filter(filterPkgFun, allImageFile))
    allXmlSkinFile = list(filter(filterPkgFun, allXmlSkinFile))
    #
    # 直接用md5  就行
    for fileName in allImageFile:
        fileArr = fileName.replace(fairyGuiPath, "").split("\\")
        pkg = fileArr[1]
        md5 = md5Tools.get_file_md5(fileName)
        if not root.get(pkg):
            root[pkg] = []
        if not md5Table.get(md5):
            md5Table[md5] = []
        md5Table[md5].append(fileName)

    dodd = False
    for md5 in md5Table:
        md5Arr = md5Table[md5]
        # 如果有重复的
        if len(md5Arr) > 1:
            print(md5Arr)
            if not needAutoReplace:
                continue
            if dodd:
                continue
            # dodd = True
            needArr = []
            for fileName in md5Arr:
                needArr.append(getFairyImgUnitByUrl(fileName))
            # 优先base  如果没有 就用第一个完事
            baseUnit = getBaseUnit(needArr)
            # 如果这个包 不是base  需要移动到base
            if baseUnit.pkg != "_Base":
                baseUnit = removeUnit2Pkg(baseUnit, "_Base")
                # base 转移 done
            # 如果都是 base  这 tmd
            isUrlSame = True
            for unit in needArr:
                if unit.pkg != baseUnit.pkg and unit.src != baseUnit.src:
                    replaceUnit2Unit(baseUnit, unit, allXmlSkinFile)
                    isUrlSame = False
            if isUrlSame:
                for unit in needArr:
                    if unit.fileName != baseUnit.fileName:
                        removePkgByName(unit.pkg, unit.fileName)
                        if os.path.isfile(unit.file):
                            os.remove(unit.file)
