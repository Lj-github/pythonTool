#!/usr/bin/env bash

rm -rf /Users/admin/Documents/ljworkspace/local/cocos/project/pikachu_vietnam_update/pikachu_english/app/static/res/data/
mkdir -p /Users/admin/Documents/ljworkspace/local/cocos/project/pikachu_vietnam_update/pikachu_english/app/static/res/data/

svnPath=/Users/admin/Documents/ljworkspace/local/cocos/assets/pikachu/sanguo/aiweiyou_pokmon/VietnamResources/
jsonPath=$svnPath/tools/exceltojson/json
appPath=/Users/admin/Documents/ljworkspace/local/cocos/project/pikachu_vietnam_update/pikachu_english/app/static/res/

svn update $svnPath
rm $appPath/data/*.json
cp  $jsonPath/*.json $appPath/data/
echo 'copy desc files'
