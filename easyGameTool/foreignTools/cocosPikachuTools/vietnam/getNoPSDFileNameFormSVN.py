# -*- coding: utf-8 -*-
# @Time    : 2018/10/24 下午4:53

#从svn 里面 获取没有psd 文件的文件名字

svnFile = "/Users/admin/Documents/ljworkspace/local/cocos/assets/pikachu/sanguo/art_pikachu/翻译美术（越南）/越语版"
imgFile = "/Users/admin/Documents/ljworkspace/local/cocos/project/pikachu_vietnam/pikachu越南版/越南版翻译/越南1023提取翻译/imgTranslate"
import os
def GetFileList(dir, ty ,fileList ):
    if os.path.isfile(dir):
        fp,fn = os.path.split(dir)
        ft = fn.split(".").pop()
        if ft in ty:
            fileList.append(fn)
    elif os.path.isdir(dir):
        for s in os.listdir(dir):
            newDir=os.path.join(dir,s)
            GetFileList(newDir,ty , fileList)
    return fileList



if __name__ == '__main__':
    allImgFile = GetFileList(imgFile,ty = ["png","jpg"],fileList = [])
    allHasPsdFile = GetFileList(svnFile,ty = "psd",fileList = [])
    allNoPsdFile = []
    ll = 0
    for f in allImgFile:
        psdF = f.replace("png","psd").replace("jpg","psd")
        if not psdF in allHasPsdFile:
            print(f)


