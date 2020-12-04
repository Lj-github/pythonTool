#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/12/4 10:59
# @Author  : Aries
# @Site    : 
# @File    : main.py
# @Software: PyCharm

# 这个是 为了下载 url 的

# 网上有很多 乱七八糟的屎
# 这个目的是从 4399 上面 下载下来所以的 嗯 资源
# 先从 chrome 里面  吧所有字符 save to .har 文件
# 然后用 fiddler 打开  复制出 所有url 房子 fileListFiddler 里面
# 修改rootUrl
# 执行就行了
#
#


import urllib.request, io, os, sys
import requests
from threading import Thread
import time

# url跟目录
rootUrl = "http://sda.4399.com/4399swf/upload_swf/ftp34/liuxinyu/20201112/2"
projectName = "game_" + time.strftime("%Y-%m-%d", time.localtime())


def mkdir(path):
    print("创建路径 ====> " + path)
    # 去除首位空格
    path = path.strip()
    # 去除尾部 \ 符号
    path = path.rstrip("\\")
    # 判断路径是否存在
    isExists = os.path.exists(path)
    print(path)
    # 判断结果
    if not isExists:
        # 如果不存在则创建目录,创建目录操作函数
        '''
        os.mkdir(path)与os.makedirs(path)的区别是,当父目录不存在的时候os.mkdir(path)不会创建，os.makedirs(path)则会创建父目录
        '''
        # 此处路径最好使用utf-8解码，否则在磁盘中可能会出现乱码的情况
        try:
            os.makedirs(path)
        except ValueError:
            print("makedirs err")
        print(path + ' 创建成功')
        return True
    else:
        # 如果目录存在则不创建，并提示目录已存在
        print(path + ' 目录已存在')
        return False


def downLoad(url2, projectPath):
    filePath, fileName = os.path.split(url2)
    print(fileName)
    print(filePath)

    file_data = requests.get(url2, allow_redirects=True).content

    # req = urllib.request.Request(url2)
    # f = urllib.request.urlopen(req)
    # s = f.read()
    # s = s.decode('utf-8', 'ignore')

    localPath = filePath.replace(rootUrl, "")
    print("localPath ===>" + localPath)
    if not (localPath == ""):
        mkdir(projectPath + localPath)
    saveFile = projectPath + localPath + "\\" + fileName
    print("保存本地的文件为 ====> " + saveFile)

    with open(saveFile, 'wb') as handler:
        handler.write(file_data)


class MyThread(Thread):
    def __init__(self, url2, projectPath):
        super(MyThread, self).__init__()
        self.url = url2
        self.projectPath = projectPath

    def run(self):  # 必须有的函数
        print("run")
        try:
            downLoad(self.url, self.projectPath)
        except ValueError:
            print("下载失败===> " + self.url + "*****" + self.projectPath)


if __name__ == '__main__':

    projectPath = os.path.split(os.path.realpath(__file__))[0]
    projectPath = projectPath + "/" + projectName
    print(projectPath)
    mkdir(projectPath)
    f = open("fileListFormFiddler")
    line = f.readline()
    while line:
        line = f.readline()
        print("line ===> " + line)
        if line != "":
            if rootUrl in line:
                print("创建线程")
                t1 = MyThread(line.replace("\n", ""), projectPath)  # 创建第一个线程，并传递参数
                t1.start()
                # downLoad(line.replace("\n", ""), projectPath)
    f.close()
    # downLoad("http://sda.4399.com/4399swf/upload_swf/ftp34/liuxinyu/20201112/2/gameIndex.html")
    # print()
    # mkdir("/src")
