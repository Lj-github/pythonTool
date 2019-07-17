import os
import sys
import requests

fileBasePath = '../static/download/'


def loadImage(serverUrl):
    request_download(serverUrl)


def request_download(url):
    if not url:
        return ''
    r = requests.get(url)
    path = fileBasePath + 'img2.png'
    with open(path, 'wb') as f:
        f.write(r.content)
    return path