'''

5ri_banne1.jpg
5ri_banne2.jpg
5ri_banne3.jpg
5ri_banne4.jpg
5ri_banne5.jpg
7r_chengha1.png
7r_chengha2.png
7r_chengha3.png
7r_chengha4.png
7r_chengha5.png



boss_sdz.png
bsy_thllb.png
chx_huiann.png
chx_kuku4.png
cjh_fayxtt3.png
cjh_jinjw11.png
cjh_jinjw12.png
cjh_laszz12.jpg
cjh_xxtai3.png
cxmh_gmz22.png
cxmh_gmz32.png
cxmh_gmz42.png
cxmh_gmz52.png
cz_zti1.png
cz_zti2.png
cz_zti3.png
dada_djzi1.png
dada_djzi2.png
dada_djzi3.png
dada_djzi4.png
dada_zt1.png
dada_zt2.png
danzlev.png
dfw_mingz.png
dj_cjquan.png
dj_xyqu.png
fb_zhouzj.png
ff_toutu.png
ff_zhuatt.jpg
ggl_kxxggl.png
gh_ghjs.png
gh_ztanniu10.png
gh_ztanniu9.png
ghbs_dxutiao.png
ghbs_tzhz.png
ghbs_tzz.png
hd_czjj1.png
hd_czjj2.png
hwhd_chengha1.png
jssx_jssx11.png
jssx_jssx12.png
kaiqiguanjuzhilu.png
lowa_zitiwj.png
lt_jiahaoy3.png
migo_ditu2.jpg
niak_tt2.png
pika_huati.png
pika_jingling_chuzhan.png
pika_shouye_iocn_boss.png
pika_shouye_iocn_qianghongbao.png
pika_xinxi_kezhi.png
pika_zhumi.png
pvp_anni1.png
pvp_anni2.png
pvp_anni3.png
pvp_anni4.png
pvp_chenghao1.png
pvp_chenghao10.png
pvp_chenghao11.png
pvp_chenghao12.png
pvp_chenghao13.png
pvp_chenghao14.png
pvp_chenghao2.png
pvp_chenghao3.png
pvp_chenghao4.png
pvp_chenghao5.png
pvp_chenghao6.png
pvp_chenghao7.png
pvp_chenghao8.png
pvp_chenghao9.png
pvp_choci.png
pvp_hhhhh.png
pvp_jran.png
pvp_jran2.png
pvp_jsziti.png
pvp_kaishi1.png
pvp_kaishi2.png
pvp_lianjisr.png
pvp_stop.png
pvp_tiequan.png
pvp_tt.jpg
pvp_zongjiji.png
qy_203k.png
qy_tqjbs1.jpg
qy_tqjbs2.jpg
qy_tqjbs3.jpg
sbb_shengli.png
sbb_xinzuo.png
sbb_zliliang.png
tkt_tks8.png
tq_ditu.jpg
tq_namee.png
UI_baoshiduihuan.png
UI_beibao.png
UI_chaojihlb.png
UI_chaozhilibao.png
ui_chixmoh.png
ui_chjihua.png
UI_chongdb1.png
UI_chongdb2.png
UI_chongdb3.png
UI_chongdb4.png
UI_chongdb5.png
UI_chongjijiangli.png
UI_chongwu.png
UI_chongzhi_jq.png
UI_chongzhi_shouchongbutongshue2.jpg
UI_chongzhi_zusi.png
UI_chongzhipaihang.png
UI_chunjiedenglu.png
UI_cjxlbb.png
ui_daijiqua.png
UI_danbichongzhi.png
UI_daoguantiaozhan.png
UI_daoju.png
UI_daqiyuyi.png
UI_dianjjinb.png
UI_duiwui_di1.png
UI_dzshs.png
UI_fengcehaoli.png
UI_fenxiang.png
UI_fubenzhongxin.png
UI_gggggao.png
UI_gh_300.png
UI_gh_900.png
UI_gonhuia.png
UI_guanjuzhil.png
UI_guanzhu.png
UI_haoyou.png
UI_huizhang.png
UI_huodofb.png
UI_huodong.png
UI_icon_xianshipipeizhan.png
UI_jinglidaren.png
UI_jinglingsongli.png
UI_jiqizhuangbei.png
ui_jnyas.png
UI_juezhantiankongta.png
UI_kafhhd.png
UI_leijichongzhi.png
UI_leijixiaofei.png
UI_liaotian2.png
UI_lixianshouyi.png
UI_meiridenglu.png
UI_meirixiaofei.png
UI_mrth.png
UI_nianka.png
UI_niudan.png
UI_niudan_shenshoulan.png
ui_niudanfb.png
UI_qiandao.png
UI_qiridenglu.png
UI_renwu.png
UI_richang.png
UI_richonghaoli.png
UI_shangcheng.png
UI_shengdanhaoli.png
UI_shilianfuli.png
UI_shilianzhekou.png
UI_shouchangjingling.png
UI_shouchong.png
UI_shouchong1.png
UI_tianjiangcaishen.png
UI_tiantianhaoli.png
UI_tiantianzhuachong.png
UI_tishengshili.png
UI_tongyong_xiafanganniu_duiwu.png
UI_tongyong_xiafanganniu_huishou.png
UI_tongyong_xiafanganniu_maoxian.png
UI_tongyong_xiafanganniu_maoxian2.png
UI_tongyong_xiafanganniu_qiyu.png
UI_tongyong_xiafanganniu_zhucheng.png
UI_tongyong_xiafanganniu_zhucheng2.png
UI_tongyong_xiafanganniu_zhujiao.png
ui_tquanka.png
UI_tsdj.png
UI_tuijian.png
UI_tujian.png
UI_vip2.png
UI_vip3.png
UI_vip_shouchong.png
UI_VIP_zishebeijing.jpg
ui_wabafb.png
UI_wangzhezhengba.png
UI_xianshichongji.png
UI_xianshizhanlisai.png
UI_xianshizhuangbei.png
UI_xingyunzhuanpan.png
UI_xinnianrichong.png
UI_xuabafb.png
UI_xuanbly.png
UI_xuyuax1.png
UI_xuyuax2.png
UI_youjian.png
UI_youjian_fujian.png
UI_youjian_new.png
UI_youxiti.png
UI_yuandanhaoli.png
UI_yuanxuai.png
UI_yueka.png
UI_yurendal.png
UI_zaixianjiangli.png
ui_zaixijl.png
ui_zajindan.png
UI_zhaungbei.png
UI_zhidingfuben.png
UI_zhidinghzuachong.png
UI_zhidingmigong.png
UI_zhizunshenshou.png
UI_zhongjilibao.png
UI_zhongshenka.png
UI_zhuijishenshou.png
UI_zuoqi.png
ui_zy_ditu.png
ui_zy_til.png
uit_mrxji.png
VIP_yanchk.jpg
xfh_libaoan.png
xianshibaoss.png
xianshixilia.png
yd_tgjq.png
zy_gjziann.png


'''
