# -*- coding: utf-8 -*-
# @Time    : 18/4/12 下午5:13
# @Author  : myTool
# @File    : Translate.py
# @Software: PyCharm

import md5
import os
#http://api.fanyi.baidu.com/api/trans/vip/translate?q=的撒&from=auto&to=en&appid=2015063000000001&salt=1435660288&sign=f89f9594663708c1605f3d736d01d2d4
import hashlib
import httplib
import random
from xlwt import Workbook
import xlrd
import sys
import urllib2
import json
sys.setrecursionlimit(1000000)
from urllib import quote
import xlwt
'''
    百度翻译    
'''
class Translate:

    appid = 20180412000145578
    key = "bAA0NVom2LS4EYeZUzB2"
    def __init__(self, appid):
        #初始化appid
        Translate.appid = appid
    #获取md5值
    def getMd5StrBy(self, stri):
        #m2 = hashlib.md5()
        # stri = stri.decode("utf8")
        # m2.update(stri)
        # md5Str = m2.hexdigest()
        m1 = md5.new()
        m1.update(stri)
        md5Str = m1.hexdigest()
        #print("str => " + stri + " ----- md5 => " + str(md5Str))
        return md5Str
    #http请求
    def getBaiduTranslate(self, url,callback):
        if not url:
            return
        try:
            print('api.fanyi.baidu.com' + url  )
            httpClient = httplib.HTTPConnection('api.fanyi.baidu.com')
            httpClient.request('GET', url)
            # response是HTTPResponse对象
            response = httpClient.getresponse()
            cc = response.read()
            ccc = cc.decode("unicode_escape")
            ccc = ccc.encode("utf-8")

            if httpClient:
                httpClient.close()
            print("==>> ccc " + ccc + "")
            if ccc != "" :
                callback(ccc)
        except httplib.error,e:
            print e.code
    #打包url
    ##!!!! _from 转为form
    def hexUrl(self,q,_from,to):
        if not q or not _from or not to :
            print("url cannot full!!!")
            return
        salt = random.randint(32768, 65536)
        sign = self.getMd5StrBy(str(Translate.appid ) + str(q)  + str(salt) + Translate.key)
        return "/api/trans/vip/translate?" +"q="+ str(quote(q) ) +"&from="  + _from + "&to=" +to +"&appid=" + str(Translate.appid)  + "&salt=" +str(salt) + "&sign=" +sign+ ""

    def getTr(self,q,_from,to,callback):
        q =  q.replace('"',"`") # 引号转为`
        url = self.hexUrl(q,_from,to)
        #print(url)
        self.getBaiduTranslate(url,callback)


def getExcelByFile(filepth,col,isKong):
    if filepth: ##是否需要判断为excel
        dataAll = []
        table_translate = xlrd.open_workbook(filepth)
        sheet_translate = table_translate.sheet_by_index(0)
        nrows_translate = sheet_translate.nrows
        ncols_translate = sheet_translate.ncols
        for j in range(nrows_translate):
            translate = sheet_translate.row_values(j, 0, ncols_translate)
            arrayitem = []
            for i in col:
                sstr = translate[i]
                if isinstance(translate[i], unicode):
                    sstr = str(translate[i].encode('utf8'))
                if str(sstr).__len__() != 0 and isKong:
                    arrayitem.append(sstr)
                else:
                    if not isKong:
                        arrayitem.append(sstr)
                    #print( "file =>" + filepth + "--------" + str(j) + " is empty !!!!  english is " + str(translate[3]))
            if arrayitem.__len__() > 0 :
                dataAll.append(arrayitem)
        return dataAll

allArr = getExcelByFile("CCBReplaceEnglish_3.xls", [0, 1, 2, 3],False)
tr = Translate(20180412000145578)
count = 0

w = Workbook()
ws = w.add_sheet('列表'.decode('utf8'))
lena = 0

def runCre(allArr) :
    len = 0
    for i in allArr:
        ind = 0
        for j in i:
            rstr = j
            if isinstance(j, str):
                rstr = j.decode('utf8')
            # print("id = " + str(len) + " " + str(rstr) + "  is add success")
            ws.write(len, ind, rstr)
            ind = ind + 1
        len = len + 1
    w.save("CCBReplaceEnglish_4_1.xls")

def getht(stt):
    global lena
    lena =  lena  +1
    if stt != "":
        print(stt)
        dict_json = json.loads(stt)
        allArr[lena][0] = dict_json["trans_result"][0]["dst"]
    if lena == (allArr.__len__()-1) :
        runCre(allArr)
        return False
    if lena < (allArr.__len__()-1):
        if allArr[lena+1][0] == "" :
            print("index = > " + str(lena))
            tr.getTr(allArr[lena+1][2].replace("\n", ""), "auto", "zh", getht)
        else:
            getht("")


if __name__ == '__main__':
    getht("")









