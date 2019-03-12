#!/usr/bin/env bash

#sh /home/serverdeploy/english_deploy/git_update_vietnam.sh
# echo "checkout file"
#cd /home/serverdeploy/svndata/越南/exceltojson
# echo "更新数据"
#sudo svn update
#
#sudo rm -rf /mnt/code/pikachu_english/app/static/res/data/*
#sudo cp -r /home/serverdeploy/svndata/越南/exceltojson/json/. /mnt/code/pikachu_english/app/static/res/data
# echo "复制到客户端"
#sudo cd /mnt/code/pikachu_english/app/update/channel
# echo "开始更新越南测试服"
#sudo python Update_vng360Test.py False True
# echo "更新完毕"



cd /home/serverdeploy/svndata/越南/exceltojson
 echo "更新数据"
svn update

rm -rf /mnt/code/pikachu_english/app/static/res/data/*
cp -r /home/serverdeploy/svndata/越南/exceltojson/json/*.json /mnt/code/pikachu_english/app/static/res/data
 echo "复制到客户端"
cd /mnt/code/pikachu_english/app/update/channel
 echo "开始更新越南测试服"
python Update_data.py vng360Test True
 echo "更新完毕"



