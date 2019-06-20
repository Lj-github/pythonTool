


import sys
import os
#需要添加项目的绝对路径 
sys.path.append('C:\\Users\\Administrator\\Desktop\\work\\pythonTool') 
import unit.xml.layaFairyGuiUIRead as xmlTool
import easyGameTool.foreignTools.cocosPikachuTools.ExcelTools as Et
fairyGuiProFile = 'F:/liujiang/svn/trunk/meishu/ProjectUI/'
print("run")
sys.exit(0)
def isPackAgeXml(path):
    return path.find('package.xml') > -1


# assets/Account\\package.xml 格式
def getPackAgeNameByPath(path):
    path = path.replace("\\", "/")
    return path.split("/")[-2]


# 通过 img 的url  查找 package xml 里面的 id  并且 应该是唯一的
def getIdByPathFormlocalPkg(pth, localPkg):
    idList = []
    for pkg in localPkg:
        for node in localPkg[pkg]['imgList']:
            if (node['path'] + node['name']) == ('/' + pth):
                node["pkg"] = pkg
                idList.append(node)
    return idList


def checkErrorID(xmlFile, localPkg):
    tree = xmlTool.read_xml(xmlFile)
    nodes = xmlTool.find_nodes(tree, "displayList/")
    for node in nodes:
        if node.tag == 'image':
            if 'fileName' in node.attrib:
                inFileName = node.attrib["fileName"]
                realIDList = getIdByPathFormlocalPkg(inFileName, localPkg)
                if len(realIDList) > 1:
                    print(inFileName + "文件重复 id 重复")
                    print(realIDList)
                    continue
                if len(realIDList) == 1:
                    if realIDList[0]['id'] == node.attrib["src"]:
                        # 正确
                        continue
                    else:
                        print(xmlFile, inFileName, '错误！')
                        # 修复一下
                        resetFairyGuiXml(
                            xmlFile, node, localPkg, realIDList[0])

                if len(realIDList) == 0:
                    print('path ' + xmlFile + '   ' + inFileName + '没有对应id')
                    continue
            continue
        if node.tag == 'loader':
            # 如果是装载器  url  =ui:// +  pkg + id  <url="ui://qdktke93nmey5g">
            # 目前 出问题的 应该比较少

            continue


# 重新写入到新的 fairyGui  XML文件中  packagexml  需要改成导出  把旧的fair xml  修改一下 id  就可以了
def resetFairyGuiXml(fairyXml, fairyXmlNode, localPkg, pkgNode):
    print("写入文件" + fairyXml)
    tree = xmlTool.read_xml(fairyXml)

    # pkgxml
    pkgXmlFile = localPkg[pkgNode['pkg']]['localFile']
    treePkg = xmlTool.read_xml(pkgXmlFile)
    nodesPkg = xmlTool.find_nodes(tree, "resources/")
    isNeedSave = False
    for node in nodesPkg:
        if node.attrib['id'] == pkgNode['id']:
            if 'exported' not in node.attrib:
                isNeedSave = True
                print('pkg', pkgNode['pkg'], node.attrib['name'], '需要设置为导出')
                sys.exit(0)
    if isNeedSave:
        xmlTool.write_xml(treePkg, pkgXmlFile)

    # fariyGui xml
    nodes = xmlTool.find_nodes(tree, "displayList/")
    isChangeID = False
    for node in nodes:
        if node.get("id") == fairyXmlNode.attrib["id"]:
            isChangeID = True
            node.attrib["src"] = pkgNode['id']
            # node.attrib["pkg"] = pkgNode['pkg'] 不需要 暂时
    if isChangeID:
        xmlTool.write_xml(tree, fairyXml)


# 获取 pkg 里面所有img 的id  因为有时候更新 id 就被冲突掉了  不知道为啥
def getPkgImgID(pkgXml):
    tree = xmlTool.read_xml(pkgXml)
    resObj = {}
    resObj["pkgID"] = tree._root.attrib["id"]
    resList = []
    nodes = xmlTool.find_nodes(tree, "resources/")
    for node in nodes:
        if node.tag == 'image':
            if not node.attrib:
                continue
            if 'exported' in node.attrib:
                if node.attrib['exported'] == 'true':
                    resList.append(node.attrib)
    resObj["imgList"] = resList
    resObj['localFile'] = pkgXml
    return resObj


if __name__ == '__main__':
    localPkg = {}
    assestFile = fairyGuiProFile + 'assets/'
    allPackageFile = Et.getFileName(assestFile, ['xml'], [])
    allpkgxml = list(filter(isPackAgeXml, allPackageFile))
    # 把所有的packagexml 解析一遍 看 引用 对不对
    for i in allpkgxml:
        pkgName = getPackAgeNameByPath(i)
        if pkgName not in localPkg:
            localPkg[pkgName] = []
            localPkg[pkgName] = getPkgImgID(i)
    # 每个 组件 单独处理一下 查看是否有 id 引用错误的
    for fi in allPackageFile:
        checkErrorID(fi, localPkg)
