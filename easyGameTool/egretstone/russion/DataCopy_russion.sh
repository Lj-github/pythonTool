#!/usr/bin/env bash

rm -rf /Users/admin/Documents/ljworkspace/local/egret/ProStoneAge/ProStoneAge/StoneAppPro/dataBake/
mkdir -p /Users/admin/Documents/ljworkspace/local/egret/ProStoneAge/ProStoneAge/StoneAppPro/dataBake/



find /Users/admin/Documents/ljworkspace/local/egret/design/stone_age/tools/exceltojson/json -iname '*.*' -exec cp \{\} /Users/admin/Documents/ljworkspace/local/egret/ProStoneAge/ProStoneAge/StoneAppPro/dataBake/ \;


svnPath=/Users/admin/Documents/ljworkspace/local/cocos/assets/pikachu/sanguo/aiweiyou_pokmon/pokmon_weixin
jsonPath=$svnPath/tools/exceltojson/json
descPath=$svnPath/tools/exceltojson/ts
appPath=/Users/admin/Documents/ljworkspace/local/egret/ProStoneAge/ProStoneAge/StoneAppPro/

svn update $svnPath
rm $appPath/dataBake/*.json
cp  $jsonPath/*.json $appPath/dataBake/
cp  $jsonPath/*Group.json $appPath/resource/data/
echo 'copy desc files'
cp $descPath/* $appPath/libs/

/Users/admin/Documents/ljworkspace/local/egret/ProStoneAge/ProStoneAge/other/resRepend/resDepend.sh