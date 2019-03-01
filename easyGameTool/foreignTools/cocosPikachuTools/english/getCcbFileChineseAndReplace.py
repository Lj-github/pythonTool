# -*- coding: utf-8 -*-
# @Time    : 2019/2/28 下午4:46


# TODO 期望获取文件中的 中文  打到提取中文 并且替换中文 到新的 id 新的id  会insert 到 数据库里面  有点问题 ！！！！！！
enFile = '/Users/admin/Documents/ljworkspace/local/cocos/project/pikachu_englishGit/pikachu_english/tools/pikachuCCB/ccb'  # /commons/EasyCommon.coffee

import easyGameTool.foreignTools.cocosPikachuTools.ExcelTools as et
import os
import copy

allCoffee = et.getFileName(enFile, ["ccb"], [])

ex = ["皮皮",'骄傲的老豆'] #皮？
allCoffeeData = None
allCoffeeData = et.processSql("SELECT Id,Chinese from ccbTranslate WHERE Id IS NOT NULL and Id != 0")

insterSql = "INSERT INTO ccbTranslate (Id,Chinese, FilePth) VALUES ('{0}','{1}','{2}')"

insertCount = 0

needInsert = []


def getIdFormData(allData, chStr):
    for row in allData:
        if row[1] == chStr:
            print("id == > " + str(row[0]) + "  str = > " + row[1])
            return row[0]


def getMaxID(allData):
    id = 0
    for row in allData:
        if row[0] >= id:
            id = row[0]
    return id + insertCount


def getInsterIdx(inserData, st):
    for i in range(inserData.__len__()):
        row = inserData[i]
        if row["ch"] == st:
            return i
    return None


def printDiffFunc(fileMore):
    global insertCount
    fp, fn = os.path.split(fileMore)
    li = ''
    l = ''
    with open(fileMore, 'r') as f:
        li = f.read()
        l = li
        # 通过 string 分割 然后 只取 奇数的部分 里面只有内容  并且 包括lbl text
        allSp = l.split("string")
        allStr = []
        for s in range(len(allSp)):
            if s%2 == 1:
                allStr.append(allSp[s].replace("</","").replace(">","").replace("\n","").replace("\t",""))
        chineseList = []
        for s in allStr:
            if et.isIncludeChinese(s):
                chineseList.append(s)
        #chineseList = et.getChineseStr(l)
        if len(chineseList) > 0:
            for ch in chineseList:
                needDe = False
                for p in ex:
                    if ch.find(p)>-1:
                        needDe = True
                if needDe:
                    continue

                id = getIdFormData(allCoffeeData, ch)
                isHasData = True
                if not id:
                    isHasData = False
                    id = getMaxID(allCoffeeData) + 1
                # 做替换

                if (">" + ch + "<") in l or ((">" + ch + "\n<") in l):
                    l = l.replace(ch, "ccbList_" + str(id))

                    if not isHasData:
                        # insert
                        print("need insert id = >> " + str(id))
                        isInsertedID = getInsterIdx(needInsert, ch)

                        if isInsertedID == None:
                            needInsert.append({"Id": id, "ch": ch, "file": fn})
                            insertCount = insertCount + 1
                        else:
                            dat = needInsert[isInsertedID]
                            if fn in dat["file"]:
                                fileName = dat["file"]
                            else:
                                fileName = dat["file"] + ";" + fn
                            needInsert[isInsertedID] = {"Id": dat["Id"], "ch": dat["ch"],
                                                        "file": fileName}
                        # et.processSql()
                    print("file = >> " + fileMore)
                    print(ch)
    with open(fileMore, 'w') as ff:
        ff.writelines(l)

if __name__ == '__main__':
    #exit(0)
    # for coffee in allCoffee:
    #     printDiffFunc(coffee)

    print(needInsert)
    needInsert = [ {'Id': 2015, 'ch': '分解', 'file': 'FormFuwen.ccb'}, {'Id': 2016, 'ch': '2级', 'file': 'FormFuwenBag.ccb'}, {'Id': 2017, 'ch': '4级', 'file': 'FormFuwenBag.ccb'}, {'Id': 2018, 'ch': '投注结果：', 'file': 'FormFuwenDuiHuan.ccb'}, {'Id': 2019, 'ch': '多选', 'file': 'FormFuwenHuoDe.ccb'}, {'Id': 2020, 'ch': '适度娱乐,理性消费', 'file': 'FormYiYuanBJL.ccb'}, {'Id': 2021, 'ch': '数量x99999999', 'file': 'FormZhuanShuHuiShou.ccb'}, {'Id': 2022, 'ch': '历史最高', 'file': 'LayerKuaFuSj.ccb'}, {'Id': 2023, 'ch': '一键击杀', 'file': 'LayerKuaFuSj.ccb'}, {'Id': 2024, 'ch': '抗破+', 'file': 'LayerLuoTuoMu.ccb'}, {'Id': 2025, 'ch': '请选择出海次数', 'file': 'LayerShopBuy.ccb'}, {'Id': 2026, 'ch': '使用一折代金券', 'file': 'LayerShopBuy.ccb'}, {'Id': 2027, 'ch': '十次摇ccbList_1663', 'file': 'LayerSlots.ccb'}, {'Id': 2028, 'ch': 'ccbList_1753宠.jpg', 'file': 'NodefollowPetlevelUp.ccb'}, {'Id': 2029, 'ch': '张翼德  Lv.36', 'file': 'NodeHeroItem.ccb'}, {'Id': 2030, 'ch': '队员名字名字 lv ', 'file': 'NodeTeamBattleEnd.ccb'}]

    for item in needInsert:
        et.insertDataSql(insterSql.format(str(item["Id"]), item["ch"], item['file']))
