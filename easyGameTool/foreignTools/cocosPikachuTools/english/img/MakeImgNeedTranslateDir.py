__author__ = 'songbin'

'''待翻译资源文件收集 并创建对应txt文件 如果有英文 则写入'''

import shutil
import os
import pymysql

#img存放目的路径
imgdistPth = '/Users/songbin/Downloads/Language/德语/joyfun/beTranslateImg'
imgdistPth = '/Users/songbin/Downloads/Language/越南/翻译包收集/190920/img'
imgsourcePthList = [
    '/Users/songbin/sanguo/art_pikachu',
    "/Users/songbin/sanguo/art_pikachu/翻译美术图（英文）/",
    "/Users/songbin/sanguo/art_pikachu/翻译美术图（俄文版）/",
    "/Users/songbin/sanguo/art_pikachu/翻译美术（越南）/",
    "/Users/songbin/sanguo/art_pikachu/翻译美术（法国）/",
    "/Users/songbin/sanguo/art_pikachu/翻译美术图（德国）"
]
isGetTranslate = False
originTxtId = 3
translateId = 3
kTitleList = ['fileName','English','Russion','Vietnam','French','German','TraditionalChinese']

#忽略中文版资源以外的路径
ignorPthlist=[
    "/Users/songbin/sanguo/art_pikachu/翻译美术图/",
    "/Users/songbin/sanguo/art_pikachu/程天游/",
    "/Users/songbin/sanguo/art_pikachu/翻译美术图（英文）/",
    "/Users/songbin/sanguo/art_pikachu/翻译美术（越南）/",
    "/Users/songbin/sanguo/art_pikachu/翻译美术图（俄文版）/",
    "/Users/songbin/sanguo/art_pikachu/绿洲/",
    "/Users/songbin/sanguo/art_pikachu/翻译美术（法国）/",
    "/Users/songbin/sanguo/art_pikachu/翻译美术图（德国）"
]
def copyfile(srcfile,dstfile):
    if not os.path.isfile(srcfile):
        print("%s not exist!"%(srcfile))
    else:
        fpath,fname=os.path.split(dstfile)
        if not os.path.exists(fpath):
            '''创建路径'''
            os.makedirs(fpath)

        '''复制文件'''
        shutil.copyfile(srcfile,dstfile)
        print("copy %s -> %s"%( srcfile,dstfile))

def makeDirFucn(list):
     for root, dirs, files in os.walk(imgsourcePthList[originTxtId]):
        for OneFileName in files:
             if (list.get(OneFileName)):
                isIgnorPth = False
                if originTxtId == 0:
                    for ignorpth in ignorPthlist:
                        pthlist = root.split(ignorpth)
                        if (len(pthlist) >= 2 and len(pthlist[1]) > 0):
                             isIgnorPth = True
                             break

                if isIgnorPth:
                    continue
                src1 = os.path.join(root,OneFileName)
                src2 = os.path.join(imgdistPth,OneFileName)
                copyfile(src1,src2)
                nameNoType = OneFileName.split('.')[0]
                imgTxtPth = os.path.join(imgdistPth,nameNoType+'.txt')

                fobj=open(imgTxtPth,'w',32,'utf8')
                fobj.write(list.get(OneFileName) )
                fobj.close()




def sqlSelect():
    '''获取数据库连接'''
    conn=pymysql.connect(host='localhost',user='root',password='',db='foreign-project',port=3306,charset='utf8mb4')
    '''获取一个游标'''
    cur=conn.cursor()
    '''limit 10 #where isSpecial=0'''
    'u'
    # s = '测试'
    # cur.execute('UPDATE ccbTranslate SET Chinese = \"'+s+'\" where Id=1')
    # cur.execute('UPDATE ccbTranslate SET Chinese = \"'+s+'\" where Id=2')
    # conn.commit()
    cur.execute('SELECT MAX(id)+1 from ccbTranslate')

    fileName = kTitleList[0]
    origin_id = originTxtId
    if originTxtId == 0:
        origin_id = 1
    originName = kTitleList[origin_id]
    disTtName = kTitleList[translateId]

    if isGetTranslate:
        cur.execute('Select fileName, '+originName+' FROM translateImgData where '+originName+' is not null')
    else:
        cur.execute('Select fileName, '+originName+' FROM translateImgData where '+disTtName+' is NULL')
    data=cur.fetchall()
    print('French:',data[0][0])
    arr = {}
    for d in data:
        print(d)
        arr[str(d[0])] = str(d[1])

    '''释放游标'''
    cur.close()
    conn.close()

    makeDirFucn(arr)

if __name__ == "__main__":
    try:
        sqlSelect()


    except Exception as e:
        print("异常" + e)