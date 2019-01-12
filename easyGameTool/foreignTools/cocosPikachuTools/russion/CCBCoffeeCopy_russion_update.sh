#!/usr/bin/env bash
#直接 从 英文版里面 覆盖 需要 提前 同步 至 英文版
rm -rf /Users/admin/Documents/ljworkspace/local/cocos/project/pikachu_russion_update/pikachu_english/app/static/coffee/
mkdir -p /Users/admin/Documents/ljworkspace/local/cocos/project/pikachu_russion_update/pikachu_english/app/static/coffee/

rm -rf /Users/admin/Documents/ljworkspace/local/cocos/project/pikachu_russion_update/pikachu_english/tools/pikachuCCB/ccb/
mkdir -p /Users/admin/Documents/ljworkspace/local/cocos/project/pikachu_russion_update/pikachu_english/tools/pikachuCCB/ccb/


engLishPrp=/Users/admin/Documents/ljworkspace/local/cocos/project/pikachu_englishGit/pikachu_english/
appPath=/Users/admin/Documents/ljworkspace/local/cocos/project/pikachu_russion_update/pikachu_english/


cp -r -f $engLishPrp/app/static/coffee/ $appPath/app/static/coffee/
cp -r -f $engLishPrp/tools/pikachuCCB/ccb/ $appPath/tools/pikachuCCB/ccb/

sh /Users/admin/Documents/ljworkspace/local/cocos/project/pikachu_russion_update/pikachu_english/tools/pikachuCCB/bin/openBin/copy_ccb.sh

echo 'copy ccb coffee success !!!'
