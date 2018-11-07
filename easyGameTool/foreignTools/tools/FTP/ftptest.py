# -*- coding: utf-8 -*-
# @Time    : 18/5/5 下午4:54
# @Author  : myTool
# @File    : ftptest.py
# @Software: PyCharm

from ftplib import FTP
import time
import tarfile
import os


from ftplib import FTP

def ftpconnect(host, username, password):
    ftp = FTP()
    # ftp.set_debuglevel(2)
    ftp.connect(host, 21)
    ftp.login(username, password)
    return ftp

#从ftp下载文件
def downloadfile(ftp, remotepath, localpath):
    bufsize = 1024
    fp = open(localpath, 'wb')
    ftp.retrbinary('RETR ' + remotepath, fp.write, bufsize)
    ftp.set_debuglevel(0)
    fp.close()

#从本地上传文件到ftp
def uploadfile(ftp, remotepath, localpath):
    bufsize = 1024
    fp = open(localpath, 'rb')
    ftp.storbinary('STOR ' + remotepath, fp, bufsize)
    ftp.set_debuglevel(0)
    fp.close()

if __name__ == "__main__":
    ftp = ftpconnect("192.168.176.128", "anonymous", "")
    #downloadfile(ftp, "Faint.mp4", "C:/Users/Administrator/Desktop/test.mp4")
    #调用本地播放器播放下载的视频

    uploadfile(ftp, "/Users/admin/Documents/ljworkspace/local/cocos/test/foreignTools/tools/FTP/aaa", "aaa")

    ftp.quit()