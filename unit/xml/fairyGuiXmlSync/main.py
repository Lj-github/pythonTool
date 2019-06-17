import unit.xml.layaFairyGuiUIRead as xmlTool
import easyGameTool.foreignTools.cocosPikachuTools.ExcelTools as Et

fairyGuiProFile = 'F:/liujiang/svn/trunk/meishu/ProjectUI/'


def isPackAgeXml(path):
    return path.find('package.xml') > -1


# assets/Account\\package.xml 格式
def getPackAgeNameByPath(path):
    path = path.replace("\\", "/")
    print(path)
    return path.split("/")[-2]

def getIdByPathFormlocalPkg(pth,localPkg):
    for pkg in localPkg:
        for node in pkg:
            pass
            #if node[""] TODO

def checkErrorID(xmlFile, localPkg):
    tree = xmlTool.read_xml(xmlFile)
    nodes = xmlTool.find_nodes(tree, "displayList/")
    for node in nodes:
        if node.tag == 'image':
            if 'fileName' in node.attrib:
                inFileName = node.attrib["fileName"]
            continue
        if node.tag == 'loader':
            continue



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
    print(localPkg)
    # 每个 组件 单独处理一下 查看是否有 id 引用错误的

    for fi in allPackageFile:
        checkErrorID(fi, localPkg)
