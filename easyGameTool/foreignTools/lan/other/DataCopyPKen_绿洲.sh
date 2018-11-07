
rm -rf /Users/admin/Documents/ljworkspace/local/cocos/project/pikachu_english/app/static/res/data
mkdir -p /Users/admin/Documents/ljworkspace/local/cocos/project/pikachu_english/app/static/res/data

find /Users/admin/Documents/ljworkspace/local/cocos/assets/Pikachu/sanguo/aiweiyou_pokmon/EnglishResources/tools-lvzhou/exceltojson/json -iname '*.*' -exec cp \{\} /Users/admin/Documents/ljworkspace/local/cocos/project/pikachu_english/app/static/res/data \;

#find  /Users/songbin/sanguo/aiweiyou_pokmon/tools/exceltojson/sql -iname '*.*' -exec cp \{\} /Users/songbin/clientprojects/Pikachu/resources/sql \;
