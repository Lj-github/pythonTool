# -*- coding: utf-8 -*-
# @Time    : 2018/12/4 下午8:38


'''

    全局  文件列表 config   包括 svn  项目路径 等等   加tmd

'''
##################################################################################################################

'''  mac mini  所有配置   '''
MACMINI_SVN_PATH = '/Users/admin/Documents/ljworkspace/local/cocos/assets/pikachu/sanguo/'


MACMINI_COCOS_PROJECT_ENGLISH = '/Users/admin/Documents/ljworkspace/local/cocos/assets/pikachu/sanguo/'

MACMINI_COCOS_PROJECT_ENGLISH_GIT = '/Users/admin/Documents/ljworkspace/local/cocos/project/pikachu_englishGit/pikachu_english'

MACMINI_COCOS_PROJECT_YUENAN = '/Users/admin/Documents/ljworkspace/local/cocos/project/pikachu_vietnam/pikachu_english'

MACMINI_COCOS_ALLPSDPATH = '/Users/admin/Documents/ljworkspace/local/cocos/assets/pikachu/sanguo/art_pikachu/翻译美术图（英文）/所有的psd/'


MACMINI_EGRET_STONE_PRO = "/Users/admin/Documents/ljworkspace/local/egret/ProStoneAge/ProStoneAge/StoneAppPro"


##################################################################################################################



##################################################################################################################

''' win 10  所有配置   '''
WIN10_SVN_PATH = 'D:\work\easygame\svn\\'

WIN10_PROJECT_EGRET = 'D:\work\easygame\client\SmartPikachu\\'




##################################################################################################################

## 数据库配置

isLocal = True
host = '127.0.0.1'
port = 3306
user = 'root'
passwd = 'root'
database = 'foreign-project'
stoneDataBase = "stone-foreigh-project"
if not isLocal:
    host = '192.168.1.207'
    passwd = ''


