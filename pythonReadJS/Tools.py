# -*- coding: utf-8 -*-
# @Time    : 2018/10/12 下午5:36


import execjs

'''
    js jsobg 返回 table 
'''

def jsStrTOTable(jsStr):
    addedFunStr = "function getWindow() {var window = {};window.document = {};" + jsStr + "; return window}"
    ctx = execjs.compile(addedFunStr)
    allObj = ctx.call('getWindow')
    return allObj


