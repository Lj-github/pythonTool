# -*- coding: utf-8 -*-
# @Time    : 2019/2/28 下午4:46


# TODO 期望获取文件中的 中文  打到提取中文 并且替换中文 到新的 id 新的id  会insert 到 数据库里面
chFile = '/Users/admin/Documents/ljworkspace/local/cocos/project/Pikachu/app/static/coffee'  # /commons/EasyCommon.coffee
enFile = '/Users/admin/Documents/ljworkspace/local/cocos/project/pikachu_englishGit/pikachu_english/app/static/coffee'  # /commons/EasyCommon.coffee

import easyGameTool.foreignTools.cocosPikachuTools.ExcelTools as et
import os
import copy

allCoffee = et.getFileName(enFile, ["coffee"], [])

ex = ["log"]  # '{0}' WHERE Id={1}
allCoffeeData = None
allCoffeeData = et.processSql("SELECT Id,Chinese from coffeeTranslate WHERE Id IS NOT NULL and Id != 0")

insterSql = "INSERT INTO coffeeTranslate (Id,Chinese, FilePth) VALUES ('{0}','{1}','{2}')"

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
    with open(fileMore, 'r') as f:
        li = f.readlines()
        for j in range(li.__len__()):
            l = li[j]
            isEx = False
            for ee in ex:
                if l.find(ee) > -1:
                    isEx = True
            if l.find('#') > -1:
                isEx = True
            if isEx:
                continue
            chineseList = et.getChineseStr(l)
            if len(chineseList) > 0:
                for ch in chineseList:
                    if l.find('"' + ch) > -1 or l.find("'" + ch) > -1:
                        id = getIdFormData(allCoffeeData, ch)
                        isHasData = True
                        if not id:
                            isHasData = False
                            id = getMaxID(allCoffeeData) + 1
                        # 做替换
                        oneDocList = l.split("'")

                        for ii in range(oneDocList.__len__()):
                            if oneDocList[ii].find(ch) > -1:
                                oldStr = "'" + oneDocList[ii] + "'"
                                llll = copy.deepcopy(li[j])

                                li[j] = li[j].replace(oldStr, "getTranslateStr(" + str(id) + ")")
                                if not isHasData and oldStr in llll:
                                    # insert
                                    print("need insert id = >> " + str(id))
                                    isInsertedID = getInsterIdx(needInsert, oneDocList[ii])

                                    if isInsertedID == None:
                                        needInsert.append({"Id": id, "ch": oneDocList[ii], "file": fn})
                                        insertCount = insertCount + 1
                                    else:
                                        dat = needInsert[isInsertedID]
                                        if fn in dat["file"]:
                                            fileName = dat["file"]
                                        else:
                                            fileName = dat["file"] + ";" + fn
                                        needInsert[isInsertedID] = {"Id": dat["Id"], "ch": dat["ch"],
                                                                    "file": fileName}

                        oneDocList = l.split('"')
                        for ii in range(oneDocList.__len__()):
                            if oneDocList[ii].find(ch) > -1:
                                oldStr = '"' + oneDocList[ii] + '"'
                                llll = copy.deepcopy(li[j])
                                li[j] = li[j].replace(oldStr, "getTranslateStr(" + str(id) + ")")
                                if not isHasData and oldStr in llll:
                                    # insert
                                    print("need insert id = >> " + str(id))
                                    isInsertedID = getInsterIdx(needInsert, oneDocList[ii])
                                    if isInsertedID == None:
                                        needInsert.append({"Id": id, "ch": oneDocList[ii], "file": fn})
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
        ff.writelines(li)

for coffee in allCoffee:
    printDiffFunc(coffee)

print(needInsert)
# needInsert = [{'Id': 3258, 'ch': '嘉年华积分', 'file': 'BaseLayer.coffee'}, {'Id': 3259, 'ch': '联盟争霸币', 'file': 'BaseLayer.coffee'}, {'Id': 3260, 'ch': '火控制', 'file': 'Constants.coffee'}, {'Id': 3261, 'ch': '水控制', 'file': 'Constants.coffee'}, {'Id': 3262, 'ch': '草控制', 'file': 'Constants.coffee'}, {'Id': 3263, 'ch': '光控制', 'file': 'Constants.coffee'}, {'Id': 3264, 'ch': '暗控制', 'file': 'Constants.coffee'}, {'Id': 3265, 'ch': '日常-寻宝乐园', 'file': 'Constants.coffee'}, {'Id': 3266, 'ch': '王者之路', 'file': 'Constants.coffee'}, {'Id': 3267, 'ch': '转生排位', 'file': 'Constants.coffee'}, {'Id': 3268, 'ch': '宅急送', 'file': 'Constants.coffee'}, {'Id': 3269, 'ch': '日常-每日签到', 'file': 'Constants.coffee'}, {'Id': 3270, 'ch': '联盟商城', 'file': 'Constants.coffee'}, {'Id': 3271, 'ch': '京', 'file': 'Constants.coffee'}, {'Id': 3272, 'ch': '抗眩晕', 'file': 'Constants.coffee'}, {'Id': 3273, 'ch': '抗混乱', 'file': 'Constants.coffee'}, {'Id': 3274, 'ch': '联盟币', 'file': 'EasyCommon.coffee'}, {'Id': 3275, 'ch': '棒棒糖', 'file': 'EasyCommon.coffee'}, {'Id': 3276, 'ch': '国庆红包', 'file': 'EasyCommon.coffee'}, {'Id': 3277, 'ch': '元素入场券{0}', 'file': 'EasyCommon.coffee'}, {'Id': 3278, 'ch': '元素入场券', 'file': 'EasyCommon.coffee'}, {'Id': 3279, 'ch': '您在本期活动最高排名:', 'file': 'LayerKuaFuHistoryTop.coffee'}, {'Id': 3280, 'ch': '我的击杀次数：', 'file': 'LayerKuaFuSj.coffee'}, {'Id': 3281, 'ch': '更换', 'file': 'FormBackpack.coffee'}, {'Id': 3282, 'ch': '镶嵌', 'file': 'FormFuwenBag.coffee'}, {'Id': 3283, 'ch': '分解', 'file': 'FormFuwenBag.coffee'}, {'Id': 3284, 'ch': '请先选择要分解的符文', 'file': 'FormFuwenHuiShou.coffee'}, {'Id': 3285, 'ch': '暂无可分解的符文', 'file': 'FormFuwenHuiShou.coffee'}, {'Id': 3286, 'ch': '请先选择足够的彩球', 'file': 'FormFuwenHuoDe.coffee'}, {'Id': 3287, 'ch': '已激活班吉拉坐骑！', 'file': 'FormYiyuanBJL.coffee'}, {'Id': 3288, 'ch': '进阶等级：', 'file': 'FormPiShenJinJie.coffee'}, {'Id': 3289, 'ch': '开放时间：8:00~23:59', 'file': 'FormQiyu.coffee'}, {'Id': 3290, 'ch': '加载第一批json', 'file': 'DefContainer.coffee'}]

for item in needInsert:
    et.insertDataSql(insterSql.format(str(item["Id"]), item["ch"], item['file']))
