#!/usr/bin/env bash
#直接 从 英文版里面 覆盖 需要 提前 同步 至 英文版

#是否更新coffee
isUpdateCoffee=true


rm -rf /Users/admin/Documents/ljworkspace/local/cocos/project/pikachu_vietnam/pikachu_english/tools/pikachuCCB/ccb/
mkdir -p /Users/admin/Documents/ljworkspace/local/cocos/project/pikachu_vietnam/pikachu_english/tools/pikachuCCB/ccb/


engLishPrp=/Users/admin/Documents/ljworkspace/local/cocos/project/pikachu_english_180511/pikachu_english/
appPath=/Users/admin/Documents/ljworkspace/local/cocos/project/pikachu_vietnam/pikachu_english/
if $isUpdateCoffee = true ;then
    echo 'copy  coffee begin'
    rm -rf /Users/admin/Documents/ljworkspace/local/cocos/project/pikachu_vietnam/pikachu_english/app/static/coffee/
    mkdir -p /Users/admin/Documents/ljworkspace/local/cocos/project/pikachu_vietnam/pikachu_english/app/static/coffee/
    cp -r -f $engLishPrp/app/static/coffee/ $appPath/app/static/coffee/
    echo 'copy  coffee success !!!'
fi

cp -r -f $engLishPrp/tools/pikachuCCB/ccb/ $appPath/tools/pikachuCCB/ccb/
sh /Users/admin/Documents/ljworkspace/local/cocos/project/pikachu_vietnam/pikachu_english/tools/pikachuCCB/bin/openBin/copy_ccb.sh

echo 'copy ccb  success !!!'
