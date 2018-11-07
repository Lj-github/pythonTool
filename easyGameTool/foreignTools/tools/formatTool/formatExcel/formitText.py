# -*- coding: utf-8 -*-
# @Time    : 2018/9/17 下午3:43

import json

def createJsonFile(jsonObj,fileName):

    with open(fileName + ".json", 'w') as f:
        json.dump(jsonObj, f,ensure_ascii=False, sort_keys=True, indent=4, separators=(',', ':'))

if __name__ == '__main__':
    print("begin")
    allObj = {}


    # for i in range(0,20):
    #     item = {}
    #     item["title"] = ""
    #     print("dddd")
    with open("test", 'r') as f:
        line = f.readlines()
        k = 0
        isBegin = False
        tem = []
        for i in line:


            item = {}
            if len(tem) == k:
                tem.append({})

            item = tem[k - 1]
            if i.find("？")>-1 :
                item["que"] = i.split("、").pop()

                tem[k-1] = item
                k = k + 1
                continue
                #写入text
            if i.find("、")>-1:
                iii = {}
                iii["text"] = i.split("、")[1].split(" ")[0]
                iii["score"] = int(i.split("、")[1].split(" ")[1][0:1])
                item[i.split("、")[0]]   = iii
                tem[k-1] = item
        createJsonFile(tem,"dd.json")