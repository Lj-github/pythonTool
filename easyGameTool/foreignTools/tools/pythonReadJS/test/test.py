# -*- coding: utf-8 -*-
# @Time    : 2018/7/4 23:14
# @Author  : Aries
# @Site    : 
# @File    : test.py
# @Software: PyCharm

import execjs
import json
import io
def get_js(jsFile):
    f = io.open(jsFile, "r", encoding='utf-8')
    line = f.readline()
    htmlstr = ''
    while line:
        htmlstr = htmlstr + line
        line = f.readline()
    return htmlstr
def jsStrTOTable(jsStr):
    addedFunStr = "function getWindow() {var window = {};window.document = {}" + jsStr +" return window}"
    ctx = execjs.compile(addedFunStr)
    allObj = ctx.call('getWindow')
    return  allObj

#制作最终js str
def exportFinallResourceJS(allObj,fileName):
    windowmd5_resource = allObj["md5_resource"]
    windowdocumentccConfig = allObj["document"]["ccConfig"]
    windownoWebpImages = allObj["noWebpImages"]
    windowmd5_resourceStr = "window.md5_resource = "+ json.dumps(windowmd5_resource)
    windowdocumentccConfigStr = "window.document.ccConfig = " + json.dumps(windowdocumentccConfig)
    windownoWebpImagesStr = " window.noWebpImages = " + json.dumps(windownoWebpImages)
    with open(fileName,'w') as f:
        f.write(windowmd5_resourceStr+ "\n"+windowdocumentccConfigStr+ "\n"+windownoWebpImagesStr)

filename = 'write_data.js'
jsStr = get_js("tes.js")
allObj = jsStrTOTable(jsStr)
exportFinallResourceJS(allObj,filename)






