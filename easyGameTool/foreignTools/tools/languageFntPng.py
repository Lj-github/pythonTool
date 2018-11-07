# -*- coding: utf-8 -*-
# @Time    : 18/4/26 上午11:36
# @Author  : myTool
# @File    : languageFntPng.py
# @Software: PyCharm

#把网上找到的字符去重

lang = 'AaĂăáÂâớBbbêbờCcxêcờDddêdờĐđđêđờEeeÊêêGggiêgờHhhắtIiingắnKkcaMmemmờmờLlelờlờNnennờnờOooÔôôƠơơPppêpờQqcuquyquờRrerờrờSsétsìsờTttêtờuƯưưVvvêvờXxíchxìxờYyidàiicờrétABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890'

#去重

print("ă")

lang2 = ""
print(lang.__len__())
strd = "AaĂ"
print(strd.__len__())
for i in strd:
    print(i)


for i in lang:
    #print(i)
    if not (i in lang2):
        lang2 = lang2 + i
#print strd.encode('utf-8')
#print se.__len__()
#print(lang2.encode("utf-8"))
import codecs

print(lang2)
content = u'你好, Hello world'

with open("/Users/admin/Documents/ljworkspace/local/cocos/test/foreignTools/tools/excelTool/tes.txt",
          "wb") as f:
    f.write(lang2)