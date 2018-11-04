# encoding: utf-8
from Tkinter import *
from tkMessageBox import *
import  os
import  datetime
import  os.path
import json
from  hashlib import md5
import shutil

def updateRES():
    root.destroy()
def updateAPP():
    root.destroy()

root = Tk()
def _test():
    text = "是否为热更新"
    if TclVersion >= 8.1:
        try:
            text = text +"\n选择否会更新app版本"
        except NameError:
            pass # no unicode support
    label = Label(root, text=text)
    label.pack()
    test = Button(root, text="是",command=updateRES).pack(fill=X)
    #test.pack()
    root.test = test
    quit = Button(root, text="否", command=updateAPP).pack(fill=X)
    ##quit.pack()
    root.iconify()
    root.update()
    root.deiconify()
    root.mainloop()

if __name__ == '__main__':
    #_test()
    appVersionFile = open('appVersion.manifest', 'r')
    appVersionJson = appVersionFile.read()
    appVersionDict = json.loads(appVersionJson)
    appVersion = appVersionDict['appVersion'].encode('unicode-escape')
    appVarr = str.split(appVersion, ".")
    print appVarr
    version = appVarr[-1]
    print version

    newVersion ='%d' %(int(version) + 1)
    appVersion = newVersion
    newVersionDict = {}
    newVersionDict["appVersion"] = "1.0." + newVersion
    newVersionDict["flag"] = appVersionDict["flag"]
    newStr = json.dumps(newVersionDict)
    r = file("appVersion.manifest", "w")
    r.write(newStr)
    r.close()
    appVersion ="1.0." + appVersion
    print  appVersion
